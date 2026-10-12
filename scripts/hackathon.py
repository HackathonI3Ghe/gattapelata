#!/usr/bin/env python3
"""Automazioni condivise Claude/Codex, solo libreria standard Python 3.10+."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ROLES = {"technical": ("demo/", ".github/workflows/"), "commercial": ("docs/",)}
NOTES = {"technical": "demo/NOTE-TECNICHE.md", "commercial": "docs/NOTE-COMMERCIALI.md"}
SKILLS = ("hackathon-sync", "hackathon-review", "hackathon-demo-check")
WATCH_CHILDREN = []


class Failure(RuntimeError):
    pass


def git(*args, check=True, raw=False):
    result = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, timeout=45)
    if check and result.returncode:
        # Non mostrare URL/remoti che potrebbero contenere credenziali.
        raise Failure(f"Git {args[0]} non riuscito (codice {result.returncode}). Controllare Git manualmente.")
    return result.stdout if raw else result.stdout.decode("utf-8", errors="replace").strip()


def state_dir():
    path = Path(git("rev-parse", "--git-path", "hackathon"))
    if not path.is_absolute():
        path = ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_state(name, default=None):
    path = state_dir() / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_state(name, data):
    path = state_dir() / name
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


@contextmanager
def locked():
    path = state_dir() / "sync.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise Failure("Un'altra sincronizzazione è attiva. Se interrotta, verificare prima di rimuovere sync.lock.")
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def config(required=False):
    data = read_state("config.json", {})
    if required and data.get("role") not in ROLES:
        raise Failure("Ruolo non configurato: python scripts/hackathon.py setup --role technical oppure commercial.")
    return data


def names(*args):
    return [s.decode("utf-8") for s in git(*args, raw=True).split(b"\0") if s]


def changed():
    return sorted(set(names("diff", "--name-only", "-z", "HEAD") +
                      names("ls-files", "--others", "--exclude-standard", "-z")))


def staged():
    return names("diff", "--cached", "--name-only", "-z")


def owned(path, role):
    return path.startswith(ROLES[role]) and not any(
        part.startswith(".env") or part.lower().endswith((".pem", ".key", ".p12"))
        for part in Path(path).parts
    )


def snapshot(paths):
    result = {}
    for name in paths:
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT.resolve()) or path.is_symlink():
            raise Failure(f"Percorso esterno o link non pubblicabile: {name}")
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    return result


def project_snapshot():
    paths = set(names("ls-files", "-z") + names("ls-files", "--others", "--exclude-standard", "-z"))
    # Il rapporto stesso non invalida la revisione appena registrata.
    selected = sorted(p for p in paths if p in ("AGENTS.md", "bando-gara-gattapelata.md") or
                      (p.startswith(("demo/", "docs/")) and not p.endswith("NOTE-REVISIONE.md")))
    return snapshot(selected)


def identity(require_role=True):
    data = config(required=require_role)
    if not data.get("branch"):
        raise Failure("Eseguire setup in questo clone prima della sincronizzazione.")
    branch = git("symbolic-ref", "--short", "HEAD")
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if branch != data["branch"] or upstream != data["upstream"]:
        raise Failure("Branch/upstream diversi da quelli configurati. Nessuna pubblicazione automatica.")
    gitdir = Path(git("rev-parse", "--absolute-git-dir"))
    if any((gitdir / item).exists() for item in ("MERGE_HEAD", "rebase-merge", "rebase-apply", "CHERRY_PICK_HEAD")):
        raise Failure("Operazione Git in corso: completarla manualmente.")
    return data


def install_skills(check_only=False, staged_index=False):
    for skill in SKILLS:
        source = ROOT / ".agents/skills" / skill / "SKILL.md"
        destination = ROOT / ".claude/skills" / skill / "SKILL.md"
        if check_only:
            if staged_index:
                left = git("show", ":" + source.relative_to(ROOT).as_posix(), raw=True)
                right = git("show", ":" + destination.relative_to(ROOT).as_posix(), raw=True)
            else:
                left = source.read_bytes()
                right = destination.read_bytes() if destination.exists() else None
            if left != right:
                raise Failure(f"Skill Claude da rigenerare: {skill}. Eseguire install-skills.")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())


def setup(role, watch_enabled=False, receive_only=False):
    install_skills(check_only=True)
    current = git("config", "--get", "core.hooksPath", check=False)
    if current != ".githooks":
        hookdir = Path(current) if current else Path(git("rev-parse", "--git-path", "hooks"))
        if not hookdir.is_absolute():
            hookdir = ROOT / hookdir
        active = [p.name for p in hookdir.glob("*") if p.is_file() and not p.name.endswith(".sample")]
        if active:
            raise Failure("Hook Git esistenti: integrarli manualmente prima di installare .githooks.")
        git("config", "--local", "core.hooksPath", ".githooks")
    for name in ("pre-commit", "pre-push"):
        path = ROOT / ".githooks" / name
        path.chmod(path.stat().st_mode | 0o111)
    branch = git("symbolic-ref", "--short", "HEAD")
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    remote = git("config", "--get", f"branch.{branch}.remote")
    merge = git("config", "--get", f"branch.{branch}.merge")
    if remote != "origin" or not merge.startswith("refs/heads/"):
        raise Failure("Configurare un upstream su origin prima del setup.")
    previous = config()
    write_state("config.json", {"role": None if receive_only else (role or previous.get("role")), "branch": branch, "upstream": upstream,
                                "remote_branch": merge.removeprefix("refs/heads/"), "watch_enabled": watch_enabled})
    if role or receive_only:
        for name in ("ready.json", "review.json"):
            (state_dir() / name).unlink(missing_ok=True)
    if watch_enabled:
        launch_watch()
    return "Hook Git installati. " + (f"Ruolo locale: {role}." if role else "Scegliere il ruolo con setup --role.")


def start():
    with locked():
        data = identity(require_role=False)
        git("fetch", "origin", data["remote_branch"])
        if changed() or staged():
            return "Fetch eseguito; checkout con modifiche, integrazione rimandata. Le note locali possono essere vecchie."
        # Equivalente a pull --ff-only, senza riscrivere i commit locali non pubblicati.
        git("merge", "--ff-only", "FETCH_HEAD")
    return "Checkout aggiornato. Leggere le NOTE del collega prima di lavorare."


def launch_watch():
    if (state_dir() / "watch.lock").exists():
        return
    options = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL,
               "cwd": str(ROOT)}
    if os.name == "nt":
        options["creationflags"] = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        options["start_new_session"] = True
    WATCH_CHILDREN[:] = [child for child in WATCH_CHILDREN if child.poll() is None]
    WATCH_CHILDREN.append(subprocess.Popen([sys.executable, str(ROOT / "scripts/hackathon.py"), "watch"], **options))


def watch_once():
    try:
        message = start()
        state = "ok"
    except (Failure, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        message, state = str(exc), "attesa"
    record = {"time": datetime.now(timezone.utc).isoformat(), "state": state, "message": message}
    write_state("watch-status.json", record)
    return record


def watch():
    path = state_dir() / "watch.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        while config().get("watch_enabled"):
            watch_once()
            for _ in range(30):
                if not config().get("watch_enabled"):
                    return
                time.sleep(1)
    finally:
        path.unlink(missing_ok=True)


def stop_watch():
    data = config()
    data["watch_enabled"] = False
    write_state("config.json", data)
    for child in WATCH_CHILDREN:
        try:
            child.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass
    return "Ricezione periodica disattivata; il processo termina entro pochi secondi."


def check(use_staged=False, use_commits=False):
    install_skills(check_only=True, staged_index=use_staged)
    if names("diff", "--name-only", "--diff-filter=U", "-z"):
        raise Failure("Conflitti Git non risolti.")
    git("diff", "--check", *( ["--cached"] if use_staged else [] ))
    data = config()
    paths = staged() if use_staged else changed()
    if use_commits and data.get("role"):
        identity()
        commits = git("rev-list", f"{data['upstream']}..HEAD").splitlines()
        paths = sorted({p for commit in commits for p in names(
            "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z", commit)})
    if data.get("role"):
        foreign = [p for p in paths if not owned(p, data["role"])]
        if foreign:
            raise Failure("File fuori dal ruolo: " + ", ".join(foreign))
    for path in paths:
        if path.endswith((".md", ".html", ".json", ".py")):
            if use_staged:
                # File eliminati non hanno una voce nell'indice.
                content = subprocess.run(["git", "-C", str(ROOT), "show", ":" + path], capture_output=True, timeout=30)
                if content.returncode:
                    continue
                text = content.stdout.decode("utf-8")
            elif (ROOT / path).is_file():
                text = (ROOT / path).read_text(encoding="utf-8")
            else:
                continue
            if re.search(r"^(<<<<<<< |=======\s*$|>>>>>>> )", text, re.MULTILINE):
                raise Failure(f"Marker di conflitto: {path}")
            if path.endswith(".json"):
                json.loads(text)
    return "Controlli meccanici superati; la conformità al bando richiede revisione semantica."


def review():
    lines = ["# Controllo meccanico Gattapelata", "",
             f"Eseguito: {datetime.now(timezone.utc).isoformat()}", "",
             "Non assegna conformità o punteggi. I file presenti richiedono revisione semantica.", "",
             "| File | Evidenza automatica |", "|---|---|"]
    for name in ("demo/index.html", "demo/NOTE-TECNICHE.md", "docs/relazione-tecnica.md",
                 "docs/offerta-economica.md", "docs/pitch.md"):
        path = ROOT / name
        if not path.exists():
            result = "MANCANTE"
        else:
            text = path.read_text(encoding="utf-8")
            todos = [str(i) for i, line in enumerate(text.splitlines(), 1)
                     if re.search(r"\bTODO\b|\[NOME[^\]]*\]", line, re.IGNORECASE)]
            result = "Presente, DA VALUTARE" + ("; segnaposto alle righe " + ", ".join(todos) if todos else "")
        lines.append(f"| {name} | {result} |")
    lines += ["", "## Prove ancora da valutare", "",
              "Usare automation/REQUISITI.md per la matrice completa B01-B16 e T01-T08.",
              "NON VERIFICATO automaticamente: efficacia, operatività T+90', privacy, somme economiche,",
              "contrasto, CSS effettivo, audio, dispositivo reale, durata della demo e consegna entro le 20:00.", "",
              "Il revisore deve distinguere app e hardware successivo, simulazione e produzione,",
              "indicatori di rischio e incidenti/vite effettivamente evitati."]
    output = "\n".join(lines) + "\n"
    (state_dir() / "controllo.md").write_text(output, encoding="utf-8")
    return output


def review_done(report):
    data = config(required=True)
    path = (ROOT / report).resolve()
    expected = (ROOT / NOTES[data["role"]]).with_name("NOTE-REVISIONE.md").resolve()
    if path != expected:
        raise Failure("Scrivere NOTE-REVISIONE.md soltanto nel proprio ruolo.")
    text = path.read_text(encoding="utf-8")
    ids = re.findall(r"^\| (B\d{2}|T\d{2}) \|", (ROOT / "automation/REQUISITI.md").read_text(encoding="utf-8"), re.MULTILINE)
    if any(not re.search(rf"\b{item}\b", text) for item in ids):
        raise Failure("Il rapporto non copre tutti gli ID della matrice.")
    if not re.search(r"^Esito: ACCETTATO\s*$", text, re.MULTILINE):
        raise Failure("La revisione non è accettata. Correggere i rilievi prima di pubblicare.")
    write_state("review.json", {"snapshot": project_snapshot(), "report": report,
                                "report_hash": hashlib.sha256(path.read_bytes()).hexdigest()})
    return "Revisione registrata per i file attuali, con i limiti dichiarati nel rapporto."


def reviewed():
    record = read_state("review.json", {})
    if record.get("snapshot") != project_snapshot():
        return False
    path = ROOT / record.get("report", "")
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == record.get("report_hash")


def ready(message):
    data = identity()
    paths = changed()
    if staged():
        raise Failure("Indice già preparato: non modifico lo staging esistente.")
    if not paths or any(not owned(p, data["role"]) for p in paths):
        raise Failure("Nessun task pubblicabile o modifiche estranee al ruolo: preservate.")
    if NOTES[data["role"]] not in paths:
        raise Failure("Aggiornare la nota di passaggio del proprio ruolo prima di marcare il task pronto.")
    check()
    if not reviewed():
        raise Failure("Eseguire hackathon-review e review-done per i file attuali prima di ready.")
    if not message.strip() or len(message) > 160:
        raise Failure("Usare un messaggio concreto da 1 a 160 caratteri.")
    write_state("ready.json", {"head": git("rev-parse", "HEAD"), "snapshot": snapshot(paths), "message": message})
    return "Task marcato pronto: Stop pubblicherà questi file; sync pubblica subito."


def sync():
    with locked():
        data = identity()
        record = read_state("ready.json")
        if not record:
            return "Nessun task marcato pronto: nessun commit o push automatico."
        paths = changed()
        if staged() or any(not owned(p, data["role"]) for p in paths):
            raise Failure("Staging presente o modifiche fuori dal ruolo: sincronizzazione arrestata.")
        if record["head"] != git("rev-parse", "HEAD") or record["snapshot"] != snapshot(paths):
            raise Failure("I file o HEAD sono cambiati dopo ready. Rivalidare e marcare nuovamente pronto.")
        if not reviewed():
            raise Failure("Revisione non più valida: ripetere hackathon-review.")
        check()
        git("add", "--", *paths)
        git("commit", "-m", record["message"])
        # Rimuovere la prenotazione prima della rete: un fallimento non deve duplicare il commit.
        (state_dir() / "ready.json").unlink(missing_ok=True)
        git("fetch", "origin", data["remote_branch"])
        git("rebase", "FETCH_HEAD")
        if not reviewed():
            raise Failure("Il rebase ha integrato modifiche ai deliverable del collega. Commit conservato localmente: "
                          "ripetere revisione e note, poi ready e sync prima di pubblicare.")
        # Nessun retry/force automatico. Un conflitto resta visibile; il commit locale è conservato.
        check(use_commits=True)
        git("push", "origin", f"HEAD:refs/heads/{data['remote_branch']}")
        return "Pubblicato " + git("rev-parse", "--short", "HEAD") + " su origin/" + data["remote_branch"] + "."


def hook(event):
    payload = json.load(sys.stdin)
    # Ignora hook di subagenti: stesso clone, nessuna pubblicazione concorrente.
    if payload.get("agent_id") or payload.get("agent_type"):
        print("{}")
        return
    cwd = Path(payload.get("cwd", str(ROOT))).resolve()
    if not cwd.is_relative_to(ROOT):
        raise Failure("Hook ricevuto per un altro checkout.")
    try:
        if event == "start":
            if config().get("branch"):
                if config().get("watch_enabled"):
                    launch_watch()
                message = start()
            else:
                message = "Scegliere il ruolo locale con setup --role technical/commercial per attivare la sincronizzazione."
            print(json.dumps({"hookSpecificOutput": {"hookEventName": payload.get("hook_event_name", "SessionStart"),
                                                     "additionalContext": message}}, ensure_ascii=False))
        else:
            review()  # Rapporto meccanico anche sui checkpoint incompleti, senza bloccare il lavoro.
            data = config()
            own_changes = data.get("role") and any(owned(p, data["role"]) for p in changed())
            if own_changes and not reviewed() and not payload.get("stop_hook_active"):
                print(json.dumps({"decision": "block", "reason":
                    "Esegui hackathon-review per questo checkpoint: leggi la skill in "
                    ".agents/skills/hackathon-review/SKILL.md. Scrivi il rapporto solo nel tuo ruolo; "
                    "i deliverable incompleti restano pendenti. Se il task è completato, applica "
                    "hackathon-sync, aggiorna la nota di passaggio e marca ready. Se è incompleto "
                    "o la revisione richiede correzioni, segnala lo stato senza marcarlo pronto."}, ensure_ascii=False))
            elif own_changes and not reviewed():
                print(json.dumps({"systemMessage": "Revisione ancora pendente: nessuna pubblicazione automatica."}))
            elif not read_state("ready.json"):
                print("{}")
            else:
                print(json.dumps({"systemMessage": sync()}, ensure_ascii=False))
    except (Failure, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        # Segnalazione visibile, nessuna continuazione infinita Stop -> Stop.
        print(json.dumps({"systemMessage": str(exc)}, ensure_ascii=False))


def main():
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("setup")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--role", choices=ROLES)
    group.add_argument("--receive-only", action="store_true")
    p.add_argument("--no-watch", action="store_true")
    for name in ("status", "start", "sync", "review", "install-skills", "watch", "watch-once", "stop-watch"):
        sub.add_parser(name)
    p = sub.add_parser("check")
    p.add_argument("--staged", action="store_true")
    p.add_argument("--commits", action="store_true")
    p = sub.add_parser("ready")
    p.add_argument("--message", required=True)
    p = sub.add_parser("review-done")
    p.add_argument("--report", required=True)
    p = sub.add_parser("hook")
    p.add_argument("event", choices=("start", "stop"))
    args = parser.parse_args()
    try:
        if args.command == "hook":
            hook(args.event)
            return
        if args.command == "setup":
            result = setup(args.role, watch_enabled=not args.no_watch, receive_only=args.receive_only)
        elif args.command == "status":
            result = json.dumps({"config": config(), "ready": bool(read_state("ready.json")),
                                 "review_current": reviewed(), "changed": changed(),
                                 "watch": read_state("watch-status.json")}, ensure_ascii=False, indent=2)
        elif args.command == "install-skills":
            install_skills()
            result = "Copie Claude aggiornate dalla fonte .agents/skills."
        elif args.command == "check":
            result = check(args.staged, args.commits)
        elif args.command == "ready":
            result = ready(args.message)
        elif args.command == "review-done":
            result = review_done(args.report)
        elif args.command == "watch":
            watch()
            return
        elif args.command == "watch-once":
            result = json.dumps(watch_once(), ensure_ascii=False)
        elif args.command == "stop-watch":
            result = stop_watch()
        else:
            result = {"start": start, "sync": sync, "review": review}[args.command]()
        print(result)
    except (Failure, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

"""Verifiche comportamentali su due cloni e un remoto locale isolato."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

SOURCE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("hackathon", SOURCE / "scripts/hackathon.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gattapelata-tests-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.remote = self.base / "remote.git"
        self.clone = self.base / "tecnica"
        self.other = self.base / "collega"
        self.original_root = h.ROOT
        self.addCleanup(setattr, h, "ROOT", self.original_root)
        self.git(self.base, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.git(self.base, "clone", str(self.remote), str(self.clone))
        for folder in (".agents", ".claude/skills", ".githooks", "automation"):
            shutil.copytree(SOURCE / folder, self.clone / folder)
        (self.clone / "scripts").mkdir()
        shutil.copy2(SOURCE / "scripts/hackathon.py", self.clone / "scripts/hackathon.py")
        for file in ("AGENTS.md", "bando-gara-gattapelata.md", ".gitignore", ".gitattributes"):
            shutil.copy2(SOURCE / file, self.clone / file)
        self.write(self.clone, "docs/relazione-tecnica.md", "Proposta iniziale\n")
        self.write(self.clone, "demo/index.html", "<html lang=\"it\"><body>Attendi</body></html>\n")
        self.set_author(self.clone)
        self.git(self.clone, "add", ".")
        self.git(self.clone, "commit", "-m", "Base test")
        self.git(self.clone, "push", "-u", "origin", "main")
        self.git(self.base, "clone", str(self.remote), str(self.other))
        self.set_author(self.other)
        h.ROOT = self.clone
        h.setup("technical")

    def git(self, cwd, *args, ok=True):
        env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
                   GIT_CONFIG_GLOBAL=os.devnull)
        p = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=30)
        if ok and p.returncode:
            self.fail(f"git {args[0]}: {p.stderr}")
        return p.stdout.strip()

    def set_author(self, clone):
        self.git(clone, "config", "user.name", "Test locale")
        self.git(clone, "config", "user.email", "test@example.invalid")
        self.git(clone, "config", "commit.gpgsign", "false")

    def write(self, clone, name, text):
        p = clone / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")

    def task(self):
        self.write(self.clone, "demo/index.html", "<html lang=\"it\"><body>Vai</body></html>\n")
        self.write(self.clone, "demo/NOTE-TECNICHE.md", "Task completato e verificato nel test isolato.\n")

    def accept(self):
        ids = [f"B{i:02}" for i in range(1, 17)] + [f"T{i:02}" for i in range(1, 9)]
        self.write(self.clone, "demo/NOTE-REVISIONE.md",
                   "# Rapporto sintetico della fixture, non evidenza reale\n" +
                   "\n".join(f"| {i} | NON VERIFICATO | Fixture isolata |" for i in ids) +
                   "\nEsito: ACCETTATO\n")
        h.review_done("demo/NOTE-REVISIONE.md")

    def remote_commit(self, name, text):
        self.write(self.other, name, text)
        self.git(self.other, "add", "--", name)
        self.git(self.other, "commit", "-m", "Aggiorna collega")
        self.git(self.other, "push")

    def test_publishes_only_completed_reviewed_task(self):
        self.task()
        before = self.git(self.remote, "rev-parse", "main")
        self.assertIn("Nessun task", h.sync())
        self.assertEqual(before, self.git(self.remote, "rev-parse", "main"))
        self.accept()
        h.ready("Completa demo")
        self.assertIn("Pubblicato", h.sync())
        self.assertEqual(h.git("rev-parse", "HEAD"), self.git(self.remote, "rev-parse", "main"))
        self.assertFalse(h.changed())
        self.assertIsNone(h.read_state("ready.json"))

    def test_technical_role_can_publish_workflow_but_ignores_build_outputs(self):
        self.task()
        self.write(self.clone, ".github/workflows/deploy-pages.yml", "name: Demo\n")
        self.write(self.clone, "demo/dist/index.html", "Build generata\n")
        self.write(self.clone, "demo/node_modules/package/index.js", "Dipendenza\n")
        self.assertNotIn("demo/dist/index.html", h.changed())
        self.assertNotIn("demo/node_modules/package/index.js", h.changed())
        self.accept()
        h.ready("Aggiorna demo e workflow")
        self.assertIn("Pubblicato", h.sync())
        self.assertIn(".github/workflows/deploy-pages.yml", self.git(self.remote, "ls-tree", "-r", "--name-only", "main"))

    def test_foreign_changes_and_existing_staging_are_preserved(self):
        self.task()
        self.accept()
        self.write(self.clone, "docs/pitch.md", "Lavoro estraneo\n")
        with self.assertRaises(h.Failure):
            h.ready("Demo")
        self.git(self.clone, "add", "docs/pitch.md")
        before = h.git("diff", "--cached")
        with self.assertRaises(h.Failure):
            h.ready("Demo")
        self.assertEqual(before, h.git("diff", "--cached"))
        self.assertEqual("Lavoro estraneo\n", (self.clone / "docs/pitch.md").read_text())

    def test_ready_is_invalidated_by_content_change(self):
        self.task()
        self.accept()
        h.ready("Demo")
        before = h.git("rev-parse", "HEAD")
        self.write(self.clone, "demo/index.html", "Modifica successiva\n")
        with self.assertRaises(h.Failure):
            h.sync()
        self.assertEqual(before, h.git("rev-parse", "HEAD"))
        self.assertFalse(h.staged())

    def test_review_requires_all_requirements_and_accepted_outcome(self):
        self.task()
        self.write(self.clone, "demo/NOTE-REVISIONE.md", "Esito: ACCETTATO\n")
        with self.assertRaises(h.Failure):
            h.review_done("demo/NOTE-REVISIONE.md")
        self.accept()
        p = self.clone / "demo/NOTE-REVISIONE.md"
        p.write_text(p.read_text().replace("ACCETTATO", "CORREZIONI NECESSARIE"))
        with self.assertRaises(h.Failure):
            h.review_done("demo/NOTE-REVISIONE.md")
        self.assertFalse(h.reviewed())

    def test_start_fetches_but_never_overwrites_dirty_checkout(self):
        self.remote_commit("docs/relazione-tecnica.md", "Nuova proposta del collega\n")
        self.task()
        before = h.git("rev-parse", "HEAD")
        self.assertIn("rimandata", h.start())
        self.assertEqual(before, h.git("rev-parse", "HEAD"))
        self.assertEqual("Proposta iniziale\n", (self.clone / "docs/relazione-tecnica.md").read_text())

    def test_rebase_of_colleague_work_requires_new_semantic_review(self):
        self.task()
        self.accept()
        h.ready("Demo")
        self.remote_commit("docs/relazione-tecnica.md", "Nuova proposta del collega\n")
        remote_head = self.git(self.remote, "rev-parse", "main")
        with self.assertRaisesRegex(h.Failure, "ripetere revisione"):
            h.sync()
        self.assertEqual(remote_head, self.git(self.remote, "rev-parse", "main"))
        self.assertEqual("Nuova proposta del collega\n", (self.clone / "docs/relazione-tecnica.md").read_text())
        self.write(self.clone, "demo/NOTE-TECNICHE.md", "Rivista compatibilità con le nuove note del collega.\n")
        self.accept()
        h.ready("Allinea note dopo integrazione")
        self.assertIn("Pubblicato", h.sync())
        self.assertEqual(h.git("rev-parse", "HEAD"), self.git(self.remote, "rev-parse", "main"))

    def test_real_rebase_conflict_keeps_local_commit_and_conflict_visible(self):
        self.task()
        self.accept()
        h.ready("Demo locale")
        self.remote_commit("demo/index.html", "Modifica concorrente incompatibile\n")
        with self.assertRaises(h.Failure):
            h.sync()
        self.assertTrue(h.names("diff", "--name-only", "--diff-filter=U", "-z"))
        self.assertTrue((self.clone / ".git/rebase-merge").exists())
        self.assertIn("Demo locale", self.git(self.clone, "log", "--all", "--format=%s"))
        self.git(self.clone, "rebase", "--abort")

    def test_rejected_push_preserves_commit_without_force_or_duplicate(self):
        self.git(self.remote, "config", "core.hooksPath", "hooks")
        hook = self.remote / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8", newline="\n")
        hook.chmod(0o755)
        before = self.git(self.remote, "rev-parse", "main")
        self.task()
        self.accept()
        h.ready("Demo da conservare")
        with self.assertRaises(h.Failure):
            h.sync()
        self.assertNotEqual(before, h.git("rev-parse", "HEAD"))
        self.assertEqual(before, self.git(self.remote, "rev-parse", "main"))
        self.assertIsNone(h.read_state("ready.json"))
        self.assertIn("Nessun task", h.sync())

    def test_staged_bad_json_cannot_be_hidden_by_fixed_worktree(self):
        self.write(self.clone, "demo/data.json", "{errato}\n")
        self.git(self.clone, "add", "demo/data.json")
        self.write(self.clone, "demo/data.json", "{}\n")
        with self.assertRaises(ValueError):
            h.check(use_staged=True)

    def test_switching_branch_prevents_automatic_publication(self):
        self.git(self.clone, "switch", "-c", "altro", "--track", "origin/main")
        with self.assertRaises(h.Failure):
            h.sync()

    def test_both_hook_protocols_request_review_once_and_handle_subdirectories(self):
        self.task()
        for name in ("claude", "codex"):
            payload = {"hook_event_name": "Stop", "cwd": str(self.clone / "demo"), "stop_hook_active": False}
            command = [sys.executable, str(self.clone / "scripts/hackathon.py"), "hook", "stop"]
            p = subprocess.run(command, input=json.dumps(payload), capture_output=True, text=True, timeout=30)
            self.assertEqual(0, p.returncode, p.stderr)
            self.assertEqual("block", json.loads(p.stdout)["decision"], name)
            payload["stop_hook_active"] = True
            p = subprocess.run(command, input=json.dumps(payload), capture_output=True, text=True, timeout=30)
            self.assertNotIn("decision", json.loads(p.stdout))

    def test_setup_preserves_existing_git_hooks(self):
        self.git(self.clone, "config", "core.hooksPath", ".git/hooks")
        self.write(self.clone, ".git/hooks/pre-commit", "#!/bin/sh\nexit 0\n")
        with self.assertRaisesRegex(h.Failure, "esistenti"):
            h.setup("technical")
        self.assertEqual(".git/hooks", h.git("config", "--get", "core.hooksPath"))

    def test_periodic_receive_integrates_colleague_commit_without_local_edits(self):
        self.remote_commit("docs/relazione-tecnica.md", "Documento aggiornato dal collega\n")
        result = h.watch_once()
        self.assertEqual("ok", result["state"])
        self.assertEqual("Documento aggiornato dal collega\n", (self.clone / "docs/relazione-tecnica.md").read_text())
        self.assertEqual(h.git("rev-parse", "HEAD"), self.git(self.remote, "rev-parse", "main"))

    def test_periodic_receive_never_rewrites_divergent_local_commits(self):
        self.write(self.clone, "demo/NOTE-TECNICHE.md", "Commit locale da conservare\n")
        self.git(self.clone, "add", "demo/NOTE-TECNICHE.md")
        self.git(self.clone, "commit", "-m", "Lavoro locale")
        before = h.git("rev-parse", "HEAD")
        self.remote_commit("docs/relazione-tecnica.md", "Lavoro remoto concorrente\n")
        self.assertEqual("attesa", h.watch_once()["state"])
        self.assertEqual(before, h.git("rev-parse", "HEAD"))
        self.assertFalse((self.clone / ".git/rebase-merge").exists())

    def test_receive_can_be_enabled_without_guessing_a_role(self):
        (h.state_dir() / "config.json").unlink()
        h.setup(None)
        self.remote_commit("docs/relazione-tecnica.md", "Aggiornamento senza ruolo locale\n")
        self.assertEqual("ok", h.watch_once()["state"])
        with self.assertRaises(h.Failure):
            h.ready("Ruolo necessario per pubblicare")

    def test_hook_commands_load_script_from_a_nested_directory(self):
        for filename in (".claude/settings.json", ".codex/hooks.json"):
            settings = json.loads((SOURCE / filename).read_text())
            command = settings["hooks"]["Stop"][0]["hooks"][0]["command"]
            payload = json.dumps({"hook_event_name": "Stop", "cwd": str(self.clone / "demo")})
            result = subprocess.run(command, shell=True, cwd=self.clone / "demo", input=payload,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual({}, json.loads(result.stdout))

    def test_background_receiver_starts_receives_and_stops(self):
        self.remote_commit("docs/relazione-tecnica.md", "Ricevuto dal processo periodico\n")
        h.setup("technical", watch_enabled=True)
        self.addCleanup(h.stop_watch)
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline and not h.read_state("watch-status.json"):
            time.sleep(0.1)
        self.assertEqual("ok", h.read_state("watch-status.json", {}).get("state"))
        self.assertEqual("Ricevuto dal processo periodico\n", (self.clone / "docs/relazione-tecnica.md").read_text())
        h.stop_watch()
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and (h.state_dir() / "watch.lock").exists():
            time.sleep(0.1)
        self.assertFalse((h.state_dir() / "watch.lock").exists())


if __name__ == "__main__":
    unittest.main()

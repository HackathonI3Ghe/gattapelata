# Automazioni del team: Claude Code e Codex

Le procedure sono condivise in `.agents/skills/`. Codex le scopre nel repository; Claude Code legge copie identiche in `.claude/skills/`. Per modificarle, cambiare la fonte e lanciare `python scripts/hackathon.py install-skills`. Gli script usano Python 3.10+ e Git, senza pacchetti Python aggiuntivi.

## Attivazione in ogni clone

Ogni persona usa un clone separato e lo stesso branch condiviso con upstream su `origin` (qui `main`). Il ruolo resta nella directory Git locale: non viene inviato ai colleghi.

Persona A:

```powershell
git pull --ff-only
python scripts/hackathon.py setup --role technical
```

Persona B:

```powershell
git pull --ff-only
python scripts/hackathon.py setup --role commercial
```

Il setup installa i controlli Git locali e associa il ruolo al branch/upstream attuale. Se esistono già hook Git attivi, si ferma per conservarli. Non modifica impostazioni globali o credenziali. Chi lavora su un altro branch deve rifare il setup intenzionalmente; uno switch di branch non cambia il destinatario del push da solo.

`python scripts/hackathon.py setup --receive-only` abilita soltanto la ricezione automatica e rimuove l'eventuale ruolo locale. Serve anche per manutenzioni esplicite dell'infrastruttura comune: i controlli Git restano attivi, ma staging e pubblicazione vengono gestiti intenzionalmente. Dopo la manutenzione riconfigurare il proprio ruolo. `--no-watch` permette di installare senza avviare il processo periodico.

Riavviare la sessione AI per caricare le skill e gli hook del progetto. In Codex aprire `/hooks`, leggere e fidarsi degli hook del repository: Codex richiede la fiducia nella definizione esatta prima di eseguirli. In Claude Code accettare la fiducia del workspace secondo il normale avvio. Il setup Git non sostituisce queste verifiche dei client. Non usare flag di bypass della fiducia. Fonti: [OpenAI Docs](https://learn.chatgpt.com/docs/hooks), [Claude Code](https://code.claude.com/docs/en/hooks).

## Cosa avviene automaticamente

- Un processo locale avviato dal setup controlla il remoto ogni 30 secondi. Con checkout pulito integra i commit con fast-forward (equivalente a `pull --ff-only`); con modifiche locali fa solo fetch. Se il processo termina, il prossimo prompt/sessione lo riavvia. Non riscrive commit locali divergenti.
- `SessionStart` e `UserPromptSubmit`: eseguono anche un aggiornamento prima che l'agente lavori. Se il checkout è sporco, aggiornano i riferimenti senza toccare i file e segnalano che le note locali possono essere vecchie.
- `Stop`: scrive un rapporto meccanico in `.git/hackathon/controllo.md`. Se il ruolo ha modifiche e manca una revisione aggiornata, chiede all'agente di applicare il revisore, una sola volta per turno. Il flag `stop_hook_active` evita continuazioni infinite. Un secondo tentativo incompleto segnala il limite e non pubblica.
- Dopo che l'agente ha completato revisione e note e ha marcato il task `ready`, `Stop` esegue controlli, staging esplicito dei soli file del ruolo, commit, fetch, rebase e push ordinario.
- `pre-commit`: controlla lo staging, encoding, JSON, conflitti, whitespace e coerenza delle copie delle skill. `pre-push`: verifica anche che i commit locali da pubblicare rispettino il ruolo. Questi controlli non dimostrano la conformità al bando.

Le configurazioni hook avviano un solo script per evento: le fasi dipendenti sono sequenziali. Un report di revisione contiene la valutazione dell'agente, non una certificazione indipendente. Non viene avviata una seconda CLI AI dagli hook. La revisione legge tutti i deliverable e scrive soltanto `NOTE-REVISIONE.md` nel ruolo locale.

## Comandi disponibili

```powershell
python scripts/hackathon.py status
python scripts/hackathon.py start
python scripts/hackathon.py watch-once
# Per fermare la ricezione periodica (setup la riattiva):
python scripts/hackathon.py stop-watch
python scripts/hackathon.py review
# Dopo la revisione AI accettata, nel ruolo tecnico:
python scripts/hackathon.py review-done --report demo/NOTE-REVISIONE.md
# Dopo aggiornamento note e verifiche del task:
python scripts/hackathon.py ready --message "Completa il percorso simulato della demo"
python scripts/hackathon.py sync
```

Nel ruolo commerciale il report è `docs/NOTE-REVISIONE.md` e la nota di passaggio è `docs/NOTE-COMMERCIALI.md`. I file del collega sono leggibili, ma non pubblicabili dalla sincronizzazione del tuo ruolo. `ready` lega l'autorizzazione a HEAD e al contenuto preciso dei file; modifiche successive la invalidano.

Il ruolo tecnico possiede `demo/` e `.github/workflows/`, come indicato nel brief aggiornato. `demo/node_modules/` e `demo/dist/` sono esclusi dalla sincronizzazione Git.

Skill: `$hackathon-sync`, `$hackathon-review`, `$hackathon-demo-check` in Codex; `/hackathon-sync`, `/hackathon-review`, `/hackathon-demo-check` in Claude Code. Se la scoperta non è disponibile nel client, l'agente può leggere direttamente i rispettivi `SKILL.md`.

## Arresti e ripresa

- Modifiche estranee, staging già presente, cambio branch, symlink esterni e operazioni Git in corso: nessuna sincronizzazione automatica. Preservare il lavoro e risolvere consapevolmente la situazione.
- Conflitto durante il rebase: resta visibile per la risoluzione manuale. Usare `git status`, risolvere e `git rebase --continue`, oppure `git rebase --abort` per tornare al commit locale. Gli hook non lo abortiscono e non riscrivono i file per nascondere il problema.
- Push respinto o rete non disponibile: il commit resta locale. Con checkout pulito eseguire `python scripts/hackathon.py start`, verificare i commit e poi `git push`. Se i branch divergono, il pull automatico si ferma: valutare un `git rebase origin/main` manuale, rivedere la compatibilità con il collega e poi pubblicare. Nessun force push o retry infinito. Un successivo task completato può pubblicare anche i commit precedenti del ruolo, controllati da pre-push.
- Modifiche del collega integrate durante il rebase prima del push: il commit resta locale e la revisione va ripetuta sul progetto aggiornato; aggiornare le note, ripetere `review-done`, `ready` e `sync`.
- `sync.lock` o `watch.lock` rimasti dopo un'interruzione: verificare che il relativo processo sia terminato prima di rimuovere il solo lock in `.git/hackathon/` (nei worktree il percorso Git può essere diverso). Il watcher usa una finestra nascosta su Windows; ultimo esito e orario sono visibili con `status`, senza log di credenziali.
- Review con correzioni necessarie: correggere il proprio ruolo e ripetere. I file ancora mancanti del collega sono pendenti; si può accettare un checkpoint parziale dichiarandolo, mai la consegna completa.

Il freeze è una regola semantica applicata dalle skill: l'hook non può distinguere automaticamente una nuova funzione da un fix. Audio, telefono reale, contrasto e durata rimangono NON VERIFICATO finché provati. Il check meccanico segnala file mancanti e segnaposto senza bloccare i commit di avanzamento.

## Verifica degli strumenti

```powershell
python -m unittest discover -s scripts/tests -v
python scripts/hackathon.py check
```

I test usano cloni e un remoto Git temporanei, senza chiamare servizi AI o pubblicare nel repository del team.

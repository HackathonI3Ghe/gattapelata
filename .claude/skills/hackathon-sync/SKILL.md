---
name: hackathon-sync
description: Sincronizza il lavoro di Gattapelata a inizio attività e pubblica i task completati, limitando commit e push ai file del ruolo locale.
---

# Sincronizzazione del team

Leggi `AGENTS.md`, `automation/README.md` e il ruolo in `python scripts/hackathon.py status`. La configurazione è locale al clone. Non scegliere il ruolo al posto di un collega.

A inizio attività esegui `python scripts/hackathon.py start`, poi leggi le `NOTE-*.md` dell'altro ruolo. Se il checkout non si aggiorna, comunica che le note potrebbero essere vecchie. Non risolvere automaticamente conflitti.

Il setup avvia anche la ricezione periodica ogni 30 secondi; gli hook la riavviano a inizio sessione/prompt se necessario. Il pull è solo fast-forward con checkout pulito; durante le modifiche locali viene rimandato. `status` riporta l'ultimo esito. Un branch divergente non va riscritto dal watcher.

A task completato:

1. Verifica soltanto il comportamento modificato. Dopo il freeze delle 19:30 del 12/10/2026 (Europe/Rome), applica solo fix e rifiniture.
2. Aggiorna una nota nel tuo ruolo: `demo/NOTE-TECNICHE.md` oppure `docs/NOTE-COMMERCIALI.md`. Riporta cosa è disponibile, verifiche effettuate, limiti e informazioni necessarie al collega. Non cambiare i deliverable del collega.
3. Se sono cambiati demo o documenti rispetto all'ultima revisione locale, applica `hackathon-review`. Se la demo è cambiata, applica anche `hackathon-demo-check`. Leggi le procedure condivise in `.agents/skills/` anche se il tuo ambiente non le espone come comandi.
4. Esegui `python scripts/hackathon.py ready --message "Descrizione concreta del task"`. Se ci sono blocchi nel rapporto di revisione, correggili prima. Un task incompleto non va marcato pronto.
5. L'hook Stop esegue commit e push; per pubblicare subito esegui `python scripts/hackathon.py sync`. Controlla l'esito e comunica l'hash pubblicato o il motivo dell'arresto.

Il consenso del team per questo flusso automatico è registrato in `AGENTS.md`; resta limitato al ruolo configurato. Nessun force push, stash automatico, bypass degli hook o modifica a configurazioni globali. Le modifiche estranee e uno staging già presente arrestano la sincronizzazione. Un push fallito lascia il commit locale e va segnalato; non dichiararlo pubblicato.

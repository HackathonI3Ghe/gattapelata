---
name: hackathon-demo-check
description: Verifica la demo Gattapelata dopo modifiche al flusso o prima della presentazione, inclusi voce, modalità simulata, accessibilità e durata.
---

# Prova della demo

Leggi `AGENTS.md`, `demo/NOTE-DEPLOY.md` e i sorgenti della demo disponibili. Esegui `python scripts/hackathon.py review` per gli indizi statici, poi prova il percorso completo nel browser se disponibile. Segui lo stack attualmente concordato: React + Vite, build statica su GitHub Pages. Se `demo/package.json` è presente, esegui `npm ci`, `npm run build` e l'anteprima; finché è assente, valuta la demo HTML transitoria dichiarando il limite. Non introdurre backend o cambiare stack per testare.

Verifica: apertura del sito e asset sotto `/gattapelata/`, azione principale, "Aspetta" / "Vai", telefono e strada coerenti, simulazione del lampeggiante e del verde, ripartenza della prova e gestione di fotocamera o voce non disponibili. Verifica la fotocamera su HTTPS con richiesta permesso dopo il tap e chiusura delle tracce. Distingui la modalità simulata dalla fotocamera e dal riconoscimento reale opzionale. L'offline e l'installabilità PWA vanno dichiarati soltanto se implementati e provati.

Misura realmente il percorso sotto 60 secondi; controlla su telefono o viewport mobile testo almeno 24px, pulsanti grandi, contrasto e assenza di contenuti tagliati. Verifica sintesi vocale italiana senza messaggi sovrapposti, quando l'ambiente consente l'audio. Una viewport emulata non equivale a una prova su telefono reale.

Registra browser, dispositivo/viewport, durata misurata, prove ed esiti in `demo/NOTE-TECNICHE.md` se sei nel ruolo tecnico; nel ruolo commerciale riporta le osservazioni in `docs/NOTE-COMMERCIALI.md`. Se strumenti, dispositivo o audio non sono disponibili, scrivi NON VERIFICATO per quelle prove. Non affermare che il controllo statico dimostri contrasto, CSS effettivo, durata o sicurezza stradale.

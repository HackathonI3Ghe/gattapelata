---
name: hackathon-review
description: Rivede demo, relazione, offerta e pitch di Gattapelata contro il bando e le decisioni condivise, con evidenze e requisiti non verificati.
---

# Revisore del bando

Leggi prima `bando-gara-gattapelata.md`, poi `AGENTS.md`, `automation/REQUISITI.md`, i deliverable disponibili e le `NOTE-*.md`. Esegui `python scripts/hackathon.py review`: il rapporto meccanico è un punto di partenza, non una valutazione semantica.

Leggi i file del collega, ma modifica solo un rapporto nel tuo ruolo: `demo/NOTE-REVISIONE.md` o `docs/NOTE-REVISIONE.md`. Se non c'è un ruolo configurato, restituisci il rapporto in chat senza cambiare deliverable. Non lanciare un'altra CLI AI dal revisore: può attivare nuovamente gli hook.

Per ogni ID in `automation/REQUISITI.md`, riporta una riga con requisito, fonte, evidenza `file:riga`, stato **OK**, **MANCANTE**, **NON VERIFICATO** o **NON APPLICABILE**, e azione necessaria. Un'affermazione nel pitch non prova un comportamento della demo. Separa requisiti del bando da decisioni del team. Non inventare un punteggio ottenuto o conformità GDPR.

Controlla anche queste contraddizioni specifiche:

- Solo l'app è prevista a T+90'; lampeggianti e modifiche ai regolatori sono successivi. La simulazione dell'hardware non prova l'installazione.
- Il rilevamento del veicolo non dimostra che sia sicuro attraversare: considera occlusioni, veicoli fuori campo, ritardo di elaborazione e velocità di cammino. Non descrivere la demo come sistema certificato.
- Un "Aspetta" seguito da un veicolo è un indicatore candidato; non equivale a una vita salvata o a un incidente certamente evitato. Servono confronto, esposizione agli attraversamenti e fonti indipendenti.
- Gli studi e i precedenti indicati "da verificare" richiedono fonti primarie prima di essere citati come prove.
- La ripartizione economica deve avere importi coerenti e somma esplicita; non spostare hardware o servizi necessari in altre voci per nascondere i costi infrastrutturali.
- Distingui disponibilità reale a T+90' da proposta, dipendenze operative e simulazione.

Termina il rapporto con `Esito: ACCETTATO` oppure `Esito: CORREZIONI NECESSARIE`, motivando eventuali limiti accettati. Durante lo sviluppo, deliverable ancora mancanti sono lavoro pendente del relativo proprietario: possono essere accettati per un checkpoint parziale, non per la consegna finale. Prove manuali non eseguite rimangono NON VERIFICATO.

Esegui `python scripts/hackathon.py review-done --report <rapporto-del-tuo-ruolo>` solo con esito ACCETTATO. Registra l'evidenza locale; modifiche successive ai file del progetto rendono la revisione da ripetere. Correggi solo il tuo ruolo; trasmetti gli altri rilievi attraverso il rapporto.

# Consegna delle automazioni

Sono disponibili le tre skill condivise, le copie Claude Code, gli adattatori hook per entrambi i client e lo script Python senza dipendenze aggiuntive. La matrice distingue i requisiti del bando dalle decisioni del team.

La ricezione dei commit del collega viene tentata ogni 30 secondi e prima dei prompt: integra solo con checkout pulito e fast-forward. La pubblicazione richiede ruolo configurato, nota aggiornata, revisione accettata e contenuto marcato pronto; non coinvolge file estranei. Un'integrazione che cambia i deliverable rende la revisione da ripetere. Conflitti e push respinti conservano il lavoro locale.

Validazione: 18 test comportamentali su cloni e remoto Git locali, inclusi processo periodico avviato/fermato, ricezione effettiva, checkout sporco, branch divergente, staging estraneo, JSON errato nell'indice, conflitto di rebase, push respinto, workflow tecnico e protocolli hook di entrambi i client. Le tre skill superano il validatore skill-creator.

Limiti: verificati gli script e i messaggi hook, non un'intera sessione interattiva dei due client. Codex richiede la fiducia negli hook tramite `/hooks`; i colleghi devono effettuare il setup nel proprio clone e riavviare la sessione. La conformità del prodotto, le prove della demo su telefono, l'audio e la durata non sono attestati da questi test. Il controllo meccanico segnala ancora segnaposto nei documenti, senza assegnare conformità.

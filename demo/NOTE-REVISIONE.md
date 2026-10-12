# Revisione delle correzioni dopo il confronto economico

Checkpoint correttivo richiesto dal team: documenti, brief, contatori e slide aggiornate. Accettazione del contenuto da pubblicare, non della conformità completa al bando o del servizio stradale. Nessuna prova, attestazione del concorrente o preventivo inventati.

| ID | Requisito / fonte | Evidenza | Stato | Azione o limite |
|---|---|---|---|---|
| B01 | Art. 2: Riduzione del rischio di morte e incidenti: meccanismo causale, limiti e comportamento dimostrato. | docs/relazione-tecnica.md:9 | NON VERIFICATO | Meccanismo e limiti espliciti; efficacia stradale da validare. |
| B02 | Art. 2; Art. 5, 20 pt: Usabilità da anziani con poca dimestichezza tecnologica. | docs/relazione-tecnica.md:26 | NON VERIFICATO | Onboarding finanziato; prove con utenti e telefoni reali pendenti. |
| B03 | Art. 2: Funzionamento nei vicoli come sono oggi, senza opere stradali necessarie. | docs/relazione-tecnica.md:70 | NON VERIFICATO | Nessuna promessa di visuale attraverso ostacoli; uso nei siti da provare. |
| B04 | Art. 2; Art. 5, 30 pt: Risultato misurabile: baseline 342 morti nel 2025, obiettivi, KPI, fonti, esposizione, confronto e limiti di attribuzione. | docs/relazione-tecnica.md:15 | NON VERIFICATO | Protocollo con esposizione, confronto e fonti; nessun risultato o conversione avvisi/vite. |
| B05 | Art. 2; Art. 5, 5 pt: Privacy: dati trattati, finalità, base giuridica, consenso ove richiesto, accessi e conservazione. | docs/relazione-tecnica.md:77 | NON VERIFICATO | Flussi e durate proposti; progettazione e valutazione privacy pendenti. |
| B06 | Art. 3; Art. 5, 10 pt: Operatività entro 90 minuti: piano, prerequisiti e dipendenze disponibili. | docs/relazione-tecnica.md:60 | NON VERIFICATO | Canale e servizio stradale distinti; piena conformità Art.3 non dimostrata. |
| B07 | Art. 3: Gestione e manutenzione per 48 mesi. | docs/offerta-economica.md:39 | NON VERIFICATO | 48 mesi, perimetro e SLA proposti; collaudo e contratto pendenti. |
| B08 | Art. 3: Base d'asta 10.000.000 euro IVA esclusa; ripartizione e somma verificabile degli importi proposti. | docs/offerta-economica.md:20 | OK | Somma €10M verificata; tetto rendicontato, tranche e riserve non automatiche. |
| B09 | Art. 4: Dichiarazione requisiti generali per contrattare con la PA. | docs/offerta-economica.md:76 | MANCANTE | Dichiarazione reale da produrre; non inventata. |
| B10 | Art. 4: Media annua almeno 5.000.000 like LinkedIn negli ultimi tre anni; trattare il requisito satirico esplicitamente senza inventare attestazioni. | docs/offerta-economica.md:77 | MANCANTE | Storico da documentare; non inventato. |
| B11 | Art. 4: Precedente app usata da nessuno ma scaricata da molti; distinguere la gag dall'evidenza reale. | docs/offerta-economica.md:78 | MANCANTE | Referenza reale da produrre. |
| B12 | Art. 5, 15 pt: Originalità della soluzione spiegata e coerente con la demo. | docs/relazione-tecnica.md:34 | OK | Originalità descritta senza unicità; confronto alternative con costi ancora da preventivare. |
| B13 | Art. 5, 20 pt: Costi infrastrutturali necessari alla completa messa in opera separati, inclusi hardware, installazione e servizi necessari. | docs/offerta-economica.md:56 | NON VERIFICATO | Costo prudenziale €3,22M verificato, massimo prudenziale €3,92M con tutta la riserva residua; preventivi, necessità e classificazione finale pendenti. |
| B14 | Art. 6: Demo, relazione tecnica e offerta economica disponibili e coerenti. | docs/relazione-tecnica.md:1 | OK | Demo, relazione, offerta e 18 slide presenti e allineati; non certificazione del servizio. |
| B15 | Art. 6: Demo dimostrata entro le 20:00 del 12/10/2026: richiede attestazione dell'evento, non controllo statico. | docs/relazione-tecnica.md:91 | NON VERIFICATO | Evento entro le 20 richiede attestazione; non dedotto da Git. |
| B16 | Art. 7: Richiamo al Fantamorto 2025-2026; non attribuire norme non disponibili al testo del regolamento. | docs/pitch.md:21 | OK | Gag distinta da norme non consultate. |
| T01 | AGENTS.md; NOTE-DEPLOY.md: React + Vite, build statica senza backend, dati simulati dichiarati e modalità simulata disponibile. Demo HTML consentita soltanto come transizione indicata nel brief. | docs/relazione-tecnica.md:87 | NON VERIFICATO | Transizione HTML mantenuta; nessuna migrazione durante il freeze. |
| T02 | AGENTS.md: Testo almeno 24px, pulsanti enormi, contrasto, mobile-first: verifica nel browser. | demo/NOTE-TECNICHE.md:157 | NON VERIFICATO | Browser non disponibile; layout, contrasto e telefono reale non riprovati. |
| T03 | AGENTS.md: Un'azione principale, voce it-IT, flusso misurato sotto 60 secondi. | demo/NOTE-TECNICHE.md:153 | NON VERIFICATO | Node con DOM e tempo simulati: flusso 27,4s virtuali, contatori e riavvio OK; audio non provato. |
| T04 | AGENTS.md: Livello 1 a T+90'; hardware Livello 2 successivo, su strutture esistenti; simulazione dichiarata. | docs/pitch.md:24 | OK | Hardware e indossabile solo dopo le prove; 16 slide principali +2 approfondimenti. |
| T05 | AGENTS.md; NOTE-DEPLOY.md: Nessuna dipendenza dal GPS; fotocamera su HTTPS, permessi dopo tap, video mobile e chiusura delle tracce. Asset sotto /gattapelata/, deploy Pages riuscito; prove non eseguite esplicite. | demo/NOTE-TECNICHE.md:157 | NON VERIFICATO | Sintassi e asset verificati; browser e camera reale pendenti. Deploy verificato separatamente dopo push. |
| T06 | AGENTS.md: Demo, note, relazione, pitch e offerta descrivono lo stesso prodotto; fonti citate verificate. | docs/NOTE-COMMERCIALI.md:13 | OK | Contraddizioni avvisi/T+90/costi corrette; fonti non verificate rimosse dalle slide, concept e 330 preservati come aspirazione. |
| T07 | AGENTS.md: Freeze 19:30, prova interna 19:45 (12/10/2026 Europe/Rome); dopo il freeze solo fix e rifinitura. | docs/NOTE-COMMERCIALI.md:15 | NON VERIFICATO | Fix autorizzati dopo il freeze; prova generale ed evento non attestati. |
| T08 | AGENTS.md: Modifiche limitate al proprio ruolo, note di passaggio aggiornate, deliverable in italiano. | docs/NOTE-COMMERCIALI.md:15 | OK | Scope trasversale espressamente richiesto; note di entrambi i ruoli aggiornate, nessun ruolo locale modificato. |

## Verifiche del task

- Somme lette dalle tabelle: €10.000.000, costo completo prudenziale €3.220.000, pilota €250.000 incluso; stessa ripartizione nelle slide.
- 18 sezioni HTML, ID univoci, immagine del collega e riferimento relativo presenti; nessuna pagina animata aggiunta.
- Sintassi JS di demo e slide, controlli meccanici e whitespace.
- Codice demo eseguito in Node con DOM e tempo simulati: contatori 1/1 e SMS illustrativo, riavvio, perdita rilevamento senza verde e senza incremento, errore modello con stop traccia e riavvio disponibile. Non una prova browser o una durata reale.
- Browser non disponibile: resa visiva, audio, telefono reale e proiettore NON VERIFICATI; nessun aggiramento.

## Rischi che restano esterni al fix

Efficacia, conformità piena a T+90, fonti indipendenti, dati della popolazione, preventivi, classificazione definitiva, privacy, affidabilità e dichiarazioni Art.4 restano aperti. Sono espliciti in relazione e offerta. Il traguardo 330 resta aspirazionale e non giustifica il prezzo. Le unità e gli SLA proposti non sono prove di capacità esistente. Le riserve non sono pagamenti garantiti.

Esito: ACCETTATO

Accettato il checkpoint correttivo per pubblicare la proposta trasparente e la demo illustrativa richiesta; non accettazione finale della gara, non autorizzazione a usare la demo per attraversare davvero.

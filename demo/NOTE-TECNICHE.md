# Note tecniche – Passo Sicuro

Nota di passaggio della Persona A (tecnica) per la relazione. Concetto: vedi "Concetto scelto" in `AGENTS.md`.

## La demo (`demo/index.html`)

- **Un solo file**, senza build, senza backend e senza librerie da CDN: funziona offline e anche aperto con doppio click. Il nome dell'app è nella costante `NOME_APP` in cima allo script.
- **Layout:** a sinistra il telefono (Livello 1, l'app), a destra la strada simulata (Livello 2, l'hardware). Su schermo stretto il telefono va a tutto schermo e la strada finisce sotto.
- **Flusso simulato** (circa 28 secondi senza voce, sotto i 60 anche con la voce):
  1. Maria preme ATTRAVERSO. Voce: "Ciao Maria. Guarda a sinistra". La fotocamera simulata riconosce un'auto (riquadro "AUTO").
  2. L'app mostra il calcolo: auto tra 3 s, a Maria servono 7 s (5 m ÷ 0,8 m/s + 1 s di margine). Schermo rosso **ASPETTA**. L'auto passa e il contatore "Quasi-incidenti evitati" sale a 1.
  3. Sinistra libera, destra libera, avanti libero.
  4. Schermo verde **VAI ADESSO**, il telefono lampeggia (bianco/giallo). In strada si accendono i lampeggianti LED, il radar vede la persona sulle strisce, il semaforo pedonale dà il verde con **+8 s per attraversamento lento**.
  5. "Sei arrivata dall'altra parte" e SMS finto al figlio: "Mamma è arrivata viva dall'altra parte ✓".
- **Regia** (in basso a destra, poco visibile): Spazio = avanti/avvia, R = riavvia e azzera i contatori, M = voce sì/no, C = fotocamera vera. A fine flusso Spazio torna all'inizio mantenendo i contatori.
- **Voce:** `speechSynthesis` in italiano (`it-IT`), parte solo dopo il primo click o tasto. Se la voce non c'è, la demo prosegue lo stesso.
- **Fotocamera vera (facoltativa, tasto C o pulsante 📷):** TensorFlow.js 4.22.0 + COCO-SSD 2.2.3 da CDN, caricati solo quando si attiva. Riconosce auto, camion, bus, moto e bici, disegna i riquadri, stima il tempo all'arrivo dalla crescita del riquadro e mostra ASPETTA / Libero con la voce. Serve HTTPS o `localhost` e la rete. Il primo caricamento del modello richiede circa 13 secondi: attivarla una volta prima della presentazione. Se fotocamera, rete o modello non sono disponibili, la demo torna da sola alla simulazione.

## Architettura in produzione

**Livello 1 – App (attiva a T+90').**
- PWA statica: HTML, CSS e JavaScript su hosting statico con HTTPS. La fotocamera nel browser funziona solo con HTTPS.
- Riconoscimento dei veicoli **sul telefono**: TensorFlow.js con il modello COCO-SSD (classi auto, moto, bus, camion, bici). Nessuna immagine esce dal dispositivo.
- **Tempo all'arrivo del veicolo** stimato da quanto cresce il riquadro del veicolo tra un fotogramma e l'altro (tempo al contatto = dimensione ÷ velocità di crescita). Non serve conoscere la distanza.
- **Tempo che serve alla persona** = larghezza del vicolo ÷ velocità di camminata personale + margine. La velocità si imposta all'installazione (o si misura nei primi attraversamenti), la larghezza ha un valore prudente predefinito.
- Decisione: se il veicolo arriva prima del tempo che serve, **ASPETTA**; altrimenti **VAI**. Guida vocale "Guarda a sinistra / a destra / avanti". Telefono al collo con porta-telefono, mani libere.
- **Niente GPS**: nei vicoli stretti è impreciso e non serve.

**Livello 2 – Hardware sugli attraversamenti esistenti (NON attivo a T+90').**
- Lampeggiante LED a energia solare con **sensore radar o termico**: si accende da solo quando qualcuno è sulle strisce, anche senza telefono. Nessuna immagine.
- Semaforo: modulo sul regolatore esistente o integrazione con la centrale semaforica. Su richiesta dell'app chiama il verde pedonale e lo allunga finché il sensore vede la persona sulle strisce.
- Collegamento app → semaforo: **via rete** (app → centrale semaforica). Il Bluetooth dal browser (Web Bluetooth) non c'è su iPhone/Safari, quindi non ci basiamo su quello; un'app nativa può arrivare in una fase successiva. Il lampeggiante non dipende dall'app.
- Installazione progressiva nei 48 mesi di gestione, partendo dagli attraversamenti con più incidenti.

## Messa in funzione in 90 minuti (solo Livello 1)

| Tempo | Attività |
|---|---|
| T+0 – T+20' | Pubblicazione della PWA su hosting statico HTTPS (es. GitHub Pages o hosting del Comune) e prova da telefono |
| T+20' – T+40' | Link e QR code diffusi dai canali del Comune (SMS, sito, social, bacheche, farmacie) |
| T+40' – T+90' | Installazione assistita: familiari, farmacie, volontari, centri anziani. Si aggiunge l'icona alla schermata Home e si imposta la velocità di camminata |
| T+90' | Livello 1 in funzione in tutti i vicoli. Il Livello 2 segue nei 48 mesi |

Distribuzione dei porta-telefono al collo: in parallelo, non blocca l'avvio.

## Dati personali trattati

- **Sul telefono soltanto:** velocità di camminata, nome per la voce, contatto del familiare per l'SMS (facoltativo, con consenso).
- **Immagini della fotocamera:** elaborate sul telefono, mai salvate né inviate.
- **Al Comune:** solo contatori anonimi aggregati: numero di attraversamenti assistiti e numero di "Aspetta" seguiti dal passaggio di un veicolo entro pochi secondi (quasi-incidenti evitati). Nessuna posizione GPS, nessun nome, nessuna immagine.
- **Sensori stradali:** radar o termici, non producono immagini identificabili. Contano attraversamenti e conflitti.
- Nessun account da creare.

## Limiti noti

- **Curve cieche:** la fotocamera non vede dietro l'angolo. Mitigazione: margine più alto nei punti noti; fase 2 "occhi del vicolo".
- **Stima con una sola fotocamera:** approssimata, soprattutto con veicoli lontani o di lato. Per questo si usa un margine di sicurezza.
- **Batteria:** fotocamera e riconoscimento consumano. L'app si accende solo per l'attraversamento.
- La fotocamera richiede HTTPS: aprire il file con doppio click va bene solo per la demo simulata.

## Prove eseguite sulla demo (12/10/2026, 19:00 circa)

| Prova | Esito |
|---|---|
| Sintassi dello script (`node --check`) | OK |
| Flusso completo in Chrome desktop, servito da `localhost` | OK, nessun errore in console |
| Durata del flusso senza voce | 27,5 s misurati |
| Vista telefono a 390 px di larghezza (iframe in Chrome) | OK: telefono a tutto schermo, nessuno scorrimento orizzontale, testo minimo 24 px, "ASPETTA" non tagliato |
| Contatori (quasi-incidenti e attraversamenti) | OK, salgono a 1 a fine flusso |
| Fotocamera negata o assente | OK: messaggio "Fotocamera non disponibile" e ritorno alla simulazione |
| Caricamento TensorFlow.js + COCO-SSD da CDN | OK in 12,7 s (backend WebGL), nessun errore |
| Riconoscimento di veicoli veri con fotocamera | NON VERIFICATO (nessuna fotocamera nell'ambiente di prova) |
| Apertura con doppio click (`file://`) | NON VERIFICATO (nessuna dipendenza esterna, quindi atteso OK) |
| Voce italiana con audio | NON VERIFICATO (provata con voce spenta) |
| Telefono reale | NON VERIFICATO |
| Contrasto misurato con strumento | NON VERIFICATO (scelti bianco su rosso #c40000 e su verde #007a33) |

## Slide della presentazione (`demo/slides/index.html`)

- Online: **https://hackathoni3ghe.github.io/gattapelata/slides/** (pubblicate dallo stesso workflow della demo). In locale si aprono con doppio click.
- Comandi: frecce o Spazio per scorrere, **N** mostra le note del relatore, **F** schermo intero, `#numero` nell'indirizzo apre una slide precisa. Per il PDF: Stampa → Salva come PDF.
- Il file è generato dai sorgenti delle slide tenuti dalla Persona A: **non modificarlo a mano**, verrebbe sovrascritto.
- Segnaposto ancora aperti: `[NOME TEAM]` (copertina, chiusura), `[__]` vite salvate all'anno (efficacia), conservazione dei contatori (privacy), tutti gli importi `[€__]` (offerta), dichiarazioni dei requisiti Art. 4. **Persona B:** metti numeri e testi in `docs/offerta-economica.md`, `docs/relazione-tecnica.md` e `docs/pitch.md`; fino alle 19:40 le slide vengono riallineate a quei file ogni 5 minuti.
- Prova eseguita: generazione delle 15 slide e resa in Chrome (senza interfaccia) delle slide 7 e 13, OK. Non provate: proiettore di sala, stampa in PDF.

## Restyling grafico della demo (12/10/2026, 19:20-19:30)

- Cambia solo l'aspetto: nessuna nuova funzione, logica JS invariata. Unica modifica JS: il disegno delle finestre con persiane nella scena della strada.
- Carattere **Atkinson Hyperlegible** (Braille Institute, pensato per chi vede poco), da Google Fonts con ripiego sui caratteri di sistema se la rete manca. Spunto per la relazione (§2, facilità d'uso).
- Telefono: logo "Passo Sicuro" (pedone con bastone sulle strisce), mirino e linea di scansione sulla fotocamera, etichetta **"Immagine simulata"** nella vista simulata (sparisce con la fotocamera vera), pulsante ATTRAVERSO con icona e anello pulsante, schermate ASPETTA/VAI con sfumature e battito, barra di avanzamento a strisce, SMS come notifica.
- Corretto: su telefono il lampeggio della fase VAI non si vedeva (l'ombra interna restava sotto lo schermo). Ora è un bordo bianco/giallo sopra lo schermo, anche su desktop.
- Su schermi molto stretti i testi principali si riducono in proporzione (minimo 24 px, tranne la barra del nome). Le animazioni decorative si spengono con "riduci movimento"; il lampeggio resta.
- Lato strada: intestazione con logo e slogan, scena con colori da centro storico, schede che si illuminano quando l'hardware è attivo. Su desktop il telefono resta sempre interamente visibile.
- Prove: `node --check` OK; i 40 id usati dal JS sono presenti; stati iniziale, fotocamera, ASPETTA, VAI e arrivo visti a 360 e 412 px (iframe in Chrome) e su desktop, senza testo tagliato. NON VERIFICATO: telefono reale, Safari iOS, voce con audio.
- Su telefono la barra di regia è una riga compatta in basso, senza coprire il contatore. Su desktop è trasparente come prima. Su schermi desktop bassi (fino a 760 px) la scena si riduce, così le schede restano visibili; la scheda "Dati anonimi" può comunque richiedere uno scorrimento, mentre il telefono resta fisso.
- Unica eccezione ai 24 px: l'etichetta "Immagine simulata" (13 px), che serve alla commissione e non all'anziano.

### Prova demo dopo il restyling (19:30, sito pubblicato)

| Prova | Esito |
|---|---|
| Sito https://hackathoni3ghe.github.io/gattapelata/ con l'ultima versione | OK (Chrome desktop, Windows) |
| Flusso completo, voce spenta, da ATTRAVERSO all'SMS | OK, **27,5 s** misurati; passi 1→7, contatori a 1, SMS visibile |
| Riavvia | OK: torna all'inizio, contatori a 0, pulsante visibile, lampeggio spento |
| Carattere Atkinson Hyperlegible caricato | OK |
| Errori in console | Nessuno |
| Revisione indipendente del diff (subagente) | Nessun problema bloccante. Corretti i 2 minori: contrasto del verde (circa 4:1) e regia sopra le schede su desktop |
| Viewport 360×740 e 412×860 (iframe) | OK: nessuno scorrimento orizzontale, regia su una riga, ATTRAVERSO entra nel pulsante |
| Fotocamera vera, voce con audio, telefono reale, Safari iOS | NON VERIFICATO in questo giro (JS della fotocamera non modificato) |

## Numeri e alternativa indossabile nelle slide pubblicate

Su richiesta del team sono aggiornate le 16 slide HTML, mantenendo il design esistente. Nuova slide 10: alternativa autonoma al telefono sul petto con una camera, computer, batteria, voce e vibrazione. Solo fase 2 dopo T+90', pilota controllato su 100 persone prima di estendere fino a 1.000 utenti. Il dispositivo non esiste ancora; non viene dichiarata visione a 360°. La pagina animata è stata esclusa dalla consegna per l'ultima indicazione dell'utente.

Importi da docs/offerta-economica.md: € 350/unità (fascia stimata € 250–400), pilota € 250.000 già incluso, totale € 10 milioni, infrastruttura € 1,24 milioni incluse riserve, 12,4%. Scenario di circa 17 vite/anno condizionato a −5% della baseline; non previsione validata. Obiettivo pilota −15% conflitti per 1.000 attraversamenti. Avvisi descritti come indicatori candidati di rischio, non incidenti certamente evitati. Durata conservazione proposta: 30 giorni eventi e 48 mesi aggregati, da motivare nella progettazione privacy.

Nome Team Passo Sicuro provvisorio. Dichiarazioni Art. 4 da documentare; nessun dato storico inventato. Relazione tecnica ancora da allineare dal ruolo commerciale. I sorgenti artifact del collega non sono nel repository: è aggiornata la copia HTML pubblicata, con istruzione di portare i numeri nei sorgenti prima di rigenerare, altrimenti si perdono. Non modificata la demo principale.

Verifiche in questo task: aritmetica, numero slide, assenza di segnaposto numerici e sintassi dello script. NON VERIFICATO: resa visiva delle slide aggiornate, proiettore, telefono reale, audio; Chrome non controllabile per permessi del computer mancanti. Deploy da verificare dopo il push.

Sincronizzazione: integrato af5ff2c del collega prima del push; revisione delle slide ripetuta sul checkout aggiornato. Nessun conflitto.

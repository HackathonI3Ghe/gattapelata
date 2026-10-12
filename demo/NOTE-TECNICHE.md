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

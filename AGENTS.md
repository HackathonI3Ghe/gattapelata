# Hackathon Gattapelata – brief condiviso per agenti (Claude / Codex)

Fonte di verità: [bando-gara-gattapelata.md](bando-gara-gattapelata.md). Leggilo prima di tutto.

## Scadenze (12/10/2026)

- **19:30** freeze: niente nuove funzioni, solo fix e rifinitura.
- **19:45** consegna interna: demo + documenti pronti, prova generale.
- **20:00** presentazione (Art. 6: la demo va *dimostrata* entro le 20:00).

## Concetto scelto

**Nome:** TODO. **Slogan:** *"Non vi diciamo se arriva una macchina. Vi diciamo se fate in tempo."*

**Livello 1 – App (PWA), in funzione a T+90' ovunque, anche nei vicoli senza strisce né semafori.** L'anziano apre l'app con un solo pulsante grande. Il telefono è appeso al collo con un porta-telefono, quindi ha le mani libere. La voce dice "Guarda a sinistra", "Guarda a destra", "Guarda avanti", come gli hanno insegnato da bambino, e lui gira il busto. La fotocamera riconosce i veicoli sul telefono stesso. L'app non si limita a segnalare se c'è un veicolo: calcola se la persona **fa in tempo**.
- *Tempo all'arrivo del veicolo:* stimato da quanto cresce il veicolo nell'inquadratura, senza misurare la distanza.
- *Tempo che serve a quella persona:* larghezza del vicolo diviso la sua velocità di camminata, più un margine.

Poi dice "Aspetta" oppure "Vai adesso". Durante l'attraversamento lo schermo e il flash lampeggiano, così chi guida lo vede. Non usa il GPS, che nei vicoli non funziona bene.

Opzionale e con consenso: SMS al familiare *"Arrivata viva dall'altra parte"*.

**Motivazione dell'efficacia:**
- Gli anziani vedono il veicolo ma **sbagliano a stimare velocità e distanza**: scelgono intervalli troppo brevi (studi sulla scelta dei "gap": Oxley et al., Dommes & Cavallo, *da verificare prima di citarli*).
- Camminano più piano, sentono meno (auto elettriche e monopattini sono silenziosi) e guardano per terra mentre attraversano.

**Livello 2 – Hardware sugli attraversamenti che esistono già (strisce e semafori).** Viene installato progressivamente nei 48 mesi di gestione, iniziando dagli attraversamenti con più incidenti. **Non è attivo a T+90'** e non va mai dichiarato tale. Si monta su pali e semafori esistenti, senza opere stradali.
- *Strisce:* lampeggiante LED a energia solare con un sensore di presenza **radar o termico, non telecamere**: non produce immagini identificabili, quindi pesa poco sulla privacy. Il lampeggiante si accende da solo quando qualcuno attraversa, quindi protegge anche chi non ha il telefono. L'app aggiunge il segnale via Bluetooth "sto attraversando, sono lento".
- *Semafori:* un modulo sul regolatore che esiste già. L'app chiama il verde pedonale senza che serva premere il pulsante e **allunga il verde** finché il sensore vede la persona ancora sulle strisce.
- *Precedenti da verificare:* Green Man+ a Singapore (gli anziani avvicinano una tessera e ottengono più tempo di verde) e i Puffin crossing nel Regno Unito (sensori che allungano la fase pedonale).

**Misura (vale i 30 punti):**
- *Dall'app:* ogni "Aspetta" seguito dal passaggio di un veicolo entro pochi secondi conta come quasi-incidente evitato, registrato in forma anonima.
- *Dai sensori:* conteggio di attraversamenti e conflitti, indipendente da quante persone usano l'app.
- *Confronto:* vicoli e incroci con la soluzione contro quelli senza, attivandola gradualmente. Baseline: 342 morti nel 2025.

**Compromesso sul prezzo, da gestire (Persona B):** l'hardware fa salire i costi infrastrutturali, che pesano 20 punti.
- Limitarlo agli attraversamenti esistenti più pericolosi, con unità economiche da aggiungere all'esistente.
- Mostrare il costo per singolo attraversamento.
- Mettere il resto dei 10M in voci non infrastrutturali: gestione, formazione e distribuzione dei porta-telefono, campagna di misura.

## Vincoli del bando che guidano ogni scelta

- **In funzione entro 90 minuti dalla firma** (Art. 3): niente app nativa da store (la review non passa in 90'). Usare PWA/web, SMS, telefonata, dispositivi già esistenti.
- **Anziani con poca dimestichezza tecnologica** (Art. 2): interazione minima. Un pulsante, voce, telefono fisso come alternativa.
- **Vicoli "così come attualmente sono"** (Art. 2): l'app deve funzionare da sola nei vicoli come sono oggi. L'hardware del Livello 2 si aggiunge soltanto, su attraversamenti, pali e semafori che esistono già, senza opere stradali. Il GPS nei vicoli stretti è impreciso (urban canyon), quindi bisogna prevedere un'alternativa.
- **Risultato misurabile** (Art. 2 + Art. 5): vite salvate e incidenti evitati, con un metodo di misura esplicito. Baseline: **342 morti nel 2025**.
- **Privacy/GDPR** (Art. 2): dati minimi, consenso, conservazione breve.
- **Prezzo** (Art. 5): pesa 20 punti ed è inteso come **costi infrastrutturali**, quindi tenerli bassi. La base d'asta è di €10.000.000 IVA esclusa e va ripartita tra voci.

## Griglia di valutazione → dove viene trattata

| Criterio (Art. 5) | Punti | Relazione tecnica | Pitch |
|---|---|---|---|
| Efficacia + metodo di misura | 30 | §1 | slide efficacia |
| Facilità d'uso anziani | 20 | §2 | demo live |
| Originalità | 15 | §3 | slide soluzione |
| Fattibilità e tempi (90') | 10 | §4 | slide "T+90 minuti" |
| Privacy | 5 | §5 | 1 slide |
| Prezzo | 20 | – | slide offerta economica |

## Divisione del lavoro (2 persone, ognuna con il proprio agente)

Regola d'oro: **ognuno modifica solo i file del proprio ruolo.** Le informazioni passano tramite i file `NOTE-*.md`.

### Persona A – Tecnica → possiede `demo/`

- `demo/index.html`: **un solo file**, niente build, niente backend, dati finti. Si apre con doppio click o da telefono.
- Mobile-first, testo ≥ 24px, pulsanti enormi, alto contrasto, sintesi vocale in italiano (`speechSynthesis`, `lang="it-IT"`).
- Un'azione principale. Il flusso della demo deve durare meno di 60 secondi.
- Layout: a sinistra il **telefono** (app), a destra la **strada**, simulata. Quando l'app dice "Vai", nella strada si accende il lampeggiante e il semaforo allunga il verde. Non serve altro scope.
- **Modalità simulata obbligatoria** (pulsante di riserva): in sala non c'è una strada, e la fotocamera o il modello possono bloccarsi.
- Fotocamera vera (facoltativa, solo se avanza tempo): TensorFlow.js + COCO-SSD da CDN. Sul telefono la fotocamera funziona solo con HTTPS: usare GitHub Pages oppure `localhost`, perché aprire il file con doppio click non basta.
- `demo/NOTE-TECNICHE.md`: stack, architettura, flusso dati, come si va in produzione in 90', quali dati personali tratta. Serve alla Persona B per la relazione.

### Persona B – Commerciale → possiede `docs/`

- `docs/relazione-tecnica.md`: struttura già pronta, segue la griglia di Art. 5.
- `docs/offerta-economica.md`: ripartizione dei 10M, costi infrastrutturali, requisiti di Art. 4.
- `docs/pitch.md`: scaletta e testo delle slide.

## Tono

Forma seria da gara pubblica, ma il bando è satirico e la commissione se lo aspetta. Gag disponibili:

- Art. 1 indica come responsabile il Dott. Goffredo Scannapuoti, ma firma Isidoro Miciomanno con un'**impronta di zampa**.
- Art. 4: 5.000.000 di like medi annui su LinkedIn; app "usata da nessuno ma scaricata da molti". Rispondere con faccia seria.
- Art. 7: si applica il **regolamento del Fantamorto 2025-2026** (conflitto di interessi?).
- Oggetto: "arrivare **vive** dall'altra parte".

Lingua di tutti i deliverable: **italiano**.

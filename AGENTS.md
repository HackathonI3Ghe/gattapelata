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

### Persona A – Tecnica → possiede `demo/` e `.github/workflows/`

- **Web app React + Vite in `demo/`, deployabile su GitHub Pages.** Sorgenti separati e build statica, senza backend per la demo. Questa scelta sostituisce il precedente requisito del singolo file HTML apribile con doppio click.
- Mobile-first, testo ≥ 24px, pulsanti enormi, alto contrasto, sintesi vocale in italiano (`speechSynthesis`, `lang="it-IT"`).
- Un'azione principale. Il flusso della demo deve durare meno di 60 secondi.
- Layout: a sinistra il **telefono** (app), a destra la **strada**, simulata. Quando l'app dice "Vai", nella strada si accende il lampeggiante e il semaforo allunga il verde. Non serve altro scope.
- **Modalità simulata obbligatoria** (pulsante di riserva): in sala non c'è una strada, e la fotocamera o il modello possono bloccarsi.
- Fotocamera del telefono: aprirla dopo il tap con `getUserMedia`, preferendo quella posteriore; mostrare la ripresa in un elemento video con `muted` e `playsInline`. La prova prevede di inquadrare un video della strada riprodotto su uno schermo esterno. Gestire permesso negato ed errori, e fermare le tracce alla chiusura. Il riconoscimento reale (es. TensorFlow.js + COCO-SSD) è una componente distinta, facoltativa se il tempo lo permette; indicare chiaramente quando i risultati sono simulati.
- Sul cellulare provare la fotocamera dal sito HTTPS pubblicato. `localhost` vale sul dispositivo che esegue il server; l'indirizzo HTTP del computer nella rete locale non è un'alternativa equivalente per la fotocamera del telefono.
- `demo/NOTE-TECNICHE.md`: stack, architettura, flusso dati, come si va in produzione in 90', quali dati personali tratta. Serve alla Persona B per la relazione.

### Requisiti di build e deploy per gli agenti tecnici

- Leggere [demo/NOTE-DEPLOY.md](demo/NOTE-DEPLOY.md) prima di creare o modificare lo stack e il deploy. Conservare i file `NOTE-*.md` durante lo scaffolding.
- Tenere `package.json`, `package-lock.json`, configurazione Vite e sorgenti applicativi in `demo/`; escludere `node_modules/` e `dist/` da Git. Prevedere gli script `dev`, `build` e `preview`.
- Impostare `base: '/gattapelata/'` in Vite. Asset e collegamenti devono funzionare sotto questo percorso; evitare percorsi assoluti alla radice del dominio. Per il flusso demo preferire lo stato React nella stessa pagina.
- Creare `.github/workflows/deploy-pages.yml`: al push su `main` che modifica l'app o il workflow, eseguire `npm ci` e `npm run build` in `demo/`, quindi pubblicare **solo `demo/dist`** con le Actions ufficiali di GitHub Pages. Prevedere anche `workflow_dispatch`. Usare il token automatico GitHub con i permessi necessari, senza token personali nel repository.
- Destinazione: **https://hackathoni3ghe.github.io/gattapelata/**. L'amministratore abilita Pages con Source `GitHub Actions`; con GitHub Free il repository deve essere pubblico. Gli agenti non cambiano visibilità o impostazioni dell'organizzazione senza richiesta esplicita.
- Prima di consegnare modifiche applicative, verificare installazione riproducibile con `npm ci`, build con `npm run build` e anteprima con `npm run preview`. Dopo il deploy verificare apertura e asset sul sito pubblicato, quindi pulsante principale, voce, simulazione e fotocamera sui telefoni disponibili. Riportare esplicitamente eventuali verifiche non eseguite.
- La consegna tecnica richiede una build pubblicabile e una demo utilizzabile da browser mobile. Non dichiarare il sito operativo solo perché Pages è abilitato: serve un deploy riuscito. PWA installabile e offline sono funzionalità ulteriori, da dichiarare solo se implementate e provate.

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

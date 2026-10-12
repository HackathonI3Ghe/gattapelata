# Web app React e pubblicazione su GitHub Pages

Scelta proposta per il team, aggiornata il 12 ottobre 2026: **React + Vite, CSS semplice e GitHub Pages con deploy tramite GitHub Actions**. L'app vive in `demo/`, si apre dal browser del cellulare tramite link HTTPS e non richiede uno store. La preferenza per React espressa nella conversazione aggiorna la precedente indicazione del brief «un solo file, niente build»: con Vite ci sono sorgenti separati e una build automatica.

## Stack e perimetro

- React per interfaccia, stato e sequenza della demo; JavaScript per partire velocemente, oppure TypeScript se il team lo usa già.
- Vite per sviluppo locale e build; CSS mobile-first, un pulsante principale e voce italiana.
- Simulazione obbligatoria, con dati finti e flusso sotto i 60 secondi. Per la prova richiesta, prevedere anche la fotocamera del telefono che inquadra un video della strada riprodotto su uno schermo esterno.
- Nessun backend per questa demo. SMS reali, raccolta centralizzata delle misure e integrazioni hardware richiedono servizi successivi. Il Livello 2 resta simulato e non va dichiarato operativo a T+90 minuti.
- PWA installabile e offline come aggiunta successiva: React da solo non offre queste caratteristiche. Per la prima prova basta il link nel browser.

## Account gratuito e indirizzo

GitHub Pages è disponibile con GitHub Free anche per organizzazioni, **su repository pubblici**. Anche Actions è gratuito per repository pubblici. Se quello attuale è privato, occorre un repository pubblico dedicato alla demo o un piano compatibile; non cambiarne automaticamente la visibilità. [Condizioni GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

Con l'origin attuale `HackathonI3Ghe/gattapelata`, l'indirizzo atteso, dopo l'attivazione, è:

`https://hackathoni3ghe.github.io/gattapelata/`

È un indirizzo previsto, non un sito già pubblicato. Per la presentazione condividere il link o un QR code.

## Avvio del progetto

Quando Persona A avvia l'app, dalla radice del repository:

```sh
npm create vite@latest demo -- --template react
cd demo
npm install
npm run dev
```

Se `demo/` contiene già file di coordinamento come questa nota, conservare quei file durante lo scaffolding: non scegliere opzioni che cancellano la cartella. In alternativa generare il template in una cartella temporanea e trasferire solo i file applicativi.

Usare Node 22.12 o superiore compatibile; committare `demo/package-lock.json`, necessario per `npm ci` in CI. [Avvio Vite](https://vite.dev/guide/).

In `demo/vite.config.js`:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/gattapelata/',
})
```

Il percorso `base` serve perché il sito è ospitato sotto il nome del repository. Per il flusso demo usare lo stato React nella stessa pagina, evitando routing aggiuntivo. [Deploy Vite](https://vite.dev/guide/static-deploy.html).

## Pubblicazione automatica

Un amministratore del repository imposta **Settings → Pages → Build and deployment → Source → GitHub Actions**. Il responsabile del deploy aggiunge `.github/workflows/deploy-pages.yml` nella radice del repository con questo contenuto, adattato al progetto in `demo/`:

```yaml
name: Pubblica demo

on:
  push:
    branches: [main]
    paths:
      - 'demo/**'
      - '.github/workflows/deploy-pages.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm
          cache-dependency-path: demo/package-lock.json
      - run: npm ci
        working-directory: demo
      - run: npm run build
        working-directory: demo
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v4
        with:
          path: demo/dist
      - name: Pubblica
        id: deployment
        uses: actions/deploy-pages@v4
```

Il workflow pubblica solo la build `demo/dist`, non i documenti del progetto, e usa il token automatico di GitHub: non serve un token personale. [Workflow Pages e permessi](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Dopo il push su `main`, controllare l'esito in **Actions** e l'URL in **Settings → Pages**. GitHub indica che la pubblicazione può richiedere fino a 10 minuti: partire prima della prova generale delle 19:45. [Tempi di pubblicazione](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Fotocamera dal telefono e video della strada

React + Vite resta adatto anche all'acquisizione in tempo reale. React gestisce l'interfaccia; il browser apre la fotocamera tramite `navigator.mediaDevices.getUserMedia`. Non serve un'app nativa né un backend per mostrare la ripresa. Servono HTTPS e il permesso dell'utente. [API della fotocamera](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).

Flusso della prova: **video della strada sul computer → fotocamera posteriore del telefono → anteprima nella web app → eventuale analisi locale**. Il video sul computer e la ripresa sul telefono sono due sorgenti distinte.

Nel gestore del pulsante di avvio, richiedere preferibilmente la fotocamera posteriore:

```js
const stream = await navigator.mediaDevices.getUserMedia({
  audio: false,
  video: {
    facingMode: { ideal: 'environment' },
    width: { ideal: 640 },
    height: { ideal: 480 },
  },
})
videoRef.current.srcObject = stream
await videoRef.current.play()
```

Usare un riferimento React al tag `<video ref={videoRef} autoPlay muted playsInline />`. `playsInline` permette la riproduzione dentro la pagina sui browser che lo supportano. Gestire errori e fermare le tracce con `stream.getTracks().forEach(track => track.stop())` quando si termina la ripresa o si smonta il componente. [Elemento video](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video).

**Mostrare la fotocamera e riconoscere i veicoli sono due attività diverse.** Per riconoscimento e stima del tempo di arrivo occorre anche un modello di visione eseguito nel browser e un algoritmo che segue i veicoli tra fotogrammi. Per mantenere fluida l'interfaccia, elaborare fotogrammi campionati senza copiarli continuamente nello stato React; aggiornare lo stato solo con i risultati utili all'utente.

Inquadrare un monitor può introdurre riflessi, sfarfallio e distorsioni: provare prima la coppia telefono/schermo effettivamente usata. Come riserva, prevedere lo stesso video caricato direttamente nella web app e una modalità con risultati simulati, distinguendole chiaramente dalla ripresa e dal riconoscimento reale. Nessuna di queste prove dimostra da sola l'affidabilità in strada.

## Prova da cellulare e consegna

1. Verificare `npm run build` e `npm run preview` sul computer.
2. Aprire il link HTTPS da Safari su iPhone e Chrome su Android, almeno sui dispositivi disponibili al team.
3. Verificare pulsante, leggibilità, voce italiana avviata dal gesto dell'utente e flusso simulato completo.
4. Se presente la fotocamera, chiedere il permesso dopo il tap; in caso di rifiuto o errore rendere subito disponibile la simulazione.
5. Provare anche con rete mobile, conservando la demo simulata locale sul computer come riserva per la sala.

La fotocamera richiede un contesto sicuro e il consenso del browser. `localhost` sul computer è adatto allo sviluppo; `http://192.168.x.x` aperto dal telefono non equivale a localhost. Per la prova della fotocamera sul cellulare usare il link HTTPS pubblicato. [Requisiti getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).

Il traguardo di questa fase è una demo raggiungibile dal telefono. Il deploy statico risolve la distribuzione, mentre affidabilità delle stime e uso reale in strada richiedono validazione separata.

## Stato della configurazione

È presente un workflow effettivo in `.github/workflows/deploy-pages.yml`, attivato dai push su `main` che modificano `demo/` o il workflow e avviabile anche manualmente. Per la prima prova pubblica la demo HTML dei colleghi copiando soltanto `demo/index.html`. Quando sarà presente `demo/package.json`, eseguirà invece `npm ci` e `npm run build`, pubblicando solo `demo/dist`: occorrono il lockfile e la configurazione Vite descritta sopra. Se la build fallisce, il deploy si interrompe.

L'app React resta da realizzare; il primo deploy usa la demo esistente senza modificarla. L'utente riferisce di aver abilitato Pages; l'esito della pubblicazione va controllato in Actions e aprendo il sito. Persona A possiede `demo/` e `.github/workflows/`. Persona B può usare questa nota per descrivere distribuzione e fattibilità nei documenti di gara.

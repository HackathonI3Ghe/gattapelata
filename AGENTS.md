# Hackathon Gattapelata – brief condiviso per agenti (Claude / Codex)

Fonte di verità: [bando-gara-gattapelata.md](bando-gara-gattapelata.md). Leggilo prima di tutto.

## Scadenze (12/10/2026)

- **19:30** freeze: niente nuove funzioni, solo fix e rifinitura.
- **19:45** consegna interna: demo + documenti pronti, prova generale.
- **20:00** presentazione (Art. 6: la demo va *dimostrata* entro le 20:00).

## Concetto scelto

> **DA DECIDERE.** Quando il team sceglie, scrivere qui un paragrafo (cosa fa l'anziano, cosa succede dopo, chi altro è coinvolto). Tutti gli agenti si allineano a questo paragrafo.

## Vincoli del bando che guidano ogni scelta

- **In funzione entro 90 minuti dalla firma** (Art. 3): niente app nativa da store (la review non passa in 90'). Usare PWA/web, SMS, telefonata, dispositivi già esistenti.
- **Anziani con poca dimestichezza tecnologica** (Art. 2): interazione minima. Un pulsante, voce, telefono fisso come alternativa.
- **Vicoli "così come attualmente sono"** (Art. 2): nessuna opera stradale. Il GPS nei vicoli stretti è impreciso (urban canyon), quindi bisogna prevedere un'alternativa.
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

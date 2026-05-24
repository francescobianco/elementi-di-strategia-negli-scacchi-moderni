# Elementi di strategia negli scacchi moderni

Repository editoriale per preparare una nuova edizione di **Elementi di
strategia negli scacchi moderni** di **Mario Leoncini**.

Il progetto conserva le sorgenti LaTeX ricavate dall'edizione precedente,
le immagini dei diagrammi, il PDF storico e una nuova appendice in formato
DOCX. La build deve produrre il nuovo PDF finale dentro `dist/`.

## Mario Leoncini

Mario Leoncini, nato a San Gimignano nel 1956, e' un maestro di scacchi,
autore e storico degli scacchi italiano. Le Due Torri lo presenta come
maestro della Federazione Scacchistica Italiana, gia' vicepresidente FSI,
scrittore e uno dei maggiori storici italiani degli scacchi; nel 2016 ha
ricevuto la Stella CONI al merito sportivo.

Nel campo storico e divulgativo ha pubblicato, tra gli altri, `La grande
storia degli scacchi`, volume del 2020 dedicato alla storia del gioco dal
VI secolo all'eta' contemporanea. La Federazione Scacchistica Italiana
pubblica inoltre suoi contributi storici in `Scacchitalia` e accredita a
Leoncini una cronologia sulla preistoria e la storia della Federazione.

Riferimenti pubblici:

- https://www.scacco.it/it/prod/la-grande-storia-degli-scacchi
- https://www.federscacchi.com/fsi/index.php/fsi/chi-siamo
- https://www.federscacchi.com/fsi/index.php/cultura/scacchitalia
- https://it.wikipedia.org/wiki/Mario_Leoncini

## Contenuti del repository

- `src/main.tex`: sorgente LaTeX principale della nuova edizione.
- `src/frontmatter/`: titolo, introduzione e materiali preliminari.
- `src/chapters/`: capitoli numerati, separati in file modificabili.
- `src/appendices/`: appendici convertite in LaTeX omogeneo.
- `src/assets/diagrams/`: diagrammi del testo storico.
- `src/diagrams/`: registro FEN e macro di rendering dinamico dei diagrammi.
- `src/assets/appendix/media/`: diagrammi della nuova appendice.
- `old_src/`: archivio dei sorgenti precedenti, del PDF storico, del DOCX originale e degli artefatti importati.
- `dist/`: destinazione del PDF generato dalla build.
- `build/`: directory temporanea generata da `make`, esclusa da git.

## Struttura del libro

La sorgente contiene l'introduzione e dieci capitoli:

1. Sviluppo dei pezzi e perdita di tempi
2. Un metodo per avvantaggiarsi in apertura: il gambetto
3. La struttura dei pedoni
4. Gli avamposti
5. Attacco e contrattacco
6. Le colonne aperte
7. Gli alfieri
8. Il sacrificio posizionale
9. Pezzi fuori gioco
10. Altri aspetti della battaglia scacchistica

La nuova struttura include gia' l'`Appendice al capitolo III` in `src/appendices/appendice-capitolo-iii.tex`. La nuova appendice 2015 e' stata convertita stabilmente in `src/appendices/appendice-2015.tex`, cosi' le modifiche massive possono avvenire direttamente sui sorgenti LaTeX.

## Nuova appendice

`src/appendices/appendice-2015.tex` contiene una nota di aggiornamento e due partite del
Campionato Italiano a squadre 2015. Il DOCX originale resta archiviato in `old_src/Appendice.docx`:

- Gazzarri-Leoncini, Cecina 2015, Difesa Siciliana.
- Borselli-Leoncini, Firenze 2015, Tartakower.

L'appendice sviluppa temi gia' presenti nel libro: pedone debole, attacco
su entrambi i lati della scacchiera, sviluppo naturale dei pezzi e
valutazione di vantaggi strutturali.

## Requisiti

- `make`
- un motore LaTeX compatibile con il sorgente, per esempio `pdflatex`

Il Makefile usa `pdflatex` per impostazione predefinita. Si puo' scegliere
un altro motore passando `LATEX`:

```sh
make LATEX=xelatex
```

## Build

Per generare la nuova edizione con un motore LaTeX locale:

```sh
make
```

Oppure tramite l'ambiente Docker riutilizzabile:

```sh
make docker-build
```

La prima esecuzione costruisce l'immagine `elementi-strategia-scacchi-latex:latest` da `docker/latex/Dockerfile`; le build successive la riutilizzano.

Output atteso:

```text
dist/elementi-di-strategia-negli-scacchi-moderni-nuova-edizione.pdf
```

I sorgenti usano gia' la notazione figurata delle mosse (`¤`, `¥`, `£`, `¦`, `¢`), senza post-processing durante la build.

## Diagrammi FEN

Il lavoro di estrazione dei diagrammi e' documentato in `docs/diagram-fen-extraction.md`.

Comandi utili:

```sh
make diagram-inventory
make diagram-draft-fens
make diagram-normalize
```

Il registro versionabile e' `src/diagrams/diagrams.csv`. Lo snapshot provvisorio dell'estrazione template e' `src/diagrams/draft-fens.tsv`. I FEN verificati sono renderizzabili con le macro in `src/diagrams/rendering.tex`; i PNG legacy restano disponibili durante la revisione. `make diagram-normalize` riscrive i vecchi `includegraphics` dei diagrammi nella macro centrata standard.


La build:

1. genera un `.tex` temporaneo in `build/` con i path corretti per la compilazione;
2. compila due volte il PDF;
3. scrive il risultato finale in `dist/`.

## Pulizia

```sh
make clean
```

Rimuove gli artefatti temporanei e i file ausiliari LaTeX.

```sh
make distclean
```

Rimuove anche il PDF generato in `dist/`.

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

- `src/elementi-di-strategia-negli-scacchi-moderni.tex`: sorgente LaTeX
  principale del libro.
- `src/vertopal_109f12be458a423d8f3cc838880eaea2/media/`: immagini dei
  diagrammi usate dalla sorgente LaTeX.
- `src/elementi-di-strategia-negli-scacchi-moderni.pdf`: PDF storico di
  riferimento.
- `src/Appendice.docx`: nuova appendice da aggiungere alla nuova edizione.
- `src/*.aux` e `src/*.log`: artefatti della precedente compilazione,
  utili solo come riferimento diagnostico.
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

La sorgente include gia' una `Appendice al capitolo III`. La nuova
appendice in `src/Appendice.docx` viene convertita da `pandoc` e aggiunta
in coda al volume durante la build, senza modificare il `.tex` originale.

## Nuova appendice

`src/Appendice.docx` contiene una nota di aggiornamento e due partite del
Campionato Italiano a squadre 2015:

- Gazzarri-Leoncini, Cecina 2015, Difesa Siciliana.
- Borselli-Leoncini, Firenze 2015, Tartakower.

L'appendice sviluppa temi gia' presenti nel libro: pedone debole, attacco
su entrambi i lati della scacchiera, sviluppo naturale dei pezzi e
valutazione di vantaggi strutturali.

## Requisiti

- `make`
- `pandoc`
- un motore LaTeX compatibile con il sorgente, per esempio `pdflatex`

Il Makefile usa `pdflatex` per impostazione predefinita. Si puo' scegliere
un altro motore passando `LATEX`:

```sh
make LATEX=xelatex
```

## Build

Per generare la nuova edizione:

```sh
make
```

Output atteso:

```text
dist/elementi-di-strategia-negli-scacchi-moderni-nuova-edizione.pdf
```

La build:

1. converte `src/Appendice.docx` in LaTeX;
2. estrae le immagini dell'appendice in `build/appendice/media/`;
3. genera un `.tex` combinato in `build/`;
4. compila due volte il PDF;
5. scrive il risultato finale in `dist/`.

## Pulizia

```sh
make clean
```

Rimuove gli artefatti temporanei e i file ausiliari LaTeX.

```sh
make distclean
```

Rimuove anche il PDF generato in `dist/`.

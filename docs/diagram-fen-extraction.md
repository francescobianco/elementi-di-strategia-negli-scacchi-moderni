# Estrazione FEN dei diagrammi

Obiettivo: sostituire i PNG statici dei diagrammi con posizioni FEN renderizzate dinamicamente da LaTeX tramite `chessboard`.

## Stato

- I diagrammi originali sono in `src/assets/diagrams/image1.png` ... `image116.png`.
- I PNG sono quasi tutti 384x384 o 320x320, a 2 colori: la griglia e' quindi regolare, con celle da 48 o 40 px.
- Il registro versionabile e' `src/diagrams/diagrams.csv`.
- Lo snapshot provvisorio rigenerabile e' `src/diagrams/draft-fens.tsv`.
- I FEN gia' verificati sono marcati `verified-from-moves`.
- I diagrammi non ancora verificati restano `todo-image-extraction`.

## Metodo usato

1. Inventario immagini con ImageMagick:
   `identify -format '%f %wx%h %[colors]\n' src/assets/diagrams/*.png`
2. Lettura delle mosse vicine al diagramma nei sorgenti.
3. Conversione manuale in FEN quando la sequenza e' completa e non ambigua.
4. Clustering dei quadrati dei PNG per costruire template riutilizzabili dei pezzi.
5. Decodifica provvisoria dei diagrammi rimanenti con `scripts/extract_diagram_fens.py`, salvata in `src/diagrams/draft-fens.tsv`.

## Perche' non fare OCR generico

I diagrammi sono monocromatici, regolari e generati dallo stesso stile. Un riconoscitore a template e' piu' controllabile di un OCR generico: se un quadrato non e' riconosciuto lo script lascia `?`, invece di produrre un FEN apparentemente valido ma sbagliato.

## Rendering dinamico

Il file `src/diagrams/rendering.tex` definisce:

- `\bookdiagramfen{<fen>}{<numero>}` per i diagrammi validati.
- `\bookdiagramplaceholder{<png>}{<numero>}` per mantenere temporaneamente un PNG durante la revisione.

Quando un FEN viene validato, il relativo `\includegraphics` puo' essere sostituito con `\bookdiagramfen`.

# Docker build images

This directory contains reusable build images for the chess book workflow.

## `latex/`

LaTeX/Pandoc environment used to build the PDF without installing TeX Live on the host.
It also includes `stockfish` as a first chess-specific tool for future validation or analysis workflows.

Build the image:

```sh
make docker-image
```

Build the book through Docker:

```sh
make docker-build
```

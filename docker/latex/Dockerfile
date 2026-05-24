FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        lmodern \
        make \
        pandoc \
        perl \
        poppler-utils \
        stockfish \
        texlive-fonts-recommended \
        texlive-games \
        texlive-latex-base \
        texlive-latex-extra \
        texlive-latex-recommended \
        texlive-pictures \
        texlive-plain-generic \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

CMD ["make"]

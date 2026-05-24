SHELL := /bin/sh

SRC_DIR := src
BUILD_DIR := build
DIST_DIR := dist
DOCKER_IMAGE ?= elementi-strategia-scacchi-latex:latest

BOOK := elementi-di-strategia-negli-scacchi-moderni
MAIN_TEX := $(SRC_DIR)/main.tex
BUILD_TEX := $(BUILD_DIR)/$(BOOK)-nuova-edizione.tex
PDF := $(DIST_DIR)/$(BOOK)-nuova-edizione.pdf

LATEX ?= pdflatex

.PHONY: all build docker-image docker-build clean distclean

all: build

build: $(PDF)


docker-image:
	@docker build -f docker/latex/Dockerfile -t $(DOCKER_IMAGE) .

docker-build: docker-image
	@docker run --rm --user $$(id -u):$$(id -g) -e HOME=/tmp -v $(CURDIR):/work -w /work $(DOCKER_IMAGE) make build

$(PDF): $(BUILD_TEX) $(shell find $(SRC_DIR) -type f)
	@mkdir -p $(DIST_DIR)
	@cd $(BUILD_DIR) && $(LATEX) -interaction=nonstopmode -halt-on-error -output-directory=../$(DIST_DIR) $(notdir $(BUILD_TEX))
	@cd $(BUILD_DIR) && $(LATEX) -interaction=nonstopmode -halt-on-error -output-directory=../$(DIST_DIR) $(notdir $(BUILD_TEX))

$(BUILD_TEX): $(MAIN_TEX)
	@mkdir -p $(BUILD_DIR)
	@sed 's#{assets/#{../$(SRC_DIR)/assets/#g; s#{frontmatter/#{../$(SRC_DIR)/frontmatter/#g; s#{chapters/#{../$(SRC_DIR)/chapters/#g; s#{appendices/#{../$(SRC_DIR)/appendices/#g' $(MAIN_TEX) > $(BUILD_TEX)

clean:
	@rm -rf $(BUILD_DIR)
	@rm -f $(DIST_DIR)/*.aux $(DIST_DIR)/*.log $(DIST_DIR)/*.out $(DIST_DIR)/*.toc

distclean: clean
	@rm -f $(PDF)

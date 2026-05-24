SHELL := /bin/sh

SRC_DIR := src
BUILD_DIR := build
DIST_DIR := dist

BOOK := elementi-di-strategia-negli-scacchi-moderni
MAIN_TEX := $(SRC_DIR)/$(BOOK).tex
APPENDIX_DOCX := $(SRC_DIR)/Appendice.docx
APPENDIX_DIR := $(BUILD_DIR)/appendice
APPENDIX_TEX := $(APPENDIX_DIR)/appendice.tex
COMBINED_TEX := $(BUILD_DIR)/$(BOOK)-nuova-edizione.tex
PDF := $(DIST_DIR)/$(BOOK)-nuova-edizione.pdf

LATEX ?= pdflatex

.PHONY: all build clean distclean

all: build

build: $(PDF)

$(PDF): $(COMBINED_TEX) $(APPENDIX_TEX)
	@mkdir -p $(DIST_DIR)
	@cd $(BUILD_DIR) && $(LATEX) -interaction=nonstopmode -halt-on-error -output-directory=../$(DIST_DIR) $(notdir $(COMBINED_TEX))
	@cd $(BUILD_DIR) && $(LATEX) -interaction=nonstopmode -halt-on-error -output-directory=../$(DIST_DIR) $(notdir $(COMBINED_TEX))

$(COMBINED_TEX): $(MAIN_TEX) $(APPENDIX_TEX)
	@mkdir -p $(BUILD_DIR)
	@awk 'BEGIN { inserted=0 } /\\end\{document\}/ && !inserted { print "\\clearpage"; print "\\input{appendice/appendice.tex}"; inserted=1 } { print }' $(MAIN_TEX) \
		| sed 's#{vertopal_#{../$(SRC_DIR)/vertopal_#g' > $(COMBINED_TEX)

$(APPENDIX_TEX): $(APPENDIX_DOCX)
	@mkdir -p $(APPENDIX_DIR)
	@pandoc $(APPENDIX_DOCX) -t latex --extract-media=$(APPENDIX_DIR) -o $(APPENDIX_TEX)
	@perl -0pi -e 's#\{(?:$(BUILD_DIR)/)?appendice/media/#\{appendice/media/#g; s#\{media/#\{appendice/media/#g' $(APPENDIX_TEX)

clean:
	@rm -rf $(BUILD_DIR)
	@rm -f $(DIST_DIR)/*.aux $(DIST_DIR)/*.log $(DIST_DIR)/*.out $(DIST_DIR)/*.toc

distclean: clean
	@rm -f $(PDF)

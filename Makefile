#####################################
# Makefile for Sphinx documentation #
#####################################


# General options
# ---------------

# Git repository
GIT_VERSION = $(shell ../lpod-python/release.py)

# Python path
PYTHON = $(shell cat ../lpod-python/python_path.txt)

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = $(PYTHON) sphinx-link.py
PAPER         =

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d .build/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: help clean html latex pdf pdf-figures png-figures changes linkcheck \
		release lpod-check

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  pdf       to make PDF files, you can set PAPER=a4 or PAPER=letter"
	@echo "  changes   to make an overview over all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"
	@echo "  release   to make html/pdf and store the files in two tar.gz"

clean:
	-rm -rf .build
	-rm -rf lpod-docs-*.tgz
	-rm -rf figures
	-rm -rf autodocs

lpod-check:
	@if [ x$(PYTHON) == "x" ]; then \
		echo "Please, you must first install lpod"; \
		exit 1; \
	fi

html: lpod-check png-figures
	mkdir -p .build/html .build/doctrees
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) .build/html
	@echo
	@echo "Build finished. The HTML pages are in .build/html."

latex: lpod-check pdf-figures
	mkdir -p .build/latex .build/doctrees
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) .build/latex
	@echo
	@echo "Build finished; the LaTeX files are in .build/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

pdf: latex
	cd .build/latex && make all-pdf && cp lpod.pdf ../../lpod-$(GIT_VERSION).pdf
	rm -f lpod.pdf
	ln -s lpod-$(GIT_VERSION).pdf lpod.pdf
	@echo
	@echo "Your PDF is available in lpod.pdf"

changes:
	mkdir -p .build/changes .build/doctrees
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) .build/changes
	@echo
	@echo "The overview file is in .build/changes."

linkcheck:
	mkdir -p .build/linkcheck .build/doctrees
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) .build/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in .build/linkcheck/output.txt."

release: pdf html
	cd .build; \
	mv html lpod-docs-html-$(GIT_VERSION); \
	tar czf ../lpod-docs-html-$(GIT_VERSION).tgz lpod-docs-html-$(GIT_VERSION); \
	mv lpod-docs-html-$(GIT_VERSION) html
	@echo
	@echo "doc is available ./lpod-docs-html-$(GIT_VERSION).tgz"


# Figures conversion
# ------------------

SRC_NAMES=$(wildcard figures-src/*)
SRC_BASE_NAMES=$(basename $(SRC_NAMES))
TARGET_BASE_NAMES=$(patsubst  figures-src/%, figures/%, $(SRC_BASE_NAMES))

PDF_NAMES=$(addsuffix .pdf, $(TARGET_BASE_NAMES))
PNG_NAMES=$(addsuffix .png, $(TARGET_BASE_NAMES))

pdf-figures: figures $(PDF_NAMES)

png-figures: figures $(PNG_NAMES)

figures:
	mkdir -p figures

# To PDF rules

figures/%.eps: figures-src/%.png
	convert $< -compress jpeg eps2:$@

figures/%.eps: figures-src/%.jpg
	convert -units PixelsPerInch -density 72 $< eps2:$@

figures/%.eps: figures-src/%.svg
	inkscape -z $< -E $@

figures/%.eps: figures-src/%.fig
	fig2dev -L eps $< $@

figures/%.eps: figures-src/%.dot
	dot -Tps $< -o $@

figures/%.eps: figures-src/%.dia
	dia $< -e $@

%.pdf: %.eps
	epstopdf $<

# To PNG rules

figures/%.png: figures-src/%.png
	cp $< $@

figures/%.png: figures-src/%.jpg
	convert  $< $@

figures/%.png: figures-src/%.svg
	inkscape -z $< -e $@

figures/%.png: figures-src/%.dot
	dot -Tpng $< -o $@

figures/%.png: figures-src/%.dia
	dia $< -e $@ -t cairo-png



-include .env.local
export

ENV_FILE ?= .env.local
DOCS_DIR := docs/proposal-phase
ASSETS_DIR := $(DOCS_DIR)/assets
PROPOSAL_DIR := $(DOCS_DIR)/proposal
PRESENTATION_DIR := $(DOCS_DIR)/presentation

PROPOSAL_TEMPLATE := $(PROPOSAL_DIR)/main.tex.template
PROPOSAL_TEX := $(PROPOSAL_DIR)/main.tex
PROPOSAL_PDF := $(PROPOSAL_DIR)/main.pdf

SLIDES_TEMPLATE := $(PRESENTATION_DIR)/presentation.tex.template
SLIDES_TEX := $(PRESENTATION_DIR)/presentation.tex
SLIDES_PDF := $(PRESENTATION_DIR)/presentation.pdf

NOTES_TEMPLATE := $(PRESENTATION_DIR)/presentation_notes.tex.template
NOTES_TEX := $(PRESENTATION_DIR)/presentation_notes.tex
NOTES_PDF := $(PRESENTATION_DIR)/presentation_notes.pdf

QNA_TEMPLATE := $(PRESENTATION_DIR)/qna.tex.template
QNA_TEX := $(PRESENTATION_DIR)/qna.tex
QNA_PDF := $(PRESENTATION_DIR)/qna.pdf

GENERATED_TEX := $(PROPOSAL_TEX) $(SLIDES_TEX) $(NOTES_TEX) $(QNA_TEX)
PDF_OUTPUTS := $(PROPOSAL_PDF) $(SLIDES_PDF) $(NOTES_PDF) $(QNA_PDF)

ifdef FORCE
  LATEXMK_FORCE := -g
else
  LATEXMK_FORCE :=
endif

LATEXMK := TEXINPUTS=.:../assets: latexmk -pdf -cd -auxdir=build -outdir=. $(LATEXMK_FORCE)

.PHONY: all help proposal-phase docs proposal slides notes qna diff diff-clean compile present clean clean-docs

all: proposal-phase

help:
	@printf "%s\n" \
		"Targets dokumentasi fase proposal:" \
		"  make proposal        Build naskah proposal PDF" \
		"  make slides          Build slide presentasi PDF" \
		"  make notes           Build naskah presentasi PDF" \
		"  make qna             Build dokumen antisipasi tanya jawab PDF" \
		"  make proposal-phase  Build semua artefak proposal" \
		"  make diff            Generate diff PDF antara proposal/v1 dan proposal/v2" \
		"  make diff-clean      Hapus artefak diff" \
		"  make clean           Hapus file build artefak proposal" \
		"" \
		"Alias lama masih ada:" \
		"  make compile         Sama dengan make proposal" \
		"  make present         Sama dengan make slides"

proposal-phase: proposal slides notes qna

docs: proposal-phase

proposal: $(PROPOSAL_TEX)
	$(LATEXMK) $<

slides: $(SLIDES_TEX)
	$(LATEXMK) $<

notes: $(NOTES_TEX) $(SLIDES_PDF)
	$(LATEXMK) $<

qna: $(QNA_TEX)
	$(LATEXMK) $<

compile: proposal

present: slides

$(PROPOSAL_TEX): $(PROPOSAL_TEMPLATE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata proposal perlu diisi."; \
	fi
	envsubst < $< > $@

$(SLIDES_TEX): $(SLIDES_TEMPLATE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata presentasi perlu diisi."; \
	fi
	envsubst < $< > $@

$(NOTES_TEX): $(NOTES_TEMPLATE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata naskah presentasi perlu diisi."; \
	fi
	envsubst < $< > $@

$(QNA_TEX): $(QNA_TEMPLATE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata QnA perlu diisi."; \
	fi
	envsubst < $< > $@

$(PROPOSAL_PDF): $(PROPOSAL_TEX) $(wildcard $(PROPOSAL_DIR)/chapters/*.tex) $(ASSETS_DIR)/isi-proposal.cls $(ASSETS_DIR)/references.bib .latexmkrc
	$(LATEXMK) $<

$(SLIDES_PDF): $(SLIDES_TEX) $(ASSETS_DIR)/logo-isi-white.png .latexmkrc
	$(LATEXMK) $<

$(NOTES_PDF): $(NOTES_TEX) $(SLIDES_PDF) .latexmkrc
	$(LATEXMK) $<

$(QNA_PDF): $(QNA_TEX) .latexmkrc
	$(LATEXMK) $<

clean: clean-docs

clean-docs:
	rm -rf $(PROPOSAL_DIR)/build $(PRESENTATION_DIR)/build
	rm -f $(GENERATED_TEX) $(PDF_OUTPUTS)
	rm -f $(PROPOSAL_DIR)/*.aux $(PROPOSAL_DIR)/*.log $(PROPOSAL_DIR)/*.fls $(PROPOSAL_DIR)/*.fdb_latexmk $(PROPOSAL_DIR)/*.bbl $(PROPOSAL_DIR)/*.bcf $(PROPOSAL_DIR)/*.blg $(PROPOSAL_DIR)/*.run.xml $(PROPOSAL_DIR)/*.out $(PROPOSAL_DIR)/*.toc $(PROPOSAL_DIR)/*.synctex.gz
	rm -f $(PRESENTATION_DIR)/*.aux $(PRESENTATION_DIR)/*.log $(PRESENTATION_DIR)/*.fls $(PRESENTATION_DIR)/*.fdb_latexmk $(PRESENTATION_DIR)/*.nav $(PRESENTATION_DIR)/*.snm $(PRESENTATION_DIR)/*.out $(PRESENTATION_DIR)/*.toc $(PRESENTATION_DIR)/*.synctex.gz

# Diff targets
DIFF_SCRIPT := scripts/sidebydiff.py
DIFF_OUTPUTS := scratch/proposal_diff.tex scratch/proposal_diff.pdf scratch/proposal_diff.aux scratch/proposal_diff.log

diff: $(DIFF_SCRIPT)
	@chmod +x $(DIFF_SCRIPT)
	@python3 $(DIFF_SCRIPT)

diff-clean:
	rm -f scratch/proposal_diff.tex scratch/proposal_diff.pdf scratch/proposal_diff.aux scratch/proposal_diff.log scratch/proposal_diff.html

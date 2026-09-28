-include .env.local
export

ENV_FILE ?= .env.local

# Directories
PROPOSAL_DOCS_DIR := docs/proposal-phase
PROPOSAL_ASSETS_DIR := $(PROPOSAL_DOCS_DIR)/assets
PROPOSAL_DIR := $(PROPOSAL_DOCS_DIR)/proposal
PROPOSAL_PRES_DIR := $(PROPOSAL_DOCS_DIR)/presentation

THESIS_DOCS_DIR := docs/final-thesis
THESIS_DIR := $(THESIS_DOCS_DIR)/thesis
THESIS_PRES_DIR := $(THESIS_DOCS_DIR)/presentation

# Proposal Targets & Files
PROPOSAL_TEMPLATE := $(PROPOSAL_DIR)/main.tex.template
PROPOSAL_TEX := $(PROPOSAL_DIR)/main.tex
PROPOSAL_PDF := $(PROPOSAL_DIR)/main.pdf

SLIDES_TEMPLATE := $(PROPOSAL_PRES_DIR)/presentation.tex.template
SLIDES_TEX := $(PROPOSAL_PRES_DIR)/presentation.tex
SLIDES_PDF := $(PROPOSAL_PRES_DIR)/presentation.pdf

NOTES_TEMPLATE := $(PROPOSAL_PRES_DIR)/presentation_notes.tex.template
NOTES_TEX := $(PROPOSAL_PRES_DIR)/presentation_notes.tex
NOTES_PDF := $(PROPOSAL_PRES_DIR)/presentation_notes.pdf

QNA_TEMPLATE := $(PROPOSAL_PRES_DIR)/qna.tex.template
QNA_TEX := $(PROPOSAL_PRES_DIR)/qna.tex
QNA_PDF := $(PROPOSAL_PRES_DIR)/qna.pdf

# Thesis Targets & Files
THESIS_TEMPLATE := $(THESIS_DIR)/main.tex.template
THESIS_TEX := $(THESIS_DIR)/main.tex
THESIS_PDF := $(THESIS_DIR)/main.pdf

ifdef FORCE
  LATEXMK_FORCE := -g
else
  LATEXMK_FORCE :=
endif

LATEXMK := TEXINPUTS=.:../assets:../../proposal-phase/assets: latexmk -pdf -interaction=nonstopmode -cd -auxdir=build -outdir=. $(LATEXMK_FORCE)

.PHONY: all help \
        setup setup-models test exp run-all eval plot \
        proposal-phase docs proposal slides notes qna compile present \
        thesis final-phase thesis-slides \
        diff diff-clean clean clean-docs

all: help

help:
	@printf "%s\n" \
		"==================================================================" \
		"  Strube Harmonic Evaluation Framework & LaTeX Document Suite" \
		"==================================================================" \
		"" \
		"🔬 PIPELINE RISET & EKSPERIMEN:" \
		"  make setup           Bootstrap dependensi model (DeepBach, NotaGen, Coconet)" \
		"  make test            Jalankan uji validitas instrumen (Face Validity)" \
		"  make exp             Jalankan full pipeline eksperimen (run_all.py)" \
		"  make eval            Jalankan evaluasi Strube batch pada file MIDI" \
		"  make plot            Generate visualisasi hasil grafik" \
		"" \
		"📄 DOKUMEN FASE PROPOSAL (docs/proposal-phase/):" \
		"  make proposal        Build naskah proposal PDF" \
		"  make slides          Build slide presentasi proposal PDF" \
		"  make notes           Build naskah presenter PDF" \
		"  make qna             Build dokumen antisipasi tanya jawab PDF" \
		"  make proposal-phase  Build semua artefak proposal" \
		"" \
		"🎓 DOKUMEN FASE SKRIPSI FINAL (docs/final-thesis/):" \
		"  make thesis          Build naskah skripsi final (5 Bab) PDF" \
		"  make final-phase     Build semua artefak skripsi final" \
		"" \
		"🔍 VERSIONING & DIFFING:" \
		"  make diff <ref1> <ref2>  Generate side-by-side diff PDF" \
		"                           Contoh: make diff proposal/v1 proposal/v2" \
		"                           Gunakan tag proposal; dukungan ref skripsi belum terverifikasi" \
		"  make diff-clean          Hapus file artefak diff" \
		"" \
		"🧹 CLEANUP:" \
		"  make clean           Hapus seluruh file build & cache LaTeX" \
		"=================================================================="

# ==============================================================================
# PIPELINE RISET
# ==============================================================================
setup: setup-models

setup-models:
	uv run python scripts/bootstrap_models.py

test:
	uv run python tests/test_strube_validity.py

exp: run-all

run-all:
	uv run python run_all.py

eval:
	uv run python experiments/scripts/run_evaluation.py

plot:
	uv run python experiments/scripts/plot_results.py

# ==============================================================================
# FASE PROPOSAL
# ==============================================================================
proposal-phase: proposal slides notes qna

docs: proposal-phase

proposal: $(PROPOSAL_TEX)
	@if [ -n "$(PROPOSAL_ARGS)" ]; then \
		chmod +x scripts/compile_version.py; \
		python3 scripts/compile_version.py $(PROPOSAL_ARGS); \
	else \
		$(LATEXMK) $<; \
	fi

slides: $(SLIDES_TEX)
	$(LATEXMK) $<

notes: $(NOTES_TEX) slides
	$(LATEXMK) $<

qna: $(QNA_TEX)
	$(LATEXMK) $<

compile: proposal
present: slides

$(PROPOSAL_TEX): $(PROPOSAL_TEMPLATE) $(ENV_FILE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata proposal perlu diisi."; \
	fi
	envsubst < $< > $@

$(SLIDES_TEX): $(SLIDES_TEMPLATE) $(ENV_FILE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata presentasi perlu diisi."; \
	fi
	envsubst < $< > $@

$(NOTES_TEX): $(NOTES_TEMPLATE) $(ENV_FILE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata naskah presentasi perlu diisi."; \
	fi
	envsubst < $< > $@

$(QNA_TEX): $(QNA_TEMPLATE) $(ENV_FILE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata QnA perlu diisi."; \
	fi
	envsubst < $< > $@

# ==============================================================================
# FASE SKRIPSI FINAL
# ==============================================================================
final-phase: thesis

thesis: $(THESIS_TEX)
	$(LATEXMK) $<

$(THESIS_TEX): $(THESIS_TEMPLATE) $(ENV_FILE)
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Warning: $(ENV_FILE) not found. Copy .env.example -> $(ENV_FILE) if metadata skripsi perlu diisi."; \
	fi
	envsubst < $< > $@

# ==============================================================================
# SIDE-BY-SIDE DIFF TARGETS
# ==============================================================================
DIFF_SCRIPT := scripts/sidebydiff.py

ifeq ($(firstword $(MAKECMDGOALS)),diff)
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

diff: $(DIFF_SCRIPT)
	@chmod +x $(DIFF_SCRIPT)
	@python3 $(DIFF_SCRIPT) $(RUN_ARGS)

diff-clean:
	rm -f scratch/proposal_diff.tex scratch/proposal_diff.pdf scratch/proposal_diff.aux scratch/proposal_diff.log scratch/proposal_diff.html

# Parse tag/ref for make proposal <ref>
ifeq ($(firstword $(MAKECMDGOALS)),proposal)
  PROPOSAL_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(PROPOSAL_ARGS):;@:)
endif

# ==============================================================================
# CLEANUP
# ==============================================================================
clean: clean-docs diff-clean

clean-docs:
	rm -rf $(PROPOSAL_DIR)/build $(PROPOSAL_PRES_DIR)/build $(THESIS_DIR)/build
	rm -f $(PROPOSAL_TEX) $(SLIDES_TEX) $(NOTES_TEX) $(QNA_TEX) $(THESIS_TEX)
	rm -f $(PROPOSAL_PDF) $(SLIDES_PDF) $(NOTES_PDF) $(QNA_PDF) $(THESIS_PDF)
	rm -f $(PROPOSAL_DIR)/*.aux $(PROPOSAL_DIR)/*.log $(PROPOSAL_DIR)/*.fls $(PROPOSAL_DIR)/*.fdb_latexmk $(PROPOSAL_DIR)/*.bbl $(PROPOSAL_DIR)/*.bcf $(PROPOSAL_DIR)/*.blg $(PROPOSAL_DIR)/*.run.xml $(PROPOSAL_DIR)/*.out $(PROPOSAL_DIR)/*.toc $(PROPOSAL_DIR)/*.synctex.gz
	rm -f $(PROPOSAL_PRES_DIR)/*.aux $(PROPOSAL_PRES_DIR)/*.log $(PROPOSAL_PRES_DIR)/*.fls $(PROPOSAL_PRES_DIR)/*.fdb_latexmk $(PROPOSAL_PRES_DIR)/*.nav $(PROPOSAL_PRES_DIR)/*.snm $(PROPOSAL_PRES_DIR)/*.out $(PROPOSAL_PRES_DIR)/*.toc $(PROPOSAL_PRES_DIR)/*.synctex.gz
	rm -f $(THESIS_DIR)/*.aux $(THESIS_DIR)/*.log $(THESIS_DIR)/*.fls $(THESIS_DIR)/*.fdb_latexmk $(THESIS_DIR)/*.bbl $(THESIS_DIR)/*.bcf $(THESIS_DIR)/*.blg $(THESIS_DIR)/*.run.xml $(THESIS_DIR)/*.out $(THESIS_DIR)/*.toc $(THESIS_DIR)/*.synctex.gz

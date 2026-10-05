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
PROPOSAL_PDF := scratch/proposal.pdf

SLIDES_TEMPLATE := $(PROPOSAL_PRES_DIR)/presentation.tex.template
SLIDES_TEX := $(PROPOSAL_PRES_DIR)/presentation.tex
SLIDES_PDF := scratch/presentation.pdf

NOTES_TEMPLATE := $(PROPOSAL_PRES_DIR)/presentation_notes.tex.template
NOTES_TEX := $(PROPOSAL_PRES_DIR)/presentation_notes.tex
NOTES_PDF := scratch/presentation_notes.pdf

QNA_TEMPLATE := $(PROPOSAL_PRES_DIR)/qna.tex.template
QNA_TEX := $(PROPOSAL_PRES_DIR)/qna.tex
QNA_PDF := scratch/qna.pdf

# Thesis Targets & Files
THESIS_TEMPLATE := $(THESIS_DIR)/main.tex.template
THESIS_TEX := $(THESIS_DIR)/main.tex
THESIS_PDF := scratch/thesis.pdf

PDF_BUILD := python3 scripts/build_pdf.py
ifdef FORCE
  PDF_BUILD_FLAGS := --force
endif

.PHONY: all help \
        setup setup-models test exp run-all eval plot \
        setup-v2 melody-templates melodies preflight membership select pilot generate \
        evaluate analyze examples check-run dry-run-v2 \
        proposal-phase docs proposal slides notes qna compile present \
        thesis final-phase thesis-slides \
        diff diff-clean tag-amend aux-clean clean clean-docs

all: proposal-phase final-phase

help:
	@printf "%s\n" \
		"==================================================================" \
		"  Strube Harmonic Evaluation Framework & LaTeX Document Suite" \
		"==================================================================" \
		"" \
		"  make all             Build seluruh PDF proposal dan skripsi final" \
		"  make help            Tampilkan daftar perintah" \
		"" \
		"🔬 PIPELINE RISET PROTOKOL v2 (lihat research/README.md):" \
		"  make test              Uji perangkat lunak (instrumen v1, v2, MusicXML, pipeline v2)" \
		"  make dry-run-v2        Seluruh rantai dengan backend palsu, tanpa model" \
		"  make setup-v2          Pasang DeepBach (commit terkunci) dan Coconet/Magenta.js 1.23.1" \
		"  make melody-templates  Buat templat ketik untuk 71 kandidat melodi Strube" \
		"  make melodies          Bangun kerangka Bach dan ubah melodi Strube yang sudah diketik" \
		"  make preflight         Cek setiap melodi terhadap masukan kedua model" \
		"  make membership        Perkirakan data latih DeepBach per chorale" \
		"  make select            Tetapkan sampel utama (seed tercatat) dan set uji coba" \
		"  make pilot             Jalankan uji coba (pilot)" \
		"  make generate          Jalankan generasi utama (menolak bila protokol belum dibekukan)" \
		"  make evaluate RUN=...  Kontrol kualitas dan pengukuran satu run" \
		"  make analyze RUN=...   Statistik, tabel LaTeX, dan grafik satu run" \
		"  make examples RUN=...  Contoh partitur acak untuk pembahasan" \
		"  make check-run RUN=... Cek kelengkapan satu run" \
		"" \
		"🗄  PIPELINE VERSI 1 (riwayat, jangan dipakai untuk data utama):" \
		"  make setup / exp / eval / plot" \
		"" \
		"📄 DOKUMEN FASE PROPOSAL (docs/proposal-phase/):" \
		"  make proposal        Build naskah proposal PDF (working tree)" \
		"  make proposal <v>    Build proposal tersimpan: v1, v2 (v3+ memakai make thesis)" \
		"  make slides          Build slide presentasi proposal PDF" \
		"  make notes           Build naskah presenter PDF" \
		"  make qna             Build dokumen antisipasi tanya jawab PDF" \
		"  make proposal-phase  Build semua artefak proposal" \
		"" \
		"🎓 DOKUMEN FASE SKRIPSI FINAL (docs/final-thesis/):" \
		"  make thesis          Build naskah skripsi v4 (Bab I-III) PDF (working tree)" \
		"  make thesis <ref>    Build revisi tersimpan: v3, thesis/v3, v4, head, ID commit" \
		"  make final-phase     Build semua artefak skripsi final" \
		"" \
		"🔍 VERSIONING & DIFFING:" \
		"  make diff <ref1> <ref2>  Generate side-by-side diff PDF" \
		"                           Peta perubahan: bagian, gambar, tabel, status, % kata sama" \
		"                           Baris per paragraf; sisipan/penghapusan menyisakan sisi kosong" \
		"                           Contoh: make diff proposal/v1 proposal/v2" \
		"                           Contoh terbaru: make diff proposal/v1 head" \
		"                           Contoh fase: make diff proposal thesis" \
		"                           Ref: tag, ID commit, branch, head/HEAD (commit terakhir)" \
		"                           proposal = tag proposal/v* terbaru; thesis = head" \
		"  make diff-clean          Hapus file artefak diff" \
		"  make tag-amend           Pindahkan tag versi terbaru ke HEAD (lokal, tanpa push)" \
		"                           DRY_RUN=1 hanya menampilkan perintah" \
		"" \
		"🧹 CLEANUP:" \
		"  PDF hasil Make disimpan di scratch/; file bantu dibersihkan otomatis" \
		"  make aux-clean       Hapus file bantu lama; pertahankan seluruh PDF" \
		"  make clean           Hapus seluruh file build & cache LaTeX" \
		"=================================================================="

# ==============================================================================
# PIPELINE RISET
# ==============================================================================
setup: setup-models

setup-models:
	uv run python research/scripts/bootstrap_models.py

test:
	uv run python research/tests/test_strube_validity.py
	uv run python -m unittest research/tests/test_voice_leading_v2.py
	uv run python -m unittest research/tests/test_harmonization_io.py
	uv run python -m unittest research/tests/test_pipeline_v2.py

# Protocol version 2 (research/experiments/scripts/v2.py). RUN=path/to/run for run-level targets.
V2 := uv run python research/experiments/scripts/v2.py

setup-v2:
	uv run python research/scripts/bootstrap_v2.py

melody-templates:
	$(V2) templates

melodies:
	$(V2) melodies --update-inventory

preflight:
	$(V2) preflight

membership:
	$(V2) membership

select:
	$(V2) select

pilot:
	$(V2) generate --stage pilot

generate:
	$(V2) generate --stage main

evaluate analyze examples:
	@test -n "$(RUN)" || { echo "Usage: make $@ RUN=research/outputs/runs/<run-id>"; exit 2; }
	$(V2) $@ $(RUN)

check-run:
	@test -n "$(RUN)" || { echo "Usage: make check-run RUN=research/outputs/runs/<run-id>"; exit 2; }
	$(V2) check $(RUN)

dry-run-v2:
	$(V2) dry-run

exp: run-all

run-all:
	uv run python research/run_all.py

eval:
	uv run python research/experiments/scripts/run_evaluation.py

plot:
	uv run python research/experiments/scripts/plot_results.py

# ==============================================================================
# FASE PROPOSAL
# ==============================================================================
proposal-phase: proposal slides notes qna

docs: proposal-phase

proposal: $(PROPOSAL_TEX)
	@if [ -n "$(PROPOSAL_ARGS)" ]; then \
		python3 scripts/compile_version.py proposal $(PROPOSAL_ARGS); \
	else \
		$(PDF_BUILD) $< $(PROPOSAL_PDF) $(PDF_BUILD_FLAGS) --submission proposal v2; \
	fi

slides: $(SLIDES_TEX)
	$(PDF_BUILD) $< $(SLIDES_PDF) $(PDF_BUILD_FLAGS)

notes: $(NOTES_TEX) slides
	$(PDF_BUILD) $< $(NOTES_PDF) $(PDF_BUILD_FLAGS)

qna: $(QNA_TEX)
	$(PDF_BUILD) $< $(QNA_PDF) $(PDF_BUILD_FLAGS)

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
	@if [ -n "$(THESIS_ARGS)" ]; then \
		python3 scripts/compile_version.py thesis $(THESIS_ARGS); \
	else \
		$(PDF_BUILD) $< $(THESIS_PDF) $(PDF_BUILD_FLAGS) --submission thesis v4; \
	fi

# Thesis metadata is tracked in $(THESIS_DIR)/metadata.tex; no .env.local values.
$(THESIS_TEX): $(THESIS_TEMPLATE)
	cp $< $@

# ==============================================================================
# SIDE-BY-SIDE DIFF TARGETS
# ==============================================================================
DIFF_SCRIPT := scripts/sidebydiff.py
DIFF_EXTENSIONS := tex pdf aux log html bib bcf bbl blg run.xml fdb_latexmk fls out toc synctex.gz

ifeq ($(firstword $(MAKECMDGOALS)),diff)
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

diff: $(DIFF_SCRIPT)
	@chmod +x $(DIFF_SCRIPT)
	@python3 $(DIFF_SCRIPT) $(RUN_ARGS)

diff-clean:
	rm -f $(foreach ext,$(DIFF_EXTENSIONS),scratch/proposal_diff*.$(ext))

# Move the latest proposal/v* or thesis/v* tag to HEAD locally; nothing is pushed.
tag-amend:
	@bash scripts/amend_latest_tag.sh

aux-clean:
	$(PDF_BUILD) --clean-aux

# Parse tag/ref for make proposal <ref> and make thesis <ref>
ifeq ($(firstword $(MAKECMDGOALS)),proposal)
  PROPOSAL_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(PROPOSAL_ARGS):;@:)
endif
ifeq ($(firstword $(MAKECMDGOALS)),thesis)
  THESIS_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(THESIS_ARGS):;@:)
endif

# ==============================================================================
# CLEANUP
# ==============================================================================
clean: clean-docs diff-clean

clean-docs: aux-clean
	rm -rf $(PROPOSAL_DIR)/build $(PROPOSAL_PRES_DIR)/build $(THESIS_DIR)/build
	rm -f $(PROPOSAL_TEX) $(SLIDES_TEX) $(NOTES_TEX) $(QNA_TEX) $(THESIS_TEX)
	rm -f $(PROPOSAL_PDF) $(SLIDES_PDF) $(NOTES_PDF) $(QNA_PDF) $(THESIS_PDF)
	rm -f $(PROPOSAL_DIR)/*.aux $(PROPOSAL_DIR)/*.log $(PROPOSAL_DIR)/*.fls $(PROPOSAL_DIR)/*.fdb_latexmk $(PROPOSAL_DIR)/*.bbl $(PROPOSAL_DIR)/*.bcf $(PROPOSAL_DIR)/*.blg $(PROPOSAL_DIR)/*.run.xml $(PROPOSAL_DIR)/*.out $(PROPOSAL_DIR)/*.toc $(PROPOSAL_DIR)/*.synctex.gz
	rm -f $(PROPOSAL_PRES_DIR)/*.aux $(PROPOSAL_PRES_DIR)/*.log $(PROPOSAL_PRES_DIR)/*.fls $(PROPOSAL_PRES_DIR)/*.fdb_latexmk $(PROPOSAL_PRES_DIR)/*.nav $(PROPOSAL_PRES_DIR)/*.snm $(PROPOSAL_PRES_DIR)/*.out $(PROPOSAL_PRES_DIR)/*.toc $(PROPOSAL_PRES_DIR)/*.synctex.gz
	rm -f $(THESIS_DIR)/*.aux $(THESIS_DIR)/*.log $(THESIS_DIR)/*.fls $(THESIS_DIR)/*.fdb_latexmk $(THESIS_DIR)/*.bbl $(THESIS_DIR)/*.bcf $(THESIS_DIR)/*.blg $(THESIS_DIR)/*.run.xml $(THESIS_DIR)/*.out $(THESIS_DIR)/*.toc $(THESIS_DIR)/*.synctex.gz

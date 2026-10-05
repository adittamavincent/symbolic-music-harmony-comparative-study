# Symbolic Music Harmony Comparative Study

This repository contains proposal v1/v2, final-thesis v3 (tag `thesis/v3`), the active final-thesis v4, and experiment code for measuring how often DeepBach and Coconet break five voice-leading rules from Gustav Strube. The academic text is in Indonesian.

On 2026-10-02 the v3 method was revised to a machine-only design that continues Huang et al. (2019): DeepBach and Coconet harmonize the same soprano melodies from Bach chorales and from Strube's exercises, and five voice-leading rules are counted per measure ([research/protocol.md](research/protocol.md), version 2). Protocol version 2.1 (2026-10-04) is implemented end to end in `research/` (melody preparation, generation with both models, evaluation, statistics, tables, figures) and checked with fake backends; no model has been run. See [research/README.md](research/README.md). The version-1 commands (`make setup`, `make exp`, `make eval`, `make plot`) remain as history.

Start final-thesis work with [the researcher guide](docs/final-thesis/study/researcher-guide.md) and [the progress record](docs/final-thesis/PROGRESS.md). Lecturer review notes belong in [feedback.md](docs/final-thesis/supervision/feedback.md).

Use this README when returning to the project: it explains where to edit, how to build, what versions mean, and which parts still need work.

## Returning to the project

Run commands from the repository root.

| I want to… | Do this |
| --- | --- |
| See my branch and uncommitted changes | `git status --short --branch` |
| See saved milestones | `git tag --list --sort=version:refname` |
| Build the current final-thesis v4 draft | `make thesis` |
| Build the current proposal | `make proposal` |
| Build all proposal documents | `make proposal-phase` |
| Build all current document PDFs | `make all` |
| Build presenter notes, including slides | `make notes` |
| Force LaTeX to rebuild | `make thesis FORCE=1` |
| Force metadata substitution too | `make -B thesis` |
| Rebuild a saved proposal | `make proposal v2` |
| Rebuild the latest committed thesis | `make thesis head` |
| Compare the two saved proposals | `make diff proposal/v1 proposal/v2` |
| Compare a proposal with the latest commit | `make diff proposal/v1 head` |
| Check the evaluator and pipeline | `make test` |
| Run the whole experiment chain without models | `make dry-run-v2` |
| Preview generation settings without loading models | `uv run python research/experiments/scripts/run_experiment.py --dry-run` |
| Evaluate existing generated MIDI | `make eval`, then `make plot` |
| Find known problems and cleanup priorities | Read [the maintenance audit](docs/maintenance.md) |
| Search OpenAlex for literature | Review `research/literature/openalex_queries.json`, then run `uv run research/scripts/openalex_search.py --batch` |

Edit chapter `.tex` files and `.tex.template` files. Generated top-level `.tex` files and PDFs are build outputs; changes made directly to them can be overwritten.

## What is ready

| Area | Current state |
| --- | --- |
| Proposal | Chapters 1–3, schedule, slides, presenter notes, and Q&A are present. |
| Saved proposal versions | `proposal/v1` and `proposal/v2` exist. |
| Thesis v4 | Front matter and BAB I–III, following the department's 2026 research-proposal outline. Results and conclusion chapters wait for main data; the earlier five-chapter draft remains in Git history. |
| Thesis versions | No `thesis/v*` tags exist yet. |
| Thesis defense slides | No template or build recipe exists. `thesis-slides` is only a phony Make target and produces nothing. |
| Evaluator | Instrument v2 (`research/voice_leading_v2.py`) measures the five Strube rules; validation checks 3–5 have been run on the Bach chorales and the textbook fixtures are pending. Instrument v1 (`research/strube_evaluator.py`: parallel fifths/octaves and a soprano leading-tone check) is kept unchanged as the historical instrument. |
| Experiments | The three adapters, condition manifest, batch evaluation, and plotting implement the superseded version-1 design (conditions A–D, BWV 66.6). Adapters for protocol version 2 are not written yet. Evaluator tests do not establish successful model inference. |
| Reproducibility | Requested run settings are recorded. Dependencies, model revisions, random seeds, and checkpoint checksums are not locked. |

`make test` runs the four version-1 checks and the 20 version-2 checks; all passed on 2026-10-02. Passing checks do not establish instrument validity or model-inference success. Generation adapters, run integrity, and the pilot must be completed before main collection; see [the progress gates](docs/final-thesis/PROGRESS.md#completion-gates).

## Contents

- [Repository map](#repository-map)
- [Setup](#setup)
- [Editing and building documents](#editing-and-building-documents)
- [Git versions and milestones](#git-versions-and-milestones)
- [Running experiments](#running-experiments)
- [Understanding the evaluator](#understanding-the-evaluator)
- [Naming and maintenance](#naming-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Repository map

```text
.
├── AGENTS.md                       Continuing project context and writing rules
├── Makefile                        Document and research commands
├── .env.example                    Metadata keys; local values in .env.local
├── requirements.txt                Compatibility include of research dependencies
├── run_all.py / strube_evaluator.py / setup.py
│                                   Compatibility entry points
├── docs/
│   ├── README.md / maintenance.md   Document guide and technical findings
│   ├── proposal-phase/             Proposal v1/v2 sources, slides, shared assets
│   └── final-thesis/               Map in its README.md
│       ├── PROGRESS.md              v4 status, completion gates, open items
│       ├── eval.md                  Writing checks
│       ├── supervision/             Lecturer notes, peer review, v2→v3 and v3→v4 changes, handouts
│       ├── study/                   Supervisor preparation, defense Q&A, researcher guide
│       ├── records/                 Research log and reading ledger
│       └── thesis/                  Active v4 template, cover, BAB I–III
├── research/
│   ├── README.md / protocol.md      Research commands and design decisions
│   ├── requirements.txt            Canonical Python dependencies
│   ├── voice_leading_v2.py          Measurement instrument, protocol version 2
│   ├── strube_evaluator.py          Instrument version 1, kept as the historical instrument
│   ├── run_all.py                   Version-1 research pipeline entry point
│   ├── tests/                      Software checks
│   ├── experiments/                Version-1 condition manifest, experiment and validation scripts
│   ├── literature/                 OpenAlex queries, Strube inventories, source screening
│   ├── scripts/bootstrap_models.py  Model setup and Coconet runner source
│   ├── models/                     Local third-party code/checkpoints, ignored
│   └── outputs/                    Local raw/derived artifacts, ignored
└── scripts/                        Document build and diff tools
```

Research code, tests, experiments, dependencies, and local artifacts have one owner: `research/`. See its [workspace guide](research/README.md) for the folder transition. The root `.venv/` remains the local Python environment. `scratch/` remains document-tool scratch space.

Local model/output directories and LaTeX build artifacts are ignored and may be absent in a fresh clone. Git does not back them up. The thesis still shares its class, bibliography, and logos under `docs/proposal-phase/assets/`; changes there can affect both phases.

## Setup

### Choose tools for your task

| Task | Tools needed |
| --- | --- |
| Read or edit source | Git and a text editor |
| Build current documents | Make, `envsubst`, `latexmk`, pdfLaTeX, Biber, and the template's TeX packages |
| Build saved proposals or visual diffs | Document tools plus Python 3 |
| Run evaluator/tests | Python 3.12 and Python dependencies (`research/requirements-lock.txt`) |
| Generate music | Evaluator tools plus model repositories/resources; Node/npm for Coconet |

Python 3.12 is the baseline used by the local environment since 2026-10-04. Coconet needs Node.js 18 or later; its exact packages are pinned in `research/coconet/package.json`. Document builds do not require model downloads or Node.

For a fresh checkout:

```bash
git clone https://github.com/adittamavincent/symbolic-music-harmony-comparative-study.git
cd symbolic-music-harmony-comparative-study
```

### Document metadata

Create the local file only if it does not already exist:

```bash
test -f .env.local || cp .env.example .env.local
```

Fill in `.env.local` before building a proposal. The thesis (v3 onward) reads its title, researcher, institution, dates, and committee from the tracked [metadata.tex](docs/final-thesis/thesis/metadata.tex), so each commit rebuilds with the metadata it had. The keys below serve proposal builds and thesis commits made before `metadata.tex` existed.

| Group | Keys |
| --- | --- |
| Title and researcher | `THESIS_TITLE`, `RESEARCHER_NAME`, `RESEARCHER_NIM` |
| Institution | `INSTITUTION_NAME`, `FACULTY_NAME`, `DEPARTMENT_NAME`, `PROGRAM_STUDY`, `CITY_NAME` |
| Dates | `SUBMISSION_DATE`, `ACADEMIC_YEAR`, `GRADUATION_YEAR` |
| Advisors | `ADVISOR_ACADEMIC`, `ADVISOR_ACADEMIC_NIP`, `ADVISOR_THESIS`, `ADVISOR_THESIS_NIP` |
| Examiners | `EXAMINER_1`, `EXAMINER_1_NIP`, `EXAMINER_2`, `EXAMINER_2_NIP` |

The Makefile reads this file as Make assignments, then exports values to `envsubst`. Use `KEY=value` without shell quotes; quotes can appear in the PDF. Values are inserted as LaTeX, so escape special characters where needed, such as `&` as `\&`. Keep the file local; generated PDFs contain those details.

The `ENV_FILE` variable currently changes file dependencies, but the Makefile still loads `.env.local`. Use `.env.local` until that mismatch is fixed.

### Python environment

For a fresh Python setup:

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r research/requirements-lock.txt
make test
```

The commands below use `uv run python`. With the existing environment, `.venv/bin/python` is also a direct option. `research/requirements-lock.txt` records the exact versions of the Python 3.12 environment (2026-10-04); `requirements.txt` pins only `music21==9.3.0`. Python 3.10 is no longer usable on this Mac: SciPy 1.15.3, its last SciPy release, fails to load.

### Model setup, when generating music

Protocol version 2.1 uses `make setup-v2`, which installs DeepBach at the pinned commit with its pretrained resources and Magenta.js 1.23.1 for Coconet, and records checksums in `research/models/MODELS.json`. The study order is in [research/README.md](research/README.md).

The version-1 setup below is kept as history:

```bash
make setup
```

This clones DeepBach and NotaGen into `research/models/`, writes Coconet's `package.json` and `run_coconet.js`, and runs `npm install` when npm is available. Re-running setup rewrites the Coconet wrapper. It does not install Python requirements or verify inference.

DeepBach resources and NotaGen-X weights download on generation when missing. Coconet initializes a remote checkpoint through its Node runner. Coconet also uses DeepBach's dataset code to extract its seed. The pipeline normally runs DeepBach first.

### OpenAlex literature search

The tracked search plan is [research/literature/openalex_queries.json](research/literature/openalex_queries.json). Each entry states its topic, purpose, exact query, earliest year, and result limit. Edit that one file before a bulk search. Create a free key in [OpenAlex settings](https://openalex.org/settings/api) and put `OPENALEX_API_KEY=your-key` in the ignored `.env.local`, or export `OPENALEX_API_KEY` in your shell. The helper uses only Python's standard library and can also run without a key on OpenAlex's smaller keyless budget.

```bash
uv run research/scripts/openalex_search.py --batch --dry-run
uv run research/scripts/openalex_search.py --batch
uv run research/scripts/openalex_search.py --query "chorale generation parallel fifths" --limit 25
uvx ruff check research/scripts/openalex_search.py research/tests/test_openalex_search.py
```

`uv run` executes the local script; `uvx` runs the Ruff quality check as an isolated tool. The bulk command saves CSV/JSONL and a manifest for each query, a deduplicated `combined.csv` with matching query IDs, and a snapshot of the query JSON in one dated directory under `research/outputs/openalex/`. It records exact key-free request URLs, retrieval times, counts, and any failed queries. Each query is capped at 1,000 records. Outputs are ignored by Git; copy any search log needed for a thesis claim into the research evidence bundle. Check the publication and the relevant passage before promoting a result to [the reading ledger](docs/final-thesis/records/reading-notes.csv) or the shared bibliography. The OpenAlex [agent guide](https://help.openalex.org/access/agents/) and [API quick reference](https://help.openalex.org/api/llm-quick-reference/) document query syntax and current limits.

## Editing and building documents

### Where to edit

| Change | Source |
| --- | --- |
| Thesis title, researcher, committee, dates, institution | `docs/final-thesis/thesis/metadata.tex` |
| Proposal researcher, advisors, dates, institution | `.env.local` |
| Proposal text | `docs/proposal-phase/proposal/chapters/*.tex` |
| Thesis front-matter pages (one file per page) | `docs/final-thesis/thesis/frontmatter/*.tex` |
| Thesis chapters | `docs/final-thesis/thesis/chapters/*.tex` |
| Thesis chapter-heading and page layouts | `docs/final-thesis/thesis/layout.tex` |
| Chapter order, macros, document-specific formatting | The relevant `main.tex.template` |
| Shared ISI formatting and title-page behavior | `docs/proposal-phase/assets/isi-proposal.cls` |
| References for both phases | `docs/proposal-phase/assets/references.bib` |
| Proposal slides | `docs/proposal-phase/presentation/presentation.tex.template` |
| Presenter script and slide thumbnails | `docs/proposal-phase/presentation/presentation_notes.tex.template` |
| Anticipated questions and answers | `docs/proposal-phase/presentation/qna.tex.template` |

Proposal and thesis chapters are separate copies. Editing one does not update the other. Slides, notes, and Q&A also contain their own text; update them deliberately when the argument changes.

### Build commands and output files

The build flow is `.env.local + .tex.template → generated .tex → latexmk/Biber → PDF`. Chapters are included by the generated entry point.

| Command | Output |
| --- | --- |
| `make proposal` | `scratch/proposal.pdf` |
| `make slides` | `scratch/presentation.pdf` |
| `make notes` | `scratch/presentation_notes.pdf`; builds slides first |
| `make qna` | `scratch/qna.pdf` |
| `make proposal-phase` | All four proposal PDFs |
| `make thesis` | `scratch/thesis.pdf` |
| `make final-phase` | Thesis PDF only |
| `make all` | All four proposal PDFs and the thesis PDF |

Aliases: `make docs` means `make proposal-phase`; `make compile` means `make proposal`; `make present` means `make slides`. Bare `make` builds all current document PDFs; `make help` lists commands.

Templates regenerate when their template or `.env.local` changes. Every document target performs a fresh `latexmk`/Biber build. If generated metadata looks stale, use `make -B thesis` to rerun substitution as well as compilation. `FORCE=1` forces LaTeX compilation but does not itself force substitution.

Make builds compile in temporary directories and publish only successful PDFs to `scratch/`. Saved proposals and diffs also stage their generated TeX, bibliography, and assets temporarily. Temporary files are removed after the build. Failed builds preserve a named `.log` in `scratch/` and leave the previous successful PDF intact. Presenter notes read `scratch/presentation.pdf` after building slides. Generated current entry-point `.tex` files remain beside their templates.

Proposal, thesis, and diff builds also publish an identical copy for sending, using `<Jenis>_<Versi>_23104810131_Vincent.pdf`. `make proposal` uses the current proposal revision v2; `make thesis` uses the current thesis revision v4. Saved revisions use their resolved tag label; untagged refs use the full commit ID.

| Command | Copy for sending, inside `scratch/` |
| --- | --- |
| `make proposal v2` | `Proposal_v2_23104810131_Vincent.pdf` |
| `make thesis` | `Skripsi_v4_23104810131_Vincent.pdf` |
| `make thesis v3` | `Skripsi_v3_23104810131_Vincent.pdf` |
| `make diff proposal/v1 proposal/v2` | `Diff_v1-v2_23104810131_Vincent.pdf` |
| `make diff proposal/v2 thesis/v3` | `Diff_v2-v3_23104810131_Vincent.pdf` |

The submission identity is set once in `scripts/build_pdf.py` (`SUBMISSION_ID`). These copies preserve the PDF bytes; they do not change the cover, contents, or page count. A successful rebuild replaces the copy for that revision or pair.

The shared builder adds embedded PDF bookmarks to current documents, saved proposals, and diffs, and requests the outline panel when opening in a supporting viewer. It loads `scripts/pdf-navigation.sty` in a temporary source copy, preserving the original source and historical Git snapshots. Slides and presenter notes define bookmarks for each slide; Q&A includes its unnumbered section headings.

The VS Code on-save recipe still invokes `latexmk` directly with its editor configuration. Use Make for the temporary-file cleanup and `scratch/` output workflow; run Make again after changing metadata.

### Cleanup and backups

```bash
make clean-docs   # Remove current generated .tex, PDFs, and LaTeX build files
make aux-clean    # Remove legacy auxiliary/staging files; preserve all PDFs
make diff-clean   # Remove selected proposal_diff files in scratch/
make clean        # Both of the above
```

`make clean` removes current document PDFs. It leaves chapters, templates, `.env.local`, model downloads, experiment outputs, and historical `scratch/proposal_v*.pdf` files. `diff-clean` removes legacy and ref-named diff files in `scratch/`. `aux-clean` removes known legacy build/staging files from document folders and `scratch/`, including copied historical assets, while preserving PDFs and unrelated scratch files.

Before a submission, copy the PDF to your submission archive. Keep a private backup of matching metadata and preserve experiment outputs separately. PDFs, local metadata, and experiment results are ignored by Git.

## Git versions and milestones

### Working tree, commits, and tags

| Item | Meaning |
| --- | --- |
| Working tree | Files being edited now, including uncommitted changes |
| Commit | A saved snapshot of tracked source |
| Tag | A named pointer to a commit, used here for an academic milestone |

`main` is the active development branch. A folder named `final-thesis` is a document phase, not a branch or release status. A tag snapshots the whole repository, not just the phase named in the tag. It does not freeze the current proposal folder; later commits can still edit it.

### Existing milestones

These are the local tags at this documentation audit:

| Tag | Target commit | Commit date | Role |
| --- | --- | --- | --- |
| `proposal/v1` | `ccb5d59` | 2026-06-23 | Original proposal milestone, including Q&A support |
| `proposal/v2` | `ffdfed5` | 2026-07-03 | Revised proposal milestone with thesis-advisor fields |

After `proposal/v2`, `bb7afc4` added the five-chapter thesis and research infrastructure on 2026-08-14. `c9bea49` then added metadata dependencies and adjusted signatures. No thesis milestone has been tagged yet. Check current state with:

```bash
git status --short --branch
git log -8 --oneline --decorate
git tag --list --sort=version:refname
git show --no-patch 'proposal/v2^{commit}'
```

### Daily revision workflow

1. Check `git status` before editing.
2. Edit the relevant sources and build the affected documents.
3. Inspect the PDF and run `git diff --check`.
4. Review `git diff`, then stage the intended source files.
5. Commit the revision. Tag a milestone when that commit is ready to identify a submitted or reviewed draft.

Use `docs:` for writing/documentation, `fix:` for incorrect behavior, `feat:` for new behavior, `refactor:` for restructuring, and `chore:` for maintenance. Example: `docs: revise thesis methodology after advisor feedback`.

### Save a final-thesis milestone

The researcher uses one continuing revision sequence: proposal v1, proposal v2, then final thesis v3 (tagged `thesis/v3` on 2026-10-03) and v4 (active). The next milestone is `thesis/v4`. Do not restart the active manuscript at `thesis/v1` or call it proposal v3.

Build and inspect the active manuscript with `make thesis`. Review `git diff` and the [completion gates](docs/final-thesis/PROGRESS.md#completion-gates), then commit the intended sources. Include research/protocol/shared-asset changes when they belong to the same reviewed snapshot.

After committing a draft that is ready to preserve as a review milestone:

```bash
git tag -a thesis/v4 -m "Final-thesis v4 continuing thesis v3"
git push origin main
git push origin thesis/v4
```

These commands are a recipe, not a record of actions taken here. Check the branch before pushing; push the actual branch if it differs from `main`. Keep published tags fixed. A review milestone can be a draft; its readiness should be recorded explicitly.

Preserve the submitted/reviewed PDF as `thesis-v4-YYYY-MM-DD.pdf` with the actual date, matching metadata, and research evidence. These artifacts are ignored by Git.

Use the diff command below to compare committed v3 sources with a proposal milestone.

### Build or compare a saved revision

Revisions v1 and v2 are proposals; v3 and later are thesis revisions. Each command accepts only its own phase and names the right command otherwise.

```bash
make proposal v1                    # scratch/proposal_v1.pdf (also: proposal/v1)
make proposal v2                    # scratch/proposal_v2.pdf
make thesis v3                      # scratch/thesis_v3.pdf (tag thesis/v3)
make thesis head                    # scratch/thesis_<commit-ID>.pdf, latest commit
make thesis 9896cb5                 # any thesis-phase commit
make proposal v3                    # rejected: v3 is a thesis revision
make proposal head                  # rejected: HEAD is in the thesis phase
make diff proposal/v1 proposal/v2   # scratch/proposal_diff_proposal_v1_proposal_v2.pdf
make diff proposal/v1 head          # Latest committed manuscript, no tag needed
make diff proposal/v2 e87d47b       # Abbreviated or full commit ID
make diff thesis/v3 head            # v3 against the latest committed v4 sources
```

The diff accepts tags, commit IDs, branches, and `head`/`HEAD`. Every untagged ref resolves to its full commit ID before source loading; the console and PDF show that ID. `head` follows the checked-out branch's latest commit and excludes uncommitted edits. Tags retain their names. A `proposal/` tag selects the proposal manuscript; other refs select the final thesis when present, falling back to the proposal in older snapshots. Chapters and nested inputs are read within the selected manuscript, including thesis chapters IV and V.

The comparison opens with a change map (*Peta Perubahan*). It lists front-matter pages, headings, figures, and tables, their counterparts, change status, and shared-word percentage. A small edit, formatting change, or object change cannot receive *sama* merely because most words stayed the same.

Front-matter pages pair by role; headings pair by their `\label{sec:...}`, otherwise by title and content. Within corresponding sections, identical paragraphs anchor the alignment before other paragraphs pair by content similarity. Each paragraph pair has its own synchronized row. For `A B C` against `A D B C`, `D` appears on the right with a blank left counterpart, and later paragraphs meet their original counterparts. Figures, tables, lists, and display equations are separate blocks, including when the source has no blank lines around them. Moved sections and paragraphs retain both reading orders and receive a `[dipindahkan …]` marker.

Within each paragraph pair, sentences and list items compare word by word; one sentence can pair with two after a split. Strong colors mark edits in corresponding text or objects; pale colors mark text or objects without a counterpart. Formatting, captions, footnotes, links, and references participate in the comparison. A changed figure/table label is colored when its object or number changes; stable references whose heading title or ordinary heading/figure/table/equation number changes are colored too. Cover and approval pages keep their short lines together to preserve their layout. Each version's own text macros expand before comparison.

Changed TikZ diagrams, tables, and display formulas receive a block background so highlights cannot break their syntax. Changed external images receive a frame. Graphics come from each compared Git revision and are staged by their byte hash, so replacing a file at the same filename is detected. Missing or ambiguous graphics stop the build. Each column keeps its original A4 text width on A3 landscape; rows can flow across pages without paragraph boxes. Source page breaks and front-matter wording are preserved. Thesis metadata comes from its ref; proposal metadata still uses `.env.local`. Bibliography entries have separate rows; changed names, dates, pages, or identifiers flag the complete entry while remaining valid for Biber.

Diff PDFs use `scratch/proposal_diff_<ref1>_<ref2>.pdf`. Tag names keep their text with `/` and other filename-unsafe characters replaced by `_`; untagged refs use their full commit IDs. For example, `make diff proposal/v1 head` writes `proposal_diff_proposal_v1_<HEAD-commit-ID>.pdf`. Supporting files are temporary; a failed build retains a `.log` with the same pair prefix. Building another pair preserves previous comparisons; a successful rebuild replaces that pair's PDF.

`make proposal` and `make thesis` resolve short names such as `v2` by phase (v1–v2 proposal, v3+ thesis). The diff resolves short names by trying `thesis/` before `proposal/`; use complete names such as `proposal/v2` there.

These commands read committed Git content and exclude uncommitted chapter edits. They also use current local metadata and some current assets; they do not guarantee identical reconstruction of a PDF submitted months ago.

Historical builds use [compile_version.py](scripts/compile_version.py). It reads the manuscript template of the requested phase at that commit, inlines its `\input` files recursively, and stages the class, bibliography, and logo stored at that commit. Untagged commits are assigned a phase by the manuscript they contain: a commit with a thesis manuscript builds only with `make thesis`. Current local metadata and the current navigation package still apply.

For source comparisons:

```bash
git diff -- docs/final-thesis/thesis
git diff proposal/v2 HEAD -- docs/proposal-phase
```

## Running experiments

### Conditions and model interfaces

The planned full run is 3 models × 4 conditions × 10 samples = 120 MIDI files.

| ID | DeepBach | Coconet | NotaGen-X metadata |
| --- | --- | --- | --- |
| `A_neutral` | Random initialization | One C4 seed note | Classical / Beethoven / Keyboard |
| `B_key` | C-major metadata | C4 seed plus final C-major chord | Baroque / Beethoven / Keyboard |
| `C_satb` | Fix soprano; generate A/T/B | Fix soprano; fill other voices | Baroque / Bach / Choir SATB |
| `D_full` | Fix soprano and bass; generate A/T | Fix soprano and bass; fill A/T | Same metadata as `C_satb` |

These are different native interfaces. NotaGen's B condition has no explicit C-major instruction, and its C and D prompts are identical. The labels describe the experimental design to examine; they do not prove equivalent constraints across models.

`research/experiments/strube_conditions.json` describes the design. NotaGen reads its prompt values, while DeepBach and Coconet implement many settings directly in code. `--manifest` affects the orchestrator's selection and metadata; adapters still read the default manifest. Editing a manifest entry alone does not reliably change all generation behavior.

### Commands

```bash
# Check the evaluator, then print/save generation settings
uv run python research/run_all.py --dry-run

# Print/save settings alone; skip tests and model imports
uv run python research/experiments/scripts/run_experiment.py --dry-run

# Request one sample per condition per model (12 total)
uv run python research/run_all.py --samples 1

# Default pipeline: tests → generation → evaluation → chart
make exp

# Tests → evaluate existing MIDI → chart
uv run python research/run_all.py --skip-generation

# Generation only: one model, two conditions
uv run python research/experiments/scripts/run_experiment.py --models deepbach --conditions A_neutral,B_key --samples 2

# Evaluate and plot separately
make eval
make plot
```

`--dry-run` writes metadata into `research/outputs/` but generates no MIDI. `--parallel-models` starts adapters together; it can expose dataset/resource dependencies and increase memory use. Start with the sequential default on a fresh model setup.

The `--download-notagen`/`--download-weights` flags remain for compatibility; missing NotaGen weights now download automatically.

### Outputs and reruns

| Path | Contents |
| --- | --- |
| `research/outputs/<model>/<condition>/<model>_<label>_01.mid` | Sample, e.g. `research/outputs/deepbach/A_neutral/deepbach_neutral_01.mid` |
| `research/outputs/RUN_METADATA_*.json` | Timestamped requested settings |
| `research/outputs/LATEST_RUN_METADATA.json` | Most recently requested settings, including dry runs |
| `research/outputs/MASTER_RESULTS.csv` | Per-file counts and scores from the main batch script |
| `research/outputs/SUMMARY_TABLE.csv` | Per-model/per-condition means and sample counts |
| `research/outputs/strube_evaluation_results.png` | Chart generated from the summary CSV |
| NotaGen condition folders | May contain failed `.abc` samples for debugging |

Generation reuses fixed filenames. A smaller rerun overwrites early samples and leaves older higher-numbered samples. Evaluation scans all MIDI in these folders, including earlier runs. Move existing `research/outputs/` to a separate archive before an independent experiment; record the source commit, environment versions, model revisions, and settings with it.

Requested sample counts are not checked as a completion gate. NotaGen can finish with fewer samples after retries. Evaluation skips errors, and evaluation/plotting can return success when input is absent. Check counts and CSV contents before accepting a run. The main batch script currently omits parse-quality flags and includes padded/duplicated voices in averages; repair this before using its summary for the thesis.

## Understanding the evaluator

`research/strube_evaluator.py` assumes the first four MIDI parts are soprano, alto, tenor, and bass in that order. It pads 2–3 parts by repeating the last part and repeats a single part four times, reporting `padded` or `duplicated_mono`. Four or more parts report `ok`; that flag alone does not establish correct voice order or monophonic SATB.

It checks parallel motion across all six voice pairs and leading-tone motion in the soprano. The implemented score is:

```text
strube_score = 1 - min(1, (fifth_flags + octave_flags + leading_tone_flags) / total_moments)
total_moments = max(number of soprano note/chord events, 1)
```

The score ranges from 0 to 1 and measures the implemented flags. It does not cover all Strube rules or musical quality. Counts from six voice pairs share a soprano-event denominator, so a violation rate can exceed 1 before the score is clipped.

Behavior to remember:

- `quantize([0.25])` uses a four-beat grid, not a quarter-beat grid; a probe collapsed distinct onsets. Fix and validate the selected timing grid before final measurement.
- Parallel checks compare shared note-onset offsets; they do not reconstruct every sustained vertical sonority.
- Chords contribute their highest pitch to parallel checking.
- The fifth check accepts both 7 and 5 semitones modulo 12, grouping fourths with fifths.
- The leading-tone check flags only upward motion from the pitch class below the tonic to a non-tonic pitch class. Descending, repeated, and final leading tones are not flagged.
- Main experiment evaluation infers the key. The standalone CLI defaults to C unless another tonic pitch class is passed.

```bash
# Single file: prints JSON, using C as tonic
uv run python strube_evaluator.py path/to/sample.mid

# Specify D as tonic (pitch class 2)
uv run python strube_evaluator.py path/to/sample.mid 2

# One flat directory: writes strube_results.csv there
uv run python strube_evaluator.py research/outputs/deepbach/A_neutral
```

The standalone directory command is nonrecursive. It keeps parse-quality/error rows and prints a valid-only view, but its CSV still contains flagged samples. The all-model `make eval` path is a separate implementation and currently drops those flags.

`make test` runs the four version-1 checks (a Bach MIDI round trip with a positive-score assertion, detection of deliberately parallel fifths, a direct parallel-octave case, and a direct leading-tone case) and the 20 version-2 checks in `research/tests/test_voice_leading_v2.py`. These are regression checks; they do not prove model inference, complete harmony-rule coverage, or statistical differences between models.

The version-2 instrument is `research/voice_leading_v2.py`. Its corpus validation (cross-check with music21, comparison with Huang et al.'s Bach rates, repeat-run hashes) runs with `uv run python research/experiments/scripts/validate_instrument_v2.py` and writes to `research/outputs/validation_v2/`.

## Naming and maintenance

Keep the phase folders, Indonesian chapter names, numeric chapter prefixes, Python `snake_case`, and uppercase metadata keys. Use full milestone names such as `proposal/v2` and `thesis/v3`.

Keep `A_neutral`, `B_key`, `C_satb`, `D_full`, output filenames, and CSV columns stable while scripts depend on them. For document submissions, use the automatically generated `Proposal_`, `Skripsi_`, and `Diff_` copies described above.

Correct evaluation validity and version-path selection first, then consolidate helpers and dependency management. Moving folders or renaming every script now would add churn without resolving those problems. See the [maintenance audit](docs/maintenance.md) for locations and proposed changes.

## Troubleshooting

| Symptom | Check or action |
| --- | --- |
| `No rule to make target .env.local` | Copy `.env.example` as described in setup. The file is required, so the recipe's missing-file warning is not reached. |
| Empty names or visible quote marks in PDF | Fill metadata; use Make assignment syntax without shell quotes. |
| Metadata remains stale | Run `make -B thesis` or the affected proposal target. |
| `envsubst`, `latexmk`, `pdflatex`, or `biber` absent | Check document tools and PATH. Model setup does not install TeX or gettext. |
| Missing `isi-proposal.cls` or logo | Build from the root with Make; the thesis relies on proposal assets. |
| Warnings seem absent in VS Code | Settings hide several warnings, including biblatex warnings. Read `build/main.log` and the Biber log. |
| `No module named DatasetManager` | Check `research/models/deepbach/`; run `make setup` if the clone is absent. |
| NotaGen cannot find `gradio` or `config` | Check model setup and upstream files; the adapter imports them before parsing arguments. |
| Coconet cannot find Node | Configure a runtime; `COCONET_NODE=/absolute/path/to/node` selects one explicitly. |
| Setup reported success but npm was absent | Bootstrap only warns in that case. Install npm and rerun setup before Coconet generation. |
| NotaGen retries need inspection | Use `NOTAGEN_VERBOSE=1`; `NOTAGEN_MAX_ATTEMPTS` defaults to 5 per requested sample. Inspect failed ABC files. |
| Empty or unexpectedly large result counts | Check missing folders and stale MIDI; archive outputs between independent experiments. |
| Historical build rejected | Read the message: v1–v2 and pre-thesis commits use `make proposal <ref>`; v3+, `head`, and thesis-phase commits use `make thesis <ref>`. `thesis/v4` exists only after it is tagged. |
| A PDF remains after a failed Make build | This is the previous successful PDF. Read the named failure log in `scratch/`; Make reports failure and does not publish a partial PDF. |

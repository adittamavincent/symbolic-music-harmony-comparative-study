# Symbolic Music Harmony Comparative Study

This repository contains the proposal, thesis draft, and experiment code for comparing DeepBach, Coconet, and NotaGen against selected harmony rules from Gustav Strube. The academic text is in Indonesian.

Use this README when returning to the project: it explains where to edit, how to build, what versions mean, and which parts still need work.

## Returning to the project

Run commands from the repository root.

| I want to… | Do this |
| --- | --- |
| See my branch and uncommitted changes | `git status --short --branch` |
| See saved milestones | `git tag --list --sort=version:refname` |
| Build the current thesis draft | `make thesis` |
| Build the current proposal | `make proposal` |
| Build all proposal documents | `make proposal-phase` |
| Build presenter notes, including slides | `make notes` |
| Force LaTeX to rebuild | `make thesis FORCE=1` |
| Force metadata substitution too | `make -B thesis` |
| Rebuild a saved proposal | `make proposal proposal/v2` |
| Compare the two saved proposals | `make diff proposal/v1 proposal/v2` |
| Check the evaluator | `make test` |
| Preview generation settings without loading models | `uv run python experiments/scripts/run_experiment.py --dry-run` |
| Evaluate existing generated MIDI | `make eval`, then `make plot` |
| Find known problems and cleanup priorities | Read [the maintenance audit](docs/maintenance.md) |

Edit chapter `.tex` files and `.tex.template` files. Generated top-level `.tex` files and PDFs are build outputs; changes made directly to them can be overwritten.

## What is ready

| Area | Current state |
| --- | --- |
| Proposal | Chapters 1–3, schedule, slides, presenter notes, and Q&A are present. |
| Saved proposal versions | `proposal/v1` and `proposal/v2` exist. |
| Thesis | Front matter and chapters 1–5 are present. Chapters 4–5 contain draft results and conclusions requiring verification against actual experiments. |
| Thesis versions | No `thesis/v*` tags exist yet. |
| Thesis defense slides | No template or build recipe exists. `thesis-slides` is only a phony Make target and produces nothing. |
| Evaluator | Parallel fifths, parallel octaves/unisons, and a restricted soprano leading-tone check are implemented. |
| Experiments | Three adapters, a condition manifest, batch evaluation, and plotting are present. Evaluator tests do not establish successful model inference. |
| Reproducibility | Requested run settings are recorded. Dependencies, model revisions, random seeds, and checkpoint checksums are not locked. |

The test run recorded in the [audit](docs/maintenance.md#verification-record) produced a Bach score of `0.7568`, with 6 fifth flags and 3 leading-tone flags. The thesis draft's table currently says zero violations. Reconcile the draft with the evaluator and its test assumptions before using that table as a result.

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
├── .env.example                    Metadata keys; copy to .env.local
├── .gitignore                      Local/generated file exclusions
├── .latexmkrc                      Root LaTeX output configuration
├── .vscode/settings.json            LaTeX Workshop recipe and warning filters
├── Makefile                        Document and research commands
├── requirements.txt                Python dependencies; mostly unpinned
├── run_all.py                      Tests → generation → evaluation → chart
├── strube_evaluator.py              Rule checks, scoring, single-file CLI
├── setup.py                        Compatibility wrapper for model bootstrap
├── docs/
│   ├── README.md                   Guide to document phases
│   ├── maintenance.md              Known problems and cleanup order
│   ├── proposal-phase/
│   │   ├── assets/                 ISI class, logos, shared bibliography
│   │   ├── proposal/
│   │   │   ├── main.tex.template   Proposal entry point
│   │   │   └── chapters/           Front matter, chapters 1–3, schedule
│   │   └── presentation/           Slides, notes, and Q&A templates
│   └── final-thesis/
│       ├── README.md               Thesis editing guide
│       └── thesis/
│           ├── main.tex.template   Thesis entry point
│           └── chapters/           Front matter and chapters 1–5
├── experiments/
│   ├── strube_conditions.json      A–D condition descriptions and prompts
│   └── scripts/
│       ├── run_experiment.py       Select models/conditions; record settings
│       ├── run_deepbach.py         DeepBach generation adapter
│       ├── run_coconet.py          Seed extraction, Node runner, MIDI conversion
│       ├── run_notagen.py          NotaGen-X generation adapter
│       ├── run_evaluation.py       All-model evaluation and CSV summaries
│       └── plot_results.py         Chart from SUMMARY_TABLE.csv
├── scripts/
│   ├── bootstrap_models.py         Clone models; write/install Coconet runner
│   ├── compile_version.py          Build a proposal from a committed Git ref
│   ├── sidebydiff.py               Main side-by-side proposal diff tool
│   └── proposal_diff.sh            Older latexdiff alternative; not used by make
└── tests/test_strube_validity.py    Four evaluator checks
```

Local directories such as `.venv/`, `models/`, `outputs/`, `scratch/`, and LaTeX `build/` directories are ignored. They may be absent in a fresh clone. Git does not back them up.

The thesis currently shares the class, bibliography, and logos under `docs/proposal-phase/assets/`. Changes there can affect both phases.

## Setup

### Choose tools for your task

| Task | Tools needed |
| --- | --- |
| Read or edit source | Git and a text editor |
| Build current documents | Make, `envsubst`, `latexmk`, pdfLaTeX, Biber, and the template's TeX packages |
| Build saved proposals or visual diffs | Document tools plus Python 3 |
| Run evaluator/tests | Python 3.10+ and Python dependencies |
| Generate music | Evaluator tools plus model repositories/resources; Node/npm for Coconet |

Python 3.10 is the baseline used by the local environment. There is no Node version file or dependency lockfile in this repository. Document builds do not require model downloads or Node.

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

Fill in `.env.local` before building.

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
uv venv .venv --python 3.10
uv pip install --python .venv/bin/python -r requirements.txt
make test
```

The commands below use `uv run python`. With the existing environment, `.venv/bin/python` is also a direct option. `requirements.txt` pins `music21==9.3.0`; other packages are unpinned. There is no `pyproject.toml` or `uv.lock`.

### Model setup, when generating music

```bash
make setup
```

This clones DeepBach and NotaGen into `models/`, writes Coconet's `package.json` and `run_coconet.js`, and runs `npm install` when npm is available. Re-running setup rewrites the Coconet wrapper. It does not install Python requirements or verify inference.

DeepBach resources and NotaGen-X weights download on generation when missing. Coconet initializes a remote checkpoint through its Node runner. Coconet also uses DeepBach's dataset code to extract its seed. The pipeline normally runs DeepBach first.

## Editing and building documents

### Where to edit

| Change | Source |
| --- | --- |
| Researcher, advisors, dates, institution | `.env.local` |
| Proposal text | `docs/proposal-phase/proposal/chapters/*.tex` |
| Thesis text | `docs/final-thesis/thesis/chapters/*.tex` |
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
| `make proposal` | `docs/proposal-phase/proposal/main.pdf` |
| `make slides` | `docs/proposal-phase/presentation/presentation.pdf` |
| `make notes` | `docs/proposal-phase/presentation/presentation_notes.pdf`; builds slides first |
| `make qna` | `docs/proposal-phase/presentation/qna.pdf` |
| `make proposal-phase` | All four proposal PDFs |
| `make thesis` | `docs/final-thesis/thesis/main.pdf` |
| `make final-phase` | Thesis PDF only |

Aliases: `make docs` means `make proposal-phase`; `make compile` means `make proposal`; `make present` means `make slides`. Bare `make` prints help.

Templates regenerate when their template or `.env.local` changes. Every document target invokes `latexmk`, which tracks chapter and bibliography dependencies. If generated metadata looks stale, use `make -B thesis` to rerun substitution as well as compilation. `FORCE=1` forces LaTeX compilation but does not itself force substitution.

Logs and auxiliary files go into a `build/` directory beside the document. In VS Code, build with Make once before opening generated `main.tex` in LaTeX Workshop. After changing metadata, run Make again. The editor's on-save recipe compiles LaTeX; it does not substitute metadata.

### Cleanup and backups

```bash
make clean-docs   # Remove current generated .tex, PDFs, and LaTeX build files
make diff-clean   # Remove selected proposal_diff files in scratch/
make clean        # Both of the above
```

`make clean` removes current document PDFs. It leaves chapters, templates, `.env.local`, model downloads, experiment outputs, and historical `scratch/proposal_v*.pdf` files. `diff-clean` is partial: copied assets and some bibliography/auxiliary files remain.

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

For the first thesis milestone, after committing and checking the PDF:

```bash
git tag -a thesis/v1 -m "First thesis draft sent for advisor review"
git push origin main
git push origin thesis/v1
```

Those commands are a recipe, not a record of a tag created here. Use `thesis/v2`, `thesis/v3`, and so on for later milestones. Keep published milestone tags fixed so each name continues to identify the same source.

### Build or compare a saved proposal

```bash
make proposal proposal/v1          # scratch/proposal_v1.pdf
make proposal proposal/v2          # scratch/proposal_v2.pdf
make diff proposal/v1 proposal/v2   # scratch/proposal_diff.pdf
```

Use complete names such as `proposal/v2`. Short names such as `v2` are resolved by trying `thesis/` before `proposal/`, which becomes ambiguous once both namespaces have versions.

These commands read committed Git content and exclude uncommitted chapter edits. They also use current local metadata and some current assets; they do not guarantee identical reconstruction of a PDF submitted months ago.

The helpers locate templates and chapters by filename. With both phases present, `HEAD` currently selects the thesis template first. The historical compiler also only knows the proposal chapter list. Use the two proposal tags above for these helpers; arbitrary thesis refs and proposal-to-thesis comparisons need the [path-resolution repair](docs/maintenance.md#document-tooling).

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

`experiments/strube_conditions.json` describes the design. NotaGen reads its prompt values, while DeepBach and Coconet implement many settings directly in code. `--manifest` affects the orchestrator's selection and metadata; adapters still read the default manifest. Editing a manifest entry alone does not reliably change all generation behavior.

### Commands

```bash
# Check the evaluator, then print/save generation settings
uv run python run_all.py --dry-run

# Print/save settings alone; skip tests and model imports
uv run python experiments/scripts/run_experiment.py --dry-run

# Request one sample per condition per model (12 total)
uv run python run_all.py --samples 1

# Default pipeline: tests → generation → evaluation → chart
make exp

# Tests → evaluate existing MIDI → chart
uv run python run_all.py --skip-generation

# Generation only: one model, two conditions
uv run python experiments/scripts/run_experiment.py --models deepbach --conditions A_neutral,B_key --samples 2

# Evaluate and plot separately
make eval
make plot
```

`--dry-run` writes metadata into `outputs/` but generates no MIDI. `--parallel-models` starts adapters together; it can expose dataset/resource dependencies and increase memory use. Start with the sequential default on a fresh model setup.

The `--download-notagen`/`--download-weights` flags remain for compatibility; missing NotaGen weights now download automatically.

### Outputs and reruns

| Path | Contents |
| --- | --- |
| `outputs/<model>/<condition>/<model>_<label>_01.mid` | Sample, e.g. `outputs/deepbach/A_neutral/deepbach_neutral_01.mid` |
| `outputs/RUN_METADATA_*.json` | Timestamped requested settings |
| `outputs/LATEST_RUN_METADATA.json` | Most recently requested settings, including dry runs |
| `outputs/MASTER_RESULTS.csv` | Per-file counts and scores from the main batch script |
| `outputs/SUMMARY_TABLE.csv` | Per-model/per-condition means and sample counts |
| `outputs/strube_evaluation_results.png` | Chart generated from the summary CSV |
| NotaGen condition folders | May contain failed `.abc` samples for debugging |

Generation reuses fixed filenames. A smaller rerun overwrites early samples and leaves older higher-numbered samples. Evaluation scans all MIDI in these folders, including earlier runs. Move existing `outputs/` to a separate archive before an independent experiment; record the source commit, environment versions, model revisions, and settings with it.

Requested sample counts are not checked as a completion gate. NotaGen can finish with fewer samples after retries. Evaluation skips errors, and evaluation/plotting can return success when input is absent. Check counts and CSV contents before accepting a run. The main batch script currently omits parse-quality flags and includes padded/duplicated voices in averages; repair this before using its summary for the thesis.

## Understanding the evaluator

`strube_evaluator.py` assumes the first four MIDI parts are soprano, alto, tenor, and bass in that order. It pads 2–3 parts by repeating the last part and repeats a single part four times, reporting `padded` or `duplicated_mono`. Four or more parts report `ok`; that flag alone does not establish correct voice order or monophonic SATB.

It checks parallel motion across all six voice pairs and leading-tone motion in the soprano. The implemented score is:

```text
strube_score = 1 - min(1, (fifth_flags + octave_flags + leading_tone_flags) / total_moments)
total_moments = max(number of soprano note/chord events, 1)
```

The score ranges from 0 to 1 and measures the implemented flags. It does not cover all Strube rules or musical quality. Counts from six voice pairs share a soprano-event denominator, so a violation rate can exceed 1 before the score is clipped.

Behavior to remember:

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
uv run python strube_evaluator.py outputs/deepbach/A_neutral
```

The standalone directory command is nonrecursive. It keeps parse-quality/error rows and prints a valid-only view, but its CSV still contains flagged samples. The all-model `make eval` path is a separate implementation and currently drops those flags.

`make test` runs four checks: a Bach MIDI round trip with a positive-score assertion, detection of deliberately parallel fifths, a direct parallel-octave case, and a direct leading-tone case. These are useful regression checks; they do not prove model inference, complete harmony-rule coverage, or statistical differences between models.

## Naming and maintenance

Keep the phase folders, Indonesian chapter names, numeric chapter prefixes, Python `snake_case`, and uppercase metadata keys. Use full milestone names such as `proposal/v2` and `thesis/v1`.

Keep `A_neutral`, `B_key`, `C_satb`, `D_full`, output filenames, and CSV columns stable while scripts depend on them. For a submission archive, use a descriptive name such as `thesis-v1-2026-09-28.pdf`; this does not require renaming the build's `main.pdf`.

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
| `No module named DatasetManager` | Check `models/deepbach/`; run `make setup` if the clone is absent. |
| NotaGen cannot find `gradio` or `config` | Check model setup and upstream files; the adapter imports them before parsing arguments. |
| Coconet cannot find Node | Configure a runtime; `COCONET_NODE=/absolute/path/to/node` selects one explicitly. |
| Setup reported success but npm was absent | Bootstrap only warns in that case. Install npm and rerun setup before Coconet generation. |
| NotaGen retries need inspection | Use `NOTAGEN_VERBOSE=1`; `NOTAGEN_MAX_ATTEMPTS` defaults to 5 per requested sample. Inspect failed ABC files. |
| Empty or unexpectedly large result counts | Check missing folders and stale MIDI; archive outputs between independent experiments. |
| Historical build uses wrong chapters | Use saved proposal tags. Helpers need explicit phase paths for refs containing both phases. |
| Diff/build prints “Done” despite TeX errors | Read the log. Historical helpers can accept a PDF's existence despite a nonzero compiler exit. |

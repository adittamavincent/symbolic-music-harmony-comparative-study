# Research workspace

This directory owns the computational research for the final thesis (v5, protocol version 3.0). Commands below run from the repository root. The academic manuscript lives in `docs/final-thesis/thesis/`; the design is in [protocol.md](protocol.md) and its machine-readable settings in `experiments/protocol_v3.json` (default). `experiments/protocol_v2.json` holds version 2.1 (thesis v4) unchanged; the pipeline still runs it with `--protocol research/experiments/protocol_v2.json`.

| Path | Job |
| --- | --- |
| `voice_leading_v2.py` | Measurement instrument (version 2.0): the five Strube rules, counted per measure |
| `harmonization_io.py` | Shared MusicXML input and output (IO version 1.0): reads a melody, writes the four-voice result, holds the Coconet and DeepBach encoders and output parsers |
| `melody_text.py` | Plain-text typing format for the Strube melodies, converted to MusicXML and read back (protocol 2.1; not used by 3.0) |
| `melody_sets.py` | Bach frame from the music21 corpus, typed Strube set, duplicates, features, seeded Bach sample, inventory templates |
| `generation_v2.py` | Run directories, attempt log, and the DeepBach, Coconet, and fake backends |
| `coconet/` | Tracked Node runner for Magenta.js Coconet and its pinned `package.json` |
| `evaluate_v2.py` | Quality control and measurement of a run (main, fermata, merged variants), phrase zones, Bach reference |
| `phrase_zones.py` | Protocol 3.0, question 3: sorts instrument flags and opportunities into the fermata zone and the inside of the phrase |
| `analysis_v2.py` | Descriptive statistics, Wilcoxon (models; phrase zones), Mann–Whitney (2.1 only), Holm, effect sizes, power, LaTeX tables, figures |
| `run_checks_v2.py` | Completeness check of a run; seeded discussion examples with score excerpts |
| `deepbach_membership.py` | Estimate which Bach chorales were in DeepBach's training portion |
| `experiments/scripts/v2.py` | Command line for all of the above (`make` targets call it) |
| `experiments/scripts/explore_fermata_zone_bach.py` | Exploration of phrase zones on Bach's own harmonizations (motivation for question 3; not study data) |
| `scripts/bootstrap_v2.py` | Install DeepBach (pinned commit and resources) and Coconet (Magenta.js 1.23.1); writes `models/MODELS.json` |
| `strube_evaluator.py`, `experiments/scripts/run_*.py`, `scripts/bootstrap_models.py`, `run_all.py` | Version 1 instrument and pipeline, kept unchanged as history; do not use for study data |
| `tests/` | Software checks with known inputs; not research data |
| `literature/` | OpenAlex plan, screening notes, Strube rule pages, exercise inventory, typed melodies, fixture list |
| `requirements.txt`, `requirements-lock.txt` | Dependencies; the lock records the exact versions of the Python 3.12 environment |
| `models/`, `outputs/` | Local model code and weights, and all generated files; ignored by Git |

Software tests check implementation behavior. Instrument validation, pilot data, and main data are separate kinds of evidence; passing tests does not validate the instrument or answer the research questions.

## Environment

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r research/requirements-lock.txt
make test
```

Python 3.12 replaced 3.10 on 2026-10-04: SciPy 1.15.3, the last release for Python 3.10, no longer loads on this macOS. Node.js 18 or later is needed for Coconet.

## Running the study

Each step writes files that the next step reads. Nothing below has been run with a model yet.

```bash
make dry-run-v2          # the whole chain with fake backends in a temporary folder; no model, no research data
make melodies            # Bach frame -> research/outputs/melodies/manifest.csv (typed Strube melodies only matter for 2.1)
make setup-v2            # downloads DeepBach code and weights and Magenta.js; records checksums
make preflight           # can each model encode each melody? (no generation)
make membership          # DeepBach training membership estimate
make select              # main sample (40 Bach melodies, seed 20261004) and pilot set (3 others)
make pilot               # pilot run -> research/outputs/runs/pilot-<time>/
make evaluate RUN=research/outputs/runs/pilot-<time>
make analyze RUN=research/outputs/runs/pilot-<time>
make check-run RUN=research/outputs/runs/pilot-<time>
```

After the pilot, record what was learned in `docs/final-thesis/records/research-log.md`, settle the open decisions in `docs/final-thesis/PROGRESS.md`, agree the protocol with the supervisor, and set `"frozen": true` in `experiments/protocol_v3.json`. Then:

```bash
make generate            # main run; refuses while the protocol is not frozen
make evaluate RUN=research/outputs/runs/main-<time>
make analyze RUN=research/outputs/runs/main-<time>
make examples RUN=research/outputs/runs/main-<time>
make check-run RUN=research/outputs/runs/main-<time>
```

`make analyze` writes the tables for BAB IV (`analysis/tables/*.tex`, in Indonesian), the box plots and the phrase-zone figure (`figures/`), and `analysis/summary.json`. A run that stops halfway continues with `uv run python research/experiments/scripts/v2.py generate --stage main --resume <run-dir>`; failed attempts are retried only with `--retry-failed` and are logged as new attempts.

## Data records

A run directory is never overwritten. It holds `run.json` (protocol snapshot, code revision and whether the working tree was clean, environment, model manifest), the melodies given to the models, `attempts.jsonl` (one line per attempt, append-only), raw model output, four-part MusicXML and MIDI, and later `evaluation/`, `analysis/`, `figures/`, and `examples/`. Back the run directories up outside the repository; Git does not keep them. Do not change the instrument without a new version number, and keep earlier measurements when it changes.

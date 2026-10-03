# Research workspace

This directory owns the computational research for final thesis v3. Commands below run from the repository root. The academic manuscript lives in `docs/final-thesis/thesis/`.

| Path | Job |
| --- | --- |
| `voice_leading_v2.py` | Measurement instrument for protocol version 2: the five Strube rules, counted per measure |
| `harmonization_io.py` | Shared MusicXML input and output for protocol version 2: reads a melody, writes the four-voice result, and holds the Coconet and DeepBach input adapters and output parsers |
| `strube_evaluator.py` | Instrument version 1 (parallels and a soprano leading-tone check), kept unchanged as the historical instrument |
| `tests/` | Software checks with known inputs and expected behavior; not the main research dataset |
| `experiments/strube_conditions.json` | Version-1 condition matrix (A–D), superseded by protocol version 2 and kept as history |
| `experiments/scripts/` | Version-1 model adapters, generation orchestration, evaluation, plotting; `validate_instrument_v2.py` runs validation checks 3–5 |
| `scripts/bootstrap_models.py` | Download/setup third-party implementations and write the Coconet runner |
| `scripts/openalex_search.py` | Bounded, repeatable literature search with CSV, JSONL, and query manifest |
| `literature/` | OpenAlex batch plan (`openalex_queries.json`), Strube rule pages, exercise inventory, textbook fixture list, screening notes |
| `requirements.txt` | Research Python dependencies; mostly unpinned |
| `protocol.md` | Protocol version 2: design, instrument definitions, validation results, analysis plan |
| `models/` | Local model clones/checkpoints, ignored by Git; may not exist yet |
| `outputs/` | Local metadata, MIDI, CSV, charts, ignored by Git |

Keep `tests` and `experiments` as separate names inside this workspace. A software test checks implementation behavior; an experiment collects evidence about a research question. Instrument validation also needs independently annotated musical examples. Listening to generated samples supports inspection but does not automatically constitute a formal listening study.

## Commands

```bash
make test
.venv/bin/python research/experiments/scripts/run_experiment.py --dry-run
make setup
make exp
make eval
make plot
```

The first two commands inspect the existing instrument/settings without model generation. The remaining commands operate the existing, unfinished pipeline. Resolve the [readiness gates](../docs/final-thesis/PROGRESS.md#completion-gates) before treating their outputs as final research data. Setup may download third-party code and dependencies; generation may download checkpoints.

`make test` uses `uv run`; the direct `.venv/bin/python` command uses the existing local environment. Install dependencies from the repository root with `uv pip install -r research/requirements.txt` after creating/activating the environment as described in the root README.

## Folder transition

The old root `experiments/`, `tests/`, and local `outputs/` moved here. Update direct commands to start with `research/`. The root `run_all.py`, `strube_evaluator.py`, `setup.py`, and `requirements.txt` retain their previous entry-point roles and delegate here. `strube_evaluator.py` is instrument version 1, kept unchanged as the historical instrument; instrument version 2 is `voice_leading_v2.py`.

Each script's existing `PROJECT_ROOT` now points to this research workspace. Relative internal paths remain `experiments/`, `models/`, and `outputs/`. Historical metadata retains its original paths as provenance; do not interpret those paths as new runtime locations.

## Data records

The current runner uses shared output folders. Run isolation has not been implemented. Do not assume that rerunning with fewer samples removes old files or that `LATEST_RUN_METADATA.json` proves successful generation.

Before main collection, implement run-specific generation, evaluation, and plotting paths together. The intended layout is `outputs/<run-id>/` with raw generation, attempt log, effective configuration, per-file evaluation, analysis, and figures bound to that run. Keep pilot and main runs distinct and retain every failed attempt. This is a proposed layout, not a current command-line feature.

For every final table, record the run ID, code revision, instrument version, manifest snapshot, model/checkpoint revisions and hashes, environment, seed policy, requested/actual counts, exclusion reasons, and analysis command. Back up the evidence bundle outside ignored folders; Git currently does not preserve raw outputs or checkpoints. Do not overwrite old measurements when changing the instrument.

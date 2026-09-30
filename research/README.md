# Research workspace

This directory owns the computational research for final thesis v3. Commands below run from the repository root. The academic manuscript lives in `docs/final-thesis/thesis/`.

| Path | Job |
| --- | --- |
| `strube_evaluator.py` | Existing rule-checking instrument; definitions and timing still require validation |
| `tests/` | Software checks with known inputs and expected behavior; not the main research dataset |
| `experiments/strube_conditions.json` | Proposed condition matrix; not yet an approved comparable design |
| `experiments/scripts/` | Model adapters, generation orchestration, evaluation, plotting |
| `scripts/bootstrap_models.py` | Download/setup third-party implementations and write the Coconet runner |
| `scripts/openalex_search.py` | Bounded, repeatable literature search with CSV, JSONL, and query manifest |
| `literature/openalex_queries.json` | Tracked batch plan for literature discovery |
| `requirements.txt` | Research Python dependencies; mostly unpinned |
| `protocol.md` | Decisions to settle before collecting main data |
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

The old root `experiments/`, `tests/`, and local `outputs/` moved here. Update direct commands to start with `research/`. The root `run_all.py`, `strube_evaluator.py`, `setup.py`, `requirements.txt`, and `scripts/bootstrap_models.py` retain their previous entry-point roles and delegate here. There is one evaluator implementation.

Each script's existing `PROJECT_ROOT` now points to this research workspace. Relative internal paths remain `experiments/`, `models/`, and `outputs/`. Historical metadata retains its original paths as provenance; do not interpret those paths as new runtime locations.

## Data records

The current runner uses shared output folders. Run isolation has not been implemented. Do not assume that rerunning with fewer samples removes old files or that `LATEST_RUN_METADATA.json` proves successful generation.

Before main collection, implement run-specific generation, evaluation, and plotting paths together. The intended layout is `outputs/<run-id>/` with raw generation, attempt log, effective configuration, per-file evaluation, analysis, and figures bound to that run. Keep pilot and main runs distinct and retain every failed attempt. This is a proposed layout, not a current command-line feature.

For every final table, record the run ID, code revision, instrument version, manifest snapshot, model/checkpoint revisions and hashes, environment, seed policy, requested/actual counts, exclusion reasons, and analysis command. Back up the evidence bundle outside ignored folders; Git currently does not preserve raw outputs or checkpoints. Do not overwrite old measurements when changing the instrument.

# Maintenance audit

Audit date: 2026-09-28. Source baseline: `c9bea49` on `main`. Findings below describe that baseline except for the small fixes listed under “Applied.”

The repo needs correctness work before a broad reorganization. Keep the document phases and chapter names; repair evaluation, run isolation, and historical file selection first.

## Applied

- Replaced the root README with an operating guide and corrected both document guides. The old guides described thesis tags/slides that do not exist and called the thesis a placeholder despite its tracked chapters.
- Fixed `make notes` to depend on the `slides` target. Previously it depended on `presentation.pdf`, which had no Make recipe, so a fresh notes build failed.
- Added generated `docs/final-thesis/thesis/main.tex` to `.gitignore`, matching the proposal entry points.
- Replaced Make help's proposal-to-thesis diff example with a note about the unverified thesis-ref support.

No experiment behavior, academic claims, chapter names, or milestone tags were changed.

## Research correctness

| Priority | Evidence and consequence | Proposed repair |
| --- | --- | --- |
| Before reporting results | [Main batch evaluation](../experiments/scripts/run_evaluation.py) discards `parse_quality` and includes padded/duplicated voices in its averages. [Standalone batch evaluation](../strube_evaluator.py) retains flags, so the two entry points behave differently. | Preserve parse quality and errors in master results; summarize only eligible SATB samples and report exclusions/counts. Reuse one evaluation-row builder. |
| Before reporting results | [Coconet MIDI reconstruction](../experiments/scripts/run_coconet.py), in `reconstruct_json_to_midi`, sets an offset and then calls `part.append(n)`. Append places the event at the part's end, shifting gaps or overlaps. A local probe changed requested offsets `[0, 2]` into `[0, 1]`. | Insert notes at their explicit offsets and verify a sequence with gaps, overlaps, and a nonzero first onset. Keep sample generation separate from this conversion test. |
| Before reporting results | [Condition manifest](../experiments/strube_conditions.json) gives NotaGen C and D identical prompts. NotaGen B does not instruct C major. DeepBach/Coconet settings are partly hardcoded, and adapters do not receive the orchestrator's custom `--manifest` path. Recorded settings can differ from executed settings. | Decide which comparisons the model interfaces support. Pass the selected manifest/resolved settings into adapters and record effective settings. Do not claim identical or equivalent constraints without support. |
| Before reporting results | [Generation adapters](../experiments/scripts/run_deepbach.py), [Coconet wrapper](../scripts/bootstrap_models.py), and [NotaGen adapter](../experiments/scripts/run_notagen.py) reuse fixed sample filenames. [Evaluation](../experiments/scripts/run_evaluation.py) scans every MIDI in those folders. A smaller rerun leaves old samples in the next summary. | Give each experiment its own run directory; bind evaluation and plotting to that run. Record requested and actual sample counts. Until then, archive `outputs/` before independent runs. |
| Before reporting results | [Chapter 4](final-thesis/thesis/chapters/04-hasil-pembahasan.tex) says Bach has zero flags and presents 120 samples as evaluated; the chart inclusion is commented out. [Chapter 5](final-thesis/thesis/chapters/05-kesimpulan-saran.tex) asserts significant differences and reduced violations without a linked measured analysis. The test output below contradicts the zero-flag table. | Replace provisional results with verified measurements. Record how the key and rule definitions were chosen, include the actual sample counts, and support significance claims with the corresponding analysis. |
| Instrument definition | [Evaluator](../strube_evaluator.py) folds perfect fourths into fifth checks, compares simultaneous onsets rather than sustained sonorities, and uses a restricted soprano leading-tone check. The Bach test explicitly forces tonic C and only asserts a positive score. | Review definitions against the intended musicological method. Add focused examples for accepted/rejected intervals, held notes, rests, leading-tone contexts, and voice mapping before changing scoring. Preserve the old definition/results if the instrument changes. |
| Completion reporting | [NotaGen](../experiments/scripts/run_notagen.py) can return after generating too few samples. [Evaluation](../experiments/scripts/run_evaluation.py) skips failed files and returns normally when no rows exist. [Plotting](../experiments/scripts/plot_results.py) also returns normally for absent input. [run_all.py](../run_all.py) relies on exit codes, so it can report completion with incomplete or stale artifacts. | Fail required stages on missing data, record per-file failures, and check expected sample/artifact counts before announcing completion. |

## Document tooling

| Priority | Evidence and consequence | Proposed repair |
| --- | --- | --- |
| Before supporting thesis snapshots | [compile_version.py](../scripts/compile_version.py) and [sidebydiff.py](../scripts/sidebydiff.py) select files using the first filename suffix match. At `HEAD`, `main.tex.template` and `00-frontmatter.tex` resolve to the thesis. The historical compiler only inlines proposal chapters, leaving thesis chapters 4–5 unresolved. | Resolve files inside an explicit phase/document root, including historical layouts. Share the resolver. Test both proposal tags and a ref containing both phases; then document thesis snapshot support. |
| Historical build reliability | Both historical tools can accept a PDF's existence despite a nonzero compiler return code. Historical rebuilds also use current local metadata; the diff can use the current class/assets. | Check compiler exit status and propagate failure. State source/metadata provenance and distinguish an archived submission PDF from a fresh reconstruction. |
| Metadata configuration | [Makefile](../Makefile) always includes `.env.local`, while `ENV_FILE` only changes dependency checks. Missing metadata triggers Make's prerequisite error before the recipe's warning. Python helpers parse values differently from Make. | Load the configured file consistently; use a clear missing-file check. Share metadata parsing or document one format with equivalent behavior across current and historical builds. |
| Unimplemented command | [Makefile](../Makefile) lists `thesis-slides` as phony without a recipe or template. `make thesis-slides` silently does nothing. | Remove the advertised target until implemented, or make it fail with a clear message. Add a thesis presentation only when it is needed. |
| Partial cleanup | `diff-clean` removes selected `proposal_diff.*` files but leaves bibliography files, copied assets, and some auxiliary files. | Isolate each diff's artifacts in a dedicated directory and clean that directory. Preserve unrelated `scratch/` files. |
| Hidden warnings | [VS Code settings](../.vscode/settings.json) suppress layout and biblatex warnings. The verified slide/notes build still has layout warnings. | Retain quiet editor behavior if preferred, but expose bibliography failures and inspect build logs/PDF layout before a milestone. |

## Structure and naming

| Area | Recommendation | Why |
| --- | --- | --- |
| Phase folders and chapters | Keep `proposal-phase/`, `final-thesis/`, and `NN-nama-bab.tex`. | They express academic purpose and reading order. Renaming would break includes and historical lookup without improving the research. |
| Shared document assets | Consider `docs/shared/assets/` after fixing historical resolution. Update Make, templates, local latexmk configs, Python helpers, and IDE behavior together. | The thesis currently depends on assets owned by the proposal folder. An explicit shared owner would clarify this dependency. |
| Git and metadata helpers | Extract shared ref resolution, phase-aware lookup, and metadata parsing from the two Python document helpers. | These are duplicated and already disagree with the current-build path. |
| Large diff script | After regression fixtures exist, split `sidebydiff.py` into Git/source loading, LaTeX token rendering, bibliography diffing, and compilation. | At roughly 1,100 lines, unrelated responsibilities are difficult to check together. Extract by responsibility rather than line count. |
| Model bootstrap | Move the embedded Coconet JavaScript/package template into tracked source files and let bootstrap copy them. | The current JavaScript lives in a Python string and its generated copy is overwritten by setup. |
| Legacy entry points | Keep `setup.py` as a compatibility wrapper until callers are accounted for; prefer `make setup`. Consider retiring `proposal_diff.sh` after confirming nothing uses it. | `setup.py` is not Python package metadata. The shell diff is an independent older implementation that is not called by Make. |
| Python style | Keep `snake_case`; remove unused imports, redundant variables, and stale comments after the correctness fixes. Use a single formatter/linter configuration if adopted. | Cosmetic edits can be kept separate from changes that alter measured results. |
| Condition IDs and CSV names | Preserve existing identifiers until all adapters, summaries, plotting, docs, and archived data can migrate together. | `A_neutral`–`D_full`, uppercase output filenames, and capitalized summary columns are active contracts. |
| Display names | Use a shared mapping for `DeepBach`, `Coconet`, and `NotaGen` when revising result schemas. | `model.capitalize()` currently yields `Deepbach`/`Notagen`, and plotting depends on those spellings. |
| Dependencies | Record a Python lock, model commit IDs, checkpoint checksums, Node runtime, and Coconet's package lock. Add random-seed/effective-setting fields to run records. | A source tag and an unpinned install cannot reconstruct the same model/environment by themselves. |

Make `README.md` the operating reference, keep phase guides short, and keep unresolved evidence here. Update the relevant entry when a fix lands so the documents remain consistent.

## Suggested work order

1. Repair SATB quality handling, Coconet event timing, and result claims.
2. Align condition definitions with executed settings and isolate experiment runs.
3. Add completion checks and reproducibility records.
4. Repair phase-aware historical builds and compiler failure handling.
5. Consolidate helpers, move shared assets, and then apply formatting/import cleanup.

## Verification record

Performed locally on 2026-09-28:

| Check | Result |
| --- | --- |
| Git history, tree, tags, Makefile, templates, adapters, evaluator review | Local `proposal/v1` → `ccb5d59`; `proposal/v2` → `ffdfed5`; no thesis tags. |
| `.venv/bin/python tests/test_strube_validity.py` | All four checks passed with Python 3.10.20, music21 9.3.0, and pandas 2.3.3. |
| Bach fixture, explicitly evaluated with tonic C by the test | Score `0.7568`; 37 soprano events; 6 fifth flags; 0 octave flags; 3 leading-tone flags. |
| Artificial parallel fixture | Score `0.0`; 14 fifth flags; 7 octave flags; 0 leading-tone flags. |
| Fresh notes dependency, before fix | `make -n notes` failed: no rule for `presentation.pdf`. |
| Fresh notes build, after fix | `make notes` exited successfully and generated both slides and presenter notes. Existing layout warnings remain; visual layout was not reviewed. |
| Current thesis build | `make thesis` exited successfully and generated `docs/final-thesis/thesis/main.pdf`, including Biber processing. Visual layout and result claims were not validated. |
| Generation-only dry run | `uv run --offline python experiments/scripts/run_experiment.py --dry-run` exited successfully using a temporary writable uv cache. It printed the matrix and wrote metadata; no models were loaded. |
| Thesis generated-source ignore | `git check-ignore -v docs/final-thesis/thesis/main.tex` matched the new rule. |
| Historical lookup probe | Both `main.tex.template` and `00-frontmatter.tex` at `HEAD` resolved to the thesis tree. |
| Coconet-style append timing probe | Requested offsets `[0, 2]` became `[0, 1]` after append, using two one-beat music21 notes. |
| `make -n thesis-slides` | Reported nothing to do; no slide build exists. |
| Documentation checks | All 37 local links/anchors, code fences, documented Make target names, and the supplied editing-pattern word checks passed across four Markdown files. |
| `git diff --check` | Passed. |

Model bootstrap, model downloads, full inference, historical PDF/diff compilation, and visual PDF review were not performed as part of this audit. The passing evaluator checks establish those four cases only.

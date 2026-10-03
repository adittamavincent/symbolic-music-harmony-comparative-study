# Maintenance audit

Audit date: 2026-09-28. Source baseline: `c9bea49` on `main`. Findings below started at that baseline. Links now use the `research/` workspace paths; subsequent v3 changes and verification are recorded below.

Research correctness remains open. Computational research has now moved into `research/` with behavior preserved; document phases and chapter names remain stable. Resolve the measurement and run-integrity findings before main data collection.

## Applied

- Replaced the root README with an operating guide and corrected both document guides. The old guides described thesis tags/slides that do not exist and called the thesis a placeholder despite its tracked chapters.
- Fixed `make notes` to depend on the `slides` target. Previously it depended on `presentation.pdf`, which had no Make recipe, so a fresh notes build failed.
- Added generated `docs/final-thesis/thesis/main.tex` to `.gitignore`, matching the proposal entry points.
- Replaced Make help's proposal-to-thesis diff example with a note about the unverified thesis-ref support.
- 2026-10-03: Reorganized `docs/final-thesis/` into `supervision/`, `study/`, and `records/`, with a folder map in its README. `PROGRESS.md` now holds the current status only; its dated history moved to `records/research-log.md`. Removed the unused legacy scripts listed under *Structure and naming*.

The original audit made no experiment-behavior or academic-claim changes. Later v3 preparation changed draft claims and research ownership as recorded below; no milestone tags were created.

## Research correctness

| Priority | Evidence and consequence | Proposed repair |
| --- | --- | --- |
| Before reporting results | [Main batch evaluation](../research/experiments/scripts/run_evaluation.py) discards `parse_quality` and includes padded/duplicated voices in its averages. [Standalone batch evaluation](../research/strube_evaluator.py) retains flags, so the two entry points behave differently. | Preserve parse quality and errors in master results; summarize only eligible SATB samples and report exclusions/counts. Reuse one evaluation-row builder. |
| Before reporting results | [Coconet MIDI reconstruction](../research/experiments/scripts/run_coconet.py), in `reconstruct_json_to_midi`, sets an offset and then calls `part.append(n)`. Append places the event at the part's end, shifting gaps or overlaps. A local probe changed requested offsets `[0, 2]` into `[0, 1]`. | Insert notes at their explicit offsets and verify a sequence with gaps, overlaps, and a nonzero first onset. Keep sample generation separate from this conversion test. |
| Before reporting results | [Condition manifest](../research/experiments/strube_conditions.json) gives NotaGen C and D identical prompts. NotaGen B does not instruct C major. DeepBach/Coconet settings are partly hardcoded, and adapters do not receive the orchestrator's custom `--manifest` path. Recorded settings can differ from executed settings. | Decide which comparisons the model interfaces support. Pass the selected manifest/resolved settings into adapters and record effective settings. Do not claim identical or equivalent constraints without support. |
| Before reporting results | [Generation adapters](../research/experiments/scripts/run_deepbach.py), [Coconet wrapper](../research/scripts/bootstrap_models.py), and [NotaGen adapter](../research/experiments/scripts/run_notagen.py) reuse fixed sample filenames. [Evaluation](../research/experiments/scripts/run_evaluation.py) scans every MIDI in those folders. A smaller rerun leaves old samples in the next summary. | Give each experiment its own run directory; bind evaluation and plotting to that run. Record requested and actual sample counts. Until then, archive `research/outputs/` before independent runs. |
| Main evidence still missing | The v3 manuscript now contains BAB I–III only. The earlier chapters IV–V (software-check measurements, bounded conclusions) remain in Git history before this outline change. | Write results and conclusion chapters from run-linked main measurements after instrument validation and data collection. |
| Before reporting results | [Evaluator quantization](../research/strube_evaluator.py) uses `quantize([0.25])`. A local probe collapsed onsets `0, 0.25, 0.5, 1, 2` to zero and made quarter-beat durations four beats. music21 treats the argument as quarter-length divisors, not time-step lengths. | Set and justify a time grid; verify onsets, durations, held notes, ties, and rests. Preserve the earlier instrument/results and rerun affected measurements. See [official quantization documentation](https://music21.org/music21docs/moduleReference/moduleStreamBase.html). |
| Instrument definition | [Evaluator](../research/strube_evaluator.py) folds perfect fourths into fifth checks, compares simultaneous onsets rather than sustained sonorities, and uses a restricted soprano leading-tone check. The Bach test explicitly forces tonic C and only asserts a positive score. | Review definitions against the intended musicological method. Add focused examples for accepted/rejected intervals, held notes, rests, leading-tone contexts, and voice mapping before changing scoring. Preserve the old definition/results if the instrument changes. |
| Completion reporting | [NotaGen](../research/experiments/scripts/run_notagen.py) can return after generating too few samples. [Evaluation](../research/experiments/scripts/run_evaluation.py) skips failed files and returns normally when no rows exist. [Plotting](../research/experiments/scripts/plot_results.py) also returns normally for absent input. [run_all.py](../research/run_all.py) relies on exit codes, so it can report completion with incomplete or stale artifacts. | Fail required stages on missing data, record per-file failures, and check expected sample/artifact counts before announcing completion. |

## Document tooling

| Priority | Evidence and consequence | Proposed repair |
| --- | --- | --- |
| Repaired 2026-09-30 | [compile_version.py](../scripts/compile_version.py) now takes a phase (`proposal`/`thesis`), selects that phase's template at the commit, and inlines exact nested inputs. The diff keeps its own resolver. | Consider sharing ref resolution between the diff and historical builds. |
| Repaired 2026-10-02 | `make diff proposal/v2 thesis/v3` failed. The thesis front matter defines `\thesiscoverhead`, `\signatory`, and `\examinercolumn` in chapter text, and each diff block is a TeX group, so later blocks lost them; `\uline` also needed the thesis template's `ulem`. Biber rejected changed author names wrapped in `\textcolor`, page-argument citations such as `\parencite[35]{strube1928}:` entered `soul`, and biblatex sentence casing broke `\textcolor` in titles. [sidebydiff.py](../scripts/sidebydiff.py) now runs source definitions at the start of each block on its side, loads both templates' packages, keeps page-argument citations whole, and colors changed bibliography fields with robust switches except fields Biber parses. The v2→v3 and v1→v2 diffs compile; v2→v3 cover, approval page, and bibliography were checked visually. | A changed name, date, URL, or page field appears in its modified entry without a text color. A changed definition shows only through its rendered use, not as source text. |
| Diff comparison rebuilt 2026-10-02 | The earlier pairing matched sections by heading text and then TF-IDF similarity, and compared whole paragraphs. In `proposal/v2 → thesis/v3` nearly all text was colored, re-leveled sections sat in separate rows, lists did not meet their counterparts, and cover and approval wording held in macros (`\thesiscoverhead`, `\examinercolumn`) was not compared. [diff_layout.py](../scripts/diff_layout.py) now pairs front-matter pages by role and headings by ID (`\label{sec:...}`, else title slug) first, pairs text only between the same two anchors, and aligns sentences, list items, and lines (one-to-one, or one sentence to two). Pages of short lines compare word by word. [diff_tokens.py](../scripts/diff_tokens.py) compares words inside formatting groups by visible style. [sidebydiff.py](../scripts/sidebydiff.py) expands each version's own macros before comparing and adds a change map with status and shared-word share. Measured on the sources: v1→v2 shares 65% of words, v2→v3 5%; 1 of 196 proposal v2 sentences has a v3 counterpart at ≥0.9 word similarity and 178 have none at ≥0.5, so most v3 text is correctly marked as new. thesis/v3 against the reorganized sources renders no highlights. | Thresholds (sentence 0.35, paragraph 0.35, structured page at ≤8 content words per line) were checked on v1→v2, v2→v3, and v3→reorganized sources only. A paragraph rewritten below the threshold stays pale on both sides. Bibliography rows approximate APA order by family name, year, and title. |
| Thesis sources reorganized 2026-10-02 | `chapters/00-titlepage.tex` and `00-frontmatter.tex` (both numbered 00) became `frontmatter/01-halaman-judul.tex` to `09-abstract.tex`, one page per file. Page and heading macros moved to `layout.tex`; each chapter file opens with its own `\thesischapter`; `03-metodologi.tex` became `03-metode-penelitian.tex`; every section and subsection carries a `\label{sec:...}` ID. `make thesis` output is unchanged: 63 pages with identical extracted text and identical word positions. | Keep a heading's label when renaming it, so `make diff` pairs the revisions; give a new section a new label. |
| Historical source provenance | Current builds, the historical compiler, and the diff now share temporary compilation and reject nonzero compiler exits. Historical rebuilds still use current local metadata; the diff can use the current class/assets. | Preserve the documented metadata/assets provenance and distinguish an archived submission PDF from a fresh reconstruction. |
| Metadata configuration | [Makefile](../Makefile) always includes `.env.local`, while `ENV_FILE` only changes dependency checks. Missing metadata triggers Make's prerequisite error before the recipe's warning. Python helpers parse values differently from Make. | Load the configured file consistently; use a clear missing-file check. Share metadata parsing or document one format with equivalent behavior across current and historical builds. |
| Unimplemented command | [Makefile](../Makefile) lists `thesis-slides` as phony without a recipe or template. `make thesis-slides` silently does nothing. | Remove the advertised target until implemented, or make it fail with a clear message. Add a thesis presentation only when it is needed. |
| Cleanup repaired for Make builds | Supporting files now compile in temporary directories and are removed afterward. `aux-clean` removes known legacy auxiliary/staging files while preserving PDFs and unrelated scratch files. `diff-clean` also removes diff PDFs. | Use Make for this workflow; direct editor `latexmk` builds still follow editor/local configuration. |
| Hidden warnings | [VS Code settings](../.vscode/settings.json) suppress layout and biblatex warnings. The verified slide/notes build still has layout warnings. | Retain quiet editor behavior if preferred, but expose bibliography failures and inspect build logs/PDF layout before a milestone. |

## Structure and naming

| Area | Recommendation | Why |
| --- | --- | --- |
| Phase folders and chapters | Keep `proposal-phase/`, `final-thesis/`, and `NN-nama-bab.tex`. | They express academic purpose and reading order. Renaming would break includes and historical lookup without improving the research. |
| Shared document assets | Consider `docs/shared/assets/` after fixing historical resolution. Update Make, templates, local latexmk configs, Python helpers, and IDE behavior together. | The thesis currently depends on assets owned by the proposal folder. An explicit shared owner would clarify this dependency. |
| Git and metadata helpers | Extract shared ref resolution, phase-aware lookup, and metadata parsing from the two Python document helpers. | These are duplicated and already disagree with the current-build path. |
| Repaired 2026-10-02 | `sidebydiff.py` is split by responsibility: Git and source assembly ([sidebydiff.py](../scripts/sidebydiff.py)), pairing and rows ([diff_layout.py](../scripts/diff_layout.py)), word highlighting ([diff_tokens.py](../scripts/diff_tokens.py)), and references ([diff_bibliography.py](../scripts/diff_bibliography.py)), each with its own tests in `scripts/tests/`. | — |
| Model bootstrap | Move the embedded Coconet JavaScript/package template into tracked source files and let bootstrap copy them. | The current JavaScript lives in a Python string and its generated copy is overwritten by setup. |
| Repaired 2026-10-03 | `setup.py` imports `research.scripts.bootstrap_models` directly, like the other root entry points. The intermediate `scripts/bootstrap_models.py` wrapper and the unused `scripts/proposal_diff.sh` (an older latexdiff implementation not called by Make or any document) were removed. Prefer `make setup`. | — |
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
| `.venv/bin/python research/tests/test_strube_validity.py` | All four checks passed with Python 3.10.20, music21 9.3.0, and pandas 2.3.3. |
| Bach fixture, explicitly evaluated with tonic C by the test | Score `0.7568`; 37 soprano events; 6 fifth flags; 0 octave flags; 3 leading-tone flags. |
| Artificial parallel fixture | Score `0.0`; 14 fifth flags; 7 octave flags; 0 leading-tone flags. |
| Fresh notes dependency, before fix | `make -n notes` failed: no rule for `presentation.pdf`. |
| Fresh notes build, after fix | `make notes` exited successfully and generated both slides and presenter notes. Existing layout warnings remain; visual layout was not reviewed. |
| Current thesis build | `make thesis` exited successfully and generated `docs/final-thesis/thesis/main.pdf`, including Biber processing. Visual layout and result claims were not validated. |
| Generation-only dry run | `uv run --offline python research/experiments/scripts/run_experiment.py --dry-run` exited successfully using a temporary writable uv cache. It printed the matrix and wrote metadata; no models were loaded. |
| Thesis generated-source ignore | `git check-ignore -v docs/final-thesis/thesis/main.tex` matched the new rule. |
| Historical lookup probe | Both `main.tex.template` and `00-frontmatter.tex` at `HEAD` resolved to the thesis tree. |
| Coconet-style append timing probe | Requested offsets `[0, 2]` became `[0, 1]` after append, using two one-beat music21 notes. |
| `make -n thesis-slides` | Reported nothing to do; no slide build exists. |
| Documentation checks | All 37 local links/anchors, code fences, documented Make target names, and the supplied editing-pattern word checks passed across four Markdown files. |
| `git diff --check` | Passed. |

Model bootstrap, model downloads, full inference, historical PDF/diff compilation, and visual PDF review were not performed as part of this audit. The passing evaluator checks establish those four cases only.

## v3 preparation and verification

Prepared on 2026-09-28, continuing proposal v2. The researcher reports lecturer review during an in-class, one-to-one tutoring session; the comments themselves are still awaited.

- Added persistent project context, v3 completion gates, feedback record, researcher guide, reading ledger, and a protocol worksheet.
- Moved evaluator, pipeline, experiments, tests, dependency list, bootstrap, and existing local outputs into `research/`. Updated Make and current guides. Root evaluator/pipeline/bootstrap/dependency entry points delegate to the new owner.
- Kept the instrument, tests, adapters, and condition definitions unchanged. This folder move does not resolve the scientific or pipeline findings above.
- Added a final-thesis cover, explicit BAB I–V divisions, and a contents page; reused class/branding assets remain unchanged. Department format requirements are still unconfirmed.
- Corrected verified DeepBach/Fang descriptions, removed unsupported mathematical model summaries and novelty/outcome claims, marked the inherited method as provisional, and replaced speculative abstracts with draft-status summaries. Chapters IV/V explicitly distinguish software checks from missing main results.

Post-move checks completed:

| Check | Result and boundary |
| --- | --- |
| Existing four software checks | Passed; same printed scores and flags as before the move |
| Generation-only dry run | Passed with the current local Python environment; uses `research/outputs/`; no model inference |
| Root pipeline compatibility dry run | Passed; invoked moved tests and condition runner |
| Byte preservation | Evaluator/test/manifest SHA-256 matches before-move copies; all 12 moved source files also match their HEAD contents byte for byte |
| Import and path checks | Root evaluator delegates to the canonical function; all three adapter paths, manifest, setup root, and output root resolve in `research/` |
| Make research recipes | Dry-run points at canonical workspace entry points; `make test` also passed using offline uv and a temporary writable cache |
| Thesis PDF build and rendering | Forced and incremental builds passed through pdfLaTeX/Biber; 31 rendered pages reviewed at overview scale, with cover, approval, contents, and preliminary result table inspected individually; no overfull boxes or unresolved-reference warnings in the final build |

Full model setup/downloads, generation, instrument repairs/validation, main statistical analysis, historical PDF rebuilds, and final department compliance were not performed in this preparation.

Python syntax, Markdown local file links, bibliography-ledger coverage, proposal-source preservation, generated-file ignore rules, and `git diff --check` passed. The PDF remains a research draft; bibliography source support and department format compliance are still open. Underfull spacing messages remain in the inherited layout.

Front-matter correction requested by the researcher: removed cover draft labeling and restored the pre-v3 approval-page/date and bilingual abstract wording. Readiness commentary remains in the project documentation. The thesis rebuilt successfully after this correction.

The researcher subsequently clarified that versioning carries revision status for the entire thesis. Removed visible draft notices, status headings, and editorial completion instructions from chapters I–V. Progress documentation retains the outstanding tasks. Chapters IV/V use ordinary academic prose limited to the measurements actually available.

## Diff ref support

Added `make diff proposal/v1 head` on 2026-09-28. Tags retain their names; branches, `head`/`HEAD`, and abbreviated/full commit IDs resolve to full commit IDs before loading sources. The diff selects the proposal for `proposal/` tags and otherwise the thesis when available, including nested front matter and chapters IV/V. It uses committed content and excludes working-tree edits. Current metadata and class/logo assets still apply.

Nine regression checks passed with `python3 -m unittest discover -s scripts/tests -v`, covering ref resolution, both proposal layouts, phase selection, nested inputs, working-tree exclusion, missing inputs, failed compilation, and citation/TeX-space rendering. PDF builds passed for `proposal/v1` against `proposal/v2`, `head`, and abbreviated commit `e87d47b`. Existing layout warnings remain; no full visual review was performed. The historical `make proposal <ref>` compiler is unchanged.

Diff filenames now include both resolved refs: `proposal_diff_<ref1>_<ref2>.*`, with tag slashes replaced by underscores and untagged refs represented by full commit IDs. Bibliography files share the pair prefix, and `diff-clean` handles these names. All 13 regression checks passed after this change, including naming, preservation of earlier comparisons, compiler output paths, and cleanup boundaries. Named PDF builds passed for `proposal/v1` against `head` and `proposal/v2`.

## PDF destinations and auxiliary cleanup

All Make PDF builds now use [build_pdf.py](../scripts/build_pdf.py). Current proposal/thesis/slides/notes/Q&A PDFs publish to `scratch/`; saved proposals and diffs keep their version/pair names there. Compilation and historical/diff source staging use temporary directories that are removed afterward. Failed builds retain a named log and preserve any previous successful PDF. This also fixes historical compiler exit handling. Current generated `.tex` entry points stay beside their templates. Direct editor builds retain their existing configuration.

All 16 tooling regression checks passed. Actual builds passed for the five current documents, saved proposal v1/v2, the HEAD diff, and the proposal v1/v2 diff. Presenter notes found the relocated slides. Ran `make aux-clean` to remove legacy auxiliary/staging files while preserving PDFs, then rebuilt proposal v2 and the tag diff: `scratch/` contained PDFs only afterward, and document source folders contained no PDFs, auxiliary files, or build directories. Manuscript/proposal sources and research behavior were unchanged; no visual layout review was performed for these builds.

## Section-based diff rendering

Updated on 2026-09-29. The comparison now aligns existing chapter, section, and subsection headings. Each column flows across pages within a section; synchronization happens at section boundaries. Removed the per-paragraph boxes, dividers, and padding.

Proposal covers expand from the `makeisititle` definition stored at each ref, preserving that version's wording. Front matter retains its text, centered layout, signatures, and font scope. Removed the invented “Judul Proposal”, “Peneliti”, and “Pendaftaran” headings, report title/date, and generic “Caption:” prefix. Chapter wording and caption labels come from the selected template, with independent numbering in each column. Current local metadata and logo assets still apply.

All 24 tooling regression checks passed. `make diff proposal/v1 proposal/v2` and `make diff proposal/v1 head` built successfully. Both final PDFs contain 13 pages; the v1/v2 comparison previously contained 16. Reviewed all pages at overview scale and inspected front matter, highlighted text, tables, and chapter transitions individually. Extracted text contains no invented headings; the final HEAD comparison has no body words crossing the column divider. `git diff --check` passed. Manuscript sources and research behavior were unchanged.

Front-matter alignment correction on 2026-09-29: the first implementation treated the entire front matter as one unit, allowing an abstract heading to remain on the preceding page. The parser now pairs cover, approval, Indonesian abstract, and English abstract separately. It preserves source `\newpage`/`\clearpage` boundaries and chapter page breaks. Headings remain absent when absent from the source; keyword labels identify abstract language without adding visible text. Compact environment wrappers are tokenized separately so a newly added heading can receive a highlight.

All 30 tooling checks passed, including missing/changed headings, a removed abstract, separate language pairing, one-sided page breaks, and duplicate-break suppression. The v1/v2 and v1/HEAD comparisons rebuilt successfully. In the v1/v2 PDF, both ABSTRAK headings are on page 3 at the same vertical coordinate, and both ABSTRACT headings are on page 4 at the same vertical coordinate. Rendered approval and abstract pages were inspected individually. Manuscript sources remain unchanged.

Math and paragraph-layout correction on 2026-09-29: changed display equations now receive a red or green background across the complete formula, preserving AMS alignment, row breaks, font scope, and equation numbering. Supported blocks include `equation`, `multline`, `align`, `alignat`, `flalign`, `gather`, their starred variants, `displaymath`, and `\[...\]`. Unchanged equations retain their original appearance.

The comparison uses A3 landscape with two original A4 text areas. Removed forced ragged alignment and extra microtype processing; source indentation, line spacing, and paragraph settings apply to each version. Text highlights are painted within formatting commands, leaving inter-word spaces available for justification and line breaks. This fixes overflowing highlighted paragraphs under the source's `\emergencystretch=\maxdimen` setting.

All 38 tooling checks passed, including the supplied leading-tone formula, changed/deleted math, nested text formatting, and separate inline-math boxes. Both v1/v2 and v1/HEAD PDFs rebuilt successfully. Inspected both abstract pages and the highlighted formula pages. Extracted Indonesian abstract line wrapping matches the original v2 PDF, and bounding-box checks found no body words overflowing either column in either comparison. Manuscript sources and research behavior remain unchanged.

Connected-highlight correction on 2026-09-29: adjacent changed words now share a background across the full justified space. Breakable rule leaders join the word highlights without boxing the phrase; soft source line breaks connect within a paragraph, while blank lines and unchanged words end the connection. Words and connecting spaces use the current font's strut height and depth. Inline math and citation backgrounds use the same bounds with no horizontal padding.

Parentheses and punctuation remain inside their changed text's background, including `(\textit{orderless NADE})`. Inline-math tokenization retains attached punctuation instead of adding spaces around `($x$)`. All 41 tooling checks passed, covering connected spans, unchanged neighbors, paragraph boundaries, and punctuation around formatted text, math, and citations. Both comparison PDFs rebuilt successfully. A rendered fixture confirms connected normal, bold, italic, and inline-math highlights with colored parentheses; the Indonesian abstract retains its original line wrapping, and both PDFs pass the body-word column-bound checks. Manuscript sources remain unchanged.

Heading-highlight correction on 2026-09-29: matched section, subsection, and subsubsection titles are now compared inside their heading command. Changed wording or formatting receives word highlights without coloring the unchanged title text or generated number. In subsection F.3, only `Music Information Retrieval` is highlighted for the normal-to-italic change; `F.3`, `Evaluasi Otomatis dalam`, and `(MIR)` stay plain.

All 44 tooling checks passed, including the exact F.3 titles, partial title edits with changed body text, starred headings, and optional short titles. Both comparison PDFs rebuilt successfully and passed column-bound checks. Inspected the F.3 heading on page 15 of the v1/v2 PDF and confirmed the highlight covers only the changed phrase. Manuscript sources remain unchanged.

## Phase-aware historical builds

Updated on 2026-09-30. `make proposal <ref>` and `make thesis <ref>` share [compile_version.py](../scripts/compile_version.py). v1–v2 are proposal revisions and v3 onward are thesis revisions. Bare versions (`v2`, `3`) resolve to the tag of their phase; up to three digits count as a version, so longer digit strings remain commit IDs. Untagged refs take the phase of the manuscript they contain: a commit with a thesis template is rejected by `make proposal`, and a commit without one is rejected by `make thesis`. The builder reads that phase's template at the commit, inlines `\input` files recursively while leaving commented inputs alone, and stages the class, bibliography, and images stored beside the class at that commit.

Eight new regression checks cover tag resolution, cross-phase rejection, missing `thesis/v3`, `head` labelling and phase inference, untagged proposal commits, committed-source staging, and unknown refs. All tooling checks passed. Built `make proposal v1` and `make proposal v2` (byte sizes identical to the previous builds) and `make thesis head` (the committed five-chapter draft). `make proposal v3`, `make proposal head`, `make thesis v2`, and `make thesis v3` (no tag yet) exit with the intended messages.

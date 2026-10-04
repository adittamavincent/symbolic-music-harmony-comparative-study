# Protocol worksheet (thesis v3–v4)

Protocol version 2, drafted 2026-10-02; updated the same day after reading Strube (1928) and implementing instrument v2. Protocol version 2.1, 2026-10-04 (thesis v4): settings pinned, quality control and sensitivity analyses completed, pipeline implemented; see [Version 2.1](#version-21-2026-10-04). Status: proposed design, not yet executed and not yet agreed with the supervisor. Machine-readable settings: `research/experiments/protocol_v2.json`. Version 1 (four conditioning levels, three models, clipped Strube Score) is superseded; see [Superseded design](#superseded-design-version-1) at the end. Link decisions to `docs/final-thesis/supervision/feedback.md` when they follow actual feedback.

## Design in one paragraph

The study continues the Bach Doodle analysis of Huang et al. (2019, §6.3). Huang et al. counted parallel fifths and octaves per measure with music21 in 21.8 million Coconet harmonizations and found more of them when the user melody fell outside the training soprano limits (MIDI 60–81, largest leap one octave). This study gives the same soprano melodies to DeepBach and Coconet, varies melody origin (Bach chorale sopranos vs melody exercises from Strube's harmony textbook), and counts five voice-leading violations per measure with a fully automatic instrument. Error categories come from the Yan et al. (2018) rubric; rule wording and exceptions come from Strube. No human graders, listeners, or participants are involved.

| Element | Decision | Source of the choice |
| --- | --- | --- |
| Task | Fixed soprano; model generates alto, tenor, bass | Bach Doodle task (Huang et al. 2019); DeepBach §2.3.2 and Coconet support partial-score completion |
| Models (X1) | DeepBach (official PyTorch repo, pretrained resources), Coconet (Magenta.js, checkpoint `coconet/bach`) | Open, accept a fixed soprano, trained on Bach chorales. NotaGen excluded: its official interface offers period/composer/instrumentation prompts, not a melody to preserve |
| Melody origin (X2) | Bach chorale sopranos (music21 corpus) vs Strube melody exercises | Huang et al. out-of-distribution finding; Yan et al. note that exercise length differs from training pieces |
| Outcome (Y) | Per-measure rates of parallel fifths, parallel octaves/unisons, upper-voice spacing, crossing above the soprano, voice overlap; Yan-weighted penalty index as secondary summary | Huang et al. unit (per measure); Yan et al. rubric categories 3, 9, 10, 11 and weights |
| Reference | Bach's own harmonization of the Bach melodies, measured identically | Huang et al. report Bach rates (0.023 P5, 0.009 P8 per measure) |
| Unit of analysis | Melody; five generations per melody per model are averaged | Avoids treating repeated generations as independent |
| Tests | Wilcoxon signed-rank (model, paired); Mann–Whitney U per model (origin); Holm over five rules per family | Huang et al. used Kruskal–Wallis and Mann–Whitney |

## Decisions and their status

| Decision | Current choice | Status |
| --- | --- | --- |
| Title and questions | Thesis v3 BAB I (2026-10-02) | Drafted; supervisor confirmation pending |
| Strube edition | Original 1928 Oliver Ditson edition (`strube1928`), scanned PDF supplied by the researcher at `references/The Theory and Use of Chords.pdf` (147 PDF pages; at least p. 48 is missing, and pages from the Suspensions chapter onward are scanned as two-page spreads) | Confirmed 2026-10-02 |
| Rule pages | `research/literature/strube-rule-pages.csv`: parallels pp. 9, 12; spacing p. 20; crossing p. 174; overlap pp. 12–13 | Filled 2026-10-02 from the scan (OCR plus page images); researcher to confirm against the print |
| Strube melody inventory | `research/literature/strube-exercise-inventory.csv`: exercises 1–118 (pp. 8–81): 71 given-soprano candidates, 47 given basses; 67–68 (p. 48, missing from the 1928 scan) read from the 2015 translation p. 58 | Filled 2026-10-02; key, meter, length, and typing pending |
| Model identities | DeepBach commit `6d75cb9` (pinned in `protocol_v2.json`); resources archive SHA-256 recorded by `make setup-v2`; Magenta.js `@magenta/music` 1.23.1 with `node-fetch` 2.7.0, checkpoint `coconet/bach` | Pinned 2026-10-04; checksums recorded at setup |
| Sample size | At least 30 melodies per origin group (power analysis below) | Proposed |
| Generations | Five per melody per model; DeepBach 500 iterations, temperature 1.0, 8 parallel updates per voice; Coconet 96 iterations, temperature 0.99 | Proposed; settings pinned 2026-10-04 |
| Instrument version | `research/voice_leading_v2.py` (v2.0) with 20 software checks in `research/tests/test_voice_leading_v2.py`; validation checks 3–5 run on the Bach corpus | Implemented 2026-10-02; textbook fixtures (check 2) pending |
| Shared input/output | `research/harmonization_io.py` (IO version 1.0): MusicXML melody in, four-part MusicXML out, adapters for both models; 27 software checks in `research/tests/test_harmonization_io.py` | Implemented 2026-10-03; model acceptance checked at the pilot |
| Analysis plan | Below; implemented in `research/analysis_v2.py`; freeze before main generation | Proposed; implemented 2026-10-04 |
| Pipeline | `research/experiments/scripts/v2.py` and `make` targets (see `research/README.md`); checked end to end with fake backends (`make dry-run-v2`) | Implemented 2026-10-04; no model run |

## Models

Record for each model: repository URL and commit, weight/checkpoint source URL and SHA-256, runtime versions, effective sampling settings, and the exact constraint mechanism.

- DeepBach: soprano fixed as a positional constraint; key and fermata metadata derived from the melody notation. DeepBach builds a per-voice note vocabulary from its training data (with transpositions); a soprano note outside that vocabulary cannot be encoded, so such melodies are ineligible.
- Coconet: soprano written into the piano roll; the other three voices are infilled. Magenta.js uses MIDI pitches 36–81 (`MIN_PITCH = 36`, `NUM_PITCHES = 46` in `coconet_utils.ts`). Maximum practical sequence length, memory use, and time per generation must be checked at the pilot; the version-2 adapter passes the full melody length (the version-1 adapter's 32 steps were too short).

### Shared input and output (IO version 1.0)

Researcher decision, 2026-10-03: melodies and harmonizations are exchanged as MusicXML, and each model has its own adapter (`research/harmonization_io.py`). MIDI is also written for listening. MusicXML is the shared format because it keeps pitch spelling, fermatas, key and time signatures, pickups, and separate voices; MIDI keeps none of these reliably.

- Input: a one-part MusicXML melody, read with the instrument's own parser (`grid_from_part`), so the models receive the melody the evaluator measures. Ineligible melodies raise a recorded reason (no key or time signature, chord, off-grid duration, outside a model's range or vocabulary).
- Bach sopranos are written from the corpus with `write_chorale_soprano`, which declares the missing time of short measures before export and reads the file back. music21 otherwise fills a short measure with rests; this affected 6 of 345 chorales (5 final measures, 1 encoded rest measure) before the padding was declared.
- Output: a four-part score (Soprano, Alto, Tenor, Bass) with the melody's measures, key, and meter, read back after writing. If the generated soprano sounds the melody's pitch at every step, the melody's own notes replace it (articulation, spelling, fermatas); any other soprano is kept as generated, so quality control rejects it.
- Coconet adapter: soprano notes as instrument 0, plus an explicit infill mask over all steps of alto, tenor, and bass. Without the mask, `infill` also fills soprano rests (`getCompletionMask` in `model.ts`). `infill` returns one-step notes, so a repeated pitch cannot be told from a held note: the parser merges consecutive equal pitches in alto, tenor, and bass. Generated voices therefore have no repeated notes, which removes events from the motion rules. Record this as a model-representation limitation.
- DeepBach adapter: soprano tokens from DeepBach's soprano vocabulary (spelled names; a name missing from the vocabulary or outside the voice range makes the melody ineligible), placeholder rests in the other voices (replaced by `random_init`), and metadata per step: fermata as in DeepBach's `FermataMetadata`, tick counted from the first downbeat so a pickup stays aligned (DeepBach's `TickMetadata` counts from the first step), key from the notated key signature instead of DeepBach's key analyzer. Output tokens START, END, OOR, or a hold at the first step are failures; DeepBach's own `tensor_to_score` prints them as rests.
- Implementation defaults found in the sources: Coconet 96 iterations and temperature 0.99 (`model.ts`); DeepBach 500 pseudo-Gibbs iterations (`deepBach.py`), temperature 1.0 and 8 parallel updates per voice (`generation`). The version-1 runners used 20 (Coconet) and 100 (DeepBach) iterations.
- Software checks: `research/tests/test_harmonization_io.py` (27 checks, no model loaded). Round trip on the music21 chorales: for all 345 four-part chorales on the sixteenth grid, Bach's harmonization rebuilt through the writer gave the same five rule counts and measure count as the original, and passed the soprano check. Whether the models accept the encoded input is checked at the pilot.

### Training membership

- DeepBach (verified from `DatasetManager/music_dataset.py` and `chorale_dataset.py` on the repository master branch, 2026-10-02): the tensor dataset is built by iterating the music21 chorale corpus in order, extracting subsequences with transpositions, then split contiguously without shuffling into 85 % train, 10 % validation, and 5 % evaluation. Chorales at the end of the iteration order are therefore outside the training portion; the chorale at each boundary is partly split. Confirm that the downloaded pretrained resources used this default split. Record, for every Bach melody, whether it falls in the training portion.
- Coconet: the training split of the Magenta.js `coconet/bach` checkpoint is not documented in the sources inspected. Huang et al. state that 382 Bach chorales were in their train and validation sets. Record membership as unknown. The Bach group is described as "the training domain, possibly seen", not as held-out data.

## Melody sets

Eligibility, applied identically to both groups:

1. Single melodic line with notated key and meter.
2. All durations representable on a sixteenth-note grid (no tuplets or shorter values).
3. Every pitch inside both models' soprano input range (DeepBach soprano vocabulary; Coconet 36–81).
4. Length the pilot shows both models can process. Record any melody either model cannot process and why.
5. Bach group only: the chorale has exactly four voices, so Bach's own harmonization can be measured as the reference.

Strube group: inventory every exercise in the consulted edition (page, number, given voice, figured or not, key, mode, meter, length in measures, eligible yes/no, reason). Include all eligible numbered melody exercises from the first melody-harmonization exercises through the Minor Modes chapter (pp. 11–80; exercises 12–108). Exclude given basses (the task fixes the soprano); exclude melody exercises from the Suspensions chapter onward, because they are built around non-chord tones (suspensions, auxiliary tones, anticipations) whose exceptions need chord analysis that the instrument cannot apply (Strube p. 35 says non-chord tones are judged from a different viewpoint); exclude the chorale chapter (pp. 174–179), whose melodies are taken from J. S. Bach. The inventory found 71 candidate melodies in that range, above the 30-melody minimum; exercises 67–68 were read from the 2015 translation (p. 58) and still need checking on p. 48 of the printed 1928 book. Type each eligible melody into MusicXML with key, meter, and printed phrase endings; name files by page and exercise number; check each file against the printed page. Keep photos or scans of the book in the Git-ignored `references/` folder only; do not commit or publish them.

Bach group: soprano parts of the 371 music21 corpus chorales with key, meter, and fermatas. After eligibility filtering, draw a random sample with a recorded seed, of the same size as the Strube group and at least 30.

Melody features computed automatically for the manipulation check: number of measures, highest and lowest pitch, largest leap, mode, meter, and whether the melody lies within Huang et al.'s limits (all pitches MIDI 60–81 and no leap larger than 12 semitones). Textbook melodies may fall inside those limits; if so, report that the two groups differ in origin and other features but not in Huang's range/leap criterion, and interpret question 3 accordingly.

## Generation

- Five generations per melody per model, with the implementation's default sampling settings recorded and held constant. Five is a judgment: it reduces the influence of a single random generation on each melody's value at affordable compute; it does not add independent observations. Record random seeds where the interface supports them; otherwise rely on archived raw outputs for reproducibility.
- Store each run in its own directory with the melody ID, model ID, run index, raw output, effective settings, and status (implemented 2026-10-04 in `research/generation_v2.py`; see Version 2.1).
- Do not regenerate failures silently. A failed attempt is logged with its reason. Analysis uses the valid generations; melodies with fewer than five valid generations are flagged for the sensitivity analysis.

## Instrument version 2

Definitions are the researcher's operationalisation. Each rule must be traced to a Strube page and to the Yan rubric category before coding is frozen.

- Parse four voices (S, A, T, B). Time grid: sixteenth note, matching DeepBach (subdivision 4 per quarter) and Coconet (sixteenth steps); Yan et al. §4.1.2 also used sixteenth-note quantization.
- At every grid step, record the sounding MIDI pitch of each voice, including held notes; rests sound nothing.
- For each voice pair, an event is a grid step where at least one of the two voices starts a new note. Motions are transitions between consecutive events of that pair where both voices sound at both events.
- Parallel fifths (all six pairs): |interval| mod 12 = 7 at both events, the upper voice moves, and both voices move in the same direction. Includes compound fifths.
- Parallel octaves/unisons (all six pairs): |interval| mod 12 = 0 at both events, with the same motion condition. Includes unisons and compound octaves.
- Upper-voice spacing (S–A, A–T): interval greater than 12 semitones at an event. T–B is not checked (Yan category 9 names only S–A and A–T).
- Crossing above the soprano (S–A, S–T, S–B): any other voice sounding above the soprano at an event. Unisons are not crossings. Crossings among alto, tenor, and bass are not counted, because Strube allows occasional crossing "not over the soprano" (p. 174).
- Voice overlap (S–A, A–T, T–B): the lower voice moves above the upper voice's previous pitch, or the upper voice moves below the lower voice's previous pitch (Strube p. 12), while the pair is not crossed at the new event (so one event is not counted twice) and neither voice of the pair moves by step (1–2 semitones), because Strube accepts overlap when one voice moves stepwise (pp. 12–13, Figs. 32–33).
- Strube exceptions not applied because they need harmonic analysis: diminished-to-perfect fifths when passing (pp. 34–35), fifths at a chord repetition (p. 35), retarded fifths produced by a suspension (p. 83). Fifths and octaves reached by contrary motion are not counted (p. 9).
- Rate per rule: count divided by the number of measures in the input melody (a pickup measure counts as one). Also store counts and opportunities (motions or events checked).
- Weighted penalty index: (P5 + P8 + 0.5 × (spacing + crossing + overlap)) / measures, using the Yan rubric weights (1 for the parallel category, 0.5 for categories 9–11).
- Main count includes every occurrence, following Huang et al. Sensitivity count excludes every motion that starts while the soprano holds a fermata note (the whole fermata note, not only the move into the next phrase; audit A06). Non-chord-tone excuses are not applied because they need chord analysis.
- Semitone arithmetic treats 7 semitones as a perfect fifth; a diminished sixth spelled enharmonically is counted as a fifth. MIDI outputs carry no spelling, so this is recorded as a limitation.

Excluded Yan categories and reasons: 1 (doubled chordal seventh), 2 (doubled leading tone), 4 (seventh resolution), 6 (non-stylistic progression), 7 (non-tertian chord) need chord, function, or key interpretation, which carries analyst disagreement and would require human checking. Category 5 (soprano leading-tone resolution) concerns the given soprano, not a generated voice. Category 8 (augmented second) needs pitch spelling, which MIDI does not keep. Covered (hidden) fifths and octaves (Strube p. 12) are not in the Yan rubric.

Known v1 code defects (from `docs/maintenance.md`), kept unchanged in the historical v1 code and not used by the version-2 pipeline, which replaces each of them (instrument v2 grid, IO version 1.0, `generation_v2.py` run directories and attempt log, `run_checks_v2.py` completeness checks): `quantize([0.25])` collapses onsets; fourths are counted as fifth candidates; parallels use shared onsets instead of sounding sonorities; batch evaluation drops `parse_quality`; Coconet MIDI reconstruction uses `append` and shifts offsets; shared output folders mix stale files; adapters hard-code settings and ignore the manifest; incomplete runs report success.

## Validation without human graders

1. Content: each rule linked to a Strube page and a Yan category, with examples and exceptions, frozen before main generation.
2. Textbook cases: Strube's printed examples of correct and incorrect voice leading, typed as test fixtures. The instrument must flag the printed errors and nothing in the correct examples. Add constructed edge cases: rests, held notes, compound intervals, unisons, crossing versus overlap, voices that stop sounding. Report every mismatch.
3. Cross-implementation check: on all 371 corpus chorales, compare the instrument with music21 `VoiceLeadingQuartet` methods (`parallelFifth`, `parallelOctave`/`parallelUnisonOrOctave`, `voiceCrossing`, `voiceOverlap`, all present in music21 9.3.0). Report agreement and explain each class of disagreement.
4. Published figures: compare per-measure P5 and P8 rates on Bach chorales with Huang et al. (0.023 and 0.009). Exact agreement is not expected (data version, fermatas, unison handling, unspecified music21 settings). A large unexplained gap blocks use of the instrument.
5. Reliability: rerunning the same files with the same instrument version must reproduce identical flags (compare output hashes).

### Results of checks 3–5 (2026-10-02)

Run: `uv run python research/experiments/scripts/validate_instrument_v2.py`, instrument v2.0, music21 9.3.0. Outputs: `research/outputs/validation_v2/20261002T065120Z/` and the repeat `20261002T065214Z` (Git-ignored). These are instrument checks on Bach's chorales, not study data.

- Corpus: 371 chorales; 345 evaluated (5,387 measures); 26 excluded (20 with more than four parts, 4 with 32nd-note durations, 2 with grace notes).
- Check 3, cross-implementation: crossing and overlap predicates agreed with music21 on every adjacent-pair motion (962 and 1,559 positives, no disagreements in about 71,000 motions). For parallels, the instrument flagged nothing music21 did not; music21 additionally flagged 53 fifths and 16 octaves, all reached by contrary motion, which Strube does not object to (p. 9).
- Check 4, published figures: Strube-definition rates on Bach were 0.0078 parallel fifths and 0.0030 parallel octaves per measure; with music21's broader definition, 0.0176 and 0.0059. Huang et al. reported 0.023 and 0.009 on 382 chorales. The remaining gap is plausibly due to data version (JSB 382 pieces, including duplicates, quantized without fermatas) and unpublished counting settings; it cannot be resolved without Huang et al.'s code. All values are more than 20 times below the 0.365 fifths per measure that Huang et al. reported for Coconet output, so the instrument separates Bach from model-level rates.
- Other Bach rates (main count): spacing 0.074, crossing above the soprano 0.010, overlap 0.093 per measure; with fermata motions excluded, overlap 0.045 and fifths 0.0061.
- Check 5, reliability: two runs produced identical per-chorale and flag files (SHA-256 `0343e353…` and `7f6d57b5…`).

## Quality control

A harmonization is analysable when it has four separable voices, each voice is monophonic, the soprano equals the input melody in pitch and onset, and all notes lie on the sixteenth grid. Report failures per model and origin group; failure rates are results, not noise. A melody without a valid harmonization from one model is dropped from paired comparisons for that model and recorded.

## Analysis plan (freeze before main generation)

- Aggregate: mean rate per rule over valid generations for each melody × model.
- Question 1 (descriptive): attempts, valid outputs, and failures per cell; median, IQR, mean, SD of each rule rate per model × origin; Bach reference rates on Bach melodies; paired model-minus-Bach differences; melody features and the share of melodies outside Huang's limits.
- Question 2: Wilcoxon signed-rank test, DeepBach vs Coconet, on all melodies with valid outputs from both models; two-sided; matched-pairs rank-biserial effect size; Holm over the five rules.
- Question 3: for each model, Mann–Whitney U, Strube vs Bach melodies; one-sided (Strube greater) for parallel fifths and parallel octaves, two-sided for spacing, crossing, overlap; rank-biserial effect size; Holm over the five rules within each model. Report two-sided p-values alongside the one-sided ones for transparency.
- Secondary: the weighted penalty index, tested the same way outside the Holm families.
- Sensitivity: (a) fermata-excluded counts; (b) DeepBach seen vs unseen Bach melodies; (c) melodies with all five generations valid.
- A non-significant result is not evidence of equivalence.
- Discussion examples: drawn at random (recorded seed) from flagged events; they illustrate context and do not change the data.

### Sample-size rationale

Computed 2026-10-02 with statsmodels (`TTestIndPower`): a two-sample t-test needs 25.5 per group to detect d = 0.8 (Cohen's large effect) at α = 0.05 two-sided with power 0.8. The asymptotic relative efficiency of rank tests to the t-test is at least 0.864 for any continuous distribution (Hodges and Lehmann 1956), so 25.5 / 0.864 = 29.5, rounded to 30 per group. Minimum detectable effects at 0.8 power with this adjustment: n = 15 → d ≈ 1.15; n = 20 → d ≈ 0.98; n = 25 → d ≈ 0.87; n = 30 → d ≈ 0.78. Recomputed 2026-10-04 with SciPy (`analysis_v2.minimum_detectable_d`): 1.15, 0.98, 0.87, and 0.79 for n = 15, 20, 25, 30; the 0.78 above for n = 30 was a rounding slip. For question 2 (paired), about 39 melody pairs detect d_z = 0.5 at α = 0.05; 60 melodies exceed this. Holm correction lowers power for the smaller p-values; report achieved minimum detectable effects with the actual n.

With 30 melodies per group, the plan is 30 × 2 groups × 2 models × 5 = 600 generations.

## Risks and contingencies

| Risk | Check | Contingency |
| --- | --- | --- |
| Strube melody exercises turn out ineligible after typing (range, grid, model limits) | Typing and pilot | 71 candidates give a margin; fewer than 30 eligible: use all and report the minimum detectable effect |
| Rule coverage in Strube | Resolved 2026-10-02 | All five rules found (pp. 9, 12–13, 20, 174); crossing narrowed to crossing above the soprano and overlap given the stepwise exception, per Strube |
| Strube prints few voice-leading examples | Fixture list | Nine printed figures listed in `strube-example-fixtures.csv` (Figs. 21, 22, 30, 32, 33, 76); supplement with constructed edge cases already in the test suite |
| Melody notes outside DeepBach's soprano vocabulary | Pilot | Ineligible; record. Do not transpose, because transposition changes the melody's distance from the training data |
| Coconet length or memory limits | Pilot | Process in fixed segments only if both models can be given identical segments; otherwise record ineligibility |
| 3/4 or other meters behave differently | Pilot | Keep, but report meter as a melody feature |
| Instrument disagrees strongly with Huang's Bach rates | Validation 4 | Trace the cause before the pilot; document instrument changes as a new version |

## Version 2.1 (2026-10-04)

Changes from version 2, made for thesis v4 before any model was run. Instrument definitions (version 2.0) are unchanged.

- **Bach frame.** `music21.corpus.chorales.Iterator()` lists 371 Riemenschneider numbers that point to 350 distinct files; 21 entries repeat a file under a second number. The melody builder (`research/melody_sets.py`) keeps the first entry and marks repeats. Of the 350 files, 23 fail eligibility (19 with more than four parts, 2 with 32nd notes, 2 with grace notes; see `research/outputs/melodies/manifest.csv`) and 9 repeat the soprano of an earlier chorale exactly (same intervals and rhythm in any transposition). The sampling frame is 318 melodies before the DeepBach vocabulary check. Only 1 of the 318 lies outside Huang et al.'s limits (MIDI 60–81, largest leap one octave).
- **Validation checks 3–5 counted repeated files.** The 2026-10-02 run evaluated 345 iterator entries, which are 327 distinct files. Recomputed from `per_chorale.csv` with each file once (5,096 measures): 0.0080 parallel fifths, 0.0031 parallel octaves, 0.073 spacing, 0.0098 crossing, 0.094 overlap per measure (fermata-excluded: 0.0063 fifths, 0.0022 octaves, 0.045 overlap). The differences from the reported figures are in the fourth decimal and do not change the conclusions of checks 3–5.
- **Melody duplicates.** A Bach melody that repeats an earlier chorale's soprano cannot be sampled; a Strube melody that repeats a Bach soprano is marked and excluded (audit A20).
- **Strube typing.** Melodies are typed as text (`research/literature/strube-melodies/`, format in its README) and converted to MusicXML by `research/melody_text.py`, which applies the key signature and measure-scoped accidentals, checks every measure's length, and reads the file back with the evaluator's parser. 71 empty templates were created from the inventory.
- **Preflight.** Before sampling, every eligible melody is encoded for both models without generating (`v2.py preflight`); a melody either model refuses is ineligible.
- **Sample and pilot.** Main sample: every eligible Strube melody plus a Bach sample of the same size, at least 30, drawn with seed 20261004. Pilot: 3 Bach melodies drawn (seed 41004) from outside the main sample and 3 Strube melodies; pilot Strube melodies stay in the main census because the Strube group is a census (decision 10 proposed, pending supervisor agreement).
- **Generation.** Settings as in the decisions table. Each attempt has a deterministic seed derived from root seed 20261004, the model, the melody, and the generation index; DeepBach seeds Python, NumPy, and PyTorch with it. Magenta.js samples without a seed, so Coconet attempts are reproducible only through their archived raw output. Each run lives in `research/outputs/runs/<run-id>/` with `run.json` (protocol snapshot, code revision, environment, model manifest), copied melodies, an append-only `attempts.jsonl`, raw outputs, and four-part MusicXML. Failed attempts are kept; retries only with `--retry-failed`, logged as new attempts. The main stage refuses to run while `protocol_v2.json` has `"frozen": false`.
- **Quality control (audit A07).** Added: output length equals the melody, and every generated voice sounds at least one note. Rests inside a voice remain allowed.
- **Sensitivity analysis d (decision 7, audit A05).** Every source (both models and Bach) is also measured after merging consecutive equal pitches in every voice into one held note, which puts DeepBach's restruck notes and Coconet's unrestruck output on the same sounding representation. The main count is unchanged.
- **Training membership (audit A21).** `research/deepbach_membership.py` repeats DeepBach's example counting per chorale. Sensitivity analysis b runs only if the total equals the length of the tensor dataset shipped with the pretrained resources; otherwise membership stays unknown.
- **Statistics.** Wilcoxon on DeepBach minus Coconet with `zero_method="wilcox"`; an all-zero difference set is reported without a p-value. Effect sizes: matched-pairs rank-biserial (positive = DeepBach higher) and rank-biserial (positive = Strube higher). Holm families: question 2 (five rules), question 3 per model (five rules each); the weighted index is tested outside the families. Minimum detectable effects are reported for the analysed n.
- **Environment.** The research environment moved from Python 3.10 (SciPy 1.15.3, whose compiled module no longer loads on this macOS) to Python 3.12 (SciPy 1.18.1, NumPy 2.5.3, music21 9.3.0, PyTorch 2.14.1); exact versions are in `research/requirements-lock.txt`.

## Superseded design (version 1)

Version 1, inherited from proposal v2 and recorded in Git history before 2026-10-02, compared DeepBach, Coconet, and NotaGen under four conditioning levels (A neutral, B key, C fixed soprano, D fixed soprano and bass), measured parallel fifths, parallel octaves, and soprano leading-tone resolution, and summarised them as `Strube Score = 1 - min(1, (P5 + P8 + LT) / N_soprano_events)`.

It was replaced because: the conditioning levels were not grounded in a prior study and NotaGen's C and D prompts were identical while B did not request C major; NotaGen cannot be given a melody to preserve; the three rules were chosen from existing code rather than from a stated source; the clipped score had no published basis and was misdescribed as a proportion of clean moments; the leading-tone check depended on automatic key detection with a silent fallback; and the researcher decided on 2026-10-02 that testing must not use human graders, which rules out a Yan-style graded design. No main data were collected under version 1. Its code, manifest (`research/experiments/strube_conditions.json`), and tests remain in the repository unchanged until version 2 is implemented; keep them as the historical instrument.

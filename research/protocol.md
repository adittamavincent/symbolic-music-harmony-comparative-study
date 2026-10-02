# v3 protocol worksheet

Protocol version 2, drafted 2026-10-02. Status: proposed design, not yet executed and not yet agreed with the supervisor. Version 1 (four conditioning levels, three models, clipped Strube Score) is superseded; see [Superseded design](#superseded-design-version-1) at the end. Link decisions to `docs/final-thesis/feedback.md` when they follow actual feedback.

## Design in one paragraph

The study continues the Bach Doodle analysis of Huang et al. (2019, §6.3). Huang et al. counted parallel fifths and octaves per measure with music21 in 21.8 million Coconet harmonizations and found more of them when the user melody fell outside the training soprano limits (MIDI 60–81, largest leap one octave). This study gives the same soprano melodies to DeepBach and Coconet, varies melody origin (Bach chorale sopranos vs melody exercises from Strube's harmony textbook), and counts five voice-leading violations per measure with a fully automatic instrument. Error categories come from the Yan et al. (2018) rubric; rule wording and exceptions come from Strube. No human graders, listeners, or participants are involved.

| Element | Decision | Source of the choice |
| --- | --- | --- |
| Task | Fixed soprano; model generates alto, tenor, bass | Bach Doodle task (Huang et al. 2019); DeepBach §2.3.2 and Coconet support partial-score completion |
| Models (X1) | DeepBach (official PyTorch repo, pretrained resources), Coconet (Magenta.js, checkpoint `coconet/bach`) | Open, accept a fixed soprano, trained on Bach chorales. NotaGen excluded: its official interface offers period/composer/instrumentation prompts, not a melody to preserve |
| Melody origin (X2) | Bach chorale sopranos (music21 corpus) vs Strube melody exercises | Huang et al. out-of-distribution finding; Yan et al. note that exercise length differs from training pieces |
| Outcome (Y) | Per-measure rates of parallel fifths, parallel octaves/unisons, upper-voice spacing, voice crossing, voice overlap; Yan-weighted penalty index as secondary summary | Huang et al. unit (per measure); Yan et al. rubric categories 3, 9, 10, 11 and weights |
| Reference | Bach's own harmonization of the Bach melodies, measured identically | Huang et al. report Bach rates (0.023 P5, 0.009 P8 per measure) |
| Unit of analysis | Melody; five generations per melody per model are averaged | Avoids treating repeated generations as independent |
| Tests | Wilcoxon signed-rank (model, paired); Mann–Whitney U per model (origin); Holm over five rules per family | Huang et al. used Kruskal–Wallis and Mann–Whitney |

## Decisions and their status

| Decision | Current choice | Status |
| --- | --- | --- |
| Title and questions | Thesis v3 BAB I (2026-10-02) | Drafted; supervisor confirmation pending |
| Strube edition | Edition actually consulted (likely the 2015 Indonesian translation in the ISI library, *Teori dan Penggunaan Akor (I)*, transl. A. Gathut Bintarto T.) | Pending: researcher confirms edition, volume coverage, and bibliography entry |
| Rule pages | One sheet per rule in `research/literature/strube-rule-pages.csv` | Pending: researcher reads Strube |
| Strube melody inventory | All exercises in `research/literature/strube-exercise-inventory.csv` | Pending: researcher inventories the book |
| Model identities | DeepBach repository commit and resource archive checksum; Magenta.js package version and checkpoint URL | Pending: record at pilot |
| Sample size | At least 30 melodies per origin group (power analysis below) | Proposed |
| Generations | Five per melody per model; default sampling settings of each implementation | Proposed |
| Instrument version | v2 definitions below; code not yet changed | Pending implementation |
| Analysis plan | Below; freeze before main generation | Proposed |

## Models

Record for each model: repository URL and commit, weight/checkpoint source URL and SHA-256, runtime versions, effective sampling settings, and the exact constraint mechanism.

- DeepBach: soprano fixed as a positional constraint; key and fermata metadata derived from the melody notation. DeepBach builds a per-voice note vocabulary from its training data (with transpositions); a soprano note outside that vocabulary cannot be encoded, so such melodies are ineligible.
- Coconet: soprano written into the piano roll; the other three voices are infilled. Magenta.js uses MIDI pitches 36–81 (`MIN_PITCH = 36`, `NUM_PITCHES = 46` in `coconet_utils.ts`). Maximum practical sequence length and memory use must be checked at the pilot; the current adapter defaults to 32 sixteenth steps, which is too short for most melodies.

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

Strube group: inventory every exercise in the consulted edition (page, number, given voice, figured or not, key, mode, meter, length in measures, eligible yes/no, reason). Include all eligible melody exercises. Type each eligible melody into MusicXML with key, meter, and printed phrase endings; name files by page and exercise number; check each file against the printed page. Keep photos or scans of the book in the Git-ignored `references/` folder only; the 2015 translation is under copyright.

Bach group: soprano parts of the 371 music21 corpus chorales with key, meter, and fermatas. After eligibility filtering, draw a random sample with a recorded seed, of the same size as the Strube group and at least 30.

Melody features computed automatically for the manipulation check: number of measures, highest and lowest pitch, largest leap, mode, meter, and whether the melody lies within Huang et al.'s limits (all pitches MIDI 60–81 and no leap larger than 12 semitones). Textbook melodies may fall inside those limits; if so, report that the two groups differ in origin and other features but not in Huang's range/leap criterion, and interpret question 3 accordingly.

## Generation

- Five generations per melody per model, with the implementation's default sampling settings recorded and held constant. Five is a judgment: it reduces the influence of a single random generation on each melody's value at affordable compute; it does not add independent observations. Record random seeds where the interface supports them; otherwise rely on archived raw outputs for reproducibility.
- Store each run in its own directory with the melody ID, model ID, run index, raw output, effective settings, and status.
- Do not regenerate failures silently. A failed attempt is logged with its reason. Analysis uses the valid generations; melodies with fewer than five valid generations are flagged for the sensitivity analysis.

## Instrument version 2

Definitions are the researcher's operationalisation. Each rule must be traced to a Strube page and to the Yan rubric category before coding is frozen.

- Parse four voices (S, A, T, B). Time grid: sixteenth note, matching DeepBach (subdivision 4 per quarter) and Coconet (sixteenth steps); Yan et al. §4.1.2 also used sixteenth-note quantization.
- At every grid step, record the sounding MIDI pitch of each voice, including held notes; rests sound nothing.
- For each voice pair, an event is a grid step where at least one of the two voices starts a new note. Motions are transitions between consecutive events of that pair where both voices sound at both events.
- Parallel fifths (all six pairs): |interval| mod 12 = 7 at both events, the upper voice moves, and both voices move in the same direction. Includes compound fifths.
- Parallel octaves/unisons (all six pairs): |interval| mod 12 = 0 at both events, with the same motion condition. Includes unisons and compound octaves.
- Upper-voice spacing (S–A, A–T): interval greater than 12 semitones at an event. T–B is not checked (Yan category 9 names only S–A and A–T).
- Voice crossing (S–A, A–T, T–B): lower voice above the upper voice at an event. Unisons are not crossings.
- Voice overlap (S–A, A–T, T–B): the lower voice moves above the upper voice's previous pitch, or the upper voice moves below the lower voice's previous pitch, while the pair is not crossed at the new event (so one event is not counted as both crossing and overlap).
- Rate per rule: count divided by the number of measures in the input melody (a pickup measure counts as one). Also store counts and opportunities (motions or events checked).
- Weighted penalty index: (P5 + P8 + 0.5 × (spacing + crossing + overlap)) / measures, using the Yan rubric weights (1 for the parallel category, 0.5 for categories 9–11).
- Main count includes every occurrence, following Huang et al. Sensitivity count excludes motions from a fermata note to the following event. Non-chord-tone excuses are not applied because they need chord analysis.
- Semitone arithmetic treats 7 semitones as a perfect fifth; a diminished sixth spelled enharmonically is counted as a fifth. MIDI outputs carry no spelling, so this is recorded as a limitation.

Excluded Yan categories and reasons: 1 (doubled chordal seventh), 2 (doubled leading tone), 4 (seventh resolution), 6 (non-stylistic progression), 7 (non-tertian chord) need chord, function, or key interpretation, which carries analyst disagreement and would require human checking. Category 5 (soprano leading-tone resolution) concerns the given soprano, not a generated voice. Category 8 (augmented second) needs pitch spelling, which MIDI does not keep.

Known v1 code defects that must be fixed before the pilot (from `docs/maintenance.md`): `quantize([0.25])` collapses onsets; fourths are counted as fifth candidates; parallels use shared onsets instead of sounding sonorities; batch evaluation drops `parse_quality`; Coconet MIDI reconstruction uses `append` and shifts offsets; shared output folders mix stale files; adapters hard-code settings and ignore the manifest; incomplete runs report success.

## Validation without human graders

1. Content: each rule linked to a Strube page and a Yan category, with examples and exceptions, frozen before main generation.
2. Textbook cases: Strube's printed examples of correct and incorrect voice leading, typed as test fixtures. The instrument must flag the printed errors and nothing in the correct examples. Add constructed edge cases: rests, held notes, compound intervals, unisons, crossing versus overlap, voices that stop sounding. Report every mismatch.
3. Cross-implementation check: on all 371 corpus chorales, compare the instrument with music21 `VoiceLeadingQuartet` methods (`parallelFifth`, `parallelOctave`/`parallelUnisonOrOctave`, `voiceCrossing`, `voiceOverlap`, all present in music21 9.3.0). Report agreement and explain each class of disagreement.
4. Published figures: compare per-measure P5 and P8 rates on Bach chorales with Huang et al. (0.023 and 0.009). Exact agreement is not expected (data version, fermatas, unison handling, unspecified music21 settings). A large unexplained gap blocks use of the instrument.
5. Reliability: rerunning the same files with the same instrument version must reproduce identical flags (compare output hashes).

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

Computed 2026-10-02 with statsmodels (`TTestIndPower`): a two-sample t-test needs 25.5 per group to detect d = 0.8 (Cohen's large effect) at α = 0.05 two-sided with power 0.8. The asymptotic relative efficiency of rank tests to the t-test is at least 0.864 for any continuous distribution (Hodges and Lehmann 1956), so 25.5 / 0.864 = 29.5, rounded to 30 per group. Minimum detectable effects at 0.8 power with this adjustment: n = 15 → d ≈ 1.15; n = 20 → d ≈ 0.98; n = 25 → d ≈ 0.87; n = 30 → d ≈ 0.78. For question 2 (paired), about 39 melody pairs detect d_z = 0.5 at α = 0.05; 60 melodies exceed this. Holm correction lowers power for the smaller p-values; report achieved minimum detectable effects with the actual n.

With 30 melodies per group, the plan is 30 × 2 groups × 2 models × 5 = 600 generations.

## Risks and contingencies

| Risk | Check | Contingency |
| --- | --- | --- |
| Strube has few or no melody exercises | Inventory | Fewer than 30: use all and report the minimum detectable effect. Fewer than about 10: method amendment agreed with the supervisor before generation (another harmony textbook's melody exercises), recorded here with reasons |
| A rule (especially overlap) is not stated in Strube | Rule pages | Keep the rule with the Yan rubric as its only source and say so in BAB II/III, or drop it; decide before freezing |
| Strube prints few voice-leading examples | Rule pages | Rely more on constructed edge cases; state the smaller textbook test set |
| Melody notes outside DeepBach's soprano vocabulary | Pilot | Ineligible; record. Do not transpose, because transposition changes the melody's distance from the training data |
| Coconet length or memory limits | Pilot | Process in fixed segments only if both models can be given identical segments; otherwise record ineligibility |
| 3/4 or other meters behave differently | Pilot | Keep, but report meter as a melody feature |
| Instrument disagrees strongly with Huang's Bach rates | Validation 4 | Trace the cause before the pilot; document instrument changes as a new version |

## Superseded design (version 1)

Version 1, inherited from proposal v2 and recorded in Git history before 2026-10-02, compared DeepBach, Coconet, and NotaGen under four conditioning levels (A neutral, B key, C fixed soprano, D fixed soprano and bass), measured parallel fifths, parallel octaves, and soprano leading-tone resolution, and summarised them as `Strube Score = 1 - min(1, (P5 + P8 + LT) / N_soprano_events)`.

It was replaced because: the conditioning levels were not grounded in a prior study and NotaGen's C and D prompts were identical while B did not request C major; NotaGen cannot be given a melody to preserve; the three rules were chosen from existing code rather than from a stated source; the clipped score had no published basis and was misdescribed as a proportion of clean moments; the leading-tone check depended on automatic key detection with a silent fallback; and the researcher decided on 2026-10-02 that testing must not use human graders, which rules out a Yan-style graded design. No main data were collected under version 1. Its code, manifest (`research/experiments/strube_conditions.json`), and tests remain in the repository unchanged until version 2 is implemented; keep them as the historical instrument.

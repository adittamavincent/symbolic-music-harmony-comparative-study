# v3 protocol worksheet

Status: proposed decisions, not an approved or executed protocol. Complete this with the researcher and supervisor before the main experiment. Link decisions to `docs/final-thesis/feedback.md` when they follow actual feedback.

## Research question and comparison

Candidate scope: measure selected voice-leading rule violations in outputs of specified DeepBach, Coconet, and NotaGen checkpoints under documented, supported generation settings.

This is a recommendation for review. A three-model comparison with different training data and interfaces cannot establish that LSTM, CNN, or Transformer architecture caused a difference.

| Decision | What to record | Status |
| --- | --- | --- |
| Final question/title | Exact wording and supervisor agreement | Pending |
| Main comparison | A shared supported task, or separate native-control comparisons | Pending |
| Model identity | Repository commit, checkpoint filename/hash, paper version, training/sampling method | Pending |
| Musical scope | Style, length, time grid, meter, keys/modes, allowed texture, source seed IDs | Pending |
| Conditioning | Exact fixed data and controls; measured constraint preservation | Pending |
| Observation unit | Generated score and any grouping by seed/input; dependency structure | Pending |
| Sample size | Justification, target attempts/usable scores per supported cell, handling unequal success rates | Pending; proposal target was 10 per cell, 120 total |
| Reproducibility | Environment snapshot, hardware, random seed controls and unsupported seed controls | Pending |
| Analysis | Primary outcomes, aggregation, uncertainty, intended tests and multiplicity treatment | Pending |

## Current control mismatch

| Condition | DeepBach / Coconet intent | Current NotaGen metadata | Consequence |
| --- | --- | --- | --- |
| A | Minimal available controls | Classical / Beethoven / Keyboard | Models still have training-style priors; A is not universally unconditioned |
| B | Key metadata or C-major cadence seed | Baroque / Beethoven / Keyboard | Does not specify C major in NotaGen; style changes differ from key constraints |
| C | Fix soprano | Baroque / Bach / Choir SATB | Metadata does not demonstrate preservation of a specific soprano |
| D | Fix soprano and bass | Same as C | Cannot be treated as a distinct NotaGen intervention |

Do not invent an unsupported control or relabel identical settings to manufacture a fourth level. Verify adapters against the selected upstream implementations/checkpoints. Consider a DeepBach/Coconet controlled sub-study plus a separate NotaGen task if a shared task cannot be established. Supervisor agreement is still needed.

## Instrument definition

Record the Strube edition/translation and exact pages/exercises for each retained rule. Write a plain-language rule, a scored example, a counterexample, and exceptions before coding.

Decide how to represent sustained sonorities, rests, ties, repeated notes, asynchronous onsets, compound intervals, spelling, voice crossings, extra/missing parts, and key changes. Four parsed tracks alone do not prove correct SATB assignment or monophony. Automatic global key detection needs a recorded confidence/verification policy; a silent fallback to C is not a musical ground truth.

The current score is `1 - min(1, (P5 + P8 + LT) / N_soprano_events)`. A single timepoint can contribute several flags, and all values below zero are clipped. This is a penalty index, not a fraction of violation-free harmonic moments. Choose and justify the denominator or redesign the metric. Preserve rule-specific counts and eligible opportunities even if a composite score is retained.

The existing quantization uses `[0.25]` as divisors, the fifth test also accepts fourths, parallel checks use shared onsets, and leading-tone checks only flag upward soprano motion to a non-tonic. These choices need musical validation; do not describe them as a complete implementation of Strube.

## Annotation and pilot

Create a small deliberately varied fixture set covering each retained rule and exception. Independently label voice IDs, key/context, event location, eligible opportunity, rule, expected flag, and reason. Ask a tutor to review disputed cases. Keep original labels and record disagreements and resolutions. When model outputs are used as validation examples, label them without seeing the model or condition that produced them (added 2026-09-30 as a researcher-bias control; see thesis III.A *Posisi Peneliti*).

If binary labels and a sufficient reference set are available, compare detector flags with the human labels using false positives/negatives and precision/recall. Explain how examples were chosen. Four passing software checks and one positive Bach score do not establish instrument validity.

Generate a small pilot across every retained model/condition. Check the score and playback against parsed notes, voice mapping, time/duration, actual controls, and exclusion rules. Keep pilot results separate from main data if pilot findings change the protocol. Select examples by a recorded procedure, not by favorable scores.

## Main collection and analysis

Freeze the protocol/instrument before main collection; record any later amendment and affected reruns. Log requested attempts, successful outputs, conversion failures, eligible scores, exclusions, retries, hashes, and reasons. Do not silently replace failed outputs until every cell has ten favorable examples.

Treat repeated generations from one seed as potentially dependent. Count independent inputs separately from generated files. Pooling all four conditions can mix intervention differences with model differences. Prefer separate comparisons within supported conditions and document the scope of any aggregate result.

Begin with eligible sample counts, generation/parse failure rates, rule-specific rates, individual observations, and descriptive summaries. Explain uncertainty and unequal denominators. A Kruskal–Wallis test requires independent observations and does not identify which pairs differ; matched or clustered designs need a suitable analysis. Decide the test, effect-size reporting, follow-up comparisons, and multiple-testing treatment before reading the main results. See [SciPy's test documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html).

For qualitative musicological discussion, retain representative scored excerpts, timestamps/bar numbers, detector flags, and manual interpretation. Listening can reveal a conversion or analytical mistake. A formal listener preference study would require a separate sampling, consent, ethics, and analysis plan; it is not currently part of this protocol.

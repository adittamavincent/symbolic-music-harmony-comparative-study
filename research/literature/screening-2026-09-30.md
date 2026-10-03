# OpenAlex screening, 2026-09-30

Source batch: `research/outputs/openalex/20260930T015029093933Z-batch/` (11 queries, 294 unique records in `combined.csv`). Abstracts and bibliographic metadata for the shortlist were fetched from the OpenAlex works endpoint and saved unchanged in `screening/shortlist_abstracts.json` inside that batch folder.

## Criteria

Screened by title, venue, and year, then by abstract.

1. Topic: symbolic music generation, its evaluation, human use of generative music models, computational harmonic analysis and annotation, or tonal-harmony theory.
2. Year: 2016 or later (last ten years). Older sources already in the manuscript (Schoenberg, Strube, music21) were kept as theory or tool references.
3. Venue: peer-reviewed journal or major conference (ACM Computing Surveys, Expert Systems with Applications, Machine Learning, Neural Computing and Applications, JNMR, TISMIR, Psychological Review, PLoS ONE, Music Theory Online, Frontiers, EURASIP, AAAI, IJCAI, CHI, NAACL, ISMIR). arXiv-only preprints were excluded unless already used for a model paper.
4. Not retracted; abstract available so every cited sentence can be checked against it.

About 70 of the 294 records were off-topic (for example 6G networks, explainable AI, speech emotion). Most music records were excluded for audio-only generation, music cognition or neuroscience without a harmony-evaluation link, or preprint status.

## Included (24 new bibliography keys)

| Key | Used for |
| --- | --- |
| carnovalini2020, civit2022, mycka2025 | Field overview and growth (I.A, II.A.1) |
| Ji2023, le2025, hsiao2021, dong2018 | Symbolic representation and example systems (I.A, II.A.1) |
| ghoshal2026, yin2023 | Architecture comparisons; deep learning did not outperform a Markov method (I.A, II.A.1, III.D) |
| hadjeres2020, araneda2023 | User constraints and score inpainting; evaluation standardisation (I.A, II.A.2, III.D) |
| lerch2025, wu2020, herremans2026 | Evaluation targets and challenges (I.A, II.A.3, III.A) |
| louie2020, suh2021, huang2020contest, zacharakis2021 | Musicians using generative models (I.A, II.A.4) |
| micchi2020, neuwirth2018, moss2019, conditschultz2018, koops2019, mcleod2023, karystinaios2023 | Computational harmonic analysis, annotation subjectivity, exceptions, voice separation (I.A, II.A.5, II.B, III.C) |
| meeus2018, harrison2020consonance | Functional-harmony theory and cultural familiarity (II.B.2) |
| mehta2025, roberts2025 | Western dominance in music-generation data; music + coding as hybrid practice (III.A) |

`ghoshal2026` has Crossref metadata only (no abstract), so it is cited only for what its title states. `wu2020` and `hsiao2021` were already in the bibliography and are now cited from their OpenAlex abstracts.

## Excluded with a reason worth recording

- *Bacher than Bach?* (Leemhuis et al., 2020, CCIS) and *Automatic Stylistic Composition of Bach Chorales with Deep LSTM* (Liang et al., ISMIR 2017): directly relevant, but OpenAlex has no abstract. Add after reading the papers.
- `choi2023` (*Teaching chorale generation model to avoid parallel motions*, CMMR 2023) is in the bibliography but could not be found in OpenAlex or Crossref. Not cited until the paper is located and read.
- JS Fake Chorales (2021), Music Transformer (2018), FIGARO (2022): arXiv records only in this batch.

## Limits

Claims were checked against abstracts, not full texts. Before submission, read each cited paper at the relevant section and record page or section numbers in `docs/final-thesis/records/reading-notes.csv`.

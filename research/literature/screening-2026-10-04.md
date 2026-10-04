# Literature search and citation check, 2026-10-04 (thesis v4)

Purpose: verify every bibliography entry after the peer review (P04: "cek semua citasinya"), find expert theories for the rebuilt landasan teori (P12), find previous studies that evaluate generated chorale harmonizations, and search Indonesian sources (PROGRESS researcher task 3 in v3).

## Searches

| Where | Query or method | Date | Outcome |
| --- | --- | --- | --- |
| OpenAlex batch | `openalex_queries.json` plan revision `2026-10-04-v4`, 27 queries (new: q22–q27) | 2026-10-04 | 679 unique records; `research/outputs/openalex/20261004T103233111814Z-batch/` |
| OpenAlex and Crossref API | Title and DOI lookups for all 61 bibliography entries | 2026-10-04 | Metadata compared field by field; errors listed below |
| Google Scholar (browser) | `Huron "Tone and Voice"`; `"Teaching chorale generation model to avoid parallel motions"`; `Pearce Meredith Wiggins "Motivations and methodologies…"`; `"four-part" harmonization "voice leading" evaluation "parallel fifths" generated chorales` (since 2020) | 2026-10-04 | Open copies of Huron (2001) and Pearce et al. (2002); Choi et al. (2023) located |
| Garuda | `harmonisasi empat suara` (0), `harmoni empat suara` (0), `kaidah harmoni` (0), `kecerdasan buatan musik` (3), `artificial intelligence musik` (11), `musik kecerdasan buatan` (3), `AI musik komposisi` (340, composition studies) | 2026-10-04 | No Indonesian study of four-part harmonization by AI models. Relevant context: Ridhwan and Wisnugraha (2026), Grenek 15(1) |
| ISI Yogyakarta repository (digilib.isi.ac.id simple search) | `kecerdasan buatan`, `artificial intelligence`, `harmonisasi` | 2026-10-04 | No study of AI harmonization; the search engine returns loosely related works |
| Reference chasing | Reference lists of Hadjeres et al. (2017), Choi et al. (2023), Leemhuis et al. (2020) | 2026-10-04 | Ebcioğlu (1988) CHORAL, BachBot (Liang et al. 2017), Allan and Williams (2005) noted; cited only through the papers that discuss them |

## Kept for v4 (new keys)

| Key | Why | Verified against |
| --- | --- | --- |
| `huron2001` | Expert theory explaining why the five rules exist | Full text, journal pagination |
| `briot2020book` | Expert framework for deep-learning music generation | arXiv v4 book draft; chapter page ranges from Crossref |
| `storkey2008` | Definition of dataset shift and covariate shift | Author copy of the MIT Press chapter |
| `pearce2002` | Theory of evaluating composing programs by motivation | Author copy |
| `leemhuis2020` | Soprano-given chorale harmonization judged by expert listeners; voice-leading violations noted | Open-access chapter |
| `ridhwan2026` | Indonesian context: AI in music education | Full PDF |
| `choi2023` (already in the bibliography, now cited) | Suppressing parallels changes other features | Full CMMR paper |
| `harrison2020` (already in the bibliography, now cited) | Computational voice-leading model based on Huron | Abstract |

## Errors found in the bibliography

- `choi2023`: authors were "Eunjeong Choi" and "Hyosung Kim"; the paper lists Eunjin Choi and Hyerin Kim. Pages 186–196 and DOI added.
- `koops2019`: "Haas, Wolfgang" and "Burgoyne, John" corrected to W. Bas de Haas and John Ashley Burgoyne (Crossref).
- `DeBerardinis2022` (not cited in v4): URL pointed to a different TASLP paper; corrected to 10.1109/TASLP.2022.3178203.
- `briot2020` (not cited in v4): arXiv title is "… — A Survey", not "a review".
- Pages added from the proceedings: `hadjeres2017` 1362–1371, `huang2017` 211–218, `huang2019` 793–800, `cuthbert2010` 637–642.

## Dropped from the manuscript

Cited in v3 but checked only against abstracts and not needed for an argument in v4: `Ji2023`, `Retkowski2024`, `araneda2023`, `carnovalini2020`, `dong2018`, `dong2020`, `ghoshal2026`, `hadjeres2020`, `harrison2020consonance`, `herremans2026`, `hsiao2021`, `le2025`, `mcleod2023`, `meeus2018`, `moss2019`, `neuwirth2018`, `schoenberg1954`, `suh2021`, `wu2020`, `yin2023`. They remain in the shared bibliography file for the proposal history but are not printed.

## Considered, not used

Ariza (2009, Computer Music Journal) on Turing tests for generative music: relevant, full text not obtained. Agres, Forth, and Wiggins (2016) and Collins et al. (2015) on evaluating creative and style-modelling systems: overlap with Pearce et al. (2002). Huron (2016, *Voice Leading*, MIT Press): the book version of the same theory; only the 2001 article was read. Phon-Amnuaisuk's rule-based and genetic-algorithm harmonization work: older, not needed for the argument.

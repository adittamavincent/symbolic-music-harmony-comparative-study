# Research log

Keep dated entries. Preserve earlier observations when methods change, and record the reason and affected reruns in a later entry.

## 2026-09-28 — v3 preparation

Recorded by the assistant from this repository session, not a lecturer-review transcript.

- Did: Inspected proposal/thesis sources and research code; verified selected primary sources; moved computational ownership into `research/`; prepared continuing final-thesis v3 documents.
- Found: Local outputs contained dry-run metadata only. Existing checks pass, but timing, score definition, controls, quality exclusions, and run isolation need resolution. NotaGen C/D prompts are identical. The quantization probe collapsed distinct onsets with `[0.25]`.
- Changed and why: Preserved computational behavior during the move. Replaced unsupported outcome claims with explicit draft evidence/status; corrected verified model/evaluation descriptions; added thesis cover/chapter divisions and planning/reading records.
- Next: Obtain the actual lecturer notes and department guide; settle scope and musical definitions with the researcher/tutor; repair and validate the instrument/pipeline before the pilot.

## 2026-10-02 — method reset to a machine-only design

Recorded by the assistant at the researcher's request.

- Did: Re-read Yan et al. (2018) §4 and Huang et al. (2019) §6.3 in the original PDFs; checked DeepBach's dataset split code, Magenta.js Coconet pitch range, music21 9.3.0 voice-leading methods, the When in Rome folder list, and Open Library metadata for Strube (1928). Computed the sample-size rationale with statsmodels.
- Found: Huang et al. define out-of-distribution input as soprano pitches outside MIDI 60–81 or a leap larger than one octave, and used Kruskal–Wallis and Mann–Whitney tests. Yan et al. used sixteenth-note quantization and noted that 4-bar exercises differ in length from training pieces. DeepBach splits its training tensors contiguously (85/10/5) in corpus order without shuffling. The Coconet checkpoint's training split is undocumented. music21 9.3.0 provides `VoiceLeadingQuartet.parallelFifth`, `parallelOctave`, `voiceCrossing`, `voiceOverlap`; the old `theoryAnalyzer` module is absent. Strube's book is not on archive.org.
- Changed and why: The researcher asked for a design traceable to one prior study and for no human evaluation. Rewrote BAB I–III around Huang et al. as the main prior study, with Yan et al. for categories and Strube for rule wording and melodies; changed the title; wrote protocol version 2; added Strube data templates and a defense Q&A file. Research code and the v1 manifest were not changed.
- Next: Read Strube and fill the rule-page template; inventory exercises; type printed examples; get supervisor agreement; implement instrument v2 and run the four validation checks; pilot.

## 2026-10-02 (later) — Strube reading, inventory, instrument v2

Recorded by the assistant at the researcher's request ("benerin semua sampai ready tag v3").

- Did: OCR-ed the supplied 1928 Strube scan (147 pages) and read the rule and exercise pages as images; filled the rule-page, exercise-inventory, and fixture-list CSVs; implemented `research/voice_leading_v2.py` and 20 software checks; ran validation checks 3–5 on the 371 music21 chorales twice; rewrote both abstracts; aligned BAB I–III, protocol, and defense notes with the Strube pages.
- Found: All five rules are stated by Strube, but crossing is allowed "not over the soprano" (p. 174) and overlap is allowed with stepwise motion (pp. 12–13); fifths by contrary motion are "not objectionable" (p. 9). music21's parallel-fifth function also flags contrary-motion fifths (all 69 extra flags on Bach were of that kind). 69 given-soprano exercises in pp. 11–80; p. 48 missing from the scan. Bach rates under Strube definitions: 0.0078 P5, 0.0030 P8 per measure.
- Changed and why: Narrowed crossing to crossing above the soprano and added the stepwise exception to overlap, so that the measured rules follow the cited source. Limited the Strube melody group to exercises before the non-chord-tone chapters, because the instrument cannot apply non-chord-tone exceptions. This is instrument version 2.0; no study data existed under the earlier draft definitions.
- Next: Researcher confirms pages in print, checks p. 48, types melodies and figures; supervisor consultation; adapters and pilot.

## Entry fields for your next session

Record the date and author, then what you did, what you found, what you changed and why, and what to resolve next. Include exact source pages, score/example IDs, run/artifact paths, commands, and any supervisor decision. Distinguish an observation from an interpretation or proposed action.

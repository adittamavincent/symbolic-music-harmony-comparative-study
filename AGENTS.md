# Project context

This repository contains one continuing undergraduate thesis project. The academic manuscript is in Indonesian.

- `proposal/v1` and `proposal/v2` are proposal milestones.
- v2 was reviewed in the course Seminar Musikologi 2 by its lecturers, Bu Suryati and Pak Galih, during an in-class, one-to-one tutoring session, according to the researcher. The researcher's notes are recorded in `docs/final-thesis/supervision/feedback.md` (F01–F12); `docs/final-thesis/supervision/perubahan-v2-ke-v3.md` separates changes that answer those notes from changes the researcher decided.
- Thesis v3 is tagged `thesis/v3` (2026-10-03) and is locked. The active revision is **v4** (working tree), revised after a peer review by a fellow student recorded in `docs/final-thesis/supervision/review-teman-2026-10-04.md` (P01–P17; peer feedback, not lecturer feedback). Do not restart numbering as thesis v1 or call the active work a proposal.
- `docs/final-thesis/thesis/` owns the active manuscript. v4 follows the department's 2026 research proposal outline (Proposal Tugas Akhir Penelitian): BAB I Pendahuluan, BAB II Tinjauan Pustaka dan Landasan Teori, BAB III Metode Penelitian. Results and conclusion chapters are added only after main data exist. The chapters are a working draft, not evidence that the thesis is complete.
- `docs/final-thesis/PROGRESS.md` records current readiness, evidence, and unresolved decisions; dated history goes in `docs/final-thesis/records/research-log.md`. `supervision/feedback.md` records lecturer comments once supplied. `docs/final-thesis/README.md` maps the folder.
- `docs/proposal-phase/` preserves the proposal sources. Leave these unchanged during final-thesis work unless the user requests a proposal edit.
- `research/` owns the evaluator, software tests, generation experiments, model setup, dependencies, and local research outputs. Root Python files are compatibility entry points.
- Run Make commands from the repository root. `make thesis` builds v4 from the working tree. `make proposal v1|v2` and `make thesis v3|head|<commit>` rebuild committed revisions with the current tooling; v1–v2 are proposal revisions and v3 onward are thesis revisions, and each command rejects the other phase. A `thesis/v4` tag should be created only after the v4 sources are committed and reviewed.

# Research and writing rules

Read `docs/final-thesis/study/researcher-guide.md` and `docs/maintenance.md` before changing methods or interpreting results.

Keep software correctness tests distinct from instrument validation, pilot data, main research data, and human listening. Passing tests alone does not validate the instrument or complete the research.

Do not invent lecturer feedback, approvals, measurements, sample counts, statistical significance, literature gaps, or citations. Label planned work and provisional interpretations. Preserve raw data and record exclusions and failed generation attempts.

Changing quantization, voice mapping, rule definitions, denominators, or conditioning changes the research instrument/protocol. Version and explain these changes; retain the old results and regenerate affected analysis. Do not silently substitute new measurements into historical proposal submissions.

Follow the user's no-AI-slop editing instructions: read the complete affected draft, preserve its voice and meaning, make the minimum effective edit, remove filler and unsupported emphasis, and explain changes. Check writing against `docs/final-thesis/eval.md` before delivery.

Do not claim architectural causation from this model comparison (DeepBach and Coconet since protocol version 2, 2026-10-02; three models before). Protocol version 2.1 (2026-10-04) pins settings and seeds; the pipeline is `research/experiments/scripts/v2.py` with Make targets. Do not run model setup, generation, or the pilot unless the researcher asks; `make dry-run-v2` uses fake backends only. Model training data, checkpoints, interfaces, and output formats differ. State what the actual comparison supports.

The current thesis reuses the proposal class for formatting. Department-specific final-thesis formatting and front-matter requirements still need confirmation from the researcher and supervisor.

The researcher explicitly requests no draft labels or project-status commentary in the front matter. Preserve cover, approval-page, and abstract wording unless a specific edit is requested. Track readiness in the project documentation.

Versioning carries revision status. Do not add draft notices, status headings, or instructions to finish sections anywhere in the thesis. Use normal academic headings and supported prose; track incomplete work in PROGRESS.md and protocol.md.

# OpenAlex literature discovery

The tracked search plan is `research/literature/openalex_queries.json`. Review and update its query objects before a literature search; run the whole file with `uv run research/scripts/openalex_search.py --batch`. Use `uv run` for this local Python script and `uvx` for standalone tools such as Ruff. The script reads `OPENALEX_API_KEY` from the environment or the ignored `.env.local`, sends it in an Authorization header, and writes per-query CSV, raw JSONL, a combined deduplicated CSV, and query manifests under ignored `research/outputs/openalex/`. Never print, commit, or put the key in a URL. A keyless search has a smaller daily budget.

Consult https://help.openalex.org/access/agents/ and https://help.openalex.org/api/llm-quick-reference/ when forming new queries. Use the OpenAlex API for discovery and metadata, record exact queries and retrieval dates, and check important records against publisher/DOI pages and full text before adding claims or citations. Do not treat OpenAlex citation counts or a matching title as proof that a source supports a musical or methodological claim. Keep source verification in `docs/final-thesis/records/reading-notes.csv` and the literature search record in the output manifest. Do not silently insert search results into the shared proposal/thesis bibliography.

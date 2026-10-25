# Project context

This repository contains one continuing undergraduate thesis project. The academic manuscript is in Indonesian.

- `proposal/v1` and `proposal/v2` are proposal milestones.
- v2 was reviewed in the course Seminar Musikologi 2 by its lecturers, Bu Suryati and Pak Galih, during an in-class, one-to-one tutoring session, according to the researcher. The researcher's notes are recorded in `docs/final-thesis/supervision/feedback.md` (F01–F12); `docs/final-thesis/supervision/perubahan-v2-ke-v3.md` separates changes that answer those notes from changes the researcher decided.
- Thesis v3, v4 and v5 remain preserved milestones. On 2026-10-21 the researcher requested v6 after reporting Pak Galih's Seminar Musikologi 2 advice to use one model. The active v6 manuscript selects Coconet for its documented parallel-motion problem and fixed-soprano SATB task. It uses a qualitative evaluative case study with contextual score analysis and numerical supporting summaries. This is a researcher-directed revision, not recorded approval of the complete design by the supervisors. MODEL 285 remains a candidate requiring a clear opening bass and final soprano duration; 20 attempts remain a workload plan. Rationale: docs/final-thesis/supervision/rancangan-v6.md. Historical v5 agreement/learning files remain preserved and still describe two models.
- `docs/final-thesis/thesis/` owns the active manuscript. V6 currently contains revised BAB I–III using the inherited department outline. The researcher requested BAB I–IV ready; actual BAB IV results still require verified source, implemented instrument, pilot and real main data. Its reporting plan is docs/final-thesis/study/rancangan-bab-iv-v6.md and record templates are research/experiments/v6/. Do not fabricate results or add an empty/result-status chapter to claim completion. Final-thesis structure remains subject to the department guide.
- `docs/final-thesis/PROGRESS.md` records current readiness, evidence, and unresolved decisions; dated history goes in `docs/final-thesis/records/research-log.md`. `supervision/feedback.md` records lecturer comments once supplied. `docs/final-thesis/README.md` maps the folder.
- `docs/proposal-phase/` preserves the proposal sources. Leave these unchanged during final-thesis work unless the user requests a proposal edit.
- `research/` owns the evaluator, software tests, generation experiments, model setup, dependencies, and local research outputs. Root Python files are compatibility entry points.
- Run Make commands from the repository root. `make thesis` builds the working tree (now v6). `make proposal v1|v2` and `make thesis v3|head|<commit>` rebuild committed revisions with the current tooling; v1–v2 are proposal revisions and v3 onward are thesis revisions, and each command rejects the other phase. Preserve the existing thesis/v5 tag. Create a thesis/v6 tag only after v6 sources are committed and reviewed; a tag is not academic approval.

# Research and writing rules

Read `docs/final-thesis/study/researcher-guide.md` and `docs/maintenance.md` before changing methods or interpreting results.

Keep software correctness tests distinct from instrument validation, pilot data, main research data, and human listening. Passing tests alone does not validate the instrument or complete the research.

Do not invent lecturer feedback, approvals, measurements, sample counts, statistical significance, literature gaps, or citations. Label planned work and provisional interpretations. Preserve raw data and record exclusions and failed generation attempts.

Changing quantization, voice mapping, rule definitions, denominators, or conditioning changes the research instrument/protocol. Version and explain these changes; retain the old results and regenerate affected analysis. Do not silently substitute new measurements into historical proposal submissions.

Follow the user's no-AI-slop editing instructions: read the complete affected draft, preserve its voice and meaning, make the minimum effective edit, remove filler and unsupported emphasis, and explain changes. Check writing against both [.agents/skills/no-ai-slop/eval.md](.agents/skills/no-ai-slop/eval.md) and `docs/final-thesis/eval.md` before delivery.

For writing, editing, or auditing thesis prose, read and apply both local skills: [human-academic-writing](.agents/skills/human-academic-writing/SKILL.md) for evidence, paragraph structure, terminology, and continuity, and [no-ai-slop](.agents/skills/no-ai-slop/SKILL.md) for wording and rhetorical patterns. Preserve necessary definitions, explanations, qualifications, technical terms, quotations, and bibliographic titles when applying stylistic cuts. Human-academic-writing adapts StoryScope's fiction findings to academic decisions; its guidance does not establish human authorship or a replicated research result. Use its source map to distinguish paper findings from local adaptations.

The active research evaluates one Coconet configuration on one fixed-soprano Strube chorale case. It does not compare architectures. Written protocol 5.0 and contextual instrument 3.1 remain plans, not implemented/frozen software; see research/protocol.md. Instrument 3.1 requires every counted opportunity to be reviewed and O=C+A+D+U accounting, plus physical episodes and decision segments. Executable defaults still use historical protocol 3.0/instrument 2.0 with 40 Bach melodies and fermata zones; research/experiments/scripts/v2.py and its Make targets do not implement v6. Preserve all historical protocols/results. Do not run model setup, generation or pilot unless the researcher asks. Fake-backend tests, source probes and old Bach-corpus measurements are not main model data. State conclusions at the actual case/checkpoint/settings/pipeline scope.

The current thesis reuses the proposal class for formatting. Department-specific final-thesis formatting and front-matter requirements still need confirmation from the researcher and supervisor.

The researcher explicitly requests no draft labels or project-status commentary in the front matter. Preserve cover, approval-page, and abstract wording unless a specific edit is requested. Track readiness in the project documentation.

Versioning carries revision status. Do not add draft notices, status headings, or instructions to finish sections anywhere in the thesis. Use normal academic headings and supported prose; track incomplete work in PROGRESS.md and protocol.md.

# OpenAlex literature discovery

The tracked search plan is `research/literature/openalex_queries.json`. Review and update its query objects before a literature search; run the whole file with `uv run research/scripts/openalex_search.py --batch`. Use `uv run` for this local Python script and `uvx` for standalone tools such as Ruff. The script reads `OPENALEX_API_KEY` from the environment or the ignored `.env.local`, sends it in an Authorization header, and writes per-query CSV, raw JSONL, a combined deduplicated CSV, and query manifests under ignored `research/outputs/openalex/`. Never print, commit, or put the key in a URL. A keyless search has a smaller daily budget.

Consult https://help.openalex.org/access/agents/ and https://help.openalex.org/api/llm-quick-reference/ when forming new queries. Use the OpenAlex API for discovery and metadata, record exact queries and retrieval dates, and check important records against publisher/DOI pages and full text before adding claims or citations. Do not treat OpenAlex citation counts or a matching title as proof that a source supports a musical or methodological claim. Keep source verification in `docs/final-thesis/records/reading-notes.csv` and the literature search record in the output manifest. Do not silently insert search results into the shared proposal/thesis bibliography.

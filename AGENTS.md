# Project context

This repository contains one continuing undergraduate thesis project. The academic manuscript is in Indonesian.

- `proposal/v1` and `proposal/v2` are proposal milestones.
- v2 was reviewed by lecturers during an in-class, one-to-one tutoring session, according to the researcher. The actual feedback has not yet been supplied.
- The active revision is **v3**, the final-thesis phase continuing from that proposal. Do not restart numbering as thesis v1 or call the active work proposal v3.
- `docs/final-thesis/thesis/` owns the active manuscript. Its five chapters are a working draft, not evidence that the thesis is complete.
- `docs/final-thesis/PROGRESS.md` records readiness, evidence, and unresolved decisions. `feedback.md` records lecturer comments once supplied.
- `docs/proposal-phase/` preserves the proposal sources. Leave these unchanged during final-thesis work unless the user requests a proposal edit.
- `research/` owns the evaluator, software tests, generation experiments, model setup, dependencies, and local research outputs. Root Python files are compatibility entry points.
- Run Make commands from the repository root. `make thesis` builds v3. A future `thesis/v3` tag identifies a reviewed source snapshot; no such tag has been created yet.

# Research and writing rules

Read `docs/final-thesis/researcher-guide.md` and `docs/maintenance.md` before changing methods or interpreting results.

Keep software correctness tests distinct from instrument validation, pilot data, main research data, and human listening. Passing tests alone does not validate the instrument or complete the research.

Do not invent lecturer feedback, approvals, measurements, sample counts, statistical significance, literature gaps, or citations. Label planned work and provisional interpretations. Preserve raw data and record exclusions and failed generation attempts.

Changing quantization, voice mapping, rule definitions, denominators, or conditioning changes the research instrument/protocol. Version and explain these changes; retain the old results and regenerate affected analysis. Do not silently substitute new measurements into historical proposal submissions.

Follow the user's no-AI-slop editing instructions: read the complete affected draft, preserve its voice and meaning, make the minimum effective edit, remove filler and unsupported emphasis, and explain changes. Check writing against `docs/final-thesis/eval.md` before delivery.

Do not claim architectural causation from this three-model comparison. Model training data, checkpoints, interfaces, and output formats differ. State what the actual comparison supports.

The current thesis reuses the proposal class for formatting. Department-specific final-thesis formatting and front-matter requirements still need confirmation from the researcher and supervisor.

The researcher explicitly requests no draft labels or project-status commentary in the front matter. Preserve cover, approval-page, and abstract wording unless a specific edit is requested. Track readiness in the project documentation.

Versioning carries revision status. Do not add draft notices, status headings, or instructions to finish sections anywhere in the thesis. Use normal academic headings and supported prose; track incomplete work in PROGRESS.md and protocol.md.

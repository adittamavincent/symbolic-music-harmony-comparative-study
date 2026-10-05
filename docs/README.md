# Research documents

The documents are separated by academic phase. Run build commands from the repository root.

| Directory | Sources | Build |
| --- | --- | --- |
| `proposal-phase/proposal/` | Front matter, chapters 1–3, schedule | `make proposal` |
| `proposal-phase/presentation/` | Slides, presenter notes, Q&A templates | `make slides`, `make notes`, `make qna` |
| `proposal-phase/assets/` | Class, logos, bibliography shared by both phases | Included in document builds |
| `final-thesis/thesis/` | Thesis-phase v3 draft, front matter and BAB I–III | `make thesis`, `make thesis <ref>` |

Edit chapters and `.tex.template` files. Make generates top-level `.tex` files from templates and local metadata; generated files are ignored by Git.

`make proposal-phase` builds all four proposal documents. `make final-phase` builds the thesis and the version map (`make map`). Thesis defense slides have not been implemented.

Proposal tags preserve earlier source snapshots. They do not prevent later edits to proposal files or shared assets. Proposal and thesis chapters are independent copies.

See the [main README](../README.md) for setup, metadata, output paths, versioning, and experiments; the [thesis guide](final-thesis/README.md) for chapter ownership; and the [maintenance audit](maintenance.md) for known problems.

The current sequence is proposal v1 → proposal v2 → final thesis v3. For research fundamentals, missing evidence, and lecturer-review actions, start with [the v3 researcher guide](final-thesis/study/researcher-guide.md) and [progress record](final-thesis/PROGRESS.md). Computational research is owned by [research/](../research/README.md).

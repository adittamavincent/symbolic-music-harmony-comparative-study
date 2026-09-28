# Research documents

The documents are separated by academic phase. Run build commands from the repository root.

| Directory | Sources | Build |
| --- | --- | --- |
| `proposal-phase/proposal/` | Front matter, chapters 1–3, schedule | `make proposal` |
| `proposal-phase/presentation/` | Slides, presenter notes, Q&A templates | `make slides`, `make notes`, `make qna` |
| `proposal-phase/assets/` | Class, logos, bibliography shared by both phases | Included in document builds |
| `final-thesis/thesis/` | Front matter and chapters 1–5 | `make thesis` |

Edit chapters and `.tex.template` files. Make generates top-level `.tex` files from templates and local metadata; generated files are ignored by Git.

`make proposal-phase` builds all four proposal documents. `make final-phase` currently builds only the thesis. Thesis defense slides have not been implemented.

Proposal tags preserve earlier source snapshots. They do not prevent later edits to proposal files or shared assets. Proposal and thesis chapters are independent copies.

See the [main README](../README.md) for setup, metadata, output paths, versioning, and experiments; the [thesis guide](final-thesis/README.md) for chapter ownership; and the [maintenance audit](maintenance.md) for known problems.

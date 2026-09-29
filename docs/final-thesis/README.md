# Final thesis v3

v3 continues proposal v2 as the final thesis. Proposal v1/v2 remain in `../proposal-phase/`. The active manuscript follows the department's 2026 research-proposal outline with BAB I–III. Results and conclusions are written after main data exist; main data, analysis, and department format approval remain open.

Start with [the researcher guide](researcher-guide.md), [progress and completion gates](PROGRESS.md), and [lecturer feedback](feedback.md). The [reading ledger](reading-notes.csv) tracks source support and your own reading separately. Research code and the protocol worksheet live in [research/](../../research/README.md).

## Edit the source

| File under `thesis/` | Purpose |
| --- | --- |
| `main.tex.template` | Version, chapter divisions, contents, metadata, formatting |
| `chapters/00-titlepage.tex` | Final-thesis cover |
| `chapters/00-frontmatter.tex` | Approval page and bilingual abstracts |
| `chapters/01-pendahuluan.tex` | Introduction |
| `chapters/02-tinjauan-pustaka.tex` | Tinjauan pustaka, landasan teori, asumsi dan hipotesis |
| `chapters/03-metodologi.tex` | Metode pendekatan, objek/populasi/sampel, pengumpulan data, validitas instrumen, analisis, alur penelitian |

The class, logos, and bibliography remain shared with `../proposal-phase/assets/`. Thesis chapters are independent of proposal chapters. The reused class does not establish compliance with the department's final-thesis guide.

## Build from the repository root

```bash
make thesis
make thesis FORCE=1
make -B thesis
```

The PDF is `scratch/thesis.pdf` from the repository root. Make removes temporary auxiliary files after compiling. Edit the template and chapters; Make can overwrite generated `thesis/main.tex`. `make clean-docs` removes generated entry points, current PDFs, and legacy build files. `make aux-clean` preserves PDFs.

`make final-phase` currently builds only the thesis. Final defense slides are not implemented. No `thesis/v3` tag has been created. Preserve a reviewed milestone using the [root version guide](../../README.md#save-final-thesis-v3) once its source and PDF have been checked.

Use [eval.md](eval.md) to check writing. See [maintenance.md](../maintenance.md) for instrument and tooling issues. Do not fill absent findings with expected outcomes.

# Final thesis v3

v3 continues proposal v2 as the final thesis. Proposal v1/v2 remain in `../proposal-phase/`. The active five-chapter manuscript is a draft; main data, analysis, conclusions, and department format approval remain open.

Start with [the researcher guide](researcher-guide.md), [progress and completion gates](PROGRESS.md), and [lecturer feedback](feedback.md). The [reading ledger](reading-notes.csv) tracks source support and your own reading separately. Research code and the protocol worksheet live in [research/](../../research/README.md).

## Edit the source

| File under `thesis/` | Purpose |
| --- | --- |
| `main.tex.template` | Version, chapter divisions, contents, metadata, formatting |
| `chapters/00-titlepage.tex` | Final-thesis cover |
| `chapters/00-frontmatter.tex` | Approval page and bilingual abstracts |
| `chapters/01-pendahuluan.tex` | Introduction |
| `chapters/02-tinjauan-pustaka.tex` | Literature review and theory |
| `chapters/03-metodologi.tex` | Methodology and operational definitions |
| `chapters/04-hasil-pembahasan.tex` | Instrument-test results and measurement discussion |
| `chapters/05-kesimpulan-saran.tex` | Conclusions from instrument tests and development suggestions |

The class, logos, and bibliography remain shared with `../proposal-phase/assets/`. Thesis chapters are independent of proposal chapters. The reused class does not establish compliance with the department's final-thesis guide.

## Build from the repository root

```bash
make thesis
make thesis FORCE=1
make -B thesis
```

The PDF is `thesis/main.pdf`. Edit the template and chapters; Make can overwrite generated `thesis/main.tex`. `make clean-docs` removes generated entry points, PDFs, and build files.

`make final-phase` currently builds only the thesis. Final defense slides are not implemented. No `thesis/v3` tag has been created. Preserve a reviewed milestone using the [root version guide](../../README.md#save-final-thesis-v3) once its source and PDF have been checked.

Use [eval.md](eval.md) to check writing. See [maintenance.md](../maintenance.md) for instrument and tooling issues. Do not fill absent findings with expected outcomes.

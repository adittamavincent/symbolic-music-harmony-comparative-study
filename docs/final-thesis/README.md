# Thesis draft

This directory contains the five-chapter thesis draft. Results and conclusions still need to be reconciled with verified experiments. There are no `thesis/v*` milestone tags or defense-slide templates yet.

## Edit the source

| File under `thesis/` | Purpose |
| --- | --- |
| `main.tex.template` | Entry point, metadata macros, chapter order, formatting |
| `chapters/00-frontmatter.tex` | Cover, approval pages, preliminary material |
| `chapters/01-pendahuluan.tex` | Introduction |
| `chapters/02-tinjauan-pustaka.tex` | Literature review |
| `chapters/03-metodologi.tex` | Methodology |
| `chapters/04-hasil-pembahasan.tex` | Results and discussion draft |
| `chapters/05-kesimpulan-saran.tex` | Conclusions and suggestions draft |

The class, logos, and references are shared with `../proposal-phase/assets/`. Thesis chapter files are separate from proposal chapters.

## Build from the repository root

```bash
make thesis           # Writes docs/final-thesis/thesis/main.pdf
make thesis FORCE=1   # Forces LaTeX compilation
make -B thesis        # Also forces metadata/template regeneration
```

`make final-phase` currently builds the thesis alone. `make thesis-slides` has no recipe and produces no slides.

Do not edit generated `thesis/main.tex`; Make can overwrite it. `make clean-docs` removes that file, the PDF, and the build directory.

Before tagging a milestone, check the chapter 4 table against test output, replace draft result statements with measured results, and support chapter 5's claims with the completed analysis. The chart inclusion in chapter 4 is currently commented out.

See the [main README](../../README.md#git-versions-and-milestones) for the commit/tag workflow and the [maintenance audit](../maintenance.md) for the evidence behind these draft limitations.

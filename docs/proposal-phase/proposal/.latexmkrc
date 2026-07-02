# Local .latexmkrc for docs/proposal-phase/proposal/
# This allows IDEs (e.g., LaTeX Workshop) to compile main.tex directly
# without needing the TEXINPUTS env var set manually via Makefile.

# Add the shared assets dir (contains isi-proposal.cls, logos, bib, etc.)
# relative to this file's directory (proposal/ -> ../assets/)
ensure_path('TEXINPUTS', '../assets//');

# Mirror the root .latexmkrc settings
$aux_dir = 'build';
$out_dir = '.';
$biber   = 'biber %O %S';

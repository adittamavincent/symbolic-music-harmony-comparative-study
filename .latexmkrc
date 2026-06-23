# This configuration tells latexmk to put all auxiliary files (like .aux, .log, .fls) 
# into a "build" directory to avoid bloating the workspace.
$aux_dir = 'build';

# Ensure the final output (like .pdf) stays in the same directory as the source .tex
$out_dir = '.';

# Tell biber to look for the .bcf file inside the build directory
$biber = 'biber --input-directory %D %O %B';

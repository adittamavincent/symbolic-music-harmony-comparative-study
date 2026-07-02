#!/usr/bin/env python3
import os
import sys
import re
import subprocess
import shutil

# Reuse git helpers
def find_git_path(ref, filename):
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if line.endswith(filename):
            return line
    return None

def get_git_content(ref, path):
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return ""
    return result.stdout

def resolve_git_ref(ref):
    res = subprocess.run(["git", "rev-parse", "--verify", ref], capture_output=True)
    if res.returncode == 0:
        return ref
    if not ref.startswith("proposal/"):
        alt_ref = f"proposal/{ref}"
        res = subprocess.run(["git", "rev-parse", "--verify", alt_ref], capture_output=True)
        if res.returncode == 0:
            return alt_ref
    return ref

def load_env_vars():
    env_path = ".env.local" if os.path.exists(".env.local") else ".env.example"
    defaults = {
        "RESEARCHER_NAME": "[Nama Peneliti]",
        "RESEARCHER_NIM": "[NIM]",
        "INSTITUTION_NAME": "[Institusi]",
        "FACULTY_NAME": "[Fakultas]",
        "DEPARTMENT_NAME": "[Jurusan]",
        "PROGRAM_STUDY": "[Program Studi]",
        "ADVISOR_ACADEMIC": "[Dosen Pembimbing Akademik]",
        "ADVISOR_ACADEMIC_NIP": "[NIP]",
        "ADVISOR_THESIS": "[Dosen Pembimbing Skripsi]",
        "ADVISOR_THESIS_NIP": "[NIP]"
    }
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if v:
                        defaults[k] = v
    return defaults

def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    tag = resolve_git_ref(tag)
    outdir = "scratch"
    os.makedirs(outdir, exist_ok=True)
    
    tag_clean = tag.replace("/", "_")
    
    # Clean old temp files for this tag to ensure clean biber compilation
    for ext in ["aux", "log", "bcf", "bbl", "blg", "run.xml", "pdf", "tex", "fdb_latexmk", "fls"]:
        path = os.path.join(outdir, f"proposal_{tag_clean}.{ext}")
        if os.path.exists(path):
            os.remove(path)
            
    print(f"=== Snapping proposal version: {tag} ===")
    
    # Fetch main.tex.template
    template_path = find_git_path(tag, "main.tex.template")
    if not template_path:
        print(f"Error: main.tex.template not found in revision {tag}")
        sys.exit(1)
        
    template_content = get_git_content(tag, template_path)
    
    # Substitute environment variables in template
    env_vars = load_env_vars()
    for k, v in env_vars.items():
        template_content = template_content.replace(f"${{{k}}}", v)
        
    # Replace references.bib path from assets relative to scratch
    template_content = template_content.replace("../assets/references.bib", "references.bib")
        
    # Replace inputs with actual chapter contents
    filenames = {
        "chapters/00-frontmatter": "00-frontmatter.tex",
        "chapters/01-pendahuluan": "01-pendahuluan.tex",
        "chapters/02-tinjauan-pustaka": "02-tinjauan-pustaka.tex",
        "chapters/03-metodologi": "03-metodologi.tex",
        "chapters/04-jadwal": "04-jadwal.tex",
    }
    
    for inp_name, fname in filenames.items():
        path = find_git_path(tag, fname)
        if path:
            content = get_git_content(tag, path)
            content = re.sub(r'(?<!\\)%.*', '', content)  # strip comments
            
            # Simple string replacements to avoid re.sub replacement escape errors
            template_content = template_content.replace(f"\\input{{{inp_name}}}", content)
            template_content = template_content.replace(f"\\input{{{inp_name}.tex}}", content)
            
    # Fetch assets
    cls_path = find_git_path(tag, "isi-proposal.cls")
    cls_content = get_git_content(tag, cls_path) if cls_path else ""
    with open(os.path.join(outdir, "isi-proposal.cls"), "w") as f:
        f.write(cls_content)
        
    bib_path = find_git_path(tag, "references.bib")
    bib_content = get_git_content(tag, bib_path) if bib_path else ""
    with open(os.path.join(outdir, "references.bib"), "w") as f:
        f.write(bib_content)
        
    # Find logo locally
    local_logo_path = None
    for root, dirs, files in os.walk("."):
        if "logo-isi.png" in files:
            local_logo_path = os.path.join(root, "logo-isi.png")
            break
    if local_logo_path:
        shutil.copy(local_logo_path, os.path.join(outdir, "logo-isi.png"))
        
    tex_path = os.path.join(outdir, f"proposal_{tag_clean}.tex")
    with open(tex_path, "w") as f:
        f.write(template_content)
        
    print("=== Compiling PDF ===")
    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode",
         "-e", f"$aux_dir='{outdir}';$out_dir='{outdir}'",
         tex_path],
        capture_output=True, text=True
    )
    
    pdf_path = os.path.join(outdir, f"proposal_{tag_clean}.pdf")
    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"=== Done: {pdf_path} ({size} bytes) ===")
    else:
        print(f"PDF not generated -- check {outdir}/proposal_{tag_clean}.log")
        sys.exit(1)

if __name__ == "__main__":
    main()

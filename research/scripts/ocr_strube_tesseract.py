"""Produce a second, page-complete OCR view of the local Strube scan previews."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "references" / "ocr"


def main():
    models = ROOT / "tessdata"
    models.mkdir(exist_ok=True)
    model_records = []
    for language in ("eng", "ind"):
        url = f"https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/{language}.traineddata"
        destination = models / f"{language}.traineddata"
        if not destination.exists():
            print(f"Downloading {language} model", flush=True)
            temporary = destination.with_suffix(".download")
            with urllib.request.urlopen(url, timeout=120) as response:
                temporary.write_bytes(response.read())
            temporary.replace(destination)
        model_records.append({"language": language, "url": url,
                              "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()})
    version = subprocess.check_output(["tesseract", "--version"], text=True).splitlines()[0]
    env = {**os.environ, "OMP_THREAD_LIMIT": "1"}

    def convert(item):
        book, image = item
        output = ROOT / book / "tesseract" / image.stem
        output.parent.mkdir(exist_ok=True)
        if output.with_suffix(".txt").exists() and output.with_suffix(".tsv").exists():
            return book, int(image.stem), "cached"
        result = subprocess.run([
            "tesseract", str(image), str(output), "--tessdata-dir", str(models),
            "-l", "eng" if book == "english" else "ind+eng", "--oem", "1",
            "--psm", "3", "-c", "tessedit_create_txt=1",
            "-c", "tessedit_create_tsv=1",
        ], capture_output=True, text=True, env=env, timeout=300)
        if result.returncode:
            output.with_suffix(".error.txt").write_text(result.stderr)
            raise RuntimeError(f"Tesseract failed: {book} {image.stem}: {result.stderr}")
        for suffix in (".txt", ".tsv"):
            if not output.with_suffix(suffix).is_file():
                raise RuntimeError(f"Missing Tesseract output: {output}{suffix}")
        return book, int(image.stem), "done"

    items = [(book, image) for book in ("english", "indonesian")
             for image in sorted((ROOT / book / "source-pages").glob("*.jpg"))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for count, result in enumerate(pool.map(convert, items), 1):
            print(f"{count}/{len(items)} {result}", flush=True)
    manifests = []
    for book, expected in (("english", 147), ("indonesian", 91)):
        directory = ROOT / book
        sections, pages = [], []
        for number in range(1, expected + 1):
            text = (directory / "tesseract" / f"{number:03}.txt").read_text()
            pages.append({"pdf_page": number, "characters": len(text.strip())})
            sections.append(f"<!-- page {number} -->\n\nPDF page {number}\n\n{text.strip()}")
        (directory / "transcript-tesseract.txt").write_text("\n\n".join(sections) + "\n")
        manifest = {"book": book, "processor": version, "psm": 3, "oem": 1,
                    "languages": "eng" if book == "english" else "ind+eng",
                    "models": model_records, "pages": pages,
                    "processed_pages": len(pages), "expected_pdf_pages": expected,
                    "purpose": "Independent OCR view; includes noise from staff notation"}
        (directory / "tesseract-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        manifests.append(manifest)
    print("FINISHED: independent OCR for all scan pages", flush=True)


if __name__ == "__main__":
    main()

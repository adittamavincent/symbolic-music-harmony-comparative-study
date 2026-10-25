"""OCR the supplied Strube scans using the installed digester, with page checkpoints.

Run with the digester's ocr/.venv/bin/python. Outputs stay in ignored references/ocr.
This extracts document text; it does not perform optical music recognition.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOKS = {
    "english": "The Theory and Use of Chords.pdf",
    "indonesian": "teori dan penggunaan akor - terjemahan pak gathut.pdf",
}


def save_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def source_info(path):
    info = subprocess.check_output(["pdfinfo", str(path)], text=True)
    return {
        "source": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "pdf_pages": int(re.search(r"^Pages:\s+(\d+)", info, re.M)[1]),
    }


def assemble(directory, metadata):
    sections, records, missing = [], [], []
    for number in range(1, metadata["pdf_pages"] + 1):
        raw = directory / "pages" / f"{number:03d}" / "result.json"
        if not raw.exists():
            missing.append(number)
            continue
        result = json.loads(raw.read_text())
        text = re.sub(r"<!-- page \d+ -->\s*", "", result["markdown"])
        extra_images = []
        for figure in result.get("figures", []):
            figure_path = Path(figure["path"])
            marker = f"_[Figure {figure['number']} on page {figure['page']}]_"
            replacement = (
                f"![Source figure {figure['number']}, PDF page {number}]"
                f"({figure_path.relative_to(directory).as_posix()})"
            )
            if marker in text:
                text = text.replace(marker, replacement)
            else:
                extra_images.append(replacement)
        if extra_images:
            text += "\n\n### Additional extracted image blocks\n\n" + "\n\n".join(extra_images)
        # HTML alignment wrappers prevent Markdown figure links from rendering.
        text = re.sub(r"</?div\b[^>]*>", "", text)
        scan = directory / "source-pages" / f"{number:03d}.jpg"
        source_link = (
            f"[Source scan](source-pages/{number:03d}.jpg)\n\n" if scan.exists() else ""
        )
        alternative = directory / "tesseract" / f"{number:03d}.txt"
        if alternative.exists():
            source_link += f"[Alternative OCR text](tesseract/{number:03d}.txt)\n\n"
        sections.append(f"<!-- page {number} -->\n\n## PDF page {number}\n\n"
                        f"{source_link}{text.strip()}")
        records.append({
            "pdf_page": number,
            "characters": len(text.strip()),
            "figures": len(result.get("figures", [])),
            "blank": bool(result["metadata"].get("blank_pages")),
            "metadata": result["metadata"],
            "raw": raw.relative_to(directory).as_posix(),
        })
    header = (
        f"# Strube - {metadata['language']} OCR\n\n"
        f"Source: `{Path(metadata['source']).name}`\n\n"
        "Machine OCR using PaddleOCR-VL-1.6 and the local MLX backend. "
        "Page labels below are PDF page numbers, not printed book numbers. "
        "Notation examples are preserved as source images where detected; "
        "recognized notation text is not a verified transcription of notes. "
        "Check quotations and musical symbols against the scan.\n\n"
    )
    (directory / "transcript.md").write_text(header + "\n\n".join(sections) + "\n")
    plain = "\n\n".join(sections)
    plain = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"[\1: \2]", plain)
    plain = re.sub(r"^#+\s+", "", plain, flags=re.M)
    (directory / "transcript.txt").write_text(plain + "\n")
    manifest = {**metadata, "processed_pages": len(records), "missing_pdf_pages": missing,
                "complete_pdf_coverage": not missing, "pages": records}
    save_json(directory / "manifest.json", manifest)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", type=Path, default=Path(
        "/Users/vincent/code-repos/projects/whatsapp-llm-digester"))
    parser.add_argument("--pages", help="Sample pages, e.g. english:51,indonesian:30")
    args = parser.parse_args()
    sys.path.insert(0, str(args.tool.resolve()))
    import launch
    from ocr import convert as engine

    original_options = engine.pipeline_options

    def book_options(endpoint):
        options = original_options(endpoint)
        # Staff notation is preserved as images, not interpreted as document text.
        options["use_ocr_for_image_block"] = False
        # Binding rings and library stamps are source images, not prose.
        options["use_seal_recognition"] = False
        options["use_chart_recognition"] = False
        return options

    engine.pipeline_options = book_options
    original_collect = engine.collect_pages

    def collect_with_labels(results, assets):
        results = list(results)
        result = original_collect(results, assets)
        result["metadata"]["block_labels"] = [
            getattr(block, "label", "unknown") for page in results
            for block in page.get("parsing_res_list", [])
        ]
        result["metadata"]["ocr_for_image_block"] = False
        result["metadata"]["seal_recognition"] = False
        result["metadata"]["chart_recognition"] = False
        return result

    engine.collect_pages = collect_with_labels

    def convert_page(page_pdf, raw, scan):
        from PIL import Image

        if not scan.exists():
            engine.convert_source(pipeline, page_pdf, raw, endpoint)
            return None
        with Image.open(scan) as image:
            if image.width <= image.height:
                engine.convert_source(pipeline, page_pdf, raw, endpoint)
                return None
            # Exclude only the central binding gutter; retain the original full scan.
            middle, margin = image.width // 2, round(image.width * 0.025)
            boxes = {"left": (0, 0, middle - margin, image.height),
                     "right": (middle + margin, 0, image.width, image.height)}
            parts = []
            for side, box in boxes.items():
                part_directory = raw.parent / side
                part_directory.mkdir(exist_ok=True)
                crop = part_directory / "source-crop.png"
                image.crop(box).save(crop)
                part_raw = part_directory / "result.json"
                engine.convert_source(pipeline, crop, part_raw, endpoint)
                parts.append((side, json.loads(part_raw.read_text())))
        merged = {"markdown": "", "figures": [], "metadata": dict(parts[0][1]["metadata"])}
        texts = []
        for side, part in parts:
            offset = len(merged["figures"])
            text = re.sub(r"_\[Figure (\d+) on page (\d+)\]_",
                          lambda m: f"_[Figure {int(m[1]) + offset} on page 1]_",
                          part["markdown"])
            text = re.sub(r"<!-- page \d+ -->\s*", "", text)
            texts.append(f"### {side.capitalize()} side of source scan\n\n{text}")
            for figure in part["figures"]:
                merged["figures"].append({**figure, "number": figure["number"] + offset})
        merged["markdown"] = "<!-- page 1 -->\n\n" + "\n\n".join(texts)
        for key in ("tables", "formulas", "charts", "pictures"):
            merged["metadata"][key] = sum(p[1]["metadata"][key] for p in parts)
        merged["metadata"]["block_labels"] = [label for p in parts for label in p[1]["metadata"]["block_labels"]]
        merged["metadata"]["blank_pages"] = "1" if all(p[1]["metadata"]["blank_pages"] for p in parts) else ""
        merged["metadata"]["spread_crops"] = boxes
        merged["metadata"]["source_processing"] = "split-spread-with-central-gutter-excluded"
        save_json(raw, merged)
        return boxes

    selected = {}
    if args.pages:
        for item in args.pages.split(","):
            book, number = item.split(":")
            if book not in BOOKS:
                parser.error(f"Unknown book: {book}")
            selected.setdefault(book, []).append(int(number))
    output = ROOT / "references" / "ocr"
    output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    manifests = []
    with launch.local_server() as endpoint:
        pipeline = engine.build_pipeline(endpoint)
        try:
            for language, name in BOOKS.items():
                if selected and language not in selected:
                    continue
                source = ROOT / "references" / name
                metadata = {**source_info(source), "language": language,
                            "tool": str(args.tool.resolve()),
                            "model": launch.OCR_MODEL,
                            "ocr_for_image_block": False,
                            "seal_recognition": False,
                            "chart_recognition": False,
                            "created_at": dt.datetime.now(dt.timezone.utc).isoformat()}
                directory = output / language
                directory.mkdir(exist_ok=True)
                previous = directory / "manifest.json"
                if previous.exists():
                    old = json.loads(previous.read_text())
                    if old["sha256"] != metadata["sha256"]:
                        raise RuntimeError("Source changed; preserve old OCR in another directory")
                pages = selected.get(language, range(1, metadata["pdf_pages"] + 1))
                for number in pages:
                    if not 1 <= number <= metadata["pdf_pages"]:
                        raise ValueError(f"Page out of range: {number}")
                    page_directory = directory / "pages" / f"{number:03d}"
                    raw = page_directory / "result.json"
                    if raw.exists():
                        json.loads(raw.read_text())
                        print(f"CACHED {language} {number}/{metadata['pdf_pages']}", flush=True)
                        continue
                    page_directory.mkdir(parents=True, exist_ok=True)
                    with tempfile.TemporaryDirectory(prefix="strube-ocr-") as temporary:
                        page_pdf = Path(temporary) / "page.pdf"
                        subprocess.run(["pdfseparate", "-f", str(number), "-l", str(number),
                                        str(source), str(page_pdf)], check=True)
                        print(f"START {language} {number}/{metadata['pdf_pages']}", flush=True)
                        before = time.monotonic()
                        try:
                            spread_boxes = convert_page(page_pdf, raw,
                                directory / "source-pages" / f"{number:03d}.jpg")
                            result = json.loads(raw.read_text())
                            if result["metadata"]["pages"] != 1:
                                raise RuntimeError("Single-page checkpoint returned unexpected page count")
                            save_json(page_directory / "source.json", {
                                "source_sha256": metadata["sha256"], "pdf_page": number,
                                "pipeline_options": book_options(endpoint),
                                "spread_crops": spread_boxes,
                                "seconds": round(time.monotonic() - before, 2)})
                        except Exception as exc:
                            if raw.exists():
                                raw.rename(page_directory / "failed-result.json")
                            save_json(page_directory / "error.json", {"error": str(exc)})
                            print(f"ERROR {language} {number}: {exc}", flush=True)
                            continue
                    manifest = assemble(directory, metadata)
                    print(f"DONE {language} {number}/{metadata['pdf_pages']} "
                          f"({round(time.monotonic() - before)}s; "
                          f"{manifest['processed_pages']} saved)", flush=True)
                manifest = assemble(directory, metadata)
                manifests.append(manifest)
                print(f"BOOK {language}: {manifest['processed_pages']}/{metadata['pdf_pages']}", flush=True)
        finally:
            del pipeline
    print(f"FINISHED in {round(time.monotonic() - started)} seconds", flush=True)
    if not selected and any(m["missing_pdf_pages"] for m in manifests):
        raise SystemExit("Incomplete OCR; rerun to retry missing pages")


if __name__ == "__main__":
    main()

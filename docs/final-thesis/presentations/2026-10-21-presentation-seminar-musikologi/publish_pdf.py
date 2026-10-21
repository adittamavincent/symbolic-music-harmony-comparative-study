"""Publish the converted slide PDF with document metadata and slide bookmarks."""
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

base = Path(__file__).resolve().parent
root = base.parents[3]
candidate = root / "research/outputs/seminar-2026-10-21/candidate.pdf"
slides = json.loads((base / "slides.json").read_text())
reader = PdfReader(candidate)
assert len(reader.pages) == len(slides) == 9
writer = PdfWriter()
writer.clone_document_from_reader(reader)
writer.root_object.pop(NameObject('/Outlines'), None)
writer.add_metadata({
    "/Title": "21 Oktober 2026 - Presentasi Seminar Musikologi 2",
    "/Author": "Vincent Nuridzati Adittama",
    "/Subject": "Final-thesis v5: evaluasi gerak suara harmonisasi DeepBach dan Coconet menurut Strube",
    "/Keywords": "Strube, DeepBach, Coconet, chorale, gerak suara, Seminar Musikologi 2",
})
for index, slide in enumerate(slides):
    writer.add_outline_item(f"{index + 1:02d}. {slide['title'].replace(chr(10), ' ')}", index)
target = base / "2026-10-21-presentation-seminar-musikologi.pdf"
with target.open("wb") as stream:
    writer.write(stream)
print(target)

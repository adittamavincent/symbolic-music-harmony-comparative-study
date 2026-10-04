"""Melody sets for protocol version 2: the Bach chorale frame and the typed Strube exercises.

Builds one manifest row per melody with its eligibility, the reason when a
melody is excluded, and the features used to describe how far the two groups
differ (BAB III, Pengumpulan Melodi). Model-specific input checks (DeepBach's
soprano vocabulary) run later, in the generation preflight, because they need
the installed model resources.

Bach frame: the soprano of every four-part chorale in the music21 corpus that
lies on the sixteenth-note grid, written to MusicXML and read back. Chorales
whose soprano repeats an earlier chorale's melody exactly (same intervals and
rhythm, any transposition) stay in the manifest but are marked as duplicates
and are not sampled, so one hymn tune is not counted twice.

Strube set: every typed exercise under research/literature/strube-melodies/.
"""

import csv
import hashlib
import random
from dataclasses import asdict, dataclass, field
from itertools import pairwise
from pathlib import Path

from harmonization_io import (
    COCONET_MAX_PITCH,
    COCONET_MIN_PITCH,
    IneligibleMelody,
    write_chorale_soprano,
)
from melody_text import MelodyTextError, parse_fields, text_to_musicxml
from music21 import corpus
from voice_leading_v2 import QualityError, score_grids

RESEARCH = Path(__file__).resolve().parent
STRUBE_TEXT_DIR = RESEARCH / "literature" / "strube-melodies"
INVENTORY = RESEARCH / "literature" / "strube-exercise-inventory.csv"
HUANG_LOW, HUANG_HIGH, HUANG_MAX_LEAP = 60, 81, 12

MANIFEST_FIELDS = (
    "melody_id", "origin", "source", "corpus_index", "text_file", "musicxml_file", "sha256",
    "status", "reason", "duplicate_of", "measures", "steps", "notes", "lowest_midi", "highest_midi",
    "ambitus", "largest_leap", "within_huang_limits", "key_sharps", "key_mode", "meter", "has_pickup",
    "fermatas", "shortest_steps",
)


@dataclass
class MelodyRecord:
    melody_id: str
    origin: str  # "bach" or "strube"
    source: str
    corpus_index: str = ""
    text_file: str = ""
    musicxml_file: str = ""
    sha256: str = ""
    status: str = ""  # eligible, ineligible, duplicate, not_typed, format_error
    reason: str = ""
    duplicate_of: str = ""
    features: dict = field(default_factory=dict)
    signature: tuple = ()

    def row(self):
        data = asdict(self)
        data.pop("features")
        data.pop("signature")
        data.update({name: self.features.get(name, "") for name in MANIFEST_FIELDS if name in self.features})
        return {name: data.get(name, "") for name in MANIFEST_FIELDS}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def melody_features(melody):
    """Features of a Melody (harmonization_io) for the manipulation check."""
    midis = [event.midi for event in melody.notes]
    leaps = [abs(b - a) for a, b in pairwise(midis)]
    largest = max(leaps) if leaps else 0
    first = melody.measures[0]
    return {
        "measures": melody.measure_count,
        "steps": melody.total_steps,
        "notes": len(melody.notes),
        "lowest_midi": min(midis),
        "highest_midi": max(midis),
        "ambitus": max(midis) - min(midis),
        "largest_leap": largest,
        "within_huang_limits": int(min(midis) >= HUANG_LOW and max(midis) <= HUANG_HIGH and largest <= HUANG_MAX_LEAP),
        "key_sharps": first.key_sharps,
        "key_mode": first.key_mode or "",
        "meter": first.time_signature,
        "has_pickup": int(first.padding_left > 0),
        "fermatas": sum(1 for event in melody.notes if event.fermata),
        "shortest_steps": min(event.end - event.start for event in melody.notes),
    }


def melody_signature(melody):
    """Transposition-invariant identity: intervals, durations, and onsets of the notes."""
    first = melody.notes[0]
    return (
        tuple(b.midi - a.midi for a, b in zip(melody.notes, melody.notes[1:])),
        tuple(event.end - event.start for event in melody.notes),
        tuple(event.start - first.start for event in melody.notes),
    )


def _check_common(melody):
    """Eligibility shared by both groups, apart from DeepBach's vocabulary (checked at preflight)."""
    low = min(event.midi for event in melody.notes)
    high = max(event.midi for event in melody.notes)
    if low < COCONET_MIN_PITCH or high > COCONET_MAX_PITCH:
        raise IneligibleMelody(f"outside Coconet pitch range {COCONET_MIN_PITCH}-{COCONET_MAX_PITCH}")


def build_bach_frame(out_dir, limit=None):
    """Write every usable Bach soprano and return MelodyRecords in corpus order."""
    out_dir = Path(out_dir)
    records = []
    seen = {}
    names = list(corpus.chorales.Iterator(returnType="filename"))
    if limit is not None:
        names = names[:limit]
    used_ids = set()
    first_index = {}
    for index, name in enumerate(names):
        melody_id = "bach-" + name.split("/")[-1].replace(".", "_")
        if melody_id in used_ids:
            # The Riemenschneider list repeats some files under a second number (371 entries, 350 files).
            record = MelodyRecord(melody_id=f"{melody_id}-entry{index}", origin="bach",
                                  source=f"music21 corpus {name}", corpus_index=str(index), status="duplicate",
                                  duplicate_of=first_index[name],
                                  reason="same corpus file listed again under another Riemenschneider number")
            records.append(record)
            continue
        used_ids.add(melody_id)
        first_index[name] = melody_id
        record = MelodyRecord(melody_id=melody_id, origin="bach", source=f"music21 corpus {name}",
                              corpus_index=str(index))
        try:
            chorale = corpus.parse(name)
            score_grids(chorale)  # four voices on the sixteenth grid, so the reference can be measured
            xml_path = out_dir / "bach" / f"{melody_id}.musicxml"
            melody = write_chorale_soprano(chorale, xml_path, melody_id)
            _check_common(melody)
        except (QualityError, IneligibleMelody) as error:
            record.status, record.reason = "ineligible", str(error)
            records.append(record)
            continue
        record.musicxml_file = str(xml_path)
        record.sha256 = sha256(xml_path)
        record.features = melody_features(melody)
        record.signature = melody_signature(melody)
        if record.signature in seen:
            record.status, record.duplicate_of = "duplicate", seen[record.signature]
            record.reason = "same melody as an earlier chorale (intervals and rhythm)"
        else:
            record.status = "eligible"
            seen[record.signature] = melody_id
        records.append(record)
    return records


def build_strube_set(out_dir, text_dir=STRUBE_TEXT_DIR):
    """Convert every typed Strube exercise and return MelodyRecords sorted by exercise code."""
    out_dir = Path(out_dir)
    records = []
    for text_path in sorted(Path(text_dir).glob("*.txt")):
        code = text_path.stem
        record = MelodyRecord(melody_id=code, origin="strube", source="", text_file=str(text_path))
        raw = text_path.read_text(encoding="utf-8")
        try:
            fields = parse_fields(raw)
            record.source = fields["sumber"]
            if not fields["nada"].strip():
                record.status, record.reason = "not_typed", "kolom nada belum diisi"
                records.append(record)
                continue
            if fields["kode"] != code:
                raise MelodyTextError(f"kode '{fields['kode']}' berbeda dari nama berkas '{code}'")
            xml_path = out_dir / "strube" / f"{code}.musicxml"
            fields, melody = text_to_musicxml(text_path, xml_path)
            _check_common(melody)
        except MelodyTextError as error:
            record.status, record.reason = "format_error", str(error)
            records.append(record)
            continue
        except IneligibleMelody as error:
            record.status, record.reason = "ineligible", str(error)
            records.append(record)
            continue
        record.musicxml_file = str(xml_path)
        record.sha256 = sha256(xml_path)
        record.features = melody_features(melody)
        record.signature = melody_signature(melody)
        record.status = "eligible"
        records.append(record)
    return records


def mark_cross_duplicates(bach_records, strube_records):
    """Mark Strube melodies that repeat a Bach soprano; they would belong to both groups."""
    bach = {r.signature: r.melody_id for r in bach_records if r.signature}
    for record in strube_records:
        if record.status == "eligible" and record.signature in bach:
            record.status, record.duplicate_of = "duplicate", bach[record.signature]
            record.reason = "same melody as a Bach chorale soprano"


def sample_bach(records, size, seed):
    """Draw `size` eligible, non-duplicate Bach melodies with a recorded seed."""
    pool = sorted(r.melody_id for r in records if r.origin == "bach" and r.status == "eligible")
    if size > len(pool):
        raise ValueError(f"requested {size} Bach melodies but only {len(pool)} are eligible")
    return sorted(random.Random(seed).sample(pool, size))


def write_manifest(records, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(record.row())
    return path


def read_manifest(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def inventory_templates(text_dir=STRUBE_TEXT_DIR, inventory=INVENTORY):
    """Create an empty typing template for every melody candidate that has none yet."""
    from melody_text import template

    text_dir = Path(text_dir)
    text_dir.mkdir(parents=True, exist_ok=True)
    created = []
    with open(inventory, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["given_voice"] != "soprano" or row["eligible"] != "candidate":
                continue
            path = text_dir / f"{row['exercise_code']}.txt"
            if path.exists():
                continue
            pdf_page = row["notes"].replace("PDF page", "").strip() if row["notes"].startswith("PDF page") else ""
            path.write_text(template(row["exercise_code"], row["page"], row["exercise_number"], pdf_page),
                            encoding="utf-8")
            created.append(path)
    return created


def update_inventory(strube_records, inventory=INVENTORY):
    """Fill key, mode, meter, length, shortest value, and fermata columns from typed melodies."""
    by_code = {r.melody_id: r for r in strube_records}
    with open(inventory, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    changed = 0
    for row in rows:
        record = by_code.get(row["exercise_code"])
        if record is None or not record.features:
            continue
        f = record.features
        row["key"] = str(f["key_sharps"])
        row["mode"] = f["key_mode"]
        row["meter"] = f["meter"]
        row["length_measures"] = str(f["measures"])
        row["shortest_value"] = f"{f['shortest_steps']} sixteenth(s)"
        row["has_fermata_or_phrase_marks"] = "yes" if f["fermatas"] else "no"
        row["musicxml_file"] = "strube-melodies/" + Path(record.text_file).name
        changed += 1
    if changed:
        with open(inventory, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    return changed

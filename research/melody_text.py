"""Plain-text typing format for the Strube melody exercises (protocol version 2).

The researcher types each printed melody as a short text file instead of
entering it in notation software. This module turns the text into a one-part
MusicXML file and reads it back with harmonization_io.read_melody, so the file
the models receive is checked by the same parser the evaluator uses.

Format (one field per line; lines starting with # are comments):

    kode: strube1928-ex012
    sumber: Strube 1928, hlm. 17, latihan 12
    kunci: 1           # key signature: number of sharps (+) or flats (-)
    mode: major        # major or minor
    birama: 4/4
    anakan: 0          # pickup length in quarter notes (0 = no pickup)
    nada: G4:1 A4:1 B4:1 C5:1 | B4:2 A4:2 | G4:4!

Each note is PITCH:LENGTH. PITCH is a letter, an optional accidental, and an
octave (C4 is middle C): # sharp, ## double sharp, b flat, bb double flat,
n natural. A letter without an accidental takes the key signature, and an
accidental written in a measure holds for the same letter and octave until the
barline, as in printed notation. LENGTH is in quarter notes (1 crotchet, 2
minim, 0.5 quaver, 1.5 dotted crotchet, 0.25 semiquaver). "r:LENGTH" is a rest.
A trailing "!" marks a fermata; a trailing "~" ties the note to the next note,
which must have the same pitch. "|" is a barline. Every full measure must match
the time signature; the first measure must equal "anakan" when it is not 0,
and the last measure may be shorter.
"""

import re
from fractions import Fraction
from pathlib import Path

from harmonization_io import IneligibleMelody, read_melody
from music21 import expressions, key, meter, note, stream, tie

FIELDS = ("kode", "sumber", "kunci", "mode", "birama", "anakan", "nada")
TOKEN = re.compile(r"^(?P<letter>[A-Ga-g])(?P<acc>##|#|bb|b|n)?(?P<octave>-?\d)$")
ACCIDENTAL_TO_ALTER = {"##": 2, "#": 1, "n": 0, "b": -1, "bb": -2}
SHARP_ORDER = "FCGDAEB"
FLAT_ORDER = "BEADGCF"


class MelodyTextError(ValueError):
    """The typed text breaks the format; the message says where."""


def parse_fields(text):
    fields = {}
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip() if not raw.lstrip().startswith("nada") else raw.strip()
        if raw.lstrip().startswith("#") or not line:
            continue
        if ":" not in line:
            raise MelodyTextError(f"baris {number}: tidak ada tanda ':' ({raw.strip()})")
        name, value = line.split(":", 1)
        name = name.strip().lower()
        if name not in FIELDS:
            raise MelodyTextError(f"baris {number}: kolom '{name}' tidak dikenal")
        if name in fields:
            raise MelodyTextError(f"baris {number}: kolom '{name}' ditulis dua kali")
        fields[name] = value.strip()
    missing = [name for name in FIELDS if name not in fields]
    if missing:
        raise MelodyTextError("kolom belum diisi: " + ", ".join(missing))
    return fields


def key_signature_alters(sharps):
    """Return {letter: alter} implied by a key signature."""
    if not -7 <= sharps <= 7:
        raise MelodyTextError(f"kunci {sharps} di luar -7..7")
    letters = SHARP_ORDER[:sharps] if sharps > 0 else FLAT_ORDER[:-sharps]
    return {letter: (1 if sharps > 0 else -1) for letter in letters}


def _pitch_name(letter, alter, octave):
    accidental = {2: "##", 1: "#", 0: "", -1: "-", -2: "--"}[alter]
    return f"{letter}{accidental}{octave}"


def _length(text, where):
    try:
        value = Fraction(text)
    except (ValueError, ZeroDivisionError):
        raise MelodyTextError(f"{where}: durasi '{text}' bukan angka") from None
    if value <= 0:
        raise MelodyTextError(f"{where}: durasi harus lebih dari 0")
    return value


def parse_notes(text, sharps):
    """Return measures as lists of (pitch_name or None, length, fermata, tie_start)."""
    signature = key_signature_alters(sharps)
    measures = []
    for index, chunk in enumerate(text.split("|"), start=1):
        items = chunk.split()
        if not items:
            if index == len(text.split("|")):
                continue
            raise MelodyTextError(f"birama {index}: kosong")
        held = {}  # (letter, octave) -> alter written earlier in this measure
        current = []
        for position, item in enumerate(items, start=1):
            where = f"birama {index}, nada {position} ('{item}')"
            if ":" not in item:
                raise MelodyTextError(f"{where}: tulis NADA:DURASI")
            name, length_text = item.split(":", 1)
            fermata = "!" in length_text
            tie_start = "~" in length_text
            length = _length(length_text.replace("!", "").replace("~", ""), where)
            if name.lower() == "r":
                if tie_start:
                    raise MelodyTextError(f"{where}: tanda diam tidak dapat diikat")
                current.append((None, length, fermata, False))
                continue
            match = TOKEN.match(name)
            if not match:
                raise MelodyTextError(f"{where}: nada tidak dikenal; contoh yang benar C4, F#4, Bb3, Fn5")
            letter = match["letter"].upper()
            octave = int(match["octave"])
            if match["acc"] is not None:
                alter = ACCIDENTAL_TO_ALTER[match["acc"]]
                held[(letter, octave)] = alter
            else:
                alter = held.get((letter, octave), signature.get(letter, 0))
            current.append((_pitch_name(letter, alter, octave), length, fermata, tie_start))
        measures.append(current)
    if not measures:
        raise MelodyTextError("kolom nada kosong")
    return measures


def build_part(fields):
    """Build a music21 Part from parsed fields, checking measure lengths."""
    try:
        sharps = int(fields["kunci"])
    except ValueError:
        raise MelodyTextError("kunci harus bilangan bulat, misalnya 0, 2, atau -3") from None
    mode = fields["mode"].lower()
    if mode not in ("major", "minor"):
        raise MelodyTextError("mode harus major atau minor")
    try:
        time_signature = meter.TimeSignature(fields["birama"])
    except Exception:  # noqa: BLE001 - music21 raises several exception types for a bad meter
        raise MelodyTextError(f"birama '{fields['birama']}' tidak dikenal") from None
    bar = Fraction(time_signature.barDuration.quarterLength)
    pickup = _length(fields["anakan"], "anakan") if fields["anakan"] not in ("0", "0.0") else Fraction(0)
    measures = parse_notes(fields["nada"], sharps)

    part = stream.Part(id="Soprano")
    pending_tie = None
    for index, items in enumerate(measures):
        total = sum(length for _, length, _, _ in items)
        is_first, is_last = index == 0, index == len(measures) - 1
        number = index if pickup else index + 1
        if is_first and pickup:
            if total != pickup:
                raise MelodyTextError(f"birama anakan berisi {total} ketukan, bukan {pickup}")
        elif total != bar and not (is_last and total < bar):
            raise MelodyTextError(f"birama {index + 1} berisi {total} ketukan, bukan {bar}")
        measure = stream.Measure(number=number)
        if is_first:
            measure.insert(0, time_signature)
            measure.insert(0, key.KeySignature(sharps).asKey(mode))
        for name, length, fermata, tie_start in items:
            element = note.Rest(quarterLength=length) if name is None else note.Note(name, quarterLength=length)
            if pending_tie is not None:
                if name is None or element.pitch.midi != pending_tie.pitch.midi:
                    raise MelodyTextError(f"birama {index + 1}: tanda ~ harus diikuti nada yang sama")
                element.tie = tie.Tie("stop" if not tie_start else "continue")
            if tie_start:
                if name is None:
                    raise MelodyTextError("tanda diam tidak dapat diikat")
                if element.tie is None:
                    element.tie = tie.Tie("start")
            if fermata:
                element.expressions.append(expressions.Fermata())
            measure.append(element)
            pending_tie = element if tie_start else None
        if is_first and pickup:
            measure.paddingLeft = float(bar - total)
        elif is_last and total < bar:
            measure.paddingRight = float(bar - total)
        part.append(measure)
    if pending_tie is not None:
        raise MelodyTextError("nada terakhir memakai ~ tetapi tidak ada nada sesudahnya")
    return part


def text_to_musicxml(text_path, xml_path):
    """Convert one typed melody to MusicXML and return (fields, Melody)."""
    text_path, xml_path = Path(text_path), Path(xml_path)
    fields = parse_fields(text_path.read_text(encoding="utf-8"))
    part = build_part(fields)
    score = stream.Score()
    score.insert(0, part)
    xml_path.parent.mkdir(parents=True, exist_ok=True)
    score.write("musicxml", fp=str(xml_path))
    try:
        melody = read_melody(xml_path, fields["kode"])
    except IneligibleMelody:
        xml_path.unlink(missing_ok=True)
        raise
    return fields, melody


def template(exercise_code, page, exercise_number, pdf_page=""):
    """Empty typing template for one inventory row."""
    return (
        f"# Ketik melodi latihan ini dari cetakan Strube (1928). Petunjuk: research/literature/strube-melodies/README.md\n"
        f"kode: {exercise_code}\n"
        f"sumber: Strube 1928, hlm. {page}, latihan {exercise_number}{f' (PDF hlm. {pdf_page})' if pdf_page else ''}\n"
        "kunci: \n"
        "mode: \n"
        "birama: \n"
        "anakan: 0\n"
        "nada: \n"
    )

"""Shared MusicXML input and output for the generation adapters (protocol version 2).

Every melody enters as a one-part MusicXML file and every harmonization leaves
as a four-part (S, A, T, B) MusicXML score. Each model has an input adapter
that translates the melody into its own encoding and an output parser that
translates its result back. Only those adapters know model formats.

Time is counted in sixteenth-note steps, the grid used by both models and by
the instrument (voice_leading_v2.py). Parsing reuses the instrument's own
grid_from_part, so a melody is read exactly as the evaluator will read it.

Model facts used here, checked against the sources on 2026-10-03:
- Coconet (magenta-js master, music/src/coconet): instrument 0-3 = S, A, T, B;
  pitches 36-81 (MIN_PITCH 36, NUM_PITCHES 46, coconet_utils.ts). infill()
  returns one-step notes, so a repeated pitch cannot be told from a held note;
  without an explicit infill mask it fills every silent step, including rests in
  the given soprano (model.ts, getCompletionMask). Defaults: 96 iterations,
  temperature 0.99.
- DeepBach (Ghadjeres/DeepBach master, commit 6d75cb9): one token per step per
  voice from a per-voice vocabulary of spelled names (nameWithOctave), '__' for
  a held step, 'rest'; pitches outside the voice range become 'OOR'
  (DatasetManager/chorale_dataset.py, helpers.py). Metadata order with the
  pretrained setup: fermata, tick, key (sharps + 8), voice index. deepBach.py
  defaults: 500 pseudo-Gibbs iterations; generation() defaults: temperature 1.0,
  batch_size_per_voice 8.
"""

from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from music21 import clef, converter, expressions, key, meter, note, pitch, stream, tie
from voice_leading_v2 import GRID, QualityError, grid_from_part, score_grids

IO_VERSION = "1.0"
STEPS_PER_QUARTER = 4
VOICE_NAMES = ("Soprano", "Alto", "Tenor", "Bass")

COCONET_MIN_PITCH = 36
COCONET_MAX_PITCH = 81
COCONET_DEFAULTS = {"numIterations": 96, "temperature": 0.99}

DEEPBACH_HOLD = "__"
DEEPBACH_REST = "rest"
DEEPBACH_SPECIAL = ("START", "END", "OOR", "XX")
DEEPBACH_DEFAULTS = {"num_iterations": 500, "temperature": 1.0, "batch_size_per_voice": 8}


class IneligibleMelody(ValueError):
    """The melody cannot be given to the models; the message is the recorded reason."""


class OutputError(QualityError):
    """A model output cannot be turned into a four-voice score; the message is the recorded reason."""


@dataclass(frozen=True)
class Event:
    """One note of a voice: sounding from step `start` up to, not including, `end`."""

    start: int
    end: int
    name: str  # spelled pitch, music21 nameWithOctave
    fermata: bool = False

    @property
    def midi(self):
        return pitch.Pitch(self.name).midi


@dataclass(frozen=True)
class MeasureInfo:
    number: int
    start: int
    length: int
    padding_left: int  # steps missing at the start (pickup)
    padding_right: int  # steps missing at the end (a measure split across a phrase or repeat)
    time_signature: str | None  # ratio string where the measure prints one
    key_sharps: int | None  # where the measure prints a key signature
    key_mode: str | None


@dataclass(frozen=True)
class Melody:
    melody_id: str
    notes: tuple  # Event, in time order; gaps are rests
    measures: tuple  # MeasureInfo

    @property
    def total_steps(self):
        last = self.measures[-1]
        return last.start + last.length

    @property
    def measure_count(self):
        return len(self.measures)

    def key_sharps_at(self, step):
        sharps = None
        for measure in self.measures:
            if measure.start > step:
                break
            if measure.key_sharps is not None:
                sharps = measure.key_sharps
        return sharps


def _steps(quarter_length, what):
    value = Fraction(quarter_length).limit_denominator(1024) / GRID
    if value.denominator != 1:
        raise IneligibleMelody(f"{what} is not on the sixteenth-note grid")
    return int(value)


def _events_from_grid(grid):
    events = []
    t = 0
    while t < len(grid):
        if grid.midi[t] is None:
            t += 1
            continue
        end = t + 1
        while end < len(grid) and grid.midi[end] == grid.midi[t] and not grid.onset[end]:
            end += 1
        events.append(Event(t, end, grid.pitch[t].nameWithOctave, grid.fermata[t]))
        t = end
    return events


def _measure_map(part):
    measures = list(part.getElementsByClass(stream.Measure))
    if not measures:
        raise IneligibleMelody("the melody has no measures")
    end = _steps(part.highestTime, "the melody end")
    infos = []
    for index, measure in enumerate(measures):
        start = _steps(measure.offset, f"measure {measure.number}")
        stop = _steps(measures[index + 1].offset, "a barline") if index + 1 < len(measures) else end
        ts = measure.timeSignature
        ks = measure.keySignature
        infos.append(MeasureInfo(
            number=measure.number,
            start=start,
            length=stop - start,
            padding_left=_steps(measure.paddingLeft, f"pickup of measure {measure.number}"),
            padding_right=_steps(measure.paddingRight, f"end of measure {measure.number}"),
            time_signature=ts.ratioString if ts is not None else None,
            key_sharps=ks.sharps if ks is not None else None,
            key_mode=getattr(ks, "mode", None) if ks is not None else None,
        ))
    if infos[0].time_signature is None:
        raise IneligibleMelody("no notated time signature in the first measure")
    if infos[0].key_sharps is None:
        raise IneligibleMelody("no notated key signature in the first measure")
    return tuple(infos)


def melody_from_part(part, melody_id):
    """Validate one melodic part and return it as a Melody. Raises IneligibleMelody with the reason."""
    try:
        grid = grid_from_part(part)
    except QualityError as error:
        raise IneligibleMelody(str(error)) from error
    events = _events_from_grid(grid)
    if not events:
        raise IneligibleMelody("the melody has no notes")
    return Melody(melody_id, tuple(events), _measure_map(part))


def read_melody(path, melody_id=None):
    """Read a one-part MusicXML melody file."""
    path = Path(path)
    score = converter.parse(str(path))
    parts = list(score.parts)
    if len(parts) != 1:
        raise IneligibleMelody(f"expected one part, found {len(parts)}")
    return melody_from_part(parts[0], melody_id or path.stem)


def write_chorale_soprano(chorale, path, melody_id=None):
    """Write the soprano of a four-part chorale as a one-part MusicXML file and return its Melody.

    music21 fills an incomplete measure with rests on export unless the measure
    declares its padding, so the missing time of each short measure is declared
    first (as a pickup for the first measure, otherwise at the end). The file is
    read back and compared with the chorale's soprano; if pitches, onsets,
    fermatas, or length differ, the file is removed and the melody is ineligible.
    """
    parts = list(chorale.parts)
    if len(parts) != 4:
        raise IneligibleMelody(f"the chorale has {len(parts)} parts, not 4")
    source = melody_from_part(parts[0], melody_id)
    soprano = deepcopy(parts[0])
    for index, measure in enumerate(soprano.getElementsByClass(stream.Measure)):
        missing = (measure.barDuration.quarterLength - measure.duration.quarterLength
                   - measure.paddingLeft - measure.paddingRight)
        if missing > 0:
            if index == 0:
                measure.paddingLeft += missing
            else:
                measure.paddingRight += missing
    score = stream.Score()
    score.insert(0, soprano)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    score.write("musicxml", fp=str(path))
    written = read_melody(path, source.melody_id or path.stem)
    if written.notes != source.notes or written.total_steps != source.total_steps:
        path.unlink()
        raise IneligibleMelody("MusicXML export changes the soprano's timing or notes")
    return written


# --- Canonical four-voice output ---------------------------------------------------------

def _per_step(events, total):
    midi = [None] * total
    onset = [False] * total
    for event in events:
        if event.start < 0 or event.end > total or event.start >= event.end:
            raise OutputError(f"note at steps {event.start}-{event.end} lies outside the melody length {total}")
        if any(m is not None for m in midi[event.start:event.end]):
            raise OutputError(f"notes overlap within one voice at step {event.start}")
        midi[event.start:event.end] = [event.midi] * (event.end - event.start)
        onset[event.start] = True
    return midi, onset


def _clef_for(voice_index):
    return (clef.TrebleClef(), clef.TrebleClef(), clef.Treble8vbClef(), clef.BassClef())[voice_index]


def _voice_part(voice_index, events, melody):
    name = VOICE_NAMES[voice_index]
    part = stream.Part(id=name)
    part.partName = name
    by_start = sorted(events, key=lambda e: e.start)
    for measure_index, info in enumerate(melody.measures):
        measure = stream.Measure(number=info.number)
        if measure_index == 0:
            measure.insert(0, _clef_for(voice_index))
        if info.key_sharps is not None:
            ks = key.KeySignature(info.key_sharps)
            measure.insert(0, ks.asKey(info.key_mode) if info.key_mode else ks)
        if info.time_signature is not None:
            measure.insert(0, meter.TimeSignature(info.time_signature))
        measure.paddingLeft = info.padding_left / STEPS_PER_QUARTER
        measure.paddingRight = info.padding_right / STEPS_PER_QUARTER
        lo, hi = info.start, info.start + info.length
        cursor = lo
        for event in by_start:
            start, end = max(event.start, lo), min(event.end, hi)
            if start >= end:
                continue
            if start > cursor:
                measure.insert((cursor - lo) / STEPS_PER_QUARTER,
                               note.Rest(quarterLength=(start - cursor) / STEPS_PER_QUARTER))
            n = note.Note(event.name, quarterLength=(end - start) / STEPS_PER_QUARTER)
            if event.start < start and event.end > end:
                n.tie = tie.Tie("continue")
            elif event.start < start:
                n.tie = tie.Tie("stop")
            elif event.end > end:
                n.tie = tie.Tie("start")
            if event.fermata and start == event.start:
                n.expressions.append(expressions.Fermata())
            measure.insert((start - lo) / STEPS_PER_QUARTER, n)
            cursor = end
        if cursor < hi:
            measure.insert((cursor - lo) / STEPS_PER_QUARTER,
                           note.Rest(quarterLength=(hi - cursor) / STEPS_PER_QUARTER))
        part.append(measure)
    return part


def harmonization_score(voices, melody):
    """Build the canonical four-voice score from Events per voice (S, A, T, B).

    When the soprano sounds the melody's pitch at every step, the melody's own
    notes (articulation, spelling, fermatas) replace it, because Coconet output
    cannot distinguish a repeated note from a held one. A soprano that differs
    in any step is kept as generated so that quality control rejects it.
    """
    if len(voices) != 4:
        raise OutputError(f"expected 4 voices, found {len(voices)}")
    total = melody.total_steps
    for events in voices:
        _per_step(events, total)
    soprano_midi, _ = _per_step(voices[0], total)
    melody_midi, _ = _per_step(melody.notes, total)
    if soprano_midi == melody_midi:
        voices = [list(melody.notes)] + list(voices[1:])
    score = stream.Score()
    for index, events in enumerate(voices):
        score.insert(0, _voice_part(index, events, melody))
    return score


def write_score(score, path):
    """Write the score as MusicXML at `path` and as MIDI next to it, for listening.

    The MusicXML file is read back; it must give the same grid as the score in memory.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    xml_path = path.with_suffix(".musicxml")
    score.write("musicxml", fp=str(xml_path))
    expected = score_grids(score)
    found = score_grids(converter.parse(str(xml_path)))
    for a, b in zip(expected, found):
        if (a.midi, a.onset, a.fermata) != (b.midi, b.onset, b.fermata):
            raise OutputError("MusicXML export changed the score")
    score.write("midi", fp=str(path.with_suffix(".mid")))
    return xml_path


# --- Coconet (Magenta.js) ----------------------------------------------------------------

def coconet_input(melody):
    """Return the quantized NoteSequence (as a dict) and the infill mask for Coconet.infill.

    The mask lists every step of alto, tenor, and bass, so soprano rests stay silent.
    """
    out_of_range = sorted({e.name for e in melody.notes
                           if not COCONET_MIN_PITCH <= e.midi <= COCONET_MAX_PITCH})
    if out_of_range:
        raise IneligibleMelody(f"outside Coconet pitch range {COCONET_MIN_PITCH}-{COCONET_MAX_PITCH}: "
                               + ", ".join(out_of_range))
    sequence = {
        "notes": [{"pitch": e.midi, "quantizedStartStep": e.start, "quantizedEndStep": e.end,
                   "instrument": 0} for e in melody.notes],
        "totalQuantizedSteps": melody.total_steps,
        "quantizationInfo": {"stepsPerQuarter": STEPS_PER_QUARTER},
    }
    mask = [{"step": step, "voice": voice} for step in range(melody.total_steps) for voice in (1, 2, 3)]
    return sequence, mask


def coconet_voices(notes, melody):
    """Parse Coconet output notes into Events per voice.

    Protobuf JSON omits zero values, so a missing instrument or start step means 0.
    Consecutive steps of the same pitch become one held note.
    """
    total = melody.total_steps
    steps = [[None] * total for _ in range(4)]
    for item in notes:
        voice = int(item.get("instrument", 0))
        if not 0 <= voice < 4:
            raise OutputError(f"unknown Coconet instrument {voice}")
        start, end = int(item.get("quantizedStartStep", 0)), int(item["quantizedEndStep"])
        if end > total:
            raise OutputError(f"Coconet note ends at step {end}, after the melody end {total}")
        for t in range(start, end):
            if steps[voice][t] is not None:
                raise OutputError(f"{VOICE_NAMES[voice]} sounds two pitches at step {t}")
            steps[voice][t] = int(item["pitch"])
    voices = []
    for line in steps:
        events = []
        t = 0
        while t < total:
            if line[t] is None:
                t += 1
                continue
            end = t + 1
            while end < total and line[end] == line[t]:
                end += 1
            events.append(Event(t, end, pitch.Pitch(midi=line[t]).nameWithOctave))
            t = end
        voices.append(events)
    return voices


# --- DeepBach ----------------------------------------------------------------------------

def deepbach_tokens(melody, note2index_dicts, voice_ranges):
    """Return the 4 x steps token matrix: the melody in the soprano, rests in the other voices.

    Alto, tenor, and bass are placeholders; generation with voice_index_range=[1, 4]
    and random_init=True replaces them. Raises IneligibleMelody when a soprano note
    is missing from DeepBach's soprano vocabulary or lies outside its range.
    """
    soprano_index = note2index_dicts[0]
    low, high = voice_ranges[0]
    missing = sorted({e.name for e in melody.notes
                      if e.name not in soprano_index or not low <= e.midi <= high})
    if missing:
        raise IneligibleMelody("outside DeepBach's soprano vocabulary: " + ", ".join(missing))
    total = melody.total_steps
    hold = soprano_index[DEEPBACH_HOLD]
    soprano = [None] * total
    for event in melody.notes:
        soprano[event.start] = soprano_index[event.name]
        for t in range(event.start + 1, event.end):
            soprano[t] = hold
    in_rest = False
    for t in range(total):
        if soprano[t] is None:
            soprano[t] = hold if in_rest else soprano_index[DEEPBACH_REST]
            in_rest = True
        else:
            in_rest = False
    rows = [soprano]
    for voice in (1, 2, 3):
        index = note2index_dicts[voice]
        rows.append([index[DEEPBACH_REST]] + [index[DEEPBACH_HOLD]] * (total - 1))
    return rows


def deepbach_metadata(melody):
    """Return metadata per voice and step as nested lists [voice][step][fermata, tick, key, voice].

    Fermata follows DeepBach's FermataMetadata (a step takes the value of the most
    recent soprano note, so a rest after a fermata keeps it). Tick is the position
    within the quarter note, counted from the first downbeat so that a pickup stays
    aligned. Key is the notated key signature (sharps + 8), not DeepBach's key analyzer.
    """
    total = melody.total_steps
    fermata = [0] * total
    current = 0
    starts = {e.start: e for e in melody.notes}
    for t in range(total):
        if t in starts:
            current = int(starts[t].fermata)
        fermata[t] = current
    shift = melody.measures[0].padding_left
    return [[[fermata[t], (t + shift) % STEPS_PER_QUARTER, melody.key_sharps_at(t) + 8, voice]
             for t in range(total)]
            for voice in range(4)]


def deepbach_voices(token_rows, index2note_dicts):
    """Parse DeepBach output tokens (4 x steps) into Events per voice.

    A special symbol (START, END, OOR, XX) or a hold at the first step is an output
    failure; DeepBach's own tensor_to_score would print these as rests.
    """
    if len(token_rows) != 4:
        raise OutputError(f"expected 4 voices, found {len(token_rows)}")
    voices = []
    for voice, (row, index2note) in enumerate(zip(token_rows, index2note_dicts)):
        events = []
        current = None  # [start, name] of the sounding note, None during a rest
        for t, token in enumerate(row):
            symbol = index2note[int(token)]
            if symbol in DEEPBACH_SPECIAL:
                raise OutputError(f"{VOICE_NAMES[voice]} has symbol {symbol} at step {t}")
            if symbol == DEEPBACH_HOLD:
                if t == 0:
                    raise OutputError(f"{VOICE_NAMES[voice]} starts with a hold symbol")
                continue
            if current is not None:
                events.append(Event(current[0], t, current[1]))
            current = None if symbol == DEEPBACH_REST else [t, symbol]
        if current is not None:
            events.append(Event(current[0], len(row), current[1]))
        voices.append(events)
    return voices

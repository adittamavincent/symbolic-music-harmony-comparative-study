"""Software checks for the shared MusicXML input/output and the model adapters.

These check the conversion code against the formats documented in
harmonization_io.py. They load no model; whether DeepBach and Coconet accept
the encoded input is checked at the pilot.

Run: uv run python -m unittest research/tests/test_harmonization_io.py
"""

import os
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harmonization_io import (
    Event,
    IneligibleMelody,
    OutputError,
    coconet_input,
    coconet_voices,
    deepbach_metadata,
    deepbach_tokens,
    deepbach_voices,
    harmonization_score,
    read_melody,
    write_chorale_soprano,
    write_score,
)
from music21 import chord, converter, corpus, expressions, key, meter, note, stream, tie
from voice_leading_v2 import evaluate_score, quality_check, score_grids


def melody_part(measures, time="4/4", sharps=0, fermata_at=(), pickup=False):
    """Build a melody part. Each measure is a string of `pitch:quarterLength` items
    ("r" is a rest, a trailing "~" starts a tie to the next note). A short first
    measure is a pickup when `pickup` is true."""
    part = stream.Part()
    for index, text in enumerate(measures):
        measure = stream.Measure(number=index if pickup else index + 1)
        if index == 0:
            measure.insert(0, meter.TimeSignature(time))
            measure.insert(0, key.KeySignature(sharps))
        for item in text.split():
            name, length = item.split(":")
            tied = length.endswith("~")
            length = Fraction(length.rstrip("~"))
            element = note.Rest(quarterLength=length) if name == "r" else note.Note(name, quarterLength=length)
            if tied:
                element.tie = tie.Tie("start")
            measure.append(element)
        if index == 0 and pickup:
            measure.paddingLeft = measure.barDuration.quarterLength - measure.duration.quarterLength
        part.append(measure)
    notes = list(part.recurse().notes)
    for index, n in enumerate(notes):
        if index in fermata_at:
            n.expressions.append(expressions.Fermata())
        if index and notes[index - 1].tie is not None and notes[index - 1].tie.type == "start":
            n.tie = tie.Tie("stop")
    return part


class TempDirTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write_melody(self, part, name="melody"):
        score = stream.Score()
        score.insert(0, part)
        path = self.dir / f"{name}.musicxml"
        score.write("musicxml", fp=str(path))
        return path


class ReadMelody(TempDirTest):
    def test_notes_key_meter_fermata(self):
        path = self.write_melody(melody_part(["C5:1 D5:1 E5:2", "F5:1 E5:1/2 D5:1/2 C5:2"], sharps=-1, fermata_at=(2, 6)))
        melody = read_melody(path)
        self.assertEqual(melody.melody_id, "melody")
        self.assertEqual(melody.total_steps, 32)
        self.assertEqual(melody.measure_count, 2)
        self.assertEqual(melody.measures[0].time_signature, "4/4")
        self.assertEqual(melody.key_sharps_at(0), -1)
        self.assertEqual(melody.notes[2], Event(8, 16, "E5", True))
        self.assertEqual(melody.notes[4], Event(20, 22, "E5", False))
        self.assertTrue(melody.notes[6].fermata)

    def test_repeated_pitch_stays_two_notes(self):
        melody = read_melody(self.write_melody(melody_part(["C5:1 C5:1 C5:2"])))
        self.assertEqual([(e.start, e.end) for e in melody.notes], [(0, 4), (4, 8), (8, 16)])

    def test_pickup_is_kept(self):
        melody = read_melody(self.write_melody(melody_part(["G4:1", "C5:1 D5:1 E5:1"], time="3/4", pickup=True)))
        self.assertEqual(melody.measures[0].padding_left, 8)
        self.assertEqual(melody.measures[0].length, 4)
        self.assertEqual(melody.measures[1].start, 4)

    def test_tie_across_barline_is_one_note(self):
        melody = read_melody(self.write_melody(melody_part(["C5:1 D5:1~", "D5:1 E5:1"], time="2/4")))
        self.assertEqual(melody.notes[1], Event(4, 12, "D5"))

    def test_rest_is_a_gap(self):
        melody = read_melody(self.write_melody(melody_part(["C5:1 r:1 D5:2"])))
        self.assertEqual([(e.start, e.end) for e in melody.notes], [(0, 4), (8, 16)])


class IneligibleMelodies(TempDirTest):
    def assertIneligible(self, part, fragment):
        with self.assertRaises(IneligibleMelody) as caught:
            read_melody(self.write_melody(part))
        self.assertIn(fragment, str(caught.exception))

    def test_no_key_signature(self):
        part = melody_part(["C5:1 D5:1 E5:2"])
        part.getElementsByClass(stream.Measure).first().remove(part.recurse().getElementsByClass(key.KeySignature).first())
        self.assertIneligible(part, "key signature")

    def test_triplet_is_off_grid(self):
        self.assertIneligible(melody_part(["C5:1/3 D5:1/3 E5:1/3 F5:1 G5:2"]), "sixteenth-note grid")

    def test_chord_is_not_a_melody(self):
        part = melody_part(["C5:1 D5:1 E5:2"])
        measure = part.getElementsByClass(stream.Measure).first()
        first = measure.notes.first()
        measure.replace(first, chord.Chord(["C5", "E5"], quarterLength=1))
        self.assertIneligible(part, "more than one note")

    def test_two_parts(self):
        score = stream.Score()
        score.insert(0, melody_part(["C5:4"]))
        score.insert(0, melody_part(["C3:4"]))
        path = self.dir / "two.musicxml"
        score.write("musicxml", fp=str(path))
        with self.assertRaises(IneligibleMelody):
            read_melody(path)


class ChoraleSoprano(TempDirTest):
    def test_bwv_66_6(self):
        chorale = corpus.parse("bach/bwv66.6")
        melody = write_chorale_soprano(chorale, self.dir / "bwv66.6.musicxml")
        self.assertEqual(melody.melody_id, "bwv66.6")
        self.assertEqual(melody.measure_count, 10)
        self.assertEqual(melody.measures[0].padding_left, 12)
        self.assertEqual(melody.key_sharps_at(0), 3)
        self.assertTrue(any(e.fermata for e in melody.notes))

    def test_short_final_measure_gets_no_added_rest(self):
        # Pickup of one beat, final measure of three beats, no declared padding at the end.
        score = stream.Score()
        for octave in (5, 4, 3, 2):
            score.insert(0, melody_part([f"C{octave}:1", f"D{octave}:4", f"E{octave}:3"], pickup=True))
        melody = write_chorale_soprano(score, self.dir / "short.musicxml")
        self.assertEqual(melody.total_steps, 32)
        self.assertEqual(melody.measures[-1].padding_right, 4)

    def test_requires_four_parts(self):
        score = stream.Score()
        score.insert(0, melody_part(["C5:4"]))
        with self.assertRaises(IneligibleMelody):
            write_chorale_soprano(score, self.dir / "one.musicxml")


def simple_melody(test):
    """C5 C5 D5(fermata) | E5 half, E5 half: repeated pitches and one fermata."""
    return read_melody(test.write_melody(melody_part(["C5:1 C5:1 D5:2", "E5:2 E5:2"], fermata_at=(2,))))


class Coconet(TempDirTest):
    def test_input_sequence_and_mask(self):
        melody = simple_melody(self)
        sequence, mask = coconet_input(melody)
        self.assertEqual(sequence["totalQuantizedSteps"], 32)
        self.assertEqual(sequence["quantizationInfo"], {"stepsPerQuarter": 4})
        self.assertEqual(sequence["notes"][0],
                         {"pitch": 72, "quantizedStartStep": 0, "quantizedEndStep": 4, "instrument": 0})
        self.assertEqual(len(mask), 32 * 3)
        self.assertNotIn(0, {m["voice"] for m in mask})

    def test_input_out_of_range(self):
        melody = read_melody(self.write_melody(melody_part(["C5:1 D5:1 E5:1 A6:1"])))
        with self.assertRaises(IneligibleMelody) as caught:
            coconet_input(melody)
        self.assertIn("A6", str(caught.exception))

    def output_notes(self, melody, voices_midi):
        """One-step notes as Coconet returns them, with protobuf JSON omitting zero values."""
        notes = []
        for voice, line in enumerate(voices_midi):
            for step, midi in enumerate(line):
                if midi is None:
                    continue
                item = {"pitch": midi, "quantizedEndStep": step + 1}
                if voice:
                    item["instrument"] = voice
                if step:
                    item["quantizedStartStep"] = step
                notes.append(item)
        return notes

    def melody_steps(self, melody):
        line = [None] * melody.total_steps
        for e in melody.notes:
            line[e.start:e.end] = [e.midi] * (e.end - e.start)
        return line

    def test_output_merges_steps_and_restores_soprano(self):
        melody = simple_melody(self)
        alto = [67] * 16 + [64] * 16
        notes = self.output_notes(melody, [self.melody_steps(melody), alto, [60] * 32, [48] * 32])
        voices = coconet_voices(notes, melody)
        self.assertEqual(voices[1], [Event(0, 16, "G4"), Event(16, 32, "E4")])
        score = harmonization_score(voices, melody)
        soprano = [n for n in score.parts[0].recurse().notes]
        self.assertEqual([n.quarterLength for n in soprano], [1, 1, 2, 2, 2])
        self.assertTrue(soprano[2].expressions)
        ok, reasons = quality_check(score, read_melody_part(self.dir / "melody.musicxml"))
        self.assertTrue(ok, reasons)

    def test_changed_soprano_is_kept_and_rejected(self):
        melody = simple_melody(self)
        soprano = self.melody_steps(melody)
        soprano[5] = 74
        notes = self.output_notes(melody, [soprano, [67] * 32, [60] * 32, [48] * 32])
        score = harmonization_score(coconet_voices(notes, melody), melody)
        ok, reasons = quality_check(score, read_melody_part(self.dir / "melody.musicxml"))
        self.assertFalse(ok)
        self.assertEqual(reasons, ["soprano differs from the input melody"])

    def test_two_pitches_in_one_voice(self):
        melody = simple_melody(self)
        notes = [{"pitch": 67, "instrument": 1, "quantizedEndStep": 1},
                 {"pitch": 69, "instrument": 1, "quantizedEndStep": 1}]
        with self.assertRaises(OutputError):
            coconet_voices(notes, melody)

    def test_unknown_instrument_and_overlong_note(self):
        melody = simple_melody(self)
        with self.assertRaises(OutputError):
            coconet_voices([{"pitch": 60, "instrument": 4, "quantizedEndStep": 1}], melody)
        with self.assertRaises(OutputError):
            coconet_voices([{"pitch": 60, "instrument": 1, "quantizedEndStep": 33}], melody)


def read_melody_part(path):
    return converter.parse(str(path)).parts[0]


def fake_vocabulary():
    """Small DeepBach-style vocabularies: index -> symbol per voice, and the reverse."""
    symbols = ["__", "START", "END", "rest", "OOR", "C5", "D5", "E5", "G4", "E4", "C4", "C3"]
    index2note = [dict(enumerate(symbols)) for _ in range(4)]
    note2index = [{s: i for i, s in enumerate(symbols)} for _ in range(4)]
    return note2index, index2note


class DeepBach(TempDirTest):
    def test_soprano_tokens(self):
        melody = read_melody(self.write_melody(melody_part(["C5:1 r:1 D5:1 D5:1"])))
        note2index, _ = fake_vocabulary()
        rows = deepbach_tokens(melody, note2index, [(60, 81)] * 4)
        c5, d5, hold, rest = (note2index[0][s] for s in ("C5", "D5", "__", "rest"))
        self.assertEqual(rows[0], [c5, hold, hold, hold, rest, hold, hold, hold,
                                   d5, hold, hold, hold, d5, hold, hold, hold])
        self.assertEqual(rows[2], [rest] + [hold] * 15)

    def test_missing_spelling_is_ineligible(self):
        melody = read_melody(self.write_melody(melody_part(["C5:1 D5:1 E5:1 F5:1"])))
        note2index, _ = fake_vocabulary()
        with self.assertRaises(IneligibleMelody) as caught:
            deepbach_tokens(melody, note2index, [(60, 81)] * 4)
        self.assertIn("F5", str(caught.exception))

    def test_out_of_voice_range_is_ineligible(self):
        melody = read_melody(self.write_melody(melody_part(["C5:1 D5:1 E5:2"])))
        note2index, _ = fake_vocabulary()
        with self.assertRaises(IneligibleMelody):
            deepbach_tokens(melody, note2index, [(60, 73)] * 4)

    def test_metadata(self):
        melody = read_melody(self.write_melody(
            melody_part(["G4:1/2", "C5:1 D5:1 E5:1 r:1", "C5:4"], sharps=2, fermata_at=(3,), pickup=True)))
        meta = deepbach_metadata(melody)
        self.assertEqual(len(meta), 4)
        self.assertEqual(len(meta[0]), melody.total_steps)
        # Pickup of an eighth: the first step is the third sixteenth of its beat.
        self.assertEqual([row[1] for row in meta[0][:4]], [2, 3, 0, 1])
        self.assertEqual({row[2] for row in meta[0]}, {10})
        self.assertEqual([meta[3][0][3], meta[1][5][3]], [3, 1])
        # E5 (fermata) sounds at steps 10-13 and the rest at 14-17 keeps the value; C5 at step 18 clears it.
        self.assertEqual([row[0] for row in meta[0][9:19]], [0, 1, 1, 1, 1, 1, 1, 1, 1, 0])

    def test_decode_tokens(self):
        _, index2note = fake_vocabulary()
        note2index, _ = fake_vocabulary()
        n = note2index[0]
        rows = [[n["C5"], n["__"], n["rest"], n["__"]],
                [n["G4"], n["__"], n["G4"], n["__"]],
                [n["E4"], n["__"], n["__"], n["__"]],
                [n["C3"], n["C4"], n["__"], n["rest"]]]
        voices = deepbach_voices(rows, index2note)
        self.assertEqual(voices[0], [Event(0, 2, "C5")])
        self.assertEqual(voices[1], [Event(0, 2, "G4"), Event(2, 4, "G4")])
        self.assertEqual(voices[3], [Event(0, 1, "C3"), Event(1, 3, "C4")])

    def test_special_symbols_fail(self):
        note2index, index2note = fake_vocabulary()
        n = note2index[0]
        ok = [n["C5"], n["__"]]
        with self.assertRaises(OutputError) as caught:
            deepbach_voices([ok, [n["G4"], n["OOR"]], ok, ok], index2note)
        self.assertIn("OOR", str(caught.exception))
        with self.assertRaises(OutputError):
            deepbach_voices([ok, [n["__"], n["G4"]], ok, ok], index2note)


class CanonicalOutput(TempDirTest):
    def test_bach_round_trip_keeps_measurements(self):
        chorale = corpus.parse("bach/bwv66.6")
        melody = write_chorale_soprano(chorale, self.dir / "bwv66.6.musicxml")
        voices = []
        for grid in score_grids(chorale):
            events, t = [], 0
            while t < len(grid):
                if grid.midi[t] is None:
                    t += 1
                    continue
                end = t + 1
                while end < len(grid) and grid.midi[end] == grid.midi[t] and not grid.onset[end]:
                    end += 1
                events.append(Event(t, end, grid.pitch[t].nameWithOctave, grid.fermata[t]))
                t = end
            voices.append(events)
        path = write_score(harmonization_score(voices, melody), self.dir / "out" / "bwv66.6")
        self.assertTrue(path.with_suffix(".mid").exists())
        back = converter.parse(str(path))
        self.assertEqual([p.partName for p in back.parts], ["Soprano", "Alto", "Tenor", "Bass"])
        self.assertEqual(evaluate_score(back)["counts"], evaluate_score(chorale)["counts"])
        self.assertEqual(len(back.parts[0].getElementsByClass(stream.Measure)), 10)
        ok, reasons = quality_check(back, read_melody_part(self.dir / "bwv66.6.musicxml"))
        self.assertTrue(ok, reasons)

    def test_long_and_cross_barline_notes(self):
        melody = read_melody(self.write_melody(melody_part(["C5:4", "D5:4"])))
        alto = [Event(0, 5, "G4"), Event(5, 20, "A4"), Event(20, 32, "B4")]
        score = harmonization_score([list(melody.notes), alto, [Event(0, 32, "E4")], [Event(0, 32, "C3")]],
                                    melody)
        back = converter.parse(str(write_score(score, self.dir / "long")))
        grid = score_grids(back)[1]
        self.assertEqual([t for t in range(32) if grid.onset[t]], [0, 5, 20])
        self.assertEqual(grid.midi[19], 69)

    def test_overlapping_events_fail(self):
        melody = read_melody(self.write_melody(melody_part(["C5:4"])))
        with self.assertRaises(OutputError):
            harmonization_score([list(melody.notes), [Event(0, 8, "G4"), Event(4, 16, "A4")], [], []], melody)


if __name__ == "__main__":
    unittest.main()

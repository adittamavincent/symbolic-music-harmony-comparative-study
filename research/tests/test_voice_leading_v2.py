"""Software checks for the version 2 voice-leading instrument.

These are constructed edge cases that check the code against the written
operational definitions. Passing them does not validate the instrument
musically; see the validation steps in research/protocol.md.

Run: uv run python -m unittest research/tests/test_voice_leading_v2.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from music21 import expressions, meter, note, stream
from voice_leading_v2 import (
    QualityError,
    crosscheck_music21,
    evaluate_grids,
    grid_from_part,
    quality_check,
    score_grids,
)


def part(pitches, length=1.0, fermata_at=None):
    """Build a part from pitch names (None = rest), each `length` quarter notes long."""
    p = stream.Part()
    p.append(meter.TimeSignature("4/4"))
    for index, name in enumerate(pitches):
        if name is None:
            element = note.Rest(quarterLength=length)
        else:
            element = note.Note(name, quarterLength=length)
            if fermata_at is not None and index == fermata_at:
                element.expressions.append(expressions.Fermata())
        p.append(element)
    return p


def satb(s, a, t, b, **kwargs):
    score = stream.Score()
    soprano_kwargs = {"fermata_at": kwargs.get("fermata_at")}
    for index, voice in enumerate((s, a, t, b)):
        score.insert(0, part(voice, **(soprano_kwargs if index == 0 else {})))
    return score


def counts(score, **kwargs):
    return evaluate_grids(score_grids(score), measures=1, **kwargs)["counts"]


class ParallelMotion(unittest.TestCase):
    def test_parallel_fifth_similar_motion(self):
        c = counts(satb(["G5", "A5"], ["C5", "D5"], ["E4", "F4"], ["C3", "D3"]))
        # S-A fifths G5/C5 -> A5/D5; S-B G5/C3 (19) -> A5/D3 (19): compound fifth.
        self.assertEqual(c["parallel_fifths"], 2)

    def test_contrary_fifth_to_twelfth_not_counted(self):
        # S-B: G4/C4 (7) -> G5/C3 (31) by contrary motion; alto and tenor hold.
        c = counts(satb(["G4", "G5"], ["E4", "E4"], ["G3", "G3"], ["C4", "C3"]))
        self.assertEqual(c["parallel_fifths"], 0)

    def test_fourth_is_not_a_fifth(self):
        c = counts(satb(["F4", "G4"], ["C4", "D4"], ["A3", "B3"], ["F2", "G2"]))
        # S-A are fourths (5 semitones); version 1 counted these as fifths.
        pairs_with_fifths = c["parallel_fifths"]
        # S-B F4/F2 (24) octaves, A-B C4/F2 (19) fifths -> D4/G2 (19): one fifth (A-B).
        self.assertEqual(pairs_with_fifths, 1)

    def test_oblique_motion_not_counted(self):
        c = counts(satb(["G4", "G4"], ["C4", "C4"], ["E3", "F3"], ["C3", "C3"]))
        self.assertEqual(c["parallel_fifths"], 0)
        self.assertEqual(c["parallel_octaves"], 0)

    def test_parallel_octave_compound_and_unison(self):
        c = counts(satb(["C5", "D5"], ["E4", "F4"], ["E4", "F4"], ["C3", "D3"]))
        # S-B compound octave C5/C3 -> D5/D3; A-T unison E4 -> F4.
        self.assertEqual(c["parallel_octaves"], 2)

    def test_repeated_note_is_not_motion(self):
        c = counts(satb(["G4", "G4"], ["C4", "C4"], ["E3", "E3"], ["C3", "C3"]))
        self.assertEqual(c["parallel_fifths"], 0)

    def test_rest_breaks_motion(self):
        c = counts(satb(["G4", "A4"], [None, "D4"], ["E3", "F3"], ["C3", "D3"]))
        # Alto rests at the first event, so S-A is not checked; S-B G4/C3 (19) -> A4/D3 (19) counts.
        self.assertEqual(c["parallel_fifths"], 1)


class VerticalRules(unittest.TestCase):
    def test_spacing_upper_pairs_only(self):
        c = counts(satb(["C6"], ["B4"], ["G4"], ["C2"]))
        # S-A 13 semitones -> 1; A-T 4; T-B 31 is not checked.
        self.assertEqual(c["spacing"], 1)

    def test_crossing_and_overlap_not_double_counted(self):
        c = counts(satb(["E4", "E4"], ["C4", "G4"], ["G3", "G3"], ["C3", "C3"]))
        # Alto moves C4 -> G4 above the soprano's E4: crossing at the second event, not overlap.
        self.assertEqual(c["crossing"], 1)
        self.assertEqual(c["overlap"], 0)

    def test_overlap_without_crossing(self):
        c = counts(satb(["E4", "A4"], ["C4", "F4"], ["G3", "A3"], ["C3", "F2"]))
        # Alto F4 rises above the soprano's previous E4, but stays below the new A4.
        self.assertEqual(c["overlap"], 1)
        self.assertEqual(c["crossing"], 0)

    def test_crossing_below_soprano_not_counted(self):
        c = counts(satb(["C5"], ["E4"], ["G3"], ["C4"]))
        # Bass above tenor: Strube (p. 174) allows occasional crossing not over the soprano.
        self.assertEqual(c["crossing"], 0)

    def test_overlap_with_stepwise_voice_not_counted(self):
        c = counts(satb(["E4", "F4"], ["C4", "F4"], ["G3", "A3"], ["C3", "F2"]))
        # Alto rises above the soprano's previous E4, but the soprano moves by step (E4-F4).
        self.assertEqual(c["overlap"], 0)

    def test_unison_is_not_crossing(self):
        c = counts(satb(["E4"], ["E4"], ["G3"], ["C3"]))
        self.assertEqual(c["crossing"], 0)


class TimingAndQuality(unittest.TestCase):
    def test_sixteenth_onsets_are_kept(self):
        p = stream.Part()
        for offset, name in ((0, "C4"), (0.25, "D4"), (0.5, "E4"), (1, "F4"), (2, "G4")):
            p.insert(offset, note.Note(name, quarterLength=0.25 if offset < 1 else 1.0))
        grid = grid_from_part(p)
        self.assertEqual([t for t, o in enumerate(grid.onset) if o], [0, 1, 2, 4, 8])

    def test_off_grid_onset_rejected(self):
        p = stream.Part()
        p.insert(0, note.Note("C4", quarterLength=1 / 3))
        with self.assertRaises(QualityError):
            grid_from_part(p)

    def test_three_voices_rejected(self):
        score = stream.Score()
        for voice in (["C5"], ["E4"], ["C3"]):
            score.insert(0, part(voice))
        ok, reasons = quality_check(score)
        self.assertFalse(ok)
        self.assertIn("expected 4 voices", reasons[0])

    def test_soprano_must_match_melody(self):
        score = satb(["C5", "D5"], ["E4", "F4"], ["G3", "A3"], ["C3", "D3"])
        self.assertTrue(quality_check(score, part(["C5", "D5"]))[0])
        self.assertFalse(quality_check(score, part(["C5", "E5"]))[0])

    def test_fermata_exclusion_only_drops_boundary_motion(self):
        score = satb(["G4", "A4"], ["C4", "D4"], ["E3", "F3"], ["C3", "D3"], fermata_at=0)
        self.assertEqual(counts(score)["parallel_fifths"], 2)
        self.assertEqual(counts(score, exclude_fermata_motion=True)["parallel_fifths"], 0)

    def test_rates_and_weighted_index(self):
        score = satb(["C6", "D6"], ["B4", "C5"], ["G4", "A4"], ["C3", "D3"])
        result = evaluate_grids(score_grids(score), measures=2)
        c = result["counts"]
        expected = (c["parallel_fifths"] + c["parallel_octaves"]
                    + 0.5 * (c["spacing"] + c["crossing"] + c["overlap"])) / 2
        self.assertAlmostEqual(result["weighted_penalty_per_measure"], expected)
        self.assertAlmostEqual(result["rates_per_measure"]["spacing"], c["spacing"] / 2)


class Music21CrossCheck(unittest.TestCase):
    def test_agrees_on_spelled_parallel_fifth(self):
        tables = crosscheck_music21(score_grids(
            satb(["G5", "A5"], ["C5", "D5"], ["E4", "F4"], ["C3", "D3"])))
        self.assertEqual(tables["parallel_fifths"]["ours_only"], 0)
        self.assertEqual(tables["parallel_fifths"]["music21_only"], 0)
        self.assertEqual(tables["parallel_fifths"]["both"], 2)


if __name__ == "__main__":
    unittest.main()

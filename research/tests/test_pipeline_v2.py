"""Software checks for the pipeline (protocol 3.0, with the 2.1 path kept): melody typing, melody sets,
sample selection, generation runs, quality control, measurement variants, phrase zones, statistics,
and run checks.

No model is loaded. Generation is exercised with the fake backend, whose output
is a fixed-interval stand-in and never research data.

Run: uv run python -m unittest research/tests/test_pipeline_v2.py
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib.util

import analysis_v2
import evaluate_v2
import generation_v2
import melody_sets
import numpy as np
import phrase_zones
import run_checks_v2
from melody_text import (
    MelodyTextError,
    build_part,
    parse_fields,
    parse_notes,
    text_to_musicxml,
)
from scipy import stats
from voice_leading_v2 import VoiceGrid, evaluate_grids

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "strube-melodies"
PROTOCOL_V21 = generation_v2.RESEARCH / "experiments" / "protocol_v2.json"


def load_cli():
    path = generation_v2.RESEARCH / "experiments" / "scripts" / "v2.py"
    spec = importlib.util.spec_from_file_location("pipeline_cli", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_text(directory, name, body):
    path = Path(directory) / name
    path.write_text(body, encoding="utf-8")
    return path


def melody_text(notes, key="0", mode="major", time="4/4", pickup="0", code="t-ex001"):
    return (f"kode: {code}\nsumber: uji\nkunci: {key}\nmode: {mode}\nbirama: {time}\n"
            f"anakan: {pickup}\nnada: {notes}\n")


class MelodyTextTests(unittest.TestCase):
    def test_key_signature_applies_and_accidentals_hold_to_the_barline(self):
        measures = parse_notes("F4:1 Fn4:1 F4:1 F#4:1 | F4:4", sharps=1)
        names = [item[0] for item in measures[0]] + [measures[1][0][0]]
        self.assertEqual(names, ["F#4", "F4", "F4", "F#4", "F#4"])

    def test_flats_and_double_accidentals(self):
        measures = parse_notes("B4:1 E5:1 Bbb4:1 C##5:1", sharps=-2)
        self.assertEqual([item[0] for item in measures[0]], ["B-4", "E-5", "B--4", "C##5"])

    def test_measure_length_is_checked(self):
        fields = parse_fields(melody_text("C5:1 D5:1 E5:1 | F5:4"))
        with self.assertRaisesRegex(MelodyTextError, "birama 1 berisi 3"):
            build_part(fields)

    def test_pickup_and_short_last_measure_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_text(tmp, "t-ex001.txt", melody_text("G4:1 | C5:2 D5:2 | E5:3!", pickup="1"))
            _, melody = text_to_musicxml(path, Path(tmp) / "t.musicxml")
            self.assertEqual(melody.measure_count, 3)
            self.assertEqual(melody.measures[0].padding_left, 12)
            self.assertEqual(melody.measures[-1].padding_right, 4)
            self.assertTrue(melody.notes[-1].fermata)
            self.assertEqual([e.name for e in melody.notes], ["G4", "C5", "D5", "E5"])

    def test_tie_joins_two_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_text(tmp, "t-ex001.txt", melody_text("C5:2 D5:2~ | D5:2 E5:2"))
            _, melody = text_to_musicxml(path, Path(tmp) / "t.musicxml")
            self.assertEqual([(e.name, e.end - e.start) for e in melody.notes], [("C5", 8), ("D5", 16), ("E5", 8)])

    def test_tie_to_a_different_pitch_is_rejected(self):
        fields = parse_fields(melody_text("C5:2 D5:2~ | E5:4"))
        with self.assertRaisesRegex(MelodyTextError, "nada yang sama"):
            build_part(fields)

    def test_bad_pitch_token_reports_its_place(self):
        with self.assertRaisesRegex(MelodyTextError, "birama 1, nada 2"):
            parse_notes("C5:2 H5:2", sharps=0)

    def test_fixtures_convert(self):
        with tempfile.TemporaryDirectory() as tmp:
            for path in sorted(FIXTURES.glob("*.txt")):
                _, melody = text_to_musicxml(path, Path(tmp) / f"{path.stem}.musicxml")
                self.assertGreater(len(melody.notes), 5)


class MelodySetTests(unittest.TestCase):
    def test_features_and_huang_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_text(tmp, "t-ex001.txt", melody_text("C5:1 C6:1 G5:2 | C5:4"))
            _, melody = text_to_musicxml(path, Path(tmp) / "t.musicxml")
            features = melody_sets.melody_features(melody)
            self.assertEqual(features["largest_leap"], 12)
            self.assertEqual(features["highest_midi"], 84)
            self.assertEqual(features["within_huang_limits"], 0)  # 84 is above MIDI 81

    def test_signature_ignores_transposition(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = write_text(tmp, "a.txt", melody_text("C5:1 D5:1 E5:2 | C5:4", code="a"))
            b = write_text(tmp, "b.txt", melody_text("D5:1 E5:1 F#5:2 | D5:4", code="b"))
            _, ma = text_to_musicxml(a, Path(tmp) / "a.musicxml")
            _, mb = text_to_musicxml(b, Path(tmp) / "b.musicxml")
            self.assertEqual(melody_sets.melody_signature(ma), melody_sets.melody_signature(mb))

    def test_strube_set_statuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            texts = Path(tmp) / "texts"
            texts.mkdir()
            write_text(texts, "s-ok.txt", melody_text("C5:1 D5:1 E5:2 | C5:4", code="s-ok"))
            write_text(texts, "s-empty.txt", melody_text("", code="s-empty"))
            write_text(texts, "s-bad.txt", melody_text("C5:1 D5:1 | C5:4", code="s-bad"))
            write_text(texts, "s-low.txt", melody_text("C1:4 | C1:4", code="s-low"))
            records = {r.melody_id: r for r in melody_sets.build_strube_set(Path(tmp) / "out", texts)}
            self.assertEqual(records["s-ok"].status, "eligible")
            self.assertEqual(records["s-empty"].status, "not_typed")
            self.assertEqual(records["s-bad"].status, "format_error")
            self.assertEqual(records["s-low"].status, "ineligible")

    def test_bach_frame_and_seeded_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = melody_sets.build_bach_frame(tmp, limit=6)
            eligible = [r for r in records if r.status == "eligible"]
            self.assertGreaterEqual(len(eligible), 4)
            first = melody_sets.sample_bach(records, 3, seed=7)
            self.assertEqual(first, melody_sets.sample_bach(records, 3, seed=7))
            self.assertEqual(len(first), 3)
            with self.assertRaises(ValueError):
                melody_sets.sample_bach(records, 99, seed=7)


class RunTests(unittest.TestCase):
    def make_run(self, tmp, backends, protocol=None):
        protocol = protocol or generation_v2.load_protocol()
        out = Path(tmp) / "melodies"
        strube = melody_sets.build_strube_set(out, FIXTURES)
        bach = melody_sets.build_bach_frame(out, limit=2)
        rows = [r.row() for r in bach + strube if r.status == "eligible"]
        return generation_v2.Run.create("t-run", protocol, rows, backends, "test", runs_dir=Path(tmp) / "runs")

    def test_run_is_never_overwritten_and_records_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.make_run(tmp, [generation_v2.FakeBackend()])
            info = run.info()
            self.assertEqual(info["instrument_version"], "2.0")
            self.assertIn("commit", info["code"])
            with self.assertRaises(FileExistsError):
                self.make_run(tmp, [generation_v2.FakeBackend()])

    def test_attempts_logged_resumed_and_failures_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            backend = generation_v2.FakeBackend(fail_every=3)
            run = self.make_run(tmp, [backend])
            counts = generation_v2.generate(run, backend, 2, 1, progress=lambda m: None)
            total = len(run.melodies()) * 2
            self.assertEqual(sum(counts.values()), total)
            self.assertIn("model_error", counts)
            again = generation_v2.generate(run, backend, 2, 1, progress=lambda m: None)
            self.assertEqual(again, {})  # failures are not retried silently
            retried = generation_v2.generate(run, generation_v2.FakeBackend(), 2, 1, retry_failed=True,
                                             progress=lambda m: None)
            self.assertEqual(retried, {"ok": counts["model_error"]})
            attempts = run.attempts()
            self.assertEqual(len(attempts), total + counts["model_error"])
            self.assertTrue(any(a["attempt"] == 2 for a in attempts))

    def test_seed_is_deterministic_per_attempt(self):
        self.assertEqual(generation_v2.attempt_seed(1, "deepbach", "m", 2), generation_v2.attempt_seed(1, "deepbach", "m", 2))
        self.assertNotEqual(generation_v2.attempt_seed(1, "deepbach", "m", 2), generation_v2.attempt_seed(1, "deepbach", "m", 3))

    def test_evaluation_and_completeness_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = generation_v2.FakeBackend("deepbach"), generation_v2.FakeBackend("coconet", offsets=(8, 16, 24))
            run = self.make_run(tmp, [a, b])
            problems = run_checks_v2.check_run(run.dir, ["deepbach", "coconet"], 2)
            self.assertTrue(any("missing attempt" in p for p in problems))
            for backend in (a, b):
                generation_v2.generate(run, backend, 2, 1, progress=lambda m: None)
            self.assertIn("evaluation has not been run", run_checks_v2.check_run(run.dir, ["deepbach", "coconet"], 2))
            result = evaluate_v2.evaluate_run(run.dir)
            self.assertEqual(result["measured"], len(run.melodies()) * 4)
            self.assertEqual(run_checks_v2.check_run(run.dir, ["deepbach", "coconet"], 2), [])
            score = next(run.dir.glob("scores/deepbach/*.musicxml"))
            score.write_text(score.read_text() + " ", encoding="utf-8")
            self.assertTrue(any("changed" in p for p in run_checks_v2.check_run(run.dir, ["deepbach", "coconet"], 2)))
            flags = (run.dir / "evaluation" / "flags.csv").read_text(encoding="utf-8").splitlines()
            self.assertTrue(flags[0].endswith(",zone"))
            summary = analysis_v2.analyze_run(run.dir)  # protocol 3.0: zone test, no origin test
            self.assertEqual(len(summary["q2"]), 6)
            self.assertEqual(len(summary["q3_zone"]), 10)
            self.assertEqual(summary["q3"], [])
            self.assertEqual(len(summary["zone_pattern"]), 15)
            self.assertTrue((run.dir / "analysis" / "tables" / "q3_zona.tex").exists())
            self.assertFalse((run.dir / "analysis" / "q3_mannwhitney.csv").exists())
            figures = analysis_v2.plot_run(run.dir)
            self.assertTrue(any(f.name == "zona_fermata.png" for f in figures))

    def test_protocol_21_path_still_runs_the_origin_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = generation_v2.FakeBackend("deepbach"), generation_v2.FakeBackend("coconet", offsets=(8, 16, 24))
            run = self.make_run(tmp, [a, b], protocol=generation_v2.load_protocol(PROTOCOL_V21))
            for backend in (a, b):
                generation_v2.generate(run, backend, 2, 1, progress=lambda m: None)
            evaluate_v2.evaluate_run(run.dir)
            summary = analysis_v2.analyze_run(run.dir)
            self.assertEqual(len(summary["q3"]), 12)
            self.assertEqual(summary["q3_zone"], [])
            self.assertTrue((run.dir / "analysis" / "tables" / "q3_mannwhitney.tex").exists())

    def test_deepbach_symbols_parse_without_model(self):
        symbols = [["C5", "__", "D5", "__"], ["E4", "__", "__", "F4"], ["G3", "__", "rest", "__"], ["C3", "__", "__", "__"]]
        voices = generation_v2.deepbach_voices_from_symbols(symbols)
        self.assertEqual([(e.start, e.end, e.name) for e in voices[2]], [(0, 2, "G3")])
        self.assertEqual([(e.start, e.end) for e in voices[1]], [(0, 3), (3, 4)])

    def test_backends_without_installation_fail_clearly(self):
        protocol = generation_v2.load_protocol()
        coconet = generation_v2.CoconetBackend(protocol["models"]["coconet"], node_dir=Path(tempfile.gettempdir()) / "none")
        with self.assertRaisesRegex(RuntimeError, "setup-v2"):
            coconet.generate([])
        deepbach = generation_v2.DeepBachBackend(protocol["models"]["deepbach"], repo_dir=Path(tempfile.gettempdir()) / "none")
        with self.assertRaisesRegex(RuntimeError, "setup-v2"):
            deepbach.check(None)


class QualityAndVariantTests(unittest.TestCase):
    @staticmethod
    def grid(pitches, onsets=None):
        onsets = onsets or [True] * len(pitches)
        return VoiceGrid(list(pitches), [None] * len(pitches), list(onsets), [False] * len(pitches))

    def test_quality_reasons(self):
        melody = self.grid([72, 74, 76, 77])
        grids = [self.grid([72, 74, 76, 77]), self.grid([None] * 4), self.grid([60] * 4), self.grid([48] * 4)]
        self.assertEqual(evaluate_v2.quality_check_v2(grids, melody), ["alto has no notes"])
        grids[0] = self.grid([72, 74, 76, 79])
        self.assertIn("soprano differs from the input melody", evaluate_v2.quality_check_v2(grids, melody))

    def test_copy_share(self):
        reference = [self.grid([72, 74]), self.grid([67, 67]), self.grid([60, None]), self.grid([48, 50])]
        output = [self.grid([72, 74]), self.grid([67, 65]), self.grid([60, 59]), self.grid([48, 50])]
        self.assertAlmostEqual(evaluate_v2.copy_share(reference, reference), 1.0)
        self.assertAlmostEqual(evaluate_v2.copy_share(output, reference), 4 / 5)

    def test_merged_repeats_remove_restruck_spacing_events(self):
        soprano = self.grid([84, 84, 84, 84], [True, False, False, False])
        alto = self.grid([60, 60, 60, 60])  # four attacks of the same pitch, more than an octave below
        tenor, bass = self.grid([55] * 4, [True, False, False, False]), self.grid([48] * 4, [True, False, False, False])
        main = evaluate_grids([soprano, alto, tenor, bass], 1)
        merged = evaluate_grids([evaluate_v2.merge_repeats(g) for g in (soprano, alto, tenor, bass)], 1)
        self.assertEqual(main["counts"]["spacing"], 4)
        self.assertEqual(merged["counts"]["spacing"], 1)


def event_grid(pitches, fermata_events=(), steps_per_event=4):
    """A VoiceGrid with one note per event, each lasting steps_per_event sixteenths."""
    midi, onset, fermata = [], [], []
    for index, pitch in enumerate(pitches):
        for step in range(steps_per_event):
            midi.append(pitch)
            onset.append(step == 0)
            fermata.append(index in fermata_events)
    return VoiceGrid(midi, [None] * len(midi), onset, fermata)


class PhraseZoneTests(unittest.TestCase):
    def grids(self):
        # Fermata on the third soprano note. S-A fifths move 0->4 (inside the phrase) and 4->8 (arrive on the
        # fermata). A-T spacing over an octave sounds on the fermata; S-A spacing over an octave after it.
        return [event_grid([72, 74, 76, 77], fermata_events={2}), event_grid([65, 67, 69, 62]),
                event_grid([55, 55, 55, 55]), event_grid([48, 48, 48, 48])]

    def test_flags_are_sorted_by_zone(self):
        grids = self.grids()
        result = evaluate_grids(grids, 1)
        counts, zones = phrase_zones.zone_counts(grids, result["flags"])
        self.assertEqual(counts["parallel_fifths"]["F"][0], 1)
        self.assertEqual(counts["parallel_fifths"]["I"][0], 1)
        self.assertEqual(counts["spacing"]["F"][0], 1)
        self.assertEqual(counts["spacing"]["I"][0], 1)
        self.assertEqual(len(zones), len(result["flags"]))
        by_flag = {(f["rule"], f["pair"], f["step"]): z for f, z in zip(result["flags"], zones)}
        self.assertEqual(by_flag[("parallel_fifths", "S-A", 4)], "I")
        self.assertEqual(by_flag[("parallel_fifths", "S-A", 8)], "F")

    def test_zones_add_up_to_the_instrument_totals(self):
        grids = self.grids()
        result = evaluate_grids(grids, 1)
        counts, _ = phrase_zones.zone_counts(grids, result["flags"])
        for rule in result["counts"]:
            self.assertEqual(counts[rule]["F"][0] + counts[rule]["I"][0], result["counts"][rule])
            self.assertEqual(counts[rule]["F"][1] + counts[rule]["I"][1], result["opportunities"][rule])

    def test_zone_rate_pools_counts_and_skips_empty_zones(self):
        row = {"main_zone_overlap_F_count": "2", "main_zone_overlap_F_opportunities": "8",
               "main_zone_overlap_I_count": "1", "main_zone_overlap_I_opportunities": "0"}
        self.assertAlmostEqual(analysis_v2.zone_rate(row, "main", "overlap", "F"), 0.25)
        self.assertIsNone(analysis_v2.zone_rate(row, "main", "overlap", "I"))


class SelectionTests(unittest.TestCase):
    def rows(self, n_bach, n_strube=0):
        rows = [{"melody_id": f"bach-{i:03d}", "origin": "bach", "source": "corpus", "status": "eligible"}
                for i in range(n_bach)]
        return rows + [{"melody_id": f"strube-{i:03d}", "origin": "strube", "source": "typed", "status": "eligible"}
                       for i in range(n_strube)]

    def test_protocol_30_draws_bach_only_and_a_disjoint_pilot(self):
        cli = load_cli()
        settings = generation_v2.load_protocol()["melodies"]
        main, pilot, n_strube, n_bach = cli.choose_samples(self.rows(60, 5), settings)
        self.assertEqual((n_strube, n_bach, len(main)), (0, 40, 40))
        self.assertTrue(all(r["origin"] == "bach" for r in main + pilot))
        self.assertEqual(len(pilot), 3)
        self.assertFalse({r["melody_id"] for r in pilot} & {r["melody_id"] for r in main})
        again, _, _, _ = cli.choose_samples(self.rows(60, 5), settings)
        self.assertEqual(main, again)

    def test_protocol_21_keeps_strube_census(self):
        cli = load_cli()
        settings = generation_v2.load_protocol(PROTOCOL_V21)["melodies"]
        main, pilot, n_strube, n_bach = cli.choose_samples(self.rows(60, 5), settings)
        self.assertEqual((n_strube, n_bach, len(main)), (5, 30, 35))
        self.assertEqual(len(pilot), 6)


class StatisticsTests(unittest.TestCase):
    def test_holm(self):
        adjusted = analysis_v2.holm([0.01, 0.04, None, 0.03])
        self.assertAlmostEqual(adjusted[0], 0.03)
        self.assertAlmostEqual(adjusted[3], 0.06)
        self.assertAlmostEqual(adjusted[1], 0.06)
        self.assertIsNone(adjusted[2])

    def test_wilcoxon_matches_scipy_and_effect_sign(self):
        x = [0.5, 0.4, 0.6, 0.3, 0.2, 0.5, 0.7, 0.1]
        y = [0.2, 0.1, 0.4, 0.3, 0.1, 0.2, 0.3, 0.2]
        result = analysis_v2.wilcoxon_paired(x, y)
        expected = stats.wilcoxon(np.array(x) - np.array(y), zero_method="wilcox")
        self.assertAlmostEqual(result["p_value"], expected.pvalue)
        self.assertGreater(result["effect_size"], 0)  # DeepBach (x) higher
        self.assertEqual(result["n_nonzero"], 7)

    def test_all_zero_differences_are_reported_not_tested(self):
        result = analysis_v2.wilcoxon_paired([0, 0, 0], [0, 0, 0])
        self.assertIsNone(result["p_value"])
        self.assertIn("zero", result["note"])

    def test_mann_whitney_one_sided_and_rank_biserial(self):
        strube, bach = [0.5, 0.6, 0.7, 0.8], [0.1, 0.2, 0.3, 0.4]
        result = analysis_v2.mann_whitney(strube, bach, "greater")
        self.assertAlmostEqual(result["p_value"], stats.mannwhitneyu(strube, bach, alternative="greater").pvalue)
        self.assertAlmostEqual(result["effect_size"], 1.0)
        reverse = analysis_v2.mann_whitney(bach, strube, "greater")
        self.assertAlmostEqual(reverse["effect_size"], -1.0)

    def test_minimum_detectable_effect_matches_the_protocol_plan(self):
        # protocol.md: n = 15, 20, 25 per group give 1.15, 0.98, 0.87 as in protocol.md; n = 30 gives 0.79 (protocol.md said 0.78)
        self.assertAlmostEqual(analysis_v2.minimum_detectable_d(30, 30), 0.79, delta=0.01)
        self.assertAlmostEqual(analysis_v2.minimum_detectable_d(20, 20), 0.98, delta=0.02)
        # protocol 3.0: 40 paired melodies detect about d_z = 0.49
        self.assertAlmostEqual(analysis_v2.minimum_detectable_d(40, paired=True), 0.49, delta=0.01)


if __name__ == "__main__":
    unittest.main()

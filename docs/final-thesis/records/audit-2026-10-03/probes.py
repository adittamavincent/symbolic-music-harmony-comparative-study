"""Diagnostic examples for the thesis audit; these are not model research data.

Run from the repository root with uv run python <this file>. The instrument is
read without modification. Results include its digest so later runs can be
distinguished if another revision changes its behavior.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import music21
from music21 import expressions, note, stream

from research import voice_leading_v2 as instrument


def score_from_events(voices):
    """Each note is (offset in beats, MIDI pitch, duration, fermata)."""
    score = stream.Score()
    for name, events in zip(instrument.VOICE_NAMES, voices):
        part = stream.Part(id=name)
        for onset, midi, duration, fermata in events:
            element = note.Note(midi, quarterLength=duration)
            if fermata:
                element.expressions.append(expressions.Fermata())
            part.insert(onset, element)
        score.insert(0, part)
    return score


def held(midi, duration=4):
    return [(0, midi, duration, False)]


def main():
    sustained = score_from_events([held(p) for p in (72, 55, 52, 48)])
    repeated = score_from_events([
        [(i, p, 1, False) for i in range(4)] for p in (72, 55, 52, 48)
    ])
    fermata = score_from_events([
        [(0, 72, 4, True)],
        [(i, p, 1, False) for i, p in enumerate((65, 67, 69, 71))],
        [(i, p, 1, False) for i, p in enumerate((58, 60, 62, 64))],
        held(48),
    ])
    gap = score_from_events([
        [(0, 72, 1, False), (2, 74, 1, False)],
        [(0, 65, 1, False), (2, 67, 1, False)],
        held(60, 3),
        held(48, 3),
    ])
    empty_alto = score_from_events([held(72), [], held(60), held(48)])
    long_bass = score_from_events([held(72), held(65), held(60), held(48, 8)])

    def evaluate(score, exclude=False):
        return instrument.evaluate_score(
            score, measures=1, exclude_fermata_motion=exclude
        )

    def qc(score):
        ok, reasons = instrument.quality_check(score, melody_part=score.parts[0])
        return {"accepted": ok, "reasons": reasons}

    report = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "synthetic implementation probes, not pilot or main model data",
        "instrument_version": instrument.INSTRUMENT_VERSION,
        "instrument_sha256": hashlib.sha256(
            (ROOT / "research/voice_leading_v2.py").read_bytes()
        ).hexdigest(),
        "music21_version": music21.__version__,
        "units": "quarterLength beats; all measurements use one explicit measure",
        "scenarios": {
            "sustained_versus_reattacked": {
                "description": "Same sounding pitch sequence and duration, different attacks.",
                "sustained": evaluate(sustained),
                "reattacked": evaluate(repeated),
            },
            "motion_during_soprano_fermata": {
                "description": "Three ascending parallel fifths in A-T during a held soprano fermata.",
                "main": evaluate(fermata),
                "exclude_fermata_motion": evaluate(fermata, True),
            },
            "motion_across_silent_gap": {
                "description": "S-A fifths separated by one silent beat in both voices.",
                "measurement": evaluate(gap),
            },
            "empty_alto": {"quality_check": qc(empty_alto)},
            "bass_longer_than_melody": {
                "soprano_duration_beats": 4,
                "bass_duration_beats": 8,
                "quality_check": qc(long_bass),
            },
        },
    }
    destination = Path(__file__).with_name("probe-results.json")
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "saved": str(destination.relative_to(ROOT)),
        "spacing_sustained": report["scenarios"]["sustained_versus_reattacked"]["sustained"]["counts"]["spacing"],
        "spacing_reattacked": report["scenarios"]["sustained_versus_reattacked"]["reattacked"]["counts"]["spacing"],
        "fermata_main_fifths": report["scenarios"]["motion_during_soprano_fermata"]["main"]["counts"]["parallel_fifths"],
        "fermata_filtered_fifths": report["scenarios"]["motion_during_soprano_fermata"]["exclude_fermata_motion"]["counts"]["parallel_fifths"],
        "gap_fifths": report["scenarios"]["motion_across_silent_gap"]["measurement"]["counts"]["parallel_fifths"],
        "empty_alto_accepted": qc(empty_alto)["accepted"],
        "long_bass_accepted": qc(long_bass)["accepted"],
    }, indent=2))


if __name__ == "__main__":
    main()

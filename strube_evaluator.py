"""
Strube Harmonic Evaluation Framework
Evaluates 4-voice SATB MIDI output against Gustav Strube's functional harmony rules.
Criteria implemented:
  1. Parallel Fifths detection
  2. Parallel Octaves detection
  3. Leading Tone Resolution (checks scale degree 7 → 8)
"""

import music21
from music21 import converter, stream, interval, note, chord
from pathlib import Path
import pandas as pd

import json

def load_midi_as_satb(midi_path: str) -> list[stream.Part]:
    """
    Load a MIDI file and return a list of 4 Part objects [S, A, T, B].
    Tries automatic voice separation first, falls back to track-based.
    """
    score = converter.parse(midi_path)
    score = score.quantize([0.25], processOffsets=True, processDurations=True)

    parts = list(score.parts)

    if len(parts) >= 4:
        return parts[:4]  # Take first 4 parts as S, A, T, B
    elif len(parts) == 1:
        # Monophonic or single-track — attempt chordify then voice split
        chordified = score.chordify()
        voices = chordified.voiceLeading
        # Fallback: return the single part 4x (will score zero violations, flag it)
        return [parts[0]] * 4
    else:
        # Pad with available parts
        while len(parts) < 4:
            parts.append(parts[-1])
        return parts[:4]

def get_notes_at_offsets(part: stream.Part) -> dict[float, int]:
    """Return {offset: midi_pitch} for all notes in a Part."""
    result = {}
    for n in part.flatten().notes:
        if isinstance(n, note.Note):
            result[float(n.offset)] = n.pitch.midi
        elif isinstance(n, chord.Chord):
            result[float(n.offset)] = n.sortAscending().pitches[-1].midi
    return result

def _interval_class(midi_a: int, midi_b: int) -> int:
    """Return the interval class (0-6) for two MIDI pitches.
    Interval class is the smaller of the two complementary intervals mod 12.
    For example: C4-G3 = 5 semitones up or 7 down → interval class = 5.
    But for parallel fifth detection we need to check against specific targets.
    """
    diff = abs(midi_a - midi_b) % 12
    return min(diff, 12 - diff)

def _is_target_interval(midi_a: int, midi_b: int, target_semitones: int) -> bool:
    """Check if two pitches form the target interval.

    A perfect fifth (7 semitones) shows up as abs diff 7 OR 5 (its complement).
    An octave/unison (0 semitones mod 12) is simply diff % 12 == 0.
    """
    diff = abs(midi_a - midi_b) % 12
    if target_semitones == 7:  # perfect fifth
        return diff == 7 or diff == 5  # fifth up or fourth down (same interval class)
    elif target_semitones == 12 or target_semitones == 0:  # octave/unison
        return diff == 0
    else:
        return diff == target_semitones or diff == (12 - target_semitones)

def check_parallel_motion(part_a: stream.Part, part_b: stream.Part,
                           interval_semitones: int) -> list[dict]:
    """
    Detect parallel motion for a given interval (7 = fifth, 12 = octave).
    Returns list of violation dicts with offset info.
    """
    notes_a = get_notes_at_offsets(part_a)
    notes_b = get_notes_at_offsets(part_b)

    common_offsets = sorted(set(notes_a.keys()) & set(notes_b.keys()))
    violations = []

    for i in range(len(common_offsets) - 1):
        t1, t2 = common_offsets[i], common_offsets[i + 1]
        try:
            p_a1, p_a2 = notes_a[t1], notes_a[t2]
            p_b1, p_b2 = notes_b[t1], notes_b[t2]
        except KeyError:
            continue

        # Check if both timepoints have the target interval
        if (_is_target_interval(p_a1, p_b1, interval_semitones) and
                _is_target_interval(p_a2, p_b2, interval_semitones)):
            # Both voices must move in the same direction (parallel motion)
            dir_a = p_a2 - p_a1
            dir_b = p_b2 - p_b1
            # Both must actually move (not static) and in same direction
            if dir_a != 0 and dir_b != 0 and (
                    (dir_a > 0 and dir_b > 0) or (dir_a < 0 and dir_b < 0)):
                ivl_name = "parallel_fifth" if interval_semitones == 7 else "parallel_octave"
                violations.append({

                    "type": ivl_name,
                    "offset": t1,
                    "voice_a_pitches": [p_a1, p_a2],
                    "voice_b_pitches": [p_b1, p_b2],
                })

    return violations

def check_leading_tone_resolution(soprano: stream.Part,
                                  key_midi_tonic: int = 60) -> list[dict]:
    """
    Check that scale degree 7 (leading tone) resolves upward to tonic (degree 8/1).
    key_midi_tonic: MIDI pitch of tonic (default 60 = C4, but we use mod 12).
    Leading tone = tonic - 1 semitone.
    """
    leading_tone_pc = (key_midi_tonic - 1) % 12
    tonic_pc = key_midi_tonic % 12

    notes = [(float(n.offset), n.pitch.midi)
             for n in soprano.flatten().notes
             if isinstance(n, note.Note)]
    notes.sort()

    violations = []
    for i in range(len(notes) - 1):
        offset, pitch = notes[i]
        next_offset, next_pitch = notes[i + 1]
        if pitch % 12 == leading_tone_pc:
            expected = (leading_tone_pc + 1) % 12  # should resolve up to tonic
            if next_pitch % 12 != expected:
                violations.append({
                    "type": "leading_tone_violation",
                    "offset": offset,
                    "leading_tone_midi": pitch,
                    "resolved_to_midi": next_pitch,
                    "expected_pc": expected,
                })
    return violations

def evaluate_satb(midi_path: str, key_tonic_pc: int = None) -> dict:
    """
    Main evaluation function. Returns full report dict.
    key_tonic_pc: pitch class of tonic (0=C, 2=D, 4=E, 5=F, 7=G, 9=A, 11=B)
    If None, dynamically detects the key using music21's key analyzer.
    """
    if key_tonic_pc is None:
        try:
            score = converter.parse(midi_path)
            analyzed_key = score.analyze('key')

            key_tonic_pc = analyzed_key.tonic.pitchClass
        except Exception:
            key_tonic_pc = 0  # Fallback to C

    parts = load_midi_as_satb(midi_path)
    s, a, t, b = parts[0], parts[1], parts[2], parts[3]

    voice_pairs = [
        ("S-A", s, a), ("S-T", s, t), ("S-B", s, b),
        ("A-T", a, t), ("A-B", a, b), ("T-B", t, b),
    ]

    all_p5 = []
    all_p8 = []

    for label, va, vb in voice_pairs:
        p5 = check_parallel_motion(va, vb, 7)
        p8 = check_parallel_motion(va, vb, 12)
        for v in p5:
            v["voice_pair"] = label
        for v in p8:
            v["voice_pair"] = label
        all_p5.extend(p5)
        all_p8.extend(p8)

    lt_violations = check_leading_tone_resolution(s, key_midi_tonic=key_tonic_pc + 60)

    # Estimate total vertical moments (chord slots)
    soprano_notes = list(s.flatten().notes)
    total_moments = max(len(soprano_notes), 1)

    report = {
        "file": str(midi_path),
        "total_moments": total_moments,
        "parallel_fifths": {
            "count": len(all_p5),
            "rate": round(len(all_p5) / total_moments, 4),
            "violations": all_p5,
        },
        "parallel_octaves": {
            "count": len(all_p8),
            "rate": round(len(all_p8) / total_moments, 4),
            "violations": all_p8,
        },
        "leading_tone_violations": {
            "count": len(lt_violations),
            "violations": lt_violations,
        },
        "strube_score": round(
            1.0 - min(1.0, (len(all_p5) + len(all_p8) + len(lt_violations)) / total_moments),
            4
        ),
    }
    return report

def batch_evaluate(midi_dir: str, output_csv: str = "results.csv",
                   key_tonic_pc: int = 0):
    """Evaluate all MIDI files in a directory, save results to CSV."""

    midi_files = list(Path(midi_dir).glob("*.mid")) + list(Path(midi_dir).glob("*.midi"))
    rows = []
    for f in sorted(midi_files):
        print(f"  Evaluating: {f.name}")
        try:
            r = evaluate_satb(str(f), key_tonic_pc=key_tonic_pc)
            rows.append({
                "file": f.name,
                "total_moments": r["total_moments"],
                "parallel_fifths": r["parallel_fifths"]["count"],
                "p5_rate": r["parallel_fifths"]["rate"],
                "parallel_octaves": r["parallel_octaves"]["count"],
                "p8_rate": r["parallel_octaves"]["rate"],
                "leading_tone_violations": r["leading_tone_violations"]["count"],
                "strube_score": r["strube_score"],
            })
        except Exception as e:
            print(f"    ERROR: {e}")
            rows.append({"file": f.name, "error": str(e)})

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"\nSaved results to {output_csv}")
    print(df.to_string())
    return df

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python strube_evaluator.py <midi_file_or_dir> [key_tonic_pc]")
        sys.exit(1)
    path = sys.argv[1]
    tonic = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    p = Path(path)
    if p.is_dir():
        batch_evaluate(str(p), output_csv=str(p / "strube_results.csv"), key_tonic_pc=tonic)
    else:
        import json
        r = evaluate_satb(str(p), key_tonic_pc=tonic)
        print(json.dumps(r, indent=2))

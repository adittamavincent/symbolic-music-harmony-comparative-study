"""
Face validity tests for the Strube Harmonic Evaluation Framework.

Tests:
  1. Real Bach chorale (BWV 66.6) from music21 corpus → should score HIGH (few violations)
  2. Deliberately wrong harmonization with parallel fifths → should score LOW
  3. Parallel octaves detection test
  4. Leading tone resolution detection test
"""

import sys
import os
import tempfile

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from music21 import corpus, note, stream
from strube_evaluator import (
    evaluate_satb,
    check_parallel_motion,
    check_leading_tone_resolution,
)

def test_bach_chorale():
    """Test 1: Real Bach Chorale (bwv66.6) should score HIGH."""
    print("=== TEST 1: Real Bach Chorale (bwv66.6) ===")
    bwv = corpus.parse('bach/bwv66.6')
    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
        bwv.write('midi', fp=f.name)
        tmp = f.name

    try:
        r = evaluate_satb(tmp, key_tonic_pc=0)
        print(f"  Strube Score:       {r['strube_score']}")
        print(f"  Total Moments:      {r['total_moments']}")
        print(f"  Parallel Fifths:    {r['parallel_fifths']['count']} (rate: {r['parallel_fifths']['rate']})")
        print(f"  Parallel Octaves:   {r['parallel_octaves']['count']} (rate: {r['parallel_octaves']['rate']})")
        print(f"  LT Violations:      {r['leading_tone_violations']['count']}")

        # Bach should have relatively few violations per moment

        assert r['strube_score'] > 0.0, "Bach chorale should have a positive Strube score"
        print("  ✓ PASS — Bach chorale scores positively")
        return True
    finally:
        os.unlink(tmp)

def test_deliberate_parallel_fifths():
    """Test 2: Deliberately Wrong Harmonization with parallel fifths → should score LOW."""
    print("\n=== TEST 2: Deliberately Wrong (forced parallel fifths) ===")

    s = stream.Score()
    soprano = stream.Part(id='Soprano')
    bass = stream.Part(id='Bass')
    alto = stream.Part(id='Alto')
    tenor = stream.Part(id='Tenor')

    # 8 chords all moving in parallel fifths upward
    soprano_pitches = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    bass_pitches = ['G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F#4', 'G4']
    alto_pitches = ['E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5']
    tenor_pitches = ['G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F#4', 'G4']

    for i in range(8):
        ns = note.Note(soprano_pitches[i])
        ns.offset = i
        soprano.append(ns)

        nb = note.Note(bass_pitches[i])
        nb.offset = i
        bass.append(nb)

        na = note.Note(alto_pitches[i])
        na.offset = i
        alto.append(na)

        nt = note.Note(tenor_pitches[i])
        nt.offset = i
        tenor.append(nt)

    s.append(soprano)
    s.append(alto)
    s.append(tenor)
    s.append(bass)

    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
        s.write('midi', fp=f.name)
        tmp = f.name

    try:
        r = evaluate_satb(tmp, key_tonic_pc=0)
        print(f"  Strube Score:       {r['strube_score']}")
        print(f"  Parallel Fifths:    {r['parallel_fifths']['count']}")
        print(f"  Parallel Octaves:   {r['parallel_octaves']['count']}")
        print(f"  LT Violations:      {r['leading_tone_violations']['count']}")

        assert r['parallel_fifths']['count'] > 0, "Expected parallel fifths in bad harmonization!"
        print("  ✓ PASS — parallel fifths detected in bad harmonization")
        return True
    finally:
        os.unlink(tmp)

def test_parallel_octaves_unit():
    """Test 3: Unit test for parallel octaves detection."""
    print("\n=== TEST 3: Parallel Octaves Unit Test ===")

    # Two voices moving in parallel octaves: C4-C3 → D4-D3
    va = stream.Part()
    vb = stream.Part()

    n1a = note.Note('C4')
    n1a.offset = 0
    va.append(n1a)
    n2a = note.Note('D4')
    n2a.offset = 1
    va.append(n2a)

    n1b = note.Note('C3')
    n1b.offset = 0
    vb.append(n1b)
    n2b = note.Note('D3')
    n2b.offset = 1
    vb.append(n2b)

    violations = check_parallel_motion(va, vb, 12)
    print(f"  Parallel octave violations found: {len(violations)}")
    assert len(violations) == 1, f"Expected 1 parallel octave, got {len(violations)}"
    assert violations[0]['type'] == 'parallel_octave'
    print("  ✓ PASS — parallel octave detected correctly")
    return True

def test_leading_tone_resolution():
    """Test 4: Leading tone resolution detection."""
    print("\n=== TEST 4: Leading Tone Resolution Test ===")

    soprano = stream.Part()

    # B4 (leading tone in C major) resolving DOWN to A4 — VIOLATION
    n1 = note.Note('B4')
    n1.offset = 0
    soprano.append(n1)

    n2 = note.Note('A4')
    n2.offset = 1
    soprano.append(n2)

    # B4 resolving UP to C5 — CORRECT (no violation)
    n3 = note.Note('B4')
    n3.offset = 2
    soprano.append(n3)

    n4 = note.Note('C5')
    n4.offset = 3
    soprano.append(n4)

    violations = check_leading_tone_resolution(soprano, key_midi_tonic=60)  # C major
    print(f"  Leading tone violations found: {len(violations)}")
    assert len(violations) == 1, f"Expected 1 LT violation, got {len(violations)}"

    assert violations[0]['offset'] == 0.0, "Violation should be at offset 0 (B→A)"
    print("  ✓ PASS — leading tone violation detected correctly (B→A is bad, B→C is good)")
    return True

def main():
    print("=" * 60)
    print("STRUBE EVALUATOR — FACE VALIDITY TESTS")
    print("=" * 60)

    results = []
    results.append(("Bach Chorale", test_bach_chorale()))
    results.append(("Parallel Fifths", test_deliberate_parallel_fifths()))
    results.append(("Parallel Octaves", test_parallel_octaves_unit()))
    results.append(("Leading Tone", test_leading_tone_resolution()))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_pass = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} — {name}")
        if not passed:
            all_pass = False

    if all_pass:
        print("\n✓ All face validity tests PASSED")
    else:
        print("\n✗ Some tests FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()

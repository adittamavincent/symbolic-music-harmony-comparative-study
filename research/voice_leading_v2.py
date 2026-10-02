"""Voice-leading instrument, version 2 (research/protocol.md, protocol version 2).

Counts five voice-leading violations in a four-voice (S, A, T, B) score:
parallel fifths, parallel octaves/unisons, upper-voice spacing, crossing above
the soprano, and voice overlap. Definitions follow BAB III of the v3 thesis and
the "Instrument version 2" section of the protocol, with rule wording and
exceptions from Strube (1928): parallels pp. 9 and 12 (contrary motion is not
objectionable), spacing p. 20, crossing p. 174 (occasional crossing is allowed,
not over the soprano), overlap pp. 12-13 (acceptable when one voice moves
stepwise). Version 1 lives unchanged in strube_evaluator.py as the historical
instrument.

Time is read on a sixteenth-note grid. For each voice pair, an event is a grid
step where at least one of the two voices starts a new note. Motion rules
compare consecutive events of a pair where both voices sound at both events.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise

from music21 import chord, expressions, note, stream, voiceLeading

INSTRUMENT_VERSION = "2.0"
GRID = Fraction(1, 4)  # quarterLength of a sixteenth note
VOICE_NAMES = ("S", "A", "T", "B")
ALL_PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
ADJACENT_PAIRS = ((0, 1), (1, 2), (2, 3))
SPACING_PAIRS = ((0, 1), (1, 2))
SOPRANO_PAIRS = ((0, 1), (0, 2), (0, 3))

# Yan et al. (2018) rubric weights: category 3 (parallels) = 1;
# categories 9 (spacing), 10 (crossing), 11 (overlap) = 0.5.
YAN_WEIGHTS = {
    "parallel_fifths": 1.0,
    "parallel_octaves": 1.0,
    "spacing": 0.5,
    "crossing": 0.5,
    "overlap": 0.5,
}
RULES = tuple(YAN_WEIGHTS)
MOTION_RULES = ("parallel_fifths", "parallel_octaves", "overlap")


class QualityError(ValueError):
    """The score cannot be measured: wrong voice count, polyphony, or off-grid timing."""


@dataclass
class VoiceGrid:
    """Sounding pitch of one voice at each sixteenth-note step."""

    midi: list  # int or None (rest) per step
    pitch: list  # music21 Pitch or None per step, keeps spelling when the source has it
    onset: list  # True where a new note starts
    fermata: list  # True while a note carrying a fermata sounds

    def __len__(self):
        return len(self.midi)


def _to_steps(quarter_length, what):
    value = Fraction(quarter_length).limit_denominator(1024)
    steps = value / GRID
    if steps.denominator != 1:
        raise QualityError(f"{what} {float(value)} is not on the sixteenth-note grid")
    return int(steps)


def grid_from_part(part, n_steps=None):
    """Convert one part to a VoiceGrid. Raises QualityError for chords, overlaps, or off-grid notes."""
    flat = part.stripTies().flatten()
    notes = list(flat.notes)
    end = 0
    for element in notes:
        if isinstance(element, chord.Chord):
            raise QualityError("a voice sounds more than one note at once")
        start = _to_steps(element.offset, "onset")
        length = _to_steps(element.quarterLength, "duration")
        if length == 0:
            raise QualityError("zero-duration (grace) note")
        end = max(end, start + length)
    total = n_steps if n_steps is not None else end
    grid = VoiceGrid([None] * total, [None] * total, [False] * total, [False] * total)
    for element in notes:
        start = _to_steps(element.offset, "onset")
        stop = min(start + _to_steps(element.quarterLength, "duration"), total)
        if start >= total:
            continue
        if any(grid.midi[step] is not None for step in range(start, stop)):
            raise QualityError("notes overlap within one voice")
        has_fermata = any(isinstance(e, expressions.Fermata) for e in element.expressions)
        for step in range(start, stop):
            grid.midi[step] = element.pitch.midi
            grid.pitch[step] = element.pitch
            grid.fermata[step] = has_fermata
        grid.onset[start] = True
    return grid


def score_grids(score):
    """Return four VoiceGrids (S, A, T, B) of equal length. Parts must already be in SATB order."""
    parts = list(score.parts)
    if len(parts) != 4:
        raise QualityError(f"expected 4 voices, found {len(parts)}")
    provisional = [grid_from_part(p) for p in parts]
    total = max(len(g) for g in provisional)
    return [grid_from_part(p, total) for p in parts]


def count_measures(part):
    """Number of notated measures; a pickup measure counts as one."""
    measures = part.getElementsByClass(stream.Measure)
    return len(measures)


def _pair_events(grids, i, j):
    return [t for t in range(len(grids[i])) if grids[i].onset[t] or grids[j].onset[t]]


def _sounding(grids, i, j, t):
    return grids[i].midi[t] is not None and grids[j].midi[t] is not None


def _sign(x):
    return (x > 0) - (x < 0)


def _is_parallel(grids, i, j, prev, t, target):
    pi0, pi1 = grids[i].midi[prev], grids[i].midi[t]
    pj0, pj1 = grids[j].midi[prev], grids[j].midi[t]
    if abs(pi0 - pj0) % 12 != target or abs(pi1 - pj1) % 12 != target:
        return False
    di, dj = pi1 - pi0, pj1 - pj0
    return di != 0 and _sign(di) == _sign(dj)


def _is_step(grid, prev, t):
    return abs(grid.midi[t] - grid.midi[prev]) in (1, 2)


def _is_overlap_raw(grids, i, j, prev, t):
    """music21-equivalent overlap test, before excluding crossed events."""
    return grids[j].midi[t] > grids[i].midi[prev] or grids[i].midi[t] < grids[j].midi[prev]


def _motions(grids, i, j):
    """Yield (prev, t) for consecutive pair events where both voices sound at both events."""
    events = _pair_events(grids, i, j)
    for prev, t in pairwise(events):
        if _sounding(grids, i, j, prev) and _sounding(grids, i, j, t):
            yield prev, t


def evaluate_grids(grids, measures, exclude_fermata_motion=False):
    """Count violations, opportunities, and per-measure rates.

    exclude_fermata_motion drops motions that start on a soprano note with a
    fermata (phrase-boundary sensitivity count). Vertical rules are unaffected.
    """
    if measures < 1:
        raise QualityError("measure count must be at least 1")
    counts = {rule: 0 for rule in RULES}
    opportunities = {rule: 0 for rule in RULES}
    flags = []

    def flag(rule, i, j, t):
        counts[rule] += 1
        flags.append({
            "rule": rule,
            "pair": f"{VOICE_NAMES[i]}-{VOICE_NAMES[j]}",
            "step": t,
            "offset_ql": float(t * GRID),
        })

    soprano = grids[0]
    for i, j in ALL_PAIRS:
        for prev, t in _motions(grids, i, j):
            if exclude_fermata_motion and soprano.fermata[prev]:
                continue
            opportunities["parallel_fifths"] += 1
            opportunities["parallel_octaves"] += 1
            if _is_parallel(grids, i, j, prev, t, 7):
                flag("parallel_fifths", i, j, t)
            if _is_parallel(grids, i, j, prev, t, 0):
                flag("parallel_octaves", i, j, t)

    for i, j in SPACING_PAIRS:
        for t in _pair_events(grids, i, j):
            if _sounding(grids, i, j, t):
                opportunities["spacing"] += 1
                if grids[i].midi[t] - grids[j].midi[t] > 12:
                    flag("spacing", i, j, t)

    # Strube p. 174: occasional crossing is allowed, but not over the soprano.
    for i, j in SOPRANO_PAIRS:
        for t in _pair_events(grids, i, j):
            if _sounding(grids, i, j, t):
                opportunities["crossing"] += 1
                if grids[i].midi[t] - grids[j].midi[t] < 0:
                    flag("crossing", i, j, t)

    # Strube pp. 12-13: overlap is acceptable when one of the two voices moves stepwise.
    for i, j in ADJACENT_PAIRS:
        for prev, t in _motions(grids, i, j):
            if exclude_fermata_motion and soprano.fermata[prev]:
                continue
            opportunities["overlap"] += 1
            crossed_now = grids[i].midi[t] - grids[j].midi[t] < 0
            stepwise = _is_step(grids[i], prev, t) or _is_step(grids[j], prev, t)
            if _is_overlap_raw(grids, i, j, prev, t) and not crossed_now and not stepwise:
                flag("overlap", i, j, t)

    rates = {rule: counts[rule] / measures for rule in RULES}
    weighted = sum(YAN_WEIGHTS[rule] * counts[rule] for rule in RULES) / measures
    return {
        "instrument_version": INSTRUMENT_VERSION,
        "measures": measures,
        "counts": counts,
        "opportunities": opportunities,
        "rates_per_measure": rates,
        "weighted_penalty_per_measure": weighted,
        "flags": flags,
    }


def evaluate_score(score, measures=None, exclude_fermata_motion=False):
    """Evaluate a parsed four-part score. Measures default to the soprano's notated measures."""
    grids = score_grids(score)
    if measures is None:
        measures = count_measures(score.parts[0])
    return evaluate_grids(grids, measures, exclude_fermata_motion)


def soprano_matches(output_grids, melody_grid):
    """True when the output soprano keeps the given melody's pitches and onsets."""
    soprano = output_grids[0]
    if len(soprano) < len(melody_grid):
        return False
    for t in range(len(melody_grid)):
        if soprano.midi[t] != melody_grid.midi[t] or soprano.onset[t] != melody_grid.onset[t]:
            return False
    return True


def quality_check(score, melody_part=None):
    """Return (ok, reasons) for the protocol's quality-control rules."""
    try:
        grids = score_grids(score)
    except QualityError as error:
        return False, [str(error)]
    reasons = []
    if melody_part is not None:
        melody_grid = grid_from_part(melody_part)
        if not soprano_matches(grids, melody_grid):
            reasons.append("soprano differs from the input melody")
    return not reasons, reasons


def crosscheck_music21(grids):
    """Compare raw motion predicates with music21 VoiceLeadingQuartet.

    For every motion (all pairs for parallels; adjacent pairs for crossing and
    overlap) returns a 2x2 agreement table per check:
    {"both", "ours_only", "music21_only", "neither"}.
    This checks the shared geometric predicates, not the final rules: the
    overlap comparison uses the raw predicate (before the crossing and stepwise
    exclusions), and crossing compares "crossed at either event" on adjacent
    pairs because that is music21's definition. music21's parallelFifth and
    parallelUnisonOrOctave also accept fifths/octaves reached by contrary motion
    (octave displacement), which Strube (p. 9) does not object to.
    """
    tables = {name: {"both": 0, "ours_only": 0, "music21_only": 0, "neither": 0}
              for name in ("parallel_fifths", "parallel_octaves", "crossing", "overlap")}

    def record(name, ours, theirs):
        key = "both" if ours and theirs else "ours_only" if ours else "music21_only" if theirs else "neither"
        tables[name][key] += 1

    def quartet(i, j, prev, t):
        return voiceLeading.VoiceLeadingQuartet(
            note.Note(grids[i].pitch[prev]), note.Note(grids[i].pitch[t]),
            note.Note(grids[j].pitch[prev]), note.Note(grids[j].pitch[t]))

    for i, j in ALL_PAIRS:
        for prev, t in _motions(grids, i, j):
            vlq = quartet(i, j, prev, t)
            record("parallel_fifths", _is_parallel(grids, i, j, prev, t, 7), vlq.parallelFifth())
            record("parallel_octaves", _is_parallel(grids, i, j, prev, t, 0), vlq.parallelUnisonOrOctave())
            if (i, j) in ADJACENT_PAIRS:
                crossed = (grids[i].midi[prev] < grids[j].midi[prev]
                           or grids[i].midi[t] < grids[j].midi[t])
                record("crossing", crossed, vlq.voiceCrossing())
                record("overlap", _is_overlap_raw(grids, i, j, prev, t), vlq.voiceOverlap())
    return tables

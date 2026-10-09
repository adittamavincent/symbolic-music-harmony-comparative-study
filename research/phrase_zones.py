"""Phrase zones for protocol version 3.0, research question 3.

Strube treats the fermata as a cadence (1928, p. 174). This module sorts the
flags and opportunities of instrument v2.0 into two zones:

- F (fermata zone): a motion whose start or arrival step lies inside a soprano
  note carrying a fermata (parallel fifths, parallel octaves, overlap); for the
  vertical rules (spacing, crossing), an event inside such a note;
- I (inside the phrase): everything else.

The instrument decides what counts as a violation and an opportunity; this
module only records where each one falls, so the instrument version stays 2.0.
Opportunities are enumerated exactly as in `voice_leading_v2.evaluate_grids`
(main count, no fermata exclusion), so the two zones always add up to the
instrument's totals.
"""

import voice_leading_v2 as vl

ZONES = ("F", "I")
MOTION_RULES = ("parallel_fifths", "parallel_octaves", "overlap")


def motion_zone(soprano, prev, t):
    return "F" if soprano.fermata[prev] or soprano.fermata[t] else "I"


def event_zone(soprano, t):
    return "F" if soprano.fermata[t] else "I"


def zone_counts(grids, flags):
    """Flags and opportunities per rule and zone, and the zone of each flag.

    grids: the four VoiceGrids that were measured; flags: the flag list of the
    main-count result of `evaluate_grids` on the same grids. Returns
    ({rule: {"F": [flags, opportunities], "I": [flags, opportunities]}}, [zone per flag]).
    """
    soprano = grids[0]
    counts = {rule: {zone: [0, 0] for zone in ZONES} for rule in vl.RULES}
    previous = {}
    for i, j in vl.ALL_PAIRS:
        for prev, t in vl._motions(grids, i, j):
            previous[(i, j, t)] = prev
            zone = motion_zone(soprano, prev, t)
            counts["parallel_fifths"][zone][1] += 1
            counts["parallel_octaves"][zone][1] += 1
    for i, j in vl.ADJACENT_PAIRS:
        for prev, t in vl._motions(grids, i, j):
            counts["overlap"][motion_zone(soprano, prev, t)][1] += 1
    for rule, pairs in (("spacing", vl.SPACING_PAIRS), ("crossing", vl.SOPRANO_PAIRS)):
        for i, j in pairs:
            for t in vl._pair_events(grids, i, j):
                if vl._sounding(grids, i, j, t):
                    counts[rule][event_zone(soprano, t)][1] += 1
    flag_zones = []
    for flag in flags:
        i, j = (vl.VOICE_NAMES.index(v) for v in flag["pair"].split("-"))
        t = flag["step"]
        if flag["rule"] in MOTION_RULES:
            zone = motion_zone(soprano, previous[(i, j, t)], t)
        else:
            zone = event_zone(soprano, t)
        counts[flag["rule"]][zone][0] += 1
        flag_zones.append(zone)
    return counts, flag_zones


def zone_columns(counts, prefix):
    """Flat columns `<prefix>_zone_<rule>_<F|I>_count` and `..._opportunities` for CSV rows."""
    row = {}
    for rule in vl.RULES:
        for zone in ZONES:
            row[f"{prefix}_zone_{rule}_{zone}_count"] = counts[rule][zone][0]
            row[f"{prefix}_zone_{rule}_{zone}_opportunities"] = counts[rule][zone][1]
    return row

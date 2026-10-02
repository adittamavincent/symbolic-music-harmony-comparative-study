"""Validation checks 3-5 for the version 2 instrument on the music21 Bach chorales.

3. Cross-implementation check against music21 VoiceLeadingQuartet (shared
   geometric predicates; music21 also accepts fifths/octaves by contrary motion).
4. Per-measure parallel fifth/octave rates compared with Huang et al. (2019, §6.3):
   0.023 P5 and 0.009 P8 per measure in 382 chorales (train + validation).
5. Reliability: two evaluation passes must give identical output.

Writes per-chorale rows, flags, and a summary to research/outputs/validation_v2/<UTC timestamp>/.
Run from the repository root: uv run python research/experiments/scripts/validate_instrument_v2.py
"""

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research"))

import music21
from music21 import corpus
from voice_leading_v2 import (
    INSTRUMENT_VERSION,
    RULES,
    QualityError,
    count_measures,
    crosscheck_music21,
    evaluate_grids,
    score_grids,
)

HUANG = {"parallel_fifths": 0.023, "parallel_octaves": 0.009}


def unison_flags(grids, flags):
    """Count parallel-octave flags whose interval is a unison at the flagged event."""
    names = "SATB"
    total = 0
    for f in flags:
        if f["rule"] != "parallel_octaves":
            continue
        i, j = (names.index(v) for v in f["pair"].split("-"))
        if grids[i].midi[f["step"]] == grids[j].midi[f["step"]]:
            total += 1
    return total


def run():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ROOT / "research" / "outputs" / "validation_v2" / stamp
    out.mkdir(parents=True, exist_ok=True)

    rows, excluded, flag_rows = [], [], []
    totals = {"measures": 0, "main": dict.fromkeys(RULES, 0), "fermata_excluded": dict.fromkeys(RULES, 0),
              "opportunities": dict.fromkeys(RULES, 0), "unison_octaves": 0}
    agreement = {}
    filenames = list(corpus.chorales.Iterator(returnType="filename"))
    for name in filenames:
        try:
            score = corpus.parse(name)
            grids = score_grids(score)
            measures = count_measures(score.parts[0])
            main = evaluate_grids(grids, measures)
            again = evaluate_grids(grids, measures)
            if json.dumps(main, sort_keys=True) != json.dumps(again, sort_keys=True):
                raise RuntimeError(f"non-deterministic result for {name}")
            sens = evaluate_grids(grids, measures, exclude_fermata_motion=True)
            cross = crosscheck_music21(grids)
        except QualityError as error:
            excluded.append({"chorale": name, "reason": str(error)})
            continue
        unisons = unison_flags(grids, main["flags"])
        totals["measures"] += measures
        totals["unison_octaves"] += unisons
        for rule in RULES:
            totals["main"][rule] += main["counts"][rule]
            totals["fermata_excluded"][rule] += sens["counts"][rule]
            totals["opportunities"][rule] += main["opportunities"][rule]
        for check, table in cross.items():
            agg = agreement.setdefault(check, dict.fromkeys(table, 0))
            for key, value in table.items():
                agg[key] += value
        row = {"chorale": name, "measures": measures, "unison_octaves": unisons}
        row.update({f"{r}_count": main["counts"][r] for r in RULES})
        row.update({f"{r}_count_fermata_excluded": sens["counts"][r] for r in RULES})
        rows.append(row)
        for f in main["flags"]:
            flag_rows.append({"chorale": name, **f})

    def write(path, data):
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)

    write(out / "per_chorale.csv", rows)
    write(out / "flags.csv", flag_rows)
    if excluded:
        write(out / "excluded.csv", excluded)

    m = totals["measures"]
    summary = {
        "instrument_version": INSTRUMENT_VERSION,
        "music21_version": music21.__version__,
        "corpus_files": len(filenames),
        "evaluated": len(rows),
        "excluded": len(excluded),
        "total_measures": m,
        "counts_main": totals["main"],
        "rates_per_measure_main": {r: totals["main"][r] / m for r in RULES},
        "counts_fermata_excluded": totals["fermata_excluded"],
        "rates_per_measure_fermata_excluded": {r: totals["fermata_excluded"][r] / m for r in RULES},
        "unison_share_of_parallel_octaves": totals["unison_octaves"],
        "parallel_octaves_without_unisons_rate": (totals["main"]["parallel_octaves"] - totals["unison_octaves"]) / m,
        "opportunities": totals["opportunities"],
        "huang2019_reference_rates": HUANG,
        "music21_agreement": agreement,
        "music21_definition_rates_per_measure": {
            "parallel_fifths": (agreement["parallel_fifths"]["both"] + agreement["parallel_fifths"]["music21_only"]) / m,
            "parallel_octaves": (agreement["parallel_octaves"]["both"] + agreement["parallel_octaves"]["music21_only"]) / m,
        },
        "per_chorale_sha256": hashlib.sha256((out / "per_chorale.csv").read_bytes()).hexdigest(),
        "flags_sha256": hashlib.sha256((out / "flags.csv").read_bytes()).hexdigest(),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    run()

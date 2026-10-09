"""Exploration on Bach's own harmonizations: where do instrument-v2 flags fall in the phrase?

Not study data. Counts the main-count flags and opportunities of instrument v2.0
inside and outside the fermata zone, for the eligible Bach melodies of the
protocol-2.1 frame (`research/outputs/melodies/manifest.csv`, built by
`make melodies`). Strube treats the fermata as a cadence (1928, p. 174).

Zones as defined in `research/phrase_zones.py` (protocol 3.0, question 3).

Run from the repository root:
    uv run python research/experiments/scripts/explore_fermata_zone_bach.py
Writes research/outputs/exploration/<UTC timestamp>/fermata_zone_bach.csv.
"""
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research"))

import voice_leading_v2 as vl
from music21 import corpus
from phrase_zones import ZONES, zone_counts

MANIFEST = ROOT / "research" / "outputs" / "melodies" / "manifest.csv"


def run():
    rows = [r for r in csv.DictReader(MANIFEST.open(encoding="utf-8"))
            if r["origin"] == "bach" and r["status"] == "eligible"]
    total = {rule: {"F": [0, 0], "I": [0, 0]} for rule in vl.RULES}
    for row in rows:
        score = corpus.parse(row["source"].removeprefix("music21 corpus "))
        grids = vl.score_grids(score)
        flags = vl.evaluate_grids(grids, vl.count_measures(score.parts[0]))["flags"]
        counts, _ = zone_counts(grids, flags)
        for rule in vl.RULES:
            for zone in ZONES:
                for k in (0, 1):
                    total[rule][zone][k] += counts[rule][zone][k]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ROOT / "research" / "outputs" / "exploration" / stamp
    out.mkdir(parents=True, exist_ok=True)
    fields = ["rule", "flags_F", "flags_I", "opportunities_F", "opportunities_I",
              "flag_share_F", "opportunity_share_F", "rate_F", "rate_I", "rate_ratio"]
    with (out / "fermata_zone_bach.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rule in vl.RULES:
            (fF, oF), (fI, oI) = total[rule]["F"], total[rule]["I"]
            rate_F, rate_I = fF / oF, fI / oI
            row = {"rule": rule, "flags_F": fF, "flags_I": fI, "opportunities_F": oF, "opportunities_I": oI,
                   "flag_share_F": round(fF / (fF + fI), 3) if fF + fI else "",
                   "opportunity_share_F": round(oF / (oF + oI), 3),
                   "rate_F": round(rate_F, 5), "rate_I": round(rate_I, 5),
                   "rate_ratio": round(rate_F / rate_I, 2) if rate_I else ""}
            writer.writerow(row)
            print(row)
    print(f"{len(rows)} melodies; written to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    run()

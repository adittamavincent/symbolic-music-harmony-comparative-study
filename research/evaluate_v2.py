"""Quality control and measurement of a protocol-version-2 run.

For every successful attempt in a run (generation_v2.py) this module checks the
output (quality control, protocol 2.1) and measures the five rules with
instrument version 2.0 in three ways:

- main: every occurrence, as defined in BAB III;
- fermata: motions that start while the soprano holds a fermata note are left
  out (sensitivity analysis a; the exclusion covers the whole fermata note,
  not only the move to the next phrase);
- merged: in every voice, consecutive steps with the same pitch count as one
  held note before measuring (sensitivity analysis d). Coconet output cannot
  show a repeated note, so this puts all sources on the same sounding
  representation.

Bach's own harmonization of each Bach melody in the run is measured the same
way as the reference. Results are written to <run>/evaluation/:

    qc.csv               one row per successful attempt: passed or the reasons
    per_generation.csv   counts, opportunities, and rates per variant and rule
    flags.csv            every main-count flag with measure number and beat
    bach_reference.csv   Bach's harmonizations of the run's Bach melodies
    per_melody.csv       mean rate per model x melody over generations that pass QC

Two descriptive columns serve open decisions in PROGRESS.md: `quarters` (melody
length in quarter notes, for rates per beat instead of per measure, decision 8)
and, on Bach melodies, `copy_share` (share of sounding steps where the model's
alto, tenor, and bass sound Bach's own pitch, a check on memorisation, decision 9).
"""

import csv
import json
from pathlib import Path

from harmonization_io import read_melody
from music21 import converter, corpus
from voice_leading_v2 import (
    GRID,
    RULES,
    YAN_WEIGHTS,
    QualityError,
    VoiceGrid,
    evaluate_grids,
    grid_from_part,
    score_grids,
    soprano_matches,
)

VARIANTS = ("main", "fermata", "merged")
VOICE_LABELS = ("soprano", "alto", "tenor", "bass")


def merge_repeats(grid):
    """Return a copy of a VoiceGrid in which a repeated equal pitch continues the previous note."""
    onset = list(grid.onset)
    for t in range(1, len(grid)):
        if onset[t] and grid.midi[t] is not None and grid.midi[t] == grid.midi[t - 1]:
            onset[t] = False
    return VoiceGrid(list(grid.midi), list(grid.pitch), onset, list(grid.fermata))


def quality_check_v2(grids, melody_grid):
    """Protocol 2.1 quality control. Returns a list of failure reasons (empty when the output passes)."""
    reasons = []
    if len(grids[0]) != len(melody_grid):
        reasons.append(f"output length {len(grids[0])} steps, melody {len(melody_grid)} steps")
    if not soprano_matches(grids, melody_grid):
        reasons.append("soprano differs from the input melody")
    for index in (1, 2, 3):
        if all(m is None for m in grids[index].midi):
            reasons.append(f"{VOICE_LABELS[index]} has no notes")
    return reasons


def measure_all(grids, measures):
    """Evaluate the three variants; returns {variant: result dict}."""
    merged = [merge_repeats(g) for g in grids]
    return {
        "main": evaluate_grids(grids, measures),
        "fermata": evaluate_grids(grids, measures, exclude_fermata_motion=True),
        "merged": evaluate_grids(merged, measures),
    }


def result_columns(results):
    row = {}
    for variant, result in results.items():
        for rule in RULES:
            row[f"{variant}_{rule}_count"] = result["counts"][rule]
            row[f"{variant}_{rule}_opportunities"] = result["opportunities"][rule]
            row[f"{variant}_{rule}_rate"] = result["rates_per_measure"][rule]
        row[f"{variant}_weighted_rate"] = result["weighted_penalty_per_measure"]
    return row


def copy_share(grids, reference):
    """Share of steps, over alto, tenor, and bass where Bach's voice sounds, with the model's pitch equal to Bach's."""
    same = total = 0
    for voice in (1, 2, 3):
        for model_pitch, bach_pitch in zip(grids[voice].midi, reference[voice].midi):
            if bach_pitch is None:
                continue
            total += 1
            same += int(model_pitch == bach_pitch)
    return same / total if total else ""


def location(melody, step):
    """Measure number and beat (quarter notes from the start of the measure, 1-based) of a grid step."""
    for info in melody.measures:
        if info.start <= step < info.start + info.length:
            offset = (step - info.start + info.padding_left) * GRID
            return info.number, float(offset) + 1
    return None, None


def _write(path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fieldnames or (list(rows[0]) if rows else [])
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def evaluate_run(run_dir, include_reference=True):
    run_dir = Path(run_dir)
    info = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    with open(run_dir / "melodies.csv", newline="", encoding="utf-8") as handle:
        melodies = {row["melody_id"]: row for row in csv.DictReader(handle)}
    attempts = [json.loads(line) for line in (run_dir / "attempts.jsonl").read_text(encoding="utf-8").splitlines()
                if line] if (run_dir / "attempts.jsonl").exists() else []
    parsed = {}

    def melody_of(melody_id):
        if melody_id not in parsed:
            row = melodies[melody_id]
            melody = read_melody(run_dir / row["musicxml_file"], melody_id)
            parsed[melody_id] = (melody, grid_from_part(converter.parse(str(run_dir / row["musicxml_file"])).parts[0]))
        return parsed[melody_id]

    references = {}

    def reference_of(melody_id):
        if melody_id not in references:
            name = melodies[melody_id]["source"].replace("music21 corpus ", "")
            references[melody_id] = score_grids(corpus.parse(name))
        return references[melody_id]

    qc_rows, generation_rows, flag_rows = [], [], []
    for entry in attempts:
        if entry["status"] != "ok":
            continue
        melody, melody_grid = melody_of(entry["melody_id"])
        base = {"run_id": info["run_id"], "model": entry["model"], "melody_id": entry["melody_id"],
                "origin": entry["origin"], "generation": entry["generation"], "attempt": entry["attempt"]}
        try:
            grids = score_grids(converter.parse(str(run_dir / entry["score_file"])))
            reasons = quality_check_v2(grids, melody_grid)
        except QualityError as error:
            grids, reasons = None, [str(error)]
        qc_rows.append({**base, "passed": int(not reasons), "reasons": "; ".join(reasons)})
        if reasons:
            continue
        results = measure_all(grids, melody.measure_count)
        extra = {"quarters": melody.total_steps / 4,
                 "copy_share": copy_share(grids, reference_of(entry["melody_id"]))
                 if include_reference and entry["origin"] == "bach" else ""}
        generation_rows.append({**base, "measures": melody.measure_count, **extra, **result_columns(results)})
        for flag in results["main"]["flags"]:
            number, beat = location(melody, flag["step"])
            flag_rows.append({**base, "rule": flag["rule"], "pair": flag["pair"], "step": flag["step"],
                              "measure": number, "beat": beat})

    out = run_dir / "evaluation"
    _write(out / "qc.csv", qc_rows, ["run_id", "model", "melody_id", "origin", "generation", "attempt", "passed",
                                     "reasons"])
    _write(out / "per_generation.csv", generation_rows)
    _write(out / "flags.csv", flag_rows, ["run_id", "model", "melody_id", "origin", "generation", "attempt", "rule",
                                         "pair", "step", "measure", "beat"])

    reference_rows = []
    if include_reference:
        for melody_id, row in melodies.items():
            if row["origin"] != "bach":
                continue
            melody, _ = melody_of(melody_id)
            results = measure_all(reference_of(melody_id), melody.measure_count)
            reference_rows.append({"run_id": info["run_id"], "model": "bach", "melody_id": melody_id,
                                   "origin": "bach", "measures": melody.measure_count,
                                   "quarters": melody.total_steps / 4, **result_columns(results)})
        _write(out / "bach_reference.csv", reference_rows)

    per_melody = aggregate(generation_rows, attempts, qc_rows, melodies, info.get("protocol", {}))
    _write(out / "per_melody.csv", per_melody)
    return {"qc": len(qc_rows), "measured": len(generation_rows), "flags": len(flag_rows),
            "reference": len(reference_rows), "melody_model_cells": len(per_melody)}


def aggregate(generation_rows, attempts, qc_rows, melodies, protocol):
    """Mean of each rate over generations that pass QC, per model x melody, with k of n recorded."""
    expected = protocol.get("generations_per_melody", 5)
    models = sorted({a["model"] for a in attempts})
    rate_columns = [c for c in (generation_rows[0] if generation_rows else {})
                    if c.endswith("_rate") or c == "copy_share"]
    rows = []
    for model in models:
        for melody_id, melody in melodies.items():
            valid = [r for r in generation_rows if r["model"] == model and r["melody_id"] == melody_id]
            tried = {(a["generation"]) for a in attempts if a["model"] == model and a["melody_id"] == melody_id}
            ineligible = any(a["status"] == "ineligible" for a in attempts
                             if a["model"] == model and a["melody_id"] == melody_id)
            row = {"model": model, "melody_id": melody_id, "origin": melody["origin"], "generations_expected": expected,
                   "generations_tried": len(tried), "generations_valid": len(valid), "ineligible": int(ineligible),
                   "all_valid": int(len(valid) == expected)}
            for column in rate_columns:
                values = [r[column] for r in valid if r[column] != ""]
                row[column] = sum(values) / len(values) if values else ""
            rows.append(row)
    return rows


def weighted_from_counts(counts, measures):
    return sum(YAN_WEIGHTS[rule] * counts[rule] for rule in RULES) / measures

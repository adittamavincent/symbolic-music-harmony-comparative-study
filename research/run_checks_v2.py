"""Completeness checks and discussion examples for a protocol-version-2 run.

check_run: compares the attempts with what the run should contain (melodies x
models x generations), verifies that every successful attempt's files exist and
match their recorded SHA-256, and that evaluation covered every successful
attempt. It returns a list of problems; an empty list means complete.

sample_examples: draws flagged events at random (recorded seed) for the
discussion in BAB IV and writes a short score excerpt around each one. The
examples illustrate context; they are not used to estimate how often anything
happens.
"""

import csv
import json
import random
from pathlib import Path

from generation_v2 import file_sha256
from music21 import converter


def check_run(run_dir, models, generations):
    run_dir = Path(run_dir)
    problems = []
    with open(run_dir / "melodies.csv", newline="", encoding="utf-8") as handle:
        melodies = [row["melody_id"] for row in csv.DictReader(handle)]
    attempts = [json.loads(line) for line in (run_dir / "attempts.jsonl").read_text(encoding="utf-8").splitlines()
                if line] if (run_dir / "attempts.jsonl").exists() else []
    final = {}
    for entry in attempts:
        key = (entry["model"], entry["melody_id"], entry["generation"])
        if key not in final or entry["attempt"] > final[key]["attempt"]:
            final[key] = entry
    for model in models:
        for melody_id in melodies:
            for generation in range(1, generations + 1):
                if (model, melody_id, generation) not in final:
                    problems.append(f"missing attempt: {model} {melody_id} g{generation}")
    ok = [e for e in final.values() if e["status"] == "ok"]
    for entry in ok:
        path = run_dir / entry["score_file"]
        if not path.exists():
            problems.append(f"missing score file: {entry['score_file']}")
        elif file_sha256(path) != entry["score_sha256"]:
            problems.append(f"score file changed after generation: {entry['score_file']}")
        if not (run_dir / entry["raw_file"]).exists():
            problems.append(f"missing raw output: {entry['raw_file']}")
    qc_path = run_dir / "evaluation" / "qc.csv"
    if ok and not qc_path.exists():
        problems.append("evaluation has not been run")
    elif ok:
        with open(qc_path, newline="", encoding="utf-8") as handle:
            checked = {(r["model"], r["melody_id"], int(r["generation"]), int(r["attempt"])) for r in csv.DictReader(handle)}
        for entry in ok:
            if (entry["model"], entry["melody_id"], entry["generation"], entry["attempt"]) not in checked:
                problems.append(f"not evaluated: {entry['model']} {entry['melody_id']} g{entry['generation']}")
    return problems


def sample_examples(run_dir, per_rule, seed, context_measures=1):
    run_dir = Path(run_dir)
    with open(run_dir / "evaluation" / "flags.csv", newline="", encoding="utf-8") as handle:
        flags = list(csv.DictReader(handle))
    attempts = {(e["model"], e["melody_id"], int(e["generation"]), int(e["attempt"])): e
                for e in (json.loads(line) for line in (run_dir / "attempts.jsonl").read_text(encoding="utf-8").splitlines() if line)}
    generator = random.Random(seed)
    chosen = []
    for rule in sorted({f["rule"] for f in flags}):
        pool = [f for f in flags if f["rule"] == rule]
        chosen.extend(generator.sample(pool, min(per_rule, len(pool))))
    out = run_dir / "examples"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, flag in enumerate(chosen, start=1):
        entry = attempts[(flag["model"], flag["melody_id"], int(flag["generation"]), int(flag["attempt"]))]
        score = converter.parse(str(run_dir / entry["score_file"]))
        measure = int(flag["measure"]) if flag["measure"] not in ("", "None") else None
        excerpt_file = ""
        if measure is not None:
            excerpt = score.measures(max(0, measure - context_measures), measure + context_measures)
            path = out / f"example_{index:02d}_{flag['rule']}.musicxml"
            excerpt.write("musicxml", fp=str(path))
            excerpt_file = path.name
        rows.append({**flag, "example": index, "seed": seed, "excerpt_file": excerpt_file})
    with open(out / "examples.csv", "w", newline="", encoding="utf-8") as handle:
        if rows:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    return rows

#!/usr/bin/env python3
"""Command line for the pipeline (protocol 3.0 by default; protocol 2.1 with --protocol). Run from the
repository root with uv.

Order of work (each step writes files the next step reads):

  templates   create one typing template per Strube melody candidate (protocol 2.1 only; kept as history)
  melodies    build the Bach frame (and convert typed Strube melodies, 2.1) -> research/outputs/melodies/manifest.csv
  preflight   check every eligible melody against both models' input encoding (needs make setup-v2)
  membership  estimate which Bach chorales DeepBach saw in training (needs make setup-v2)
  select      fix the main sample (3.0: seeded sample of 40 Bach melodies; 2.1: all eligible Strube melodies +
              a Bach sample of the same size) and the pilot set
  generate    run a stage: --stage pilot or --stage main (main refuses while the protocol is not frozen)
  evaluate    quality control and measurement of a run
  analyze     statistics, tables, and figures of a run
  examples    seeded score excerpts of flagged events for the discussion
  check       completeness check of a run (exit code 1 when anything is missing)
  dry-run     the whole chain on a few melodies with a fake backend, in a temporary folder; no model

Examples:
  uv run python research/experiments/scripts/v2.py melodies --update-inventory
  uv run python research/experiments/scripts/v2.py generate --stage pilot
  uv run python research/experiments/scripts/v2.py evaluate research/outputs/runs/pilot-20261010T0900Z
"""

import argparse
import csv
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RESEARCH))

import analysis_v2
import evaluate_v2
import generation_v2
import melody_sets
import run_checks_v2

MELODY_DIR = RESEARCH / "outputs" / "melodies"
MANIFEST = MELODY_DIR / "manifest.csv"
PREFLIGHT = MELODY_DIR / "preflight.csv"
MEMBERSHIP = MELODY_DIR / "deepbach_membership.csv"
SELECTION = {"main": MELODY_DIR / "selection_main.csv", "pilot": MELODY_DIR / "selection_pilot.csv"}
MODELS = ("deepbach", "coconet")


def stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%MZ")


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def cmd_templates(args, protocol):
    created = melody_sets.inventory_templates()
    print(f"Created {len(created)} templates in {melody_sets.STRUBE_TEXT_DIR}")


def cmd_melodies(args, protocol, out_dir=MELODY_DIR, text_dir=None, bach_limit=None):
    text_dir = Path(text_dir or RESEARCH.parent / protocol["melodies"]["strube_text_dir"])
    bach = melody_sets.build_bach_frame(out_dir, limit=bach_limit or getattr(args, "bach_limit", None))
    strube = melody_sets.build_strube_set(out_dir, text_dir)
    melody_sets.mark_cross_duplicates(bach, strube)
    path = melody_sets.write_manifest(bach + strube, out_dir / "manifest.csv")
    for origin, records in (("bach", bach), ("strube", strube)):
        counts = {}
        for record in records:
            counts[record.status] = counts.get(record.status, 0) + 1
        print(f"{origin}: {counts}")
    for record in strube:
        if record.status in ("format_error", "ineligible"):
            print(f"  {record.melody_id}: {record.status}: {record.reason}")
    if getattr(args, "update_inventory", False):
        print(f"Inventory rows filled: {melody_sets.update_inventory(strube)}")
    print(f"Wrote {path}")


def cmd_preflight(args, protocol):
    rows = [r for r in read_rows(MANIFEST) if r["status"] == "eligible"]
    backends = [generation_v2.make_backend(name, protocol) for name in args.models]
    report = generation_v2.preflight(rows, backends)
    write_rows(PREFLIGHT, report)
    refused = [r for r in report if r["accepted"] == 0]
    print(f"Checked {len(rows)} melodies x {len(backends)} models; refused {len(refused)}")
    for r in refused:
        print(f"  {r['melody_id']} ({r['model']}): {r['reason']}")


def accepted_by_all(rows, preflight_rows, models):
    accepted = {}
    for r in preflight_rows:
        accepted.setdefault(r["melody_id"], {})[r["model"]] = r["accepted"] == "1"
    return [r for r in rows if all(accepted.get(r["melody_id"], {}).get(m, False) for m in models)]


def choose_samples(rows, settings):
    """Main sample and pilot set from eligible manifest rows that both models accept.

    Protocol 3.0 (`bach_sample_size`): a seeded sample of Bach melodies and a pilot drawn from the remaining
    Bach melodies. Protocol 2.1: every Strube melody plus a Bach sample of the same size (at least
    `bach_sample_minimum`), and a pilot of each origin.
    """
    import random

    origins = settings.get("origins", ["bach", "strube"])
    strube = [r for r in rows if r["origin"] == "strube" and "strube" in origins]
    bach_records = [melody_sets.MelodyRecord(melody_id=r["melody_id"], origin="bach", source=r["source"], status="eligible")
                    for r in rows if r["origin"] == "bach"]
    if "bach_sample_size" in settings:
        size = settings["bach_sample_size"]
        pilot_size = settings["pilot_size"]
    else:
        size = max(settings["bach_sample_minimum"], len(strube))
        pilot_size = settings["pilot_size_per_origin"]
    chosen = set(melody_sets.sample_bach(bach_records, size, settings["bach_sample_seed"]))
    main = strube + [r for r in rows if r["melody_id"] in chosen]
    rest = sorted(r.melody_id for r in bach_records if r.melody_id not in chosen)
    pilot_ids = set(random.Random(settings["pilot_seed"]).sample(rest, pilot_size))
    if strube:
        pilot_ids |= set(random.Random(settings["pilot_seed"]).sample(sorted(r["melody_id"] for r in strube),
                                                                      min(pilot_size, len(strube))))
    pilot = [r for r in rows if r["melody_id"] in pilot_ids]
    return main, pilot, len(strube), len(chosen)


def cmd_select(args, protocol):
    settings = protocol["melodies"]
    rows = [r for r in read_rows(MANIFEST) if r["status"] == "eligible"]
    if PREFLIGHT.exists():
        rows = accepted_by_all(rows, read_rows(PREFLIGHT), args.models)
    elif not args.allow_without_preflight:
        raise SystemExit("Run preflight first (or pass --allow-without-preflight for a dry selection)")
    main, pilot, n_strube, n_bach = choose_samples(rows, settings)
    write_rows(SELECTION["main"], main)
    write_rows(SELECTION["pilot"], pilot)
    print(f"Main: {n_strube} Strube + {n_bach} Bach (seed {settings['bach_sample_seed']}); pilot: {len(pilot)} melodies")
    if "bach_sample_minimum" in settings and n_strube < settings["bach_sample_minimum"]:
        print(f"NOTE: only {n_strube} eligible Strube melodies; protocol contingency applies (use all, report MDE)")


def cmd_membership(args, protocol):
    import deepbach_membership

    backend = generation_v2.make_backend("deepbach", protocol)
    backend._load()
    cached = None
    tensor_dir = backend.repo_dir / "DatasetManager" / "dataset_cache" / "tensor_datasets"
    candidates = list(tensor_dir.glob("*")) if tensor_dir.exists() else []
    if candidates:
        import torch

        cached = len(torch.load(candidates[0], weights_only=False))
    rows = deepbach_membership.estimate_membership(backend.dataset, cached_length=cached)
    deepbach_membership.write_membership(rows, MEMBERSHIP)
    print(f"Wrote {MEMBERSHIP}; total examples {rows[0]['total_examples']}, cached {cached}, verified {rows[0]['verified']}")


def cmd_generate(args, protocol):
    if args.stage == "main" and not protocol.get("frozen"):
        raise SystemExit("the protocol file is not frozen; agree the protocol and finish the pilot first")
    if args.resume:
        run = generation_v2.Run(args.resume)
    else:
        rows = read_rows(SELECTION[args.stage])
        backends = [generation_v2.make_backend(name, protocol) for name in args.models]
        run = generation_v2.Run.create(args.run_id or f"{args.stage}-{stamp()}", protocol, rows, backends, args.stage)
        print(f"Created run {run.dir}")
    for name in args.models:
        backend = generation_v2.make_backend(name, protocol)
        counts = generation_v2.generate(run, backend, protocol["generations_per_melody"], protocol["root_seed"],
                                        retry_failed=args.retry_failed)
        print(f"{name}: {counts}")
    print(f"Next: v2.py evaluate {run.dir}")


def cmd_evaluate(args, protocol):
    print(evaluate_v2.evaluate_run(args.run))


def cmd_analyze(args, protocol):
    summary = analysis_v2.analyze_run(args.run, membership_file=MEMBERSHIP if MEMBERSHIP.exists() else None)
    written = analysis_v2.plot_run(args.run)
    print(f"Q2 rows {len(summary['q2'])}, Q3 zone rows {len(summary['q3_zone'])}, Q3 origin rows {len(summary['q3'])}, "
          f"figures {len(written)}")


def cmd_examples(args, protocol):
    rows = run_checks_v2.sample_examples(args.run, protocol["analysis"]["examples_per_rule"],
                                         protocol["analysis"]["examples_seed"])
    print(f"Wrote {len(rows)} examples to {Path(args.run) / 'examples'}")


def cmd_check(args, protocol):
    info = json.loads((Path(args.run) / "run.json").read_text(encoding="utf-8"))
    problems = run_checks_v2.check_run(args.run, list(info["backends"]), protocol["generations_per_melody"])
    for problem in problems:
        print("PROBLEM:", problem)
    print("complete" if not problems else f"{len(problems)} problems")
    return 1 if problems else 0


def cmd_dry_run(args, protocol):
    """Whole chain with fake backends on a few melodies, in a temporary folder."""
    work = Path(tempfile.mkdtemp(prefix="v2-dry-run-"))
    fixtures = RESEARCH / "tests" / "fixtures" / "strube-melodies"
    try:
        cmd_melodies(argparse.Namespace(update_inventory=False), protocol, out_dir=work / "melodies",
                     text_dir=fixtures, bach_limit=args.bach_limit)
        origins = protocol["melodies"].get("origins", ["bach", "strube"])
        rows = [r for r in read_rows(work / "melodies" / "manifest.csv")
                if r["status"] == "eligible" and r["origin"] in origins]
        backends = [generation_v2.FakeBackend("deepbach", offsets=(9, 15, 24)),
                    generation_v2.FakeBackend("coconet", offsets=(8, 16, 24))]
        run = generation_v2.Run.create("dry-run", {**protocol, "generations_per_melody": 2}, rows, backends,
                                       "dry-run", runs_dir=work / "runs")
        for backend in backends:
            print(backend.name, generation_v2.generate(run, backend, 2, protocol["root_seed"], progress=lambda m: None))
        print("evaluate:", evaluate_v2.evaluate_run(run.dir))
        summary = analysis_v2.analyze_run(run.dir, protocol={**protocol, "generations_per_melody": 2})
        print("analysis: q2", len(summary["q2"]), "q3 zone", len(summary["q3_zone"]), "q3 origin", len(summary["q3"]),
              "figures", len(analysis_v2.plot_run(run.dir)))
        print("examples:", len(run_checks_v2.sample_examples(run.dir, 1, 1)))
        problems = run_checks_v2.check_run(run.dir, ["deepbach", "coconet"], 2)
        print("check:", "complete" if not problems else problems)
        print(f"Dry run finished in {work} (fake backends; not research data)")
        if not args.keep:
            shutil.rmtree(work)
        return 1 if problems else 0
    except BaseException:
        print(f"Dry run failed; files kept in {work}")
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--protocol", default=str(generation_v2.PROTOCOL_FILE))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("templates")
    p = sub.add_parser("melodies")
    p.add_argument("--update-inventory", action="store_true")
    p.add_argument("--bach-limit", type=int, default=None, help="only the first N corpus chorales (testing)")
    for name in ("preflight", "select"):
        p = sub.add_parser(name)
        p.add_argument("--models", nargs="+", default=list(MODELS))
        if name == "select":
            p.add_argument("--allow-without-preflight", action="store_true")
    sub.add_parser("membership")
    p = sub.add_parser("generate")
    p.add_argument("--stage", choices=("pilot", "main"), required=True)
    p.add_argument("--models", nargs="+", default=list(MODELS))
    p.add_argument("--run-id")
    p.add_argument("--resume", help="existing run directory to continue")
    p.add_argument("--retry-failed", action="store_true")
    for name in ("evaluate", "analyze", "examples", "check"):
        sub.add_parser(name).add_argument("run")
    p = sub.add_parser("dry-run")
    p.add_argument("--bach-limit", type=int, default=8)
    p.add_argument("--keep", action="store_true")
    args = parser.parse_args()
    protocol = generation_v2.load_protocol(args.protocol)
    handler = globals()["cmd_" + args.command.replace("-", "_")]
    return handler(args, protocol) or 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""

run_all.py — Single entrypoint for the Strube Symbolic Music Evaluation pipeline.

Runs the full experiment in order:
  1. Face validity tests (proves the evaluator works before generating anything)
  2. Generation — all three models, all four conditions
  3. Strube evaluation — batch evaluate all generated MIDI files
  4. Plot results — generate the summary chart

Usage:
    python run_all.py                     # full run (10 samples per condition)
    python run_all.py --samples 1         # quick smoke test
    python run_all.py --dry-run           # print prompt matrix, no generation
    python run_all.py --skip-generation   # evaluate existing outputs only
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

def run(cmd: list[str], label: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"STEP: {label}")
    print(f"{'=' * 60}")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        print(f"\n✗ FAILED: {label}")
        sys.exit(result.returncode)
    print(f"\n✓ DONE: {label}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Run full Strube evaluation pipeline.")
    parser.add_argument("--samples", type=int, default=10,
                        help="Samples per condition per model (default: 10)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print prompt matrix without generating")
    parser.add_argument("--skip-generation", action="store_true",
                        help="Skip generation, only evaluate existing outputs")
    parser.add_argument("--parallel-models", action="store_true",
                        help="Run model generation in parallel (requires sufficient RAM)")
    parser.add_argument("--download-notagen", action="store_true",

                        help="Deprecated: NotaGen checkpoint downloads automatically when missing")
    args = parser.parse_args()

    # Step 1: Face validity — must pass before anything else
    run(
        [sys.executable, "tests/test_strube_validity.py"],
        "Face Validity Tests"
    )

    if not args.skip_generation:
        # Step 2: Generation
        gen_cmd = [
            sys.executable, "experiments/scripts/run_experiment.py",
            "--samples", str(args.samples),
        ]
        if args.dry_run:
            gen_cmd.append("--dry-run")
        if args.parallel_models:
            gen_cmd.append("--parallel-models")
        if args.download_notagen:
            gen_cmd.append("--download-notagen")

        run(gen_cmd, "Model Generation (DeepBach + Coconet + NotaGen)")

        if args.dry_run:
            print("\nDry run complete. No evaluation performed.")
            return

    # Step 3: Evaluation
    run(
        [sys.executable, "experiments/scripts/run_evaluation.py"],
        "Strube Batch Evaluation"
    )

    # Step 4: Plot
    run(
        [sys.executable, "experiments/scripts/plot_results.py"],
        "Results Visualization"
    )

    print(f"\n{'=' * 60}")
    print("ALL STEPS COMPLETE")
    print("Results saved to:")
    print("  outputs/MASTER_RESULTS.csv")
    print("  outputs/SUMMARY_TABLE.csv")
    print("  outputs/strube_evaluation_results.png")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()

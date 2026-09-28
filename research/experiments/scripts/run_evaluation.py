"""

Orchestration script to run Strube evaluations across all generated files
for all three models (DeepBach, Coconet, NotaGen) and all four conditions (A–D).
Generates MASTER_RESULTS.csv and SUMMARY_TABLE.csv.
"""

import os
import sys
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from strube_evaluator import evaluate_satb

def main():
    print("=" * 60)
    print("STRUBE HARMONIC EVALUATION FRAMEWORK — BATCH EVALUATOR")
    print("=" * 60)

    outputs_base = PROJECT_ROOT / "outputs"
    models = ["deepbach", "coconet", "notagen"]
    conditions = ["A_neutral", "B_key", "C_satb", "D_full"]

    rows = []

    for model in models:
        for cond in conditions:
            cond_dir = outputs_base / model / cond
            if not cond_dir.exists():
                print(f"Skipping {model}/{cond}: directory does not exist.")
                continue

            midi_files = list(cond_dir.glob("*.mid")) + list(cond_dir.glob("*.midi"))
            if not midi_files:
                print(f"Skipping {model}/{cond}: no MIDI files found.")
                continue

            for f in tqdm(sorted(midi_files), desc=f"Evaluate {model}/{cond}", unit="file"):
                try:
                    # Dynamically detect key of the MIDI file and run Strube evaluator
                    r = evaluate_satb(str(f), key_tonic_pc=None)

                    rows.append({
                        "model": model,
                        "condition": cond,
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
                    tqdm.write(f"  Error evaluating {f.name}: {e}")

    if not rows:
        print("Error: No evaluation data gathered!")
        return

    # Save Master Results
    df_master = pd.DataFrame(rows)
    master_path = outputs_base / "MASTER_RESULTS.csv"
    df_master.to_csv(master_path, index=False)
    print(f"\nSaved MASTER_RESULTS.csv to {master_path}")

    # Generate Summary Table
    print("\nGenerating SUMMARY_TABLE.csv...")
    summary_rows = []
    grouped = df_master.groupby(["model", "condition"])

    for (model, cond), group in grouped:
        summary_rows.append({
            "Model": model.capitalize(),
            "Condition": cond,
            "Total Samples": len(group),
            "Avg Moments": round(group["total_moments"].mean(), 1),
            "Avg Parallel Fifths": round(group["parallel_fifths"].mean(), 2),
            "Avg Parallel Octaves": round(group["parallel_octaves"].mean(), 2),
            "Avg LT Violations": round(group["leading_tone_violations"].mean(), 2),
            "Avg Strube Score": round(group["strube_score"].mean(), 4),
        })

    df_summary = pd.DataFrame(summary_rows)
    summary_path = outputs_base / "SUMMARY_TABLE.csv"
    df_summary.to_csv(summary_path, index=False)
    print(f"Saved SUMMARY_TABLE.csv to {summary_path}")

    print("\nSummary Table:")
    print(df_summary.to_string(index=False))
    print("=" * 60)

if __name__ == "__main__":
    main()

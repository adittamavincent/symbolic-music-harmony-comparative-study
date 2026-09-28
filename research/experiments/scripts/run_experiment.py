"""

Manifest-driven Strube research runner.

This is the top-level entrypoint for generation experiments. It records the
exact model conditioning used for each model/condition pair, then dispatches
the existing model-specific adapters.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_MANIFEST = PROJECT_ROOT / "experiments" / "strube_conditions.json"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ALL_MODELS = ("deepbach", "coconet", "notagen")

def parse_csv(value: str, valid_values: tuple[str, ...] | set[str]) -> list[str]:
    values = [item.strip() for item in value.split(",") if item.strip()]
    invalid = sorted(set(values) - set(valid_values))
    if invalid:
        raise argparse.ArgumentTypeError(f"invalid values: {', '.join(invalid)}")
    return values

def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def print_prompt_matrix(manifest: dict, models: list[str], conditions: list[str]) -> None:
    print("=" * 72)
    print("STRUBE EXPERIMENT PROMPT / CONDITIONING MATRIX")
    print("=" * 72)
    for condition in conditions:
        condition_spec = manifest["conditions"][condition]
        print(f"\n[{condition}] {condition_spec['description']}")
        for model in models:
            prompt = condition_spec["models"][model]["prompt"]
            if isinstance(prompt, dict):
                prompt = ", ".join(f"{key}={value}" for key, value in prompt.items())
            print(f"  - {model}: {prompt}")
    print("=" * 72)

def write_run_metadata(
    manifest_path: Path,
    manifest: dict,
    models: list[str],
    conditions: list[str],
    samples: int,
    parallel_models: bool,

    dry_run: bool,
    download_notagen: bool,
) -> Path:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    selected_conditions = {
        condition: manifest["conditions"][condition] for condition in conditions
    }
    payload = {
        "started_at_utc": started_at,
        "manifest_path": str(manifest_path),
        "samples_per_condition": samples,
        "models": models,
        "conditions": conditions,
        "parallel_models": parallel_models,
        "dry_run": dry_run,
        "download_notagen": download_notagen,
        "selected_conditioning": selected_conditions,
    }
    stamped_path = OUTPUTS_DIR / f"RUN_METADATA_{started_at.replace(':', '').replace('+', 'Z')}.json"
    latest_path = OUTPUTS_DIR / "LATEST_RUN_METADATA.json"
    for path in (stamped_path, latest_path):
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")
    print(f"\nSaved run metadata: {latest_path}")
    return latest_path

def command_for_model(
    model: str,
    conditions: list[str],
    samples: int,
    download_notagen: bool = False,
) -> list[str]:
    script = PROJECT_ROOT / "experiments" / "scripts" / f"run_{model}.py"
    cmd = [
        sys.executable,
        str(script),
        "--conditions",
        ",".join(conditions),
        "--samples",
        str(samples),
    ]
    if model == "notagen" and download_notagen:
        cmd.append("--download-weights")
    return cmd

def run_sequential(
    models: list[str],
    conditions: list[str],
    samples: int,
    download_notagen: bool = False,
) -> None:
    for model in tqdm(models, desc="Model adapters", unit="model"):
        cmd = command_for_model(model, conditions, samples, download_notagen)
        tqdm.write(f"\nRunning {model}: {' '.join(cmd)}")

        subprocess.run(cmd, cwd=str(PROJECT_ROOT), check=True)

def run_parallel(
    models: list[str],
    conditions: list[str],
    samples: int,
    download_notagen: bool = False,
) -> None:
    processes: list[tuple[str, subprocess.Popen]] = []
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    for model in models:
        cmd = command_for_model(model, conditions, samples, download_notagen)
        print(f"\nStarting {model}: {' '.join(cmd)}")
        processes.append(
            (
                model,
                subprocess.Popen(cmd, cwd=str(PROJECT_ROOT), env=env),
            )
        )

    failed: list[str] = []
    for model, process in tqdm(processes, desc="Model adapters", unit="model"):
        return_code = process.wait()
        if return_code != 0:
            failed.append(f"{model} exited with {return_code}")

    if failed:
        raise RuntimeError("; ".join(failed))

def main() -> None:
    parser = argparse.ArgumentParser(description="Run manifest-driven Strube generation experiments.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--models", default=",".join(ALL_MODELS))
    parser.add_argument("--conditions", default=None)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument(
        "--parallel-models",
        action="store_true",
        help="Run model adapters at the same time. Use only when RAM/GPU/Node resources are sufficient.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print and save prompts without generating.")
    parser.add_argument(
        "--download-notagen",
        action="store_true",
        help="Download the NotaGen-X checkpoint if it is missing.",
    )
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest = load_manifest(manifest_path)

    valid_conditions = tuple(manifest["conditions"].keys())
    models = parse_csv(args.models, set(ALL_MODELS))
    conditions = (
        parse_csv(args.conditions, set(valid_conditions))
        if args.conditions
        else list(valid_conditions)
    )
    samples = args.samples or int(manifest.get("default_samples_per_condition", 10))
    if samples < 1:
        raise ValueError("--samples must be >= 1")

    print_prompt_matrix(manifest, models, conditions)
    write_run_metadata(
        manifest_path=manifest_path,
        manifest=manifest,
        models=models,
        conditions=conditions,
        samples=samples,
        parallel_models=args.parallel_models,
        dry_run=args.dry_run,
        download_notagen=args.download_notagen,
    )

    if args.dry_run:
        print("\nDry run complete. No generation executed.")
        return

    if args.parallel_models:
        run_parallel(models, conditions, samples, args.download_notagen)
    else:
        run_sequential(models, conditions, samples, args.download_notagen)

    print("\nGeneration complete. Run `python experiments/scripts/run_evaluation.py` to evaluate outputs.")

if __name__ == "__main__":
    main()

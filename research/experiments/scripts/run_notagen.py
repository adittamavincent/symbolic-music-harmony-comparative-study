"""
Script to generate MIDI samples from NotaGen-X under manifest-defined conditions.
"""

import os
import sys
from pathlib import Path
import argparse
import contextlib
import io
import json
import re
import urllib.request
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
NOTAGEN_DIR = PROJECT_ROOT / "models" / "notagen"
GRADIO_DIR = NOTAGEN_DIR / "gradio"
CONDITIONS_FILE = PROJECT_ROOT / "experiments" / "strube_conditions.json"
NOTAGEN_WEIGHTS_URL = (
    "https://huggingface.co/ElectricAlexis/NotaGen/resolve/main/"
    "weights_notagenx_p_size_16_p_length_1024_p_layers_20_h_size_1280.pth"
)

# Change working directory to gradio directory for relative weight loading
os.chdir(str(GRADIO_DIR))

# Add notagen and gradio directories to path
sys.path.append(str(NOTAGEN_DIR))
sys.path.append(str(GRADIO_DIR))

from music21 import converter

from config import INFERENCE_WEIGHTS_PATH

inference = None

def load_inference():
    global inference
    if inference is None:
        import inference as inference_module
        inference = inference_module
    return inference

def download_weights() -> None:
    if INFERENCE_WEIGHTS_PATH.exists():
        return

    INFERENCE_WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    part_path = INFERENCE_WEIGHTS_PATH.with_suffix(INFERENCE_WEIGHTS_PATH.suffix + ".part")

    print(f"Downloading NotaGen-X checkpoint to {INFERENCE_WEIGHTS_PATH}")
    with urllib.request.urlopen(NOTAGEN_WEIGHTS_URL) as response:
        total = int(response.headers.get("Content-Length", 0))
        with part_path.open("wb") as f, tqdm(
            total=total or None,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="NotaGen checkpoint",
        ) as progress:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                progress.update(len(chunk))

    part_path.replace(INFERENCE_WEIGHTS_PATH)

def inference_patch_quiet(period, composer, instrumentation):
    if os.environ.get("NOTAGEN_VERBOSE") == "1":
        return load_inference().inference_patch(period, composer, instrumentation)

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
        return load_inference().inference_patch(period, composer, instrumentation)

def sanitize_abc(abc_text: str) -> str:

    abc_text = re.sub(r"\[r:[^\]]*\]", "", abc_text)
    abc_text = re.sub(r"//+", "/", abc_text)
    abc_text = abc_text.replace("::", "|")
    abc_text = abc_text.replace(":|", "|")
    abc_text = abc_text.replace("|:", "|")
    abc_text = abc_text.replace("!D.C.!", "")
    abc_text = re.sub(r"[\^_=]+(?![A-Ga-g])", "", abc_text)
    return abc_text

def parse_abc(abc_text: str):
    try:
        return converter.parseData(abc_text, format='abc')
    except Exception:
        return converter.parseData(sanitize_abc(abc_text), format='abc')

def generate_condition(period, composer, instrumentation, output_dir, name_prefix, count=10):
    print(f"Generating Condition {name_prefix}...")
    os.makedirs(output_dir, exist_ok=True)

    max_attempts = int(os.environ.get("NOTAGEN_MAX_ATTEMPTS", "5"))
    with tqdm(total=count, desc=f"NotaGen {name_prefix}", unit="sample") as progress:
        saved = 0
        attempts = 0
        while saved < count and attempts < count * max_attempts:
            attempts += 1
            abc_text = None
            try:
                abc_text = inference_patch_quiet(period, composer, instrumentation)
                score = parse_abc(abc_text)
                sample_index = saved + 1
                out_path = Path(output_dir) / f"notagen_{name_prefix}_{sample_index:02d}.mid"
                score.write('midi', fp=str(out_path))
                saved += 1
                progress.update(1)
            except Exception as e:
                if abc_text:
                    failed_path = Path(output_dir) / f"notagen_{name_prefix}_failed_{attempts:02d}.abc"
                    failed_path.write_text(abc_text, encoding="utf-8")
                tqdm.write(f"    Retry {attempts}/{count * max_attempts} for {name_prefix}: {e}")

        if saved < count:
            tqdm.write(

                f"NotaGen generated {saved}/{count} valid MIDI samples for {name_prefix} "
                f"after {attempts} attempts."
            )
            return

    print(f"  Saved {count} NotaGen {name_prefix} sample(s).")

def load_condition_prompts() -> dict:
    with open(CONDITIONS_FILE) as f:
        manifest = json.load(f)
    result = {}
    for cond_name, cond_spec in manifest["conditions"].items():
        ng = cond_spec["models"]["notagen"]["prompt"]
        result[cond_name] = (
            ng["period"],
            ng["composer"],
            ng["instrumentation"],
            cond_name.split("_")[1],
        )
    return result

CONDITION_PROMPTS = load_condition_prompts()

def parse_conditions(value):
    conditions = [item.strip() for item in value.split(",") if item.strip()]
    invalid = sorted(set(conditions) - set(CONDITION_PROMPTS))
    if invalid:
        raise argparse.ArgumentTypeError(f"invalid conditions: {', '.join(invalid)}")
    return conditions

def main():
    parser = argparse.ArgumentParser(description="Generate NotaGen MIDI samples.")
    parser.add_argument("--conditions", type=parse_conditions, default=list(CONDITION_PROMPTS))
    parser.add_argument("--samples", type=int, default=10)
    parser.add_argument(
        "--download-weights",
        action="store_true",
        help="Deprecated: weights now download automatically when missing.",
    )
    args = parser.parse_args()

    if args.samples < 1:
        raise ValueError("--samples must be >= 1")

    if not INFERENCE_WEIGHTS_PATH.exists():
        download_weights()

    # Change working directory to gradio directory for relative weight loading
    os.chdir(str(GRADIO_DIR))

    outputs_base = PROJECT_ROOT / "outputs" / "notagen"

    for condition in args.conditions:
        period, composer, instrumentation, name_prefix = CONDITION_PROMPTS[condition]

        generate_condition(
            period,
            composer,
            instrumentation,
            outputs_base / condition,
            name_prefix,
            args.samples,
        )

    print("\nNotaGen generation complete!")

if __name__ == "__main__":
    main()

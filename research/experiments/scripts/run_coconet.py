"""
Script to orchestrate Coconet generation:
  1. Extract a seed chorale's Soprano and Bass notes from the Bach dataset in Python.
  2. Save them to models/coconet/seed_chorale.json.
  3. Call the Node.js generator script scripts/run_coconet.js to execute 4 experimental conditions.
  4. Parse the generated JSON note sequence outputs and reconstruct them into standard MIDI files.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
import argparse
from tqdm import tqdm

# Add deepbach/notagen to path if necessary
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEEPBACH_DIR = PROJECT_ROOT / "models" / "deepbach"
COCONET_DIR = PROJECT_ROOT / "models" / "coconet"
CONDITIONS_FILE = PROJECT_ROOT / "experiments" / "strube_conditions.json"
sys.path.append(str(DEEPBACH_DIR))

# Monkeypatch torch.load for PyTorch >= 2.6 safety
import torch
original_load = torch.load
def patched_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_load(*args, **kwargs)
torch.load = patched_load

from music21 import stream, note, duration
from DatasetManager.dataset_manager import DatasetManager
from DatasetManager.metadata import FermataMetadata, KeyMetadata, TickMetadata

def extract_seed_chorale():
    print("Extracting seed chorale from dataset...")
    # Make sure we change directory to deepbach root to load local files/models
    original_cwd = os.getcwd()
    os.chdir(str(DEEPBACH_DIR))

    dataset_manager = DatasetManager()

    metadatas = [FermataMetadata(), TickMetadata(subdivision=4), KeyMetadata()]
    chorale_dataset_kwargs = {
        'voice_ids': [0, 1, 2, 3],
        'metadatas': metadatas,
        'sequences_size': 8,
        'subdivision': 4,
    }

    dataset = dataset_manager.get_dataset(name='bach_chorales', **chorale_dataset_kwargs)

    # Locate a valid seed chorale robustly
    seed_chorale = None
    for chorale in dataset.iterator_gen():
        try:
            # Test getting metadata and score tensor to verify it works without exceptions
            _ = dataset.get_score_tensor(chorale, offsetStart=0., offsetEnd=chorale.flat.highestTime)
            _ = dataset.get_metadata_tensor(chorale)
            seed_chorale = chorale
            break
        except Exception as e:
            continue

    os.chdir(original_cwd)

    if seed_chorale is None:
        raise RuntimeError("Failed to extract a valid seed chorale from the dataset!")

    length_ticks = int(seed_chorale.flat.highestTime * dataset.subdivision)
    print(f"Extracted valid seed chorale with length {length_ticks} ticks.")

    # Extract Soprano (0) and Bass (3) notes
    # We quantize and scale offsets/durations by subdivision=4 to get integer steps
    soprano_notes = []
    for n in seed_chorale.parts[0].flat.notes:
        if n.isNote:
            soprano_notes.append({
                "pitch": n.pitch.midi,
                "quantizedStartStep": int(n.offset * 4),
                "quantizedEndStep": int((n.offset + n.duration.quarterLength) * 4)
            })

    bass_notes = []
    for n in seed_chorale.parts[3].flat.notes:
        if n.isNote:
            bass_notes.append({
                "pitch": n.pitch.midi,
                "quantizedStartStep": int(n.offset * 4),
                "quantizedEndStep": int((n.offset + n.duration.quarterLength) * 4)
            })

    seed_data = {

        "totalQuantizedSteps": length_ticks,
        "sopranoNotes": soprano_notes,
        "bassNotes": bass_notes
    }

    os.makedirs(str(COCONET_DIR), exist_ok=True)
    out_path = COCONET_DIR / "seed_chorale.json"
    with open(out_path, 'w') as f:
        json.dump(seed_data, f, indent=2)
    print(f"Saved seed chorale data to {out_path}")

def load_condition_names():
    with open(CONDITIONS_FILE) as f:
        manifest = json.load(f)
    return list(manifest["conditions"])

def parse_conditions(value):
    conditions = [item.strip() for item in value.split(",") if item.strip()]
    invalid = sorted(set(conditions) - set(load_condition_names()))
    if invalid:
        raise argparse.ArgumentTypeError(f"invalid conditions: {', '.join(invalid)}")
    return conditions

def run_node_generation(conditions, samples):
    print("\nLaunching Coconet generation script via Node.js...")
    js_script = COCONET_DIR / "run_coconet.js"
    env = os.environ.copy()
    env["COCONET_CONDITIONS"] = ",".join(conditions)
    env["COCONET_SAMPLES"] = str(samples)

    local_node = COCONET_DIR / "node_modules" / "node" / "bin" / "node"
    node_executable = (
        env.get("COCONET_NODE")
        or (str(local_node) if local_node.exists() else None)
        or shutil.which("node")
    )
    if not node_executable:
        raise RuntimeError("Node.js not found. Install Node 18/20 or set COCONET_NODE.")

    # Execute node run_coconet.js
    res = subprocess.run([node_executable, str(js_script)], cwd=str(COCONET_DIR), env=env, check=True)
    if res.returncode == 0:
        print("Node.js Coconet generation completed successfully!")
    else:
        raise RuntimeError("Node.js Coconet generation script failed!")

def reconstruct_json_to_midi(conditions):
    print("\nReconstructing generated JSON sequences back into MIDI files...")

    outputs_base = PROJECT_ROOT / "outputs" / "coconet"

    for cond in conditions:
        cond_dir = outputs_base / cond
        json_files = list(cond_dir.glob("*.json"))

        for j_file in tqdm(sorted(json_files), desc=f"Coconet {cond} reconstruct", unit="sample"):
            midi_name = j_file.stem + ".mid"
            midi_path = cond_dir / midi_name

            with open(j_file, 'r') as f:
                notes_data = json.load(f)

            score = stream.Score()
            parts = [
                stream.Part(id='Soprano', partName='Soprano'),
                stream.Part(id='Alto', partName='Alto'),
                stream.Part(id='Tenor', partName='Tenor'),
                stream.Part(id='Bass', partName='Bass')
            ]

            # Group note events by voice (instrument index 0-3)
            voice_notes = {0: [], 1: [], 2: [], 3: []}
            for n in notes_data:
                voice_idx = int(n['instrument'])
                if voice_idx in voice_notes:
                    voice_notes[voice_idx].append({
                        "pitch": int(n["pitch"]),
                        "quantizedStartStep": int(n["quantizedStartStep"]),
                        "quantizedEndStep": int(n["quantizedEndStep"]),
                    })

            for voice_idx, part in enumerate(parts):
                # Sort note events chronologically
                v_notes = sorted(voice_notes[voice_idx], key=lambda x: x['quantizedStartStep'])
                for n_data in v_notes:
                    n = note.Note(n_data['pitch'])
                    n.offset = n_data['quantizedStartStep'] / 4.0
                    n.duration = duration.Duration((n_data['quantizedEndStep'] - n_data['quantizedStartStep']) / 4.0)
                    part.append(n)
                score.insert(part)

            # Write to MIDI

            score.write('midi', fp=str(midi_path))
            # Delete temporary JSON file
            os.remove(j_file)

    print("Reconstruction complete! All Coconet samples converted to MIDI.")

def main():
    parser = argparse.ArgumentParser(description="Generate Coconet MIDI samples.")
    parser.add_argument("--conditions", type=parse_conditions, default=load_condition_names())
    parser.add_argument("--samples", type=int, default=10)
    args = parser.parse_args()

    if args.samples < 1:
        raise ValueError("--samples must be >= 1")

    extract_seed_chorale()
    run_node_generation(args.conditions, args.samples)
    reconstruct_json_to_midi(args.conditions)
    print("\nCoconet orchestration finished!")

if __name__ == "__main__":
    main()

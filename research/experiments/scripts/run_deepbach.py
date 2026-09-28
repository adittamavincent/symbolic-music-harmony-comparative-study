"""
Script to generate MIDI samples from DeepBach under 4 different conditions:
  - A_neutral: No constraints (random generation)
  - B_key: Key constraint (forced C Major)
  - C_satb: Soprano constraint (using BWV 66.6 Soprano voice, generating A, T, B)
  - D_full: Soprano + Bass constraint (using BWV 66.6 Soprano and Bass voices, generating A, T)
"""

import os
import sys
from pathlib import Path
import random
import shutil
import numpy as np
import argparse
import json
import tarfile
import urllib.request
from tqdm import tqdm

# Add deepbach directory to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEEPBACH_DIR = PROJECT_ROOT / "models" / "deepbach"
CONDITIONS_FILE = PROJECT_ROOT / "experiments" / "strube_conditions.json"
DEEPBACH_RESOURCES_URL = "https://www.dropbox.com/scl/fi/26o7byo483tsm9k3jfbaj/deepbach_pytorch_resources.tar.gz?rlkey=fqkddap7on2ix81wlj8tsqklp&dl=1"
sys.path.append(str(DEEPBACH_DIR))

# Monkeypatch torch.load to bypass the weights_only default of PyTorch >= 2.6
import torch
original_load = torch.load
def patched_load(*args, **kwargs):

    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_load(*args, **kwargs)
torch.load = patched_load

from music21 import corpus, converter
from DatasetManager.chorale_dataset import ChoraleDataset
from DatasetManager.dataset_manager import DatasetManager
from DatasetManager.metadata import FermataMetadata, KeyMetadata, TickMetadata
from DeepBach.model_manager import DeepBach

def ensure_deepbach_resources():
    models_dir = DEEPBACH_DIR / "models"
    expected_weights = [
        models_dir / (
            "VoiceModel(ChoraleDataset([0, 1, 2, 3],bach_chorales,"
            "['fermata', 'tick', 'key'],8,4),"
            f"{voice_index},20,20,2,256,0.5,256)"
        )
        for voice_index in range(4)
    ]
    dataset_cache = DEEPBACH_DIR / "DatasetManager" / "dataset_cache"
    if all(path.exists() for path in expected_weights) and dataset_cache.exists():
        return

    archive_path = DEEPBACH_DIR / "deepbach_pytorch_resources.tar.gz"
    resources_dir = DEEPBACH_DIR / "resources"
    print("Downloading DeepBach pretrained resources...")
    with urllib.request.urlopen(DEEPBACH_RESOURCES_URL) as response:
        total = int(response.headers.get("Content-Length", 0))
        with archive_path.open("wb") as f, tqdm(
            total=total or None,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="DeepBach resources",
        ) as progress:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                progress.update(len(chunk))

    with tarfile.open(archive_path, "r:gz") as archive:
        archive.extractall(DEEPBACH_DIR)

    if dataset_cache.exists():
        shutil.rmtree(dataset_cache)
    if models_dir.exists():
        shutil.rmtree(models_dir)

    (resources_dir / "dataset_cache").replace(dataset_cache)
    (resources_dir / "models").replace(models_dir)
    shutil.rmtree(resources_dir)

def setup_deepbach():
    print("Setting up DeepBach...")
    ensure_deepbach_resources()
    dataset_manager = DatasetManager()
    metadatas = [FermataMetadata(), TickMetadata(subdivision=4), KeyMetadata()]
    chorale_dataset_kwargs = {
        'voice_ids': [0, 1, 2, 3],
        'metadatas': metadatas,
        'sequences_size': 8,
        'subdivision': 4,
    }
    # Load dataset
    dataset = dataset_manager.get_dataset(name='bach_chorales', **chorale_dataset_kwargs)

    # Initialize model manager
    deepbach = DeepBach(
        dataset=dataset,
        note_embedding_dim=20,
        meta_embedding_dim=20,
        num_layers=2,
        lstm_hidden_size=256,
        dropout_lstm=0.5,
        linear_hidden_size=256,
    )
    deepbach.load()
    return deepbach, dataset

def generate_neutral(deepbach, output_dir, count=10):
    print("Generating Condition A: Neutral...")
    os.makedirs(output_dir, exist_ok=True)
    for i in tqdm(range(count), desc="DeepBach A_neutral", unit="sample"):
        score, _, _ = deepbach.generation(
            num_iterations=100,
            sequence_length_ticks=160,
            random_init=True
        )
        out_path = Path(output_dir) / f"deepbach_neutral_{i+1:02d}.mid"
        score.write('midi', fp=str(out_path))

def generate_key(deepbach, output_dir, count=10):
    print("Generating Condition B: Key (C Major)...")
    os.makedirs(output_dir, exist_ok=True)

    # Pre-generate metadata tensor with C major (index 8)
    test_chorale = next(deepbach.dataset.corpus_it_gen().__iter__())
    tensor_metadata = deepbach.dataset.get_metadata_tensor(test_chorale)
    if tensor_metadata.size(1) < 160:

        tensor_metadata = tensor_metadata.repeat(1, 160 // tensor_metadata.size(1) + 1, 1)
    tensor_metadata = tensor_metadata[:, :160, :]

    # Set key metadata to 8 (0 sharps/flats = C major)
    tensor_metadata[:, :, 2] = 8

    for i in tqdm(range(count), desc="DeepBach B_key", unit="sample"):
        score, _, _ = deepbach.generation(
            num_iterations=100,
            sequence_length_ticks=160,
            tensor_metadata=tensor_metadata,
            random_init=True
        )
        out_path = Path(output_dir) / f"deepbach_key_{i+1:02d}.mid"
        score.write('midi', fp=str(out_path))

def generate_satb(deepbach, dataset, output_dir, count=10):
    print("Generating Condition C: Soprano-constrained (SATB)...")
    os.makedirs(output_dir, exist_ok=True)

    # Load seed from dataset iterator robustly
    seed_chorale = None
    chorale_tensor = None
    metadata_tensor = None
    for chorale in dataset.iterator_gen():
        try:
            chorale_tensor = dataset.get_score_tensor(chorale, offsetStart=0., offsetEnd=chorale.flat.highestTime)
            metadata_tensor = dataset.get_metadata_tensor(chorale)
            seed_chorale = chorale
            break
        except Exception as e:
            print(f"  Skipping seed candidate due to: {e}")
            continue

    if seed_chorale is None:
        raise RuntimeError("Could not find any valid seed chorale in dataset!")

    length_ticks = int(seed_chorale.flat.highestTime * dataset.subdivision)
    print(f"  Using seed chorale: {seed_chorale} with length {length_ticks} ticks")

    for i in tqdm(range(count), desc="DeepBach C_satb", unit="sample"):
        # voice_index_range=[1, 4] means Alto, Tenor, Bass are randomized and generated
        # Soprano (0) is kept fixed
        score, _, _ = deepbach.generation(
            num_iterations=100,

            sequence_length_ticks=length_ticks,
            tensor_chorale=chorale_tensor.clone(),
            tensor_metadata=metadata_tensor.clone(),
            voice_index_range=[1, 4],
            random_init=True
        )
        out_path = Path(output_dir) / f"deepbach_satb_{i+1:02d}.mid"
        score.write('midi', fp=str(out_path))

def generate_full(deepbach, dataset, output_dir, count=10):
    print("Generating Condition D: Soprano + Bass constrained (Full)...")
    os.makedirs(output_dir, exist_ok=True)

    # Load seed from dataset iterator robustly
    seed_chorale = None
    chorale_tensor = None
    metadata_tensor = None
    for chorale in dataset.iterator_gen():
        try:
            chorale_tensor = dataset.get_score_tensor(chorale, offsetStart=0., offsetEnd=chorale.flat.highestTime)
            metadata_tensor = dataset.get_metadata_tensor(chorale)
            seed_chorale = chorale
            break
        except Exception as e:
            print(f"  Skipping seed candidate due to: {e}")
            continue

    if seed_chorale is None:
        raise RuntimeError("Could not find any valid seed chorale in dataset!")

    length_ticks = int(seed_chorale.flat.highestTime * dataset.subdivision)
    print(f"  Using seed chorale: {seed_chorale} with length {length_ticks} ticks")

    for i in tqdm(range(count), desc="DeepBach D_full", unit="sample"):
        # voice_index_range=[1, 3] means Alto (1) and Tenor (2) are randomized and generated
        # Soprano (0) and Bass (3) are kept fixed
        score, _, _ = deepbach.generation(
            num_iterations=100,
            sequence_length_ticks=length_ticks,
            tensor_chorale=chorale_tensor.clone(),
            tensor_metadata=metadata_tensor.clone(),
            voice_index_range=[1, 3],
            random_init=True
        )

        out_path = Path(output_dir) / f"deepbach_full_{i+1:02d}.mid"
        score.write('midi', fp=str(out_path))

CONDITION_GENERATORS = {
    "A_neutral": lambda deepbach, dataset, output_dir, count: generate_neutral(deepbach, output_dir, count),
    "B_key": lambda deepbach, dataset, output_dir, count: generate_key(deepbach, output_dir, count),
    "C_satb": generate_satb,
    "D_full": generate_full,
}

def load_condition_names():
    with open(CONDITIONS_FILE) as f:
        manifest = json.load(f)
    return list(manifest["conditions"])

def parse_conditions(value):
    conditions = [item.strip() for item in value.split(",") if item.strip()]
    valid_conditions = set(load_condition_names()) & set(CONDITION_GENERATORS)
    invalid = sorted(set(conditions) - valid_conditions)
    if invalid:
        raise argparse.ArgumentTypeError(f"invalid conditions: {', '.join(invalid)}")
    return conditions

def main():
    parser = argparse.ArgumentParser(description="Generate DeepBach MIDI samples.")
    parser.add_argument("--conditions", type=parse_conditions, default=load_condition_names())
    parser.add_argument("--samples", type=int, default=10)
    args = parser.parse_args()

    if args.samples < 1:
        raise ValueError("--samples must be >= 1")

    # Make sure we are in models/deepbach directory for relative model path resolutions
    os.chdir(str(DEEPBACH_DIR))

    deepbach, dataset = setup_deepbach()

    outputs_base = PROJECT_ROOT / "outputs" / "deepbach"

    for condition in args.conditions:
        CONDITION_GENERATORS[condition](deepbach, dataset, outputs_base / condition, args.samples)

    print("\nDeepBach generation complete!")

if __name__ == "__main__":
    main()

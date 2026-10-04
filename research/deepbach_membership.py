"""Estimate which Bach chorales fell in DeepBach's training portion.

DeepBach (DatasetManager/chorale_dataset.py and music_dataset.py, commit
6d75cb9) builds its training examples by walking the music21 chorales in
corpus order, cutting every sixteenth-note window of 8 beats, and adding every
transposition that keeps all voices inside the corpus ranges. The resulting
tensor is split contiguously, without shuffling: the first 85 % for training,
the next 10 % for validation, the last 5 % for evaluation.

This module repeats that counting without building tensors, so each chorale's
examples get positions in the tensor, and the split boundaries tell whether the
chorale was seen in training. The estimate is marked verified only when the
total number of examples equals the length of the tensor dataset cached with
the pretrained resources; otherwise sensitivity analysis b is not run
(research/analysis_v2.py).
"""

import csv
from pathlib import Path

import numpy as np
from music21 import corpus


def count_examples(dataset, chorale):
    """Number of training examples DeepBach makes from one chorale (all windows x transpositions)."""
    one_tick = 1 / dataset.subdivision
    total = 0
    flat = chorale.flatten()
    for offset_start in np.arange(flat.lowestOffset - (dataset.sequences_size - one_tick), flat.highestOffset, one_tick):
        offset_end = offset_start + dataset.sequences_size
        ranges = dataset.voice_range_in_subsequence(chorale, offsetStart=offset_start, offsetEnd=offset_end)
        low, high = dataset.min_max_transposition(ranges)
        total += max(0, high - low + 1)
    return total


def estimate_membership(dataset, cached_length=None, split=(0.85, 0.10)):
    """Return one row per four-part corpus chorale with its example span and split."""
    rows = []
    position = 0
    for corpus_index, name in enumerate(corpus.chorales.Iterator(returnType="filename")):
        chorale = corpus.parse(name)
        if len(chorale.parts) != 4:
            continue
        examples = count_examples(dataset, chorale)
        rows.append({"melody_id": "bach-" + name.split("/")[-1].replace(".", "_"), "corpus_index": corpus_index,
                     "start": position, "end": position + examples, "examples": examples})
        position += examples
    train_end = int(split[0] * position)
    validation_end = int((split[0] + split[1]) * position)
    verified = int(cached_length is not None and cached_length == position)
    for row in rows:
        if row["end"] <= train_end:
            row["split"] = "train"
        elif row["start"] >= validation_end:
            row["split"] = "evaluation"
        elif row["start"] >= train_end and row["end"] <= validation_end:
            row["split"] = "validation"
        else:
            row["split"] = "boundary"
        row["total_examples"] = position
        row["cached_examples"] = "" if cached_length is None else cached_length
        row["verified"] = verified
    return rows


def write_membership(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path

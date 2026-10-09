"""Generation runs for protocol version 2.

A run lives in its own directory, research/outputs/runs/<run_id>/, and is
never overwritten. It holds:

    run.json          protocol snapshot, code revision, environment, backend settings
    melodies.csv      the melodies given to the models (copied manifest rows)
    melodies/         the exact MusicXML files given to the models
    attempts.jsonl    one line per generation attempt, appended, never rewritten
    raw/<model>/      raw model output per attempt (JSON)
    scores/<model>/   the four-voice MusicXML (and MIDI for listening) per successful attempt

Every attempt is logged with its status: ok, ineligible (the model cannot
encode the melody), model_error (the model raised an error), or output_error
(the output cannot be turned into four voices). Failed attempts are kept; a
retry happens only with --retry-failed and gets a new attempt number.

Backends: DeepBach runs in-process from research/models/deepbach; Coconet runs
through the tracked Node script research/coconet/run_coconet_v2.js; the fake
backend makes a deterministic, deliberately crude harmonization so the pipeline
can be checked without any model. Fake output is never research data.
"""

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from harmonization_io import (
    COCONET_DEFAULTS,
    DEEPBACH_DEFAULTS,
    IO_VERSION,
    Event,
    IneligibleMelody,
    OutputError,
    coconet_input,
    coconet_voices,
    deepbach_metadata,
    deepbach_tokens,
    deepbach_voices,
    harmonization_score,
    read_melody,
    write_score,
)
from voice_leading_v2 import INSTRUMENT_VERSION

RESEARCH = Path(__file__).resolve().parent
ROOT = RESEARCH.parent
PROTOCOL_FILE = RESEARCH / "experiments" / "protocol_v3.json"
RUNS_DIR = RESEARCH / "outputs" / "runs"
MODELS_DIR = RESEARCH / "models"
COCONET_SCRIPT = RESEARCH / "coconet" / "run_coconet_v2.js"


def load_protocol(path=PROTOCOL_FILE):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def attempt_seed(root_seed, model, melody_id, generation):
    """Deterministic per-attempt seed from the run's root seed."""
    text = f"{root_seed}|{model}|{melody_id}|{generation}"
    return int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)


def code_revision():
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                              check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True,
                               check=True).stdout.strip()
        return {"commit": head, "dirty_working_tree": bool(dirty)}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "dirty_working_tree": None}


def environment():
    import music21

    info = {"python": sys.version.split()[0], "platform": platform.platform(), "music21": music21.__version__}
    for module in ("numpy", "scipy", "torch"):
        try:
            info[module] = __import__(module).__version__
        except ImportError:
            info[module] = None
    return info


# --- Backends ----------------------------------------------------------------------------

class Backend:
    """Interface: name, settings(), check(melody), generate(jobs) -> {job_id: result}."""

    name = "base"
    seedable = False

    def settings(self):
        return {}

    def check(self, melody):
        """Raise IneligibleMelody when the model cannot encode the melody."""

    def generate(self, jobs):
        """jobs: list of dicts with job_id, melody, seed. Returns {job_id: dict(raw=..., error=...)}."""
        raise NotImplementedError

    def voices(self, raw, melody):
        """Turn raw output into Events per voice (S, A, T, B)."""
        raise NotImplementedError


class FakeBackend(Backend):
    """Deterministic stand-in for pipeline checks: alto, tenor, bass follow the soprano at fixed
    distances (a sixth, an octave plus a third, two octaves), shifted by the seed. Output is
    musically crude on purpose and produces parallel motion; it is not a harmonization model."""

    seedable = True

    def __init__(self, name="fake", fail_every=0, offsets=(9, 15, 24)):
        self.name = name
        self.fail_every = fail_every
        self.offsets = offsets
        self.calls = 0

    def settings(self):
        return {"backend": "fake", "description": "fixed-interval stand-in; pipeline check only",
                "fail_every": self.fail_every, "offsets": list(self.offsets)}

    def generate(self, jobs):
        results = {}
        for job in jobs:
            self.calls += 1
            if self.fail_every and self.calls % self.fail_every == 0:
                results[job["job_id"]] = {"error": "fake failure for testing"}
                continue
            shift = job["seed"] % 2
            notes = []
            alto, tenor, bass = self.offsets
            for event in job["melody"].notes:
                for voice, offset in ((1, alto + shift), (2, tenor), (3, bass)):
                    notes.append({"pitch": event.midi - offset, "quantizedStartStep": event.start,
                                  "quantizedEndStep": event.end, "instrument": voice})
            results[job["job_id"]] = {"raw": {"notes": notes}}
        return results

    def voices(self, raw, melody):
        voices = [list(melody.notes), [], [], []]
        from music21 import pitch

        for item in raw["notes"]:
            voices[item["instrument"]].append(
                Event(item["quantizedStartStep"], item["quantizedEndStep"], pitch.Pitch(midi=item["pitch"]).nameWithOctave))
        for line in voices[1:]:
            line.sort(key=lambda e: e.start)
        return voices


class DeepBachBackend(Backend):
    """DeepBach (Hadjeres et al. 2017), official PyTorch code with its pretrained resources."""

    name = "deepbach"
    seedable = True

    def __init__(self, settings, repo_dir=MODELS_DIR / "deepbach"):
        self.repo_dir = Path(repo_dir)
        self.config = {**DEEPBACH_DEFAULTS, **{k: v for k, v in settings.items() if k in DEEPBACH_DEFAULTS}}
        self.hyper = settings.get("hyperparameters", {})
        self.model = None
        self.dataset = None

    def _load(self):
        if self.model is not None:
            return
        if not (self.repo_dir / "DeepBach" / "model_manager.py").exists():
            raise RuntimeError(f"DeepBach is not installed in {self.repo_dir}; run make setup-v2")
        import torch

        original_load = torch.load

        def load_full(*args, **kwargs):  # resources were saved with torch 1.0 objects
            kwargs.setdefault("weights_only", False)
            return original_load(*args, **kwargs)

        torch.load = load_full
        sys.path.insert(0, str(self.repo_dir))
        from DatasetManager.dataset_manager import DatasetManager
        from DatasetManager.metadata import FermataMetadata, KeyMetadata, TickMetadata
        from DeepBach.model_manager import DeepBach

        previous = os.getcwd()
        os.chdir(self.repo_dir)  # VoiceModel.load reads models/ relative to the working directory
        try:
            metadatas = [FermataMetadata(), TickMetadata(subdivision=4), KeyMetadata()]
            self.dataset = DatasetManager().get_dataset(
                name="bach_chorales", voice_ids=[0, 1, 2, 3], metadatas=metadatas,
                sequences_size=8, subdivision=4)
            self.model = DeepBach(dataset=self.dataset, **self.hyper)
            self.model.load()
            self.model.cuda()
        finally:
            os.chdir(previous)

    def settings(self):
        return {"backend": "deepbach", **self.config, "hyperparameters": self.hyper,
                "voice_index_range": [1, 4], "random_init": True, "repo_dir": str(self.repo_dir)}

    def check(self, melody):
        self._load()
        deepbach_tokens(melody, self.dataset.note2index_dicts, self.dataset.voice_ranges)

    def generate(self, jobs):
        import random

        import numpy as np
        import torch

        self._load()
        results = {}
        for job in jobs:
            melody = job["melody"]
            try:
                tokens = deepbach_tokens(melody, self.dataset.note2index_dicts, self.dataset.voice_ranges)
                metadata = deepbach_metadata(melody)
                random.seed(job["seed"])
                np.random.seed(job["seed"])
                torch.manual_seed(job["seed"])
                _, tensor_chorale, _ = self.model.generation(
                    temperature=self.config["temperature"],
                    batch_size_per_voice=self.config["batch_size_per_voice"],
                    num_iterations=self.config["num_iterations"],
                    tensor_chorale=torch.tensor(tokens, dtype=torch.long),
                    tensor_metadata=torch.tensor(metadata, dtype=torch.long),
                    voice_index_range=[1, 4],
                    random_init=True,
                )
            except IneligibleMelody as error:
                results[job["job_id"]] = {"ineligible": str(error)}
                continue
            except Exception as error:  # noqa: BLE001 - any model failure is a recorded outcome, not a crash
                results[job["job_id"]] = {"error": f"{type(error).__name__}: {error}"}
                continue
            rows = tensor_chorale.cpu().tolist() if hasattr(tensor_chorale, "cpu") else tensor_chorale
            symbols = [[self.dataset.index2note_dicts[v][int(i)] for i in row] for v, row in enumerate(rows)]
            results[job["job_id"]] = {"raw": {"symbols": symbols}}
        return results

    def voices(self, raw, melody):
        return deepbach_voices_from_symbols(raw["symbols"])


def deepbach_voices_from_symbols(symbol_rows):
    """Parse DeepBach output stored as symbol strings (no model needed)."""
    index_rows, index2note = [], []
    for row in symbol_rows:
        vocab = {}
        indices = [vocab.setdefault(symbol, len(vocab)) for symbol in row]
        index_rows.append(indices)
        index2note.append({index: symbol for symbol, index in vocab.items()})
    return deepbach_voices(index_rows, index2note)


class CoconetBackend(Backend):
    """Coconet (Huang et al. 2017) through Magenta.js in Node, checkpoint coconet/bach."""

    name = "coconet"
    seedable = False  # Magenta.js samples with unseeded tf.randomUniform

    def __init__(self, settings, node_dir=MODELS_DIR / "coconet-v2", script=COCONET_SCRIPT):
        self.node_dir = Path(node_dir)
        self.script = Path(script)
        self.config = {**COCONET_DEFAULTS, **{k: v for k, v in settings.items() if k in COCONET_DEFAULTS}}
        self.checkpoint = settings.get("checkpoint_url")
        self.timeout = settings.get("timeout_seconds_per_job", 1800)

    def settings(self):
        return {"backend": "coconet", **self.config, "checkpoint_url": self.checkpoint,
                "infill_mask": "every step of alto, tenor, bass", "seed": "not supported by Magenta.js",
                "node_dir": str(self.node_dir)}

    def check(self, melody):
        coconet_input(melody)

    def generate(self, jobs, work_dir=None):
        if not (self.node_dir / "node_modules" / "@magenta" / "music").exists():
            raise RuntimeError(f"Magenta.js is not installed in {self.node_dir}; run make setup-v2")
        results = {}
        payload = []
        for job in jobs:
            try:
                sequence, mask = coconet_input(job["melody"])
            except IneligibleMelody as error:
                results[job["job_id"]] = {"ineligible": str(error)}
                continue
            payload.append({"job_id": job["job_id"], "sequence": sequence, "infillMask": mask,
                            "numIterations": self.config["numIterations"],
                            "temperature": self.config["temperature"]})
        if not payload:
            return results
        work_dir = Path(work_dir or self.node_dir)
        work_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        jobs_path = work_dir / f"coconet_jobs_{stamp}.jsonl"
        out_path = work_dir / f"coconet_results_{stamp}.jsonl"
        jobs_path.write_text("".join(json.dumps(item) + "\n" for item in payload), encoding="utf-8")
        command = ["node", str(self.script), "--jobs", str(jobs_path), "--out", str(out_path),
                   "--checkpoint", self.checkpoint, "--modules", str(self.node_dir / "node_modules")]
        process = subprocess.run(command, capture_output=True, text=True, check=False,
                                 timeout=self.timeout * max(1, len(payload)))
        received = {}
        if out_path.exists():
            for line in out_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    item = json.loads(line)
                    received[item["job_id"]] = item
        for item in payload:
            found = received.get(item["job_id"])
            if found is None:
                tail = (process.stderr or "")[-400:]
                results[item["job_id"]] = {"error": f"no Coconet output (exit {process.returncode}): {tail}"}
            elif "error" in found:
                results[item["job_id"]] = {"error": found["error"]}
            else:
                results[item["job_id"]] = {"raw": {"notes": found["notes"], "seconds": found.get("seconds")}}
        return results

    def voices(self, raw, melody):
        return coconet_voices(raw["notes"], melody)


def make_backend(name, protocol):
    settings = protocol["models"].get(name, {})
    if name == "deepbach":
        return DeepBachBackend(settings)
    if name == "coconet":
        return CoconetBackend(settings)
    if name == "fake":
        return FakeBackend()
    raise ValueError(f"unknown model {name}")


# --- Runs --------------------------------------------------------------------------------

class Run:
    def __init__(self, run_dir):
        self.dir = Path(run_dir)
        self.attempts_path = self.dir / "attempts.jsonl"

    @property
    def run_id(self):
        return self.dir.name

    @classmethod
    def create(cls, run_id, protocol, melody_rows, backends, stage, runs_dir=RUNS_DIR):
        run_dir = Path(runs_dir) / run_id
        if run_dir.exists():
            raise FileExistsError(f"{run_dir} exists; a run is never overwritten (use --resume)")
        (run_dir / "melodies").mkdir(parents=True)
        copied = []
        for row in melody_rows:
            target = run_dir / "melodies" / f"{row['melody_id']}.musicxml"
            shutil.copyfile(row["musicxml_file"], target)
            if row.get("sha256") and file_sha256(target) != row["sha256"]:
                raise RuntimeError(f"{row['melody_id']}: MusicXML changed since the manifest was written")
            copied.append({**row, "musicxml_file": str(target.relative_to(run_dir))})
        with open(run_dir / "melodies.csv", "w", newline="", encoding="utf-8") as handle:
            import csv

            writer = csv.DictWriter(handle, fieldnames=list(copied[0]))
            writer.writeheader()
            writer.writerows(copied)
        record = {
            "run_id": run_id,
            "stage": stage,
            "created_utc": utc_now(),
            "protocol": protocol,
            "instrument_version": INSTRUMENT_VERSION,
            "io_version": IO_VERSION,
            "code": code_revision(),
            "environment": environment(),
            "backends": {b.name: b.settings() for b in backends},
            "models_manifest": _models_manifest(),
            "melody_count": len(copied),
        }
        (run_dir / "run.json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        return cls(run_dir)

    def info(self):
        return json.loads((self.dir / "run.json").read_text(encoding="utf-8"))

    def melodies(self):
        import csv

        with open(self.dir / "melodies.csv", newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def attempts(self):
        if not self.attempts_path.exists():
            return []
        return [json.loads(line) for line in self.attempts_path.read_text(encoding="utf-8").splitlines() if line]

    def log(self, entry):
        with open(self.attempts_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _models_manifest():
    path = MODELS_DIR / "MODELS.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def pending_jobs(run, model, generations, retry_failed=False):
    """(melody_row, generation index, next attempt number) still to do for one model."""
    done, tries = set(), {}
    for entry in run.attempts():
        if entry["model"] != model:
            continue
        key = (entry["melody_id"], entry["generation"])
        tries[key] = max(tries.get(key, 0), entry["attempt"])
        if entry["status"] in ("ok", "ineligible") or not retry_failed:
            done.add(key)
    jobs = []
    for row in run.melodies():
        for generation in range(1, generations + 1):
            key = (row["melody_id"], generation)
            if key not in done:
                jobs.append((row, generation, tries.get(key, 0) + 1))
    return jobs


def generate(run, backend, generations, root_seed, retry_failed=False, batch_size=10, progress=print):
    """Run every pending attempt for one backend; return a count per status."""
    counts = {}
    pending = pending_jobs(run, backend.name, generations, retry_failed)
    for start in range(0, len(pending), batch_size):
        batch = pending[start:start + batch_size]
        jobs, meta = [], {}
        for row, generation, attempt in batch:
            melody = read_melody(run.dir / row["musicxml_file"], row["melody_id"])
            job_id = f"{backend.name}|{row['melody_id']}|g{generation}|a{attempt}"
            seed = attempt_seed(root_seed, backend.name, row["melody_id"], generation) + attempt - 1
            jobs.append({"job_id": job_id, "melody": melody, "seed": seed})
            meta[job_id] = (row, generation, attempt, melody, seed)
        started = time.time()
        if isinstance(backend, CoconetBackend):
            results = backend.generate(jobs, work_dir=run.dir / "work")
        else:
            results = backend.generate(jobs)
        elapsed = (time.time() - started) / max(1, len(jobs))
        for job_id, (row, generation, attempt, melody, seed) in meta.items():
            result = results.get(job_id, {"error": "backend returned no result"})
            entry = {"run_id": run.run_id, "model": backend.name, "melody_id": row["melody_id"],
                     "origin": row["origin"], "generation": generation, "attempt": attempt,
                     "seed": seed if backend.seedable else None, "seconds": round(elapsed, 3),
                     "finished_utc": utc_now(), "status": None, "reason": "", "raw_file": "", "score_file": "",
                     "score_sha256": ""}
            stem = f"{row['melody_id']}_g{generation}_a{attempt}"
            if "ineligible" in result:
                entry.update(status="ineligible", reason=result["ineligible"])
            elif "error" in result:
                entry.update(status="model_error", reason=result["error"])
            else:
                raw_path = run.dir / "raw" / backend.name / f"{stem}.json"
                raw_path.parent.mkdir(parents=True, exist_ok=True)
                raw_path.write_text(json.dumps(result["raw"]), encoding="utf-8")
                entry["raw_file"] = str(raw_path.relative_to(run.dir))
                try:
                    voices = backend.voices(result["raw"], melody)
                    score = harmonization_score(voices, melody)
                    xml_path = write_score(score, run.dir / "scores" / backend.name / stem)
                    entry.update(status="ok", score_file=str(xml_path.relative_to(run.dir)),
                                 score_sha256=file_sha256(xml_path))
                except OutputError as error:
                    entry.update(status="output_error", reason=str(error))
            run.log(entry)
            counts[entry["status"]] = counts.get(entry["status"], 0) + 1
        progress(f"{backend.name}: {min(start + batch_size, len(pending))}/{len(pending)} attempts done {counts}")
    return counts


def preflight(melody_rows, backends):
    """Check every melody against every backend's input encoding without generating."""
    report = []
    for row in melody_rows:
        melody = read_melody(row["musicxml_file"], row["melody_id"])
        for backend in backends:
            try:
                backend.check(melody)
                report.append({"melody_id": row["melody_id"], "model": backend.name, "accepted": 1, "reason": ""})
            except IneligibleMelody as error:
                report.append({"melody_id": row["melody_id"], "model": backend.name, "accepted": 0,
                               "reason": str(error)})
    return report

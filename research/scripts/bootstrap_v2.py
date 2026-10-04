#!/usr/bin/env python3
"""Install the two models for protocol version 2 and record their identities.

- DeepBach: official repository pinned to the commit in protocol_v2.json, plus
  the pretrained resources archive named in its dl_dataset_and_models.sh. The
  archive's SHA-256 is recorded; when the protocol already holds a checksum,
  a different archive stops the setup.
- Coconet: Magenta.js at the exact version in research/coconet/package.json,
  installed with npm into research/models/coconet-v2 together with the tracked
  runner script. The package lock and the checkpoint's weights manifest are hashed.

Writes research/models/MODELS.json, which every run copies into its run.json.
Downloads code, packages, and model weights; it does not generate music.

Usage (from the repository root):
    uv run python research/scripts/bootstrap_v2.py            # install and record
    uv run python research/scripts/bootstrap_v2.py --check    # report only, no downloads
    uv run python research/scripts/bootstrap_v2.py --with-tfjs-node   # also try the native TF backend
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[1]
MODELS = RESEARCH / "models"
PROTOCOL = RESEARCH / "experiments" / "protocol_v2.json"
DEEPBACH_DIR = MODELS / "deepbach"
COCONET_DIR = MODELS / "coconet-v2"
COCONET_SOURCE = RESEARCH / "coconet"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command, cwd=None):
    print("$", " ".join(map(str, command)))
    return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def deepbach(settings, check_only):
    record = {"repository": settings["repository"], "pinned_commit": settings["commit"]}
    if not DEEPBACH_DIR.exists():
        if check_only:
            return {**record, "status": "not installed"}
        run(["git", "clone", settings["repository"], str(DEEPBACH_DIR)])
    run(["git", "fetch", "--quiet", "origin"], cwd=DEEPBACH_DIR) if not check_only else None
    if not check_only:
        run(["git", "checkout", "--quiet", settings["commit"]], cwd=DEEPBACH_DIR)
    head = run(["git", "rev-parse", "HEAD"], cwd=DEEPBACH_DIR)
    record["installed_commit"] = head
    if head != settings["commit"]:
        raise SystemExit(f"DeepBach is at {head}, not the pinned {settings['commit']}")

    archive = MODELS / "deepbach_pytorch_resources.tar.gz"
    weights_ready = (DEEPBACH_DIR / "models").exists() and (DEEPBACH_DIR / "DatasetManager" / "dataset_cache").exists()
    if not archive.exists() and not weights_ready:
        if check_only:
            return {**record, "status": "code installed; resources missing"}
        last_error = None
        for url in settings["resources_urls"]:
            try:
                print(f"Downloading DeepBach resources from {url}")
                with urllib.request.urlopen(url, timeout=120) as response, open(archive, "wb") as handle:
                    shutil.copyfileobj(response, handle)
                record["resources_url"] = url
                break
            except OSError as error:
                last_error = error
                archive.unlink(missing_ok=True)
        else:
            raise SystemExit(f"Could not download DeepBach resources: {last_error}")
    if archive.exists():
        record["resources_sha256"] = sha256(archive)
        expected = settings.get("resources_sha256")
        if expected and expected != record["resources_sha256"]:
            raise SystemExit(f"DeepBach resources checksum {record['resources_sha256']} differs from the protocol's {expected}")
        if not weights_ready and not check_only:
            with tarfile.open(archive, "r:gz") as handle:
                handle.extractall(MODELS / "deepbach_extract")
            extracted = MODELS / "deepbach_extract" / "resources"
            (extracted / "dataset_cache").replace(DEEPBACH_DIR / "DatasetManager" / "dataset_cache")
            (extracted / "models").replace(DEEPBACH_DIR / "models")
            shutil.rmtree(MODELS / "deepbach_extract")
    record["weight_files"] = {p.name: sha256(p) for p in sorted((DEEPBACH_DIR / "models").glob("*"))} \
        if (DEEPBACH_DIR / "models").exists() else {}
    try:
        import torch

        record["torch"] = torch.__version__
    except ImportError:
        record["torch"] = None
        print("WARNING: PyTorch is not installed in this environment; run: uv pip install -r research/requirements.txt")
    record["status"] = "installed" if record["weight_files"] else "resources missing"
    return record


def coconet(settings, check_only, with_tfjs_node):
    record = {"package": "@magenta/music", "checkpoint_url": settings["checkpoint_url"]}
    if not check_only:
        COCONET_DIR.mkdir(parents=True, exist_ok=True)
        for name in ("package.json", "run_coconet_v2.js"):
            shutil.copyfile(COCONET_SOURCE / name, COCONET_DIR / name)
        npm = shutil.which("npm")
        if npm is None:
            raise SystemExit("npm is not installed; install Node.js 18 or later")
        run([npm, "install", "--no-audit", "--no-fund"], cwd=COCONET_DIR)
        if with_tfjs_node:
            try:
                run([npm, "install", "--no-audit", "--no-fund", "--no-save", "@tensorflow/tfjs-node@2.8.6"], cwd=COCONET_DIR)
                record["tfjs_node"] = "installed"
            except subprocess.CalledProcessError as error:
                record["tfjs_node"] = f"failed; CPU backend will be used ({error.stderr[-200:] if error.stderr else ''})"
    modules = COCONET_DIR / "node_modules"
    if not (modules / "@magenta" / "music").exists():
        return {**record, "status": "not installed"}
    record["magenta_version"] = json.loads((modules / "@magenta" / "music" / "package.json").read_text())["version"]
    record["tfjs_version"] = json.loads((modules / "@tensorflow" / "tfjs" / "package.json").read_text())["version"]
    lock = COCONET_DIR / "package-lock.json"
    record["package_lock_sha256"] = sha256(lock) if lock.exists() else None
    record["runner_sha256"] = sha256(COCONET_DIR / "run_coconet_v2.js")
    record["node"] = run(["node", "--version"])
    if not check_only:
        try:
            with urllib.request.urlopen(settings["checkpoint_url"] + "/weights_manifest.json", timeout=60) as response:
                manifest = response.read()
            record["weights_manifest_sha256"] = hashlib.sha256(manifest).hexdigest()
        except OSError as error:
            record["weights_manifest_sha256"] = f"not fetched: {error}"
    record["status"] = "installed"
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report the installed state without downloading")
    parser.add_argument("--with-tfjs-node", action="store_true", help="also install the native TensorFlow backend")
    args = parser.parse_args()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    MODELS.mkdir(exist_ok=True)
    manifest = {
        "written_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "protocol_version": protocol["protocol_version"],
        "deepbach": deepbach(protocol["models"]["deepbach"], args.check),
        "coconet": coconet(protocol["models"]["coconet"], args.check, args.with_tfjs_node),
    }
    print(json.dumps(manifest, indent=2))
    if not args.check:
        (MODELS / "MODELS.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"Wrote {MODELS / 'MODELS.json'}")
    return 0 if all(manifest[m]["status"] == "installed" for m in ("deepbach", "coconet")) else 1


if __name__ == "__main__":
    sys.exit(main())

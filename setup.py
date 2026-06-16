#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

COCONET_PACKAGE_JSON = """{
  "name": "coconet-runner",
  "version": "1.0.0",
  "description": "Coconet SATB generation via @magenta/music",
  "main": "run_coconet.js",
  "dependencies": {
    "@magenta/music": "^1.23.1"
  }
}"""

COCONET_RUNNER_JS = """/**
 * run_coconet.js — Coconet SATB generation wrapper
 * Dipanggil oleh experiments/scripts/run_coconet.py via subprocess.
 */
const fs   = require('fs');
const path = require('path');
const { Coconet } = (
  require(path.join(__dirname, 'node_modules', '@tensorflow', 'tfjs')),
  require(path.join(__dirname, 'node_modules', '@magenta', 'music', 'node', 'coconet'))
);

const CONDITIONS    = (process.env.COCONET_CONDITIONS || 'A_neutral,B_key,C_satb,D_full').split(',');
const SAMPLES       = parseInt(process.env.COCONET_SAMPLES || '10', 10);
const PROJECT_ROOT  = path.resolve(__dirname, '..', '..');
const SEED_PATH     = path.join(__dirname, 'seed_chorale.json');

function buildSeedSequence(seedData, condition) {
  const totalSteps = seedData.totalQuantizedSteps || 32;
  const notes = [];

  if (condition === 'A_neutral') {
    notes.push({ pitch: 60, quantizedStartStep: 0, quantizedEndStep: 4, instrument: 0 });
  } else if (condition === 'B_key') {
    notes.push({ pitch: 60, quantizedStartStep: 0, quantizedEndStep: 4, instrument: 0 });
    const cadenceStart = Math.max(0, totalSteps - 8);
    [{ p: 48, v: 3 }, { p: 55, v: 2 }, { p: 60, v: 0 }, { p: 64, v: 1 }].forEach(({ p, v }) => {
      notes.push({ pitch: p, quantizedStartStep: cadenceStart, quantizedEndStep: totalSteps, instrument: v });
    });
  } else if (condition === 'C_satb') {
    seedData.sopranoNotes.forEach(n => {
      notes.push({ pitch: n.pitch, quantizedStartStep: n.quantizedStartStep, quantizedEndStep: n.quantizedEndStep, instrument: 0 });
    });
  } else if (condition === 'D_full') {
    seedData.sopranoNotes.forEach(n => {
      notes.push({ pitch: n.pitch, quantizedStartStep: n.quantizedStartStep, quantizedEndStep: n.quantizedEndStep, instrument: 0 });
    });
    seedData.bassNotes.forEach(n => {
      notes.push({ pitch: n.pitch, quantizedStartStep: n.quantizedStartStep, quantizedEndStep: n.quantizedEndStep, instrument: 3 });
    });
  }
  return { notes, totalQuantizedSteps: totalSteps, quantizationInfo: { stepsPerQuarter: 4 } };
}

function getConditionShortName(condition) {
  return condition.split('_')[1] || condition;
}

async function main() {
  console.log('Coconet JS runner starting...');
  if (!fs.existsSync(SEED_PATH)) {
    throw new Error('Seed file not found. Run Python orchestrator first.');
  }
  const seedData = JSON.parse(fs.readFileSync(SEED_PATH, 'utf8'));
  const coconet = new Coconet('https://storage.googleapis.com/magentadata/js/checkpoints/coconet/bach');
  await coconet.initialize();
  console.log('Coconet model loaded.');

  for (const condition of CONDITIONS) {
    const shortName = getConditionShortName(condition);
    const outDir = path.join(PROJECT_ROOT, 'outputs', 'coconet', condition);
    fs.mkdirSync(outDir, { recursive: true });

    for (let i = 0; i < SAMPLES; i++) {
      const seed = buildSeedSequence(seedData, condition);
      const result = await coconet.infill(seed, { numIterations: 20, temperature: 0.99 });
      const allNotes = result.notes.map(n => ({
        pitch:               n.pitch,
        quantizedStartStep:  n.quantizedStartStep,
        quantizedEndStep:    n.quantizedEndStep,
        instrument:          n.instrument || 0,
      }));
      const idx     = String(i + 1).padStart(2, '0');
      const outPath = path.join(outDir, `coconet_${shortName}_${idx}.json`);
      fs.writeFileSync(outPath, JSON.stringify(allNotes, null, 2));
    }
  }
  console.log('Coconet JS generation complete!');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
"""

def run_cmd(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

def main():
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(exist_ok=True)

    # 1. Clone DeepBach
    deepbach_dir = models_dir / "deepbach"
    if not deepbach_dir.exists():
        print("Cloning DeepBach...")
        run_cmd(["git", "clone", "https://github.com/Ghadjeres/DeepBach.git", str(deepbach_dir)])
    else:
        print("DeepBach already exists.")

    # 2. Clone NotaGen
    notagen_dir = models_dir / "notagen"
    if not notagen_dir.exists():
        print("Cloning NotaGen...")
        run_cmd(["git", "clone", "https://github.com/ElectricAlexis/NotaGen.git", str(notagen_dir)])
    else:
        print("NotaGen already exists.")

    # 3. Setup Coconet
    coconet_dir = models_dir / "coconet"
    coconet_dir.mkdir(exist_ok=True)

    package_json_path = coconet_dir / "package.json"
    print("Writing coconet package.json...")
    package_json_path.write_text(COCONET_PACKAGE_JSON, encoding="utf-8")

    runner_js_path = coconet_dir / "run_coconet.js"
    print("Writing coconet run_coconet.js...")
    runner_js_path.write_text(COCONET_RUNNER_JS, encoding="utf-8")

    print("Installing Node dependencies for Coconet...")
    npm_cmd = shutil.which("npm")
    if not npm_cmd:
        print("WARNING: npm not found! Please install Node.js and run 'npm install' in models/coconet manually.")
    else:
        run_cmd([npm_cmd, "install"], cwd=str(coconet_dir))

    print("\nSetup successful! All models configured.")

if __name__ == "__main__":
    main()

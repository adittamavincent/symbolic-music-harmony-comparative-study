#!/usr/bin/env node
/**
 * Coconet runner for protocol version 2 (called by research/generation_v2.py).
 *
 * Reads one job per line from --jobs (JSON: job_id, sequence, infillMask,
 * numIterations, temperature), infills alto, tenor, and bass with the
 * Magenta.js Coconet checkpoint given by --checkpoint, and appends one result
 * per line to --out as soon as each job finishes, so finished jobs survive a
 * crash. A failed job is written with an "error" field; the runner continues.
 *
 * Magenta.js samples with tf.randomUniform without a seed, so runs cannot be
 * repeated bit for bit; the Python side records the seed as unsupported and
 * keeps every raw output instead.
 *
 * Usage: node run_coconet_v2.js --jobs jobs.jsonl --out results.jsonl \
 *          --checkpoint URL --modules path/to/node_modules
 */
'use strict';

const fs = require('fs');
const path = require('path');

function option(name) {
  const index = process.argv.indexOf(name);
  if (index === -1 || index + 1 >= process.argv.length) {
    throw new Error(`missing ${name}`);
  }
  return process.argv[index + 1];
}

async function main() {
  const jobsPath = option('--jobs');
  const outPath = option('--out');
  const checkpoint = option('--checkpoint');
  const modules = path.resolve(option('--modules'));
  const load = (name) => require(require.resolve(name, {paths: [modules]}));

  let backend = 'cpu';
  try {
    load('@tensorflow/tfjs-node');  // optional native backend; much faster when it installs
    backend = 'tensorflow';
  } catch (error) {
    backend = 'cpu';
  }
  const tf = load('@tensorflow/tfjs');
  const {Coconet} = load('@magenta/music/node/coconet');

  const model = new Coconet(checkpoint);
  await model.initialize();

  const jobs = fs.readFileSync(jobsPath, 'utf8').split('\n').filter((line) => line.trim());
  for (const line of jobs) {
    const job = JSON.parse(line);
    const started = Date.now();
    let result;
    try {
      const output = await model.infill(job.sequence, {
        numIterations: job.numIterations,
        temperature: job.temperature,
        infillMask: job.infillMask,
      });
      result = {
        job_id: job.job_id,
        notes: output.notes.map((n) => ({
          pitch: n.pitch,
          quantizedStartStep: n.quantizedStartStep || 0,
          quantizedEndStep: n.quantizedEndStep,
          instrument: n.instrument || 0,
        })),
        seconds: (Date.now() - started) / 1000,
        tf_backend: tf.getBackend() || backend,
      };
    } catch (error) {
      result = {job_id: job.job_id, error: String(error && error.stack ? error.stack : error)};
    }
    fs.appendFileSync(outPath, JSON.stringify(result) + '\n');
  }
  model.dispose();
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exit(1);
});

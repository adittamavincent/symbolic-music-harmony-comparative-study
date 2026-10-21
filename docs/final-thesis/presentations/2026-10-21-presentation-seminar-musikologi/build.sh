#!/usr/bin/env bash
set -euo pipefail
task_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "$task_dir/../../../.." && pwd)"
runtime_dir="${SEMINAR_RUNTIME_ROOT:-/Users/vincent/.cache/codex-runtimes/codex-primary-runtime/dependencies}"
cd "$repo_dir"
"$runtime_dir/python/bin/python3" "$task_dir/prepare_content.py"
"$runtime_dir/node/bin/node" "$task_dir/build.mjs" "$runtime_dir/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs"
"$runtime_dir/bin/override/soffice" --headless --convert-to pdf --outdir "$repo_dir/research/outputs/seminar-2026-10-21" "$repo_dir/research/outputs/seminar-2026-10-21/candidate.pptx"
"$runtime_dir/python/bin/python3" "$task_dir/publish_pdf.py"

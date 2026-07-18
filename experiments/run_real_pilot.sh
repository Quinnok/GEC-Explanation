#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"

"$PYTHON_BIN" experiments/src/real_pilot_pipeline.py \
  --expect-root data/downloads/Explainable_GEC \
  --sample-size 300 \
  --min-sample-size 100 \
  --check-size 30

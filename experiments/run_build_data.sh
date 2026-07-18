#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"

"$PYTHON_BIN" experiments/src/real_pilot_pipeline.py \
  --expect-root data/downloads/Explainable_GEC \
  --sample-size "${SAMPLE_SIZE:-300}" \
  --min-sample-size "${MIN_SAMPLE_SIZE:-100}" \
  --check-size "${CHECK_SIZE:-30}"

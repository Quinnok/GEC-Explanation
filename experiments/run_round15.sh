#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"

"$PYTHON_BIN" experiments/src/finalize_annotation_gold.py
"$PYTHON_BIN" experiments/src/evaluate_human_gold_metrics.py

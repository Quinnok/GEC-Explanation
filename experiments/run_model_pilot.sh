#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"
SAMPLE_SIZE="${SAMPLE_SIZE:-300}"
CHECK_SIZE="${CHECK_SIZE:-30}"
EXPLANATION_LIMIT="${EXPLANATION_LIMIT:-300}"

"$PYTHON_BIN" experiments/src/run_model_predictions.py \
  --sample-size "$SAMPLE_SIZE" \
  --overwrite \
  --output results/model_predictions/expect_v1_model_predictions.jsonl \
  --metadata results/model_predictions/runtime_metadata.json

"$PYTHON_BIN" experiments/src/analyze_model_edits.py \
  --predictions results/model_predictions/expect_v1_model_predictions.jsonl \
  --out-dir results/model_edits \
  --check-size "$CHECK_SIZE"

"$PYTHON_BIN" experiments/src/generate_model_edit_explanations.py \
  --input results/model_edits/model_edit_dataset.jsonl \
  --output data/processed/model_edit_explanation_candidates.jsonl \
  --stats data/processed/model_edit_explanation_candidate_stats.json \
  --limit "$EXPLANATION_LIMIT" \
  --batch-size "${EXPLANATION_BATCH_SIZE:-8}"

"$PYTHON_BIN" experiments/src/audit_explanation_candidates.py \
  --input data/processed/model_edit_explanation_candidates.jsonl \
  --out-dir results/model_explanations \
  --check-size "$CHECK_SIZE"

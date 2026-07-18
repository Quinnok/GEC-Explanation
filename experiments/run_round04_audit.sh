#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"

"$PYTHON_BIN" experiments/src/build_round04_audit.py \
  --count "${EXPLANATION_AUDIT_COUNT:-60}" \
  --out-dir results/audit

"$PYTHON_BIN" experiments/src/build_model_behavior_audit.py \
  --count "${MODEL_BEHAVIOR_AUDIT_COUNT:-100}" \
  --out-dir results/audit

"$PYTHON_BIN" experiments/src/t5_normalization_ablation.py \
  --out-dir results/model_edits

"$PYTHON_BIN" experiments/src/audit_alignment_reliability.py \
  --count "${ALIGNMENT_AUDIT_COUNT:-50}" \
  --out-dir results/audit

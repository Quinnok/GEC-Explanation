#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"

"$PYTHON_BIN" experiments/src/build_jfleg_samples.py \
  --jfleg-root data/downloads/jfleg \
  --sample-size "${JFLEG_SAMPLE_SIZE:-160}"

if [ "${RUN_JFLEG_MODELS:-0}" = "1" ]; then
  "$PYTHON_BIN" experiments/src/run_model_predictions.py \
    --input data/processed/jfleg_v1_samples.jsonl \
    --sample-size "${JFLEG_MODEL_SAMPLE_SIZE:-80}" \
    --models gector_roberta_base t5_base_grammar \
    --overwrite \
    --output results/model_predictions/jfleg_v1_model_predictions.jsonl \
    --metadata results/model_predictions/jfleg_v1_runtime_metadata.json

  "$PYTHON_BIN" experiments/src/analyze_model_edits.py \
    --predictions results/model_predictions/jfleg_v1_model_predictions.jsonl \
    --out-dir results/model_edits_jfleg \
    --check-size "${CHECK_SIZE:-30}"
fi

if [ "${RUN_COEDIT_MODELS:-0}" = "1" ]; then
  "$PYTHON_BIN" experiments/src/run_model_predictions.py \
    --input data/processed/expect_v1_samples.jsonl \
    --sample-size "${COEDIT_SAMPLE_SIZE:-20}" \
    --models coedit_large \
    --overwrite \
    --output results/model_predictions/expect_v1_coedit_predictions.jsonl \
    --metadata results/model_predictions/expect_v1_coedit_runtime_metadata.json

  "$PYTHON_BIN" experiments/src/analyze_model_edits.py \
    --predictions results/model_predictions/expect_v1_coedit_predictions.jsonl \
    --out-dir results/model_edits_coedit_expect \
    --check-size "${CHECK_SIZE:-30}"
fi

EDIT_FILES=(results/model_edits/model_edit_dataset.jsonl)
MISSING_FILES=(results/model_edits/missing_edit_diagnosis.jsonl)

if [ -f results/model_edits_jfleg/model_edit_dataset.jsonl ]; then
  EDIT_FILES+=(results/model_edits_jfleg/model_edit_dataset.jsonl)
  MISSING_FILES+=(results/model_edits_jfleg/missing_edit_diagnosis.jsonl)
fi

if [ -f results/model_edits_coedit_expect/model_edit_dataset.jsonl ]; then
  EDIT_FILES+=(results/model_edits_coedit_expect/model_edit_dataset.jsonl)
  MISSING_FILES+=(results/model_edits_coedit_expect/missing_edit_diagnosis.jsonl)
fi

"$PYTHON_BIN" experiments/src/build_faithfulness_benchmark.py \
  --edit-files "${EDIT_FILES[@]}" \
  --missing-files "${MISSING_FILES[@]}" \
  --explanation-files data/processed/model_edit_explanation_candidates.jsonl \
  --out-dir data/faithfulness_benchmark \
  --min-edits "${BENCHMARK_MIN_EDITS:-500}" \
  --max-edits "${BENCHMARK_MAX_EDITS:-700}" \
  --max-missing "${BENCHMARK_MAX_MISSING:-160}"

"$PYTHON_BIN" experiments/src/build_benchmark_docs.py \
  --benchmark-dir data/faithfulness_benchmark \
  --docs-dir docs

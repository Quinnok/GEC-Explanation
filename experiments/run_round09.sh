#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"
CF_MAX_PER_MODEL="${CF_MAX_PER_MODEL:-20}"
CHECK_SIZE="${CHECK_SIZE:-30}"
BOOTSTRAP_SAMPLES="${BOOTSTRAP_SAMPLES:-200}"

"$PYTHON_BIN" experiments/src/build_counterfactuals.py \
  --benchmark data/faithfulness_benchmark/edit_records.jsonl \
  --out-dir data/counterfactuals_round09 \
  --max-per-model "$CF_MAX_PER_MODEL"

PREDICTION_FILES=()
for MODEL in gector_roberta_base t5_base_grammar coedit_large; do
  INPUT="data/counterfactuals_round09/round08_counterfactual_sources_${MODEL}.jsonl"
  if [ -f "$INPUT" ]; then
    OUTPUT="results/round09/counterfactual_predictions_${MODEL}.jsonl"
    METADATA="results/round09/counterfactual_runtime_${MODEL}.json"
    "$PYTHON_BIN" experiments/src/run_model_predictions.py \
      --input "$INPUT" \
      --sample-size 100000 \
      --models "$MODEL" \
      --overwrite \
      --output "$OUTPUT" \
      --metadata "$METADATA"
    PREDICTION_FILES+=("$OUTPUT")
  fi
done

"$PYTHON_BIN" experiments/src/analyze_counterfactuals.py \
  --prediction-files "${PREDICTION_FILES[@]}" \
  --out-dir results/round09 \
  --check-size "$CHECK_SIZE"

"$PYTHON_BIN" experiments/src/run_counterfactual_simulators.py \
  --counterfactuals results/round09/counterfactual_labels.jsonl \
  --benchmark-dir data/faithfulness_benchmark \
  --out-dir results/round09

"$PYTHON_BIN" experiments/src/analyze_round09.py \
  --benchmark-dir data/faithfulness_benchmark \
  --round08-dir results/round08 \
  --round09-dir results/round09 \
  --docs-dir docs \
  --bootstrap-samples "$BOOTSTRAP_SAMPLES"

#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"
CF_MAX_PER_MODEL="${CF_MAX_PER_MODEL:-8}"
CHECK_SIZE="${CHECK_SIZE:-30}"

"$PYTHON_BIN" experiments/src/run_faithfulness_methods.py \
  --benchmark-dir data/faithfulness_benchmark \
  --out-dir results/round08

"$PYTHON_BIN" experiments/src/build_counterfactuals.py \
  --benchmark data/faithfulness_benchmark/edit_records.jsonl \
  --out-dir data/counterfactuals \
  --max-per-model "$CF_MAX_PER_MODEL"

PREDICTION_FILES=()

for MODEL in gector_roberta_base t5_base_grammar coedit_large; do
  INPUT="data/counterfactuals/round08_counterfactual_sources_${MODEL}.jsonl"
  if [ -f "$INPUT" ]; then
    OUTPUT="results/round08/counterfactual_predictions_${MODEL}.jsonl"
    METADATA="results/round08/counterfactual_runtime_${MODEL}.json"
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
  --out-dir results/round08 \
  --check-size "$CHECK_SIZE"

"$PYTHON_BIN" experiments/src/summarize_round08.py \
  --results-dir results/round08 \
  --docs-dir docs \
  --tables-dir results/tables

#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 INPUT_JSONL MODEL_KEY OUTPUT_JSONL METADATA_JSON" >&2
  echo "Environment: PYTHON_BIN=.venv311/bin/python CHUNKS=4 JOBS=2 WORK_DIR=tmp/prediction_chunks" >&2
  exit 2
fi

INPUT_JSONL="$1"
MODEL_KEY="$2"
OUTPUT_JSONL="$3"
METADATA_JSON="$4"

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"
CHUNKS="${CHUNKS:-4}"
JOBS="${JOBS:-2}"
WORK_DIR="${WORK_DIR:-tmp/prediction_chunks/${MODEL_KEY}_$(date +%Y%m%d_%H%M%S)}"

if [ -e "$WORK_DIR" ]; then
  echo "Refusing to reuse existing WORK_DIR: $WORK_DIR" >&2
  exit 2
fi
mkdir -p "$WORK_DIR"

"$PYTHON_BIN" experiments/src/split_jsonl.py \
  --input "$INPUT_JSONL" \
  --out-dir "$WORK_DIR/chunks" \
  --chunks "$CHUNKS"

count=0
for CHUNK in "$WORK_DIR"/chunks/chunk_*.jsonl; do
  NAME="$(basename "$CHUNK" .jsonl)"
  (
    "$PYTHON_BIN" experiments/src/run_model_predictions.py \
      --input "$CHUNK" \
      --sample-size 100000 \
      --models "$MODEL_KEY" \
      --overwrite \
      --output "$WORK_DIR/pred_${NAME}.jsonl" \
      --metadata "$WORK_DIR/meta_${NAME}.json"
  ) &
  count=$((count + 1))
  if [ $((count % JOBS)) -eq 0 ]; then
    wait
  fi
done
wait

"$PYTHON_BIN" experiments/src/merge_prediction_chunks.py \
  --prediction-dir "$WORK_DIR" \
  --output "$OUTPUT_JSONL" \
  --metadata "$METADATA_JSON"

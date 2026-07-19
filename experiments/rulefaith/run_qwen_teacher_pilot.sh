#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"
LIMIT="${RULEFAITH_QWEN_LIMIT:-80}"
SHARDS="${RULEFAITH_QWEN_SHARDS:-1}"
MODEL="${RULEFAITH_QWEN_MODEL:-Qwen/Qwen2.5-0.5B-Instruct}"
OUT="data/rulefaith/teacher_candidates_qwen_small_pilot.jsonl"
STATS="results/rulefaith/qwen_teacher_generation_stats.json"
PARSE_FAILURES="results/rulefaith/qwen_teacher_parse_failures.jsonl"
RAW_DIR="results/rulefaith/qwen_teacher_raw_responses"

mkdir -p data/rulefaith results/rulefaith logs/rulefaith
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"

if [[ "$SHARDS" == "1" ]]; then
  "$PYTHON_BIN" experiments/rulefaith/generate_teacher_candidates.py \
    --provider qwen_small \
    --qwen-model "$MODEL" \
    --limit "$LIMIT" \
    --output "$OUT" \
    --stats "$STATS" \
    --parse-failures "$PARSE_FAILURES" \
    --raw-dir "$RAW_DIR" \
    --resume
else
  mkdir -p data/rulefaith/qwen_shards results/rulefaith/qwen_shards "$RAW_DIR"
  pids=()
  for shard_index in $(seq 0 $((SHARDS - 1))); do
    shard_out="data/rulefaith/qwen_shards/teacher_candidates_qwen_small_pilot_shard_${shard_index}.jsonl"
    shard_stats="results/rulefaith/qwen_shards/teacher_generation_stats_shard_${shard_index}.json"
    shard_failures="results/rulefaith/qwen_shards/teacher_parse_failures_shard_${shard_index}.jsonl"
    shard_raw="${RAW_DIR}/shard_${shard_index}"
    "$PYTHON_BIN" experiments/rulefaith/generate_teacher_candidates.py \
      --provider qwen_small \
      --qwen-model "$MODEL" \
      --limit "$LIMIT" \
      --num-shards "$SHARDS" \
      --shard-index "$shard_index" \
      --output "$shard_out" \
      --stats "$shard_stats" \
      --parse-failures "$shard_failures" \
      --raw-dir "$shard_raw" \
      --resume \
      > "logs/rulefaith/qwen_shard_${shard_index}.out" \
      2> "logs/rulefaith/qwen_shard_${shard_index}.err" &
    pids+=("$!")
  done
  for pid in "${pids[@]}"; do
    wait "$pid"
  done
  "$PYTHON_BIN" experiments/rulefaith/merge_teacher_candidate_shards.py \
    --glob "data/rulefaith/qwen_shards/teacher_candidates_qwen_small_pilot_shard_*.jsonl" \
    --output "$OUT" \
    --stats "$STATS"
fi

"$PYTHON_BIN" experiments/rulefaith/audit_teacher_candidates.py \
  --input "$OUT" \
  --json-output results/rulefaith/qwen_teacher_candidate_quality_flags.json \
  --md-output results/rulefaith/qwen_teacher_candidate_quality_report.md

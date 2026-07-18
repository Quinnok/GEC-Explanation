#!/usr/bin/env bash
set -euo pipefail

EDIT_LIMIT="${EDIT_LIMIT:-80}"
LLM_JUDGE_LIMIT="${LLM_JUDGE_LIMIT:-2000}"
LLM_BATCH_SIZE="${LLM_BATCH_SIZE:-16}"
RUN_LOCAL_LLM_JUDGE="${RUN_LOCAL_LLM_JUDGE:-1}"

cmd=(
  .venv311/bin/python experiments/src/run_reranking_experiment.py
  --benchmark-dir data/faithfulness_benchmark
  --round09-dir results/round09
  --out-dir results/round11
  --docs-dir docs
  --edit-limit "$EDIT_LIMIT"
  --llm-judge-limit "$LLM_JUDGE_LIMIT"
  --llm-batch-size "$LLM_BATCH_SIZE"
)

if [[ "$RUN_LOCAL_LLM_JUDGE" == "1" ]]; then
  cmd+=(--run-local-llm-judge)
fi

"${cmd[@]}"

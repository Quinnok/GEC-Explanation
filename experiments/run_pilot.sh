#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p logs results/predictions
LOG_PATH="logs/toy_pilot_$(date +%Y%m%d_%H%M%S).log"

{
  echo "date=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit=NOT_A_GIT_REPOSITORY"
  echo "command=python3 experiments/src/run_toy_pilot.py"
  python3 experiments/src/run_toy_pilot.py \
    --input data/raw/toy_pilot.jsonl \
    --predictions results/predictions/toy_pilot_predictions.jsonl \
    --summary results/summary.json \
    --raw-results results/raw_results.json
} 2>&1 | tee "$LOG_PATH"

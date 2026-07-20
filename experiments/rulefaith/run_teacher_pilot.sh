#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"
PROVIDER="${RULEFAITH_TEACHER_PROVIDER:-open_teacher}"
LIMIT="${RULEFAITH_TEACHER_LIMIT:-80}"

"$PYTHON_BIN" experiments/rulefaith/generate_teacher_candidates.py \
  --provider "$PROVIDER" \
  --limit "$LIMIT" \
  --resume

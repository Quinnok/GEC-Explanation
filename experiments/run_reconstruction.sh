#!/usr/bin/env bash
set -euo pipefail
python3 experiments/src/reconstruct_edit.py \
  --source "She go home ." \
  --explanation "Replace \"go\" with \"goes\" because the subject is singular." \
  --error-type "SVA"


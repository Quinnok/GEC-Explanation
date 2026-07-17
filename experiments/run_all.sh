#!/usr/bin/env bash
set -euo pipefail
python3 -m unittest discover -s experiments/tests
bash experiments/run_pilot.sh
python3 experiments/src/generate_tables.py


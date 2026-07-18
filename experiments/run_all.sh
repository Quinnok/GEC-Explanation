#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"

"$PYTHON_BIN" -m unittest discover -s experiments/tests
bash experiments/run_build_data.sh
bash experiments/run_model_pilot.sh

if command -v latexmk >/dev/null 2>&1; then
  (cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex)
elif [ -x ".local-tex/TinyTeX/bin/universal-darwin/latexmk" ]; then
  TEXBIN="$PWD/.local-tex/TinyTeX/bin/universal-darwin"
  (export PATH="$TEXBIN:$PATH"; cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex)
fi

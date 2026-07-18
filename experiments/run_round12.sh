#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv311/bin/python}"
TEXBIN="$PWD/.local-tex/TinyTeX/bin/universal-darwin"

"$PYTHON_BIN" experiments/src/build_paper_assets.py

(
  export PATH="$TEXBIN:$PATH"
  cd paper
  "$TEXBIN/latexmk" -pdf -interaction=nonstopmode -halt-on-error main.tex
  ! grep -E "LaTeX Warning|Citation.*undefined|Reference.*undefined|Undefined control sequence|Fatal error|Overfull|Underfull" main.log
)

(
  export PATH="$TEXBIN:$PATH"
  cd paper/supplementary
  "$TEXBIN/latexmk" -pdf -interaction=nonstopmode -halt-on-error appendix.tex
  ! grep -E "LaTeX Warning|Citation.*undefined|Reference.*undefined|Undefined control sequence|Fatal error|Overfull|Underfull" appendix.log
)

"$PYTHON_BIN" experiments/src/check_paper_consistency.py

# Round 05: Literature Package and Research Lineage

Date: 2026-07-18

## Objective

Build a complete literature folder and novelty-threat map before locking the paper idea.

## Commands Run

- `.venv311/bin/python -m pip install openpyxl`
- `.venv311/bin/python experiments/src/build_literature_package.py`
- `find literature -maxdepth 2 -type f | sort`
- `.venv311/bin/python - <<'PY' ...` to validate row/card counts and year/status distributions

## Outputs

- `experiments/src/build_literature_package.py`
- `literature/00_overview/README.md`
- `literature/01_gec_explanation/README.md`
- `literature/02_gec_evaluation/README.md`
- `literature/03_explanation_faithfulness/README.md`
- `literature/04_simulatability/README.md`
- `literature/05_counterfactual_explanation/README.md`
- `literature/06_gec_robustness/README.md`
- `literature/07_rule_grounding/README.md`
- `literature/08_novelty_threats/README.md`
- `literature/paper_cards/*.md`
- `literature/literature_matrix.csv`
- `literature/literature_matrix.md`
- `literature/literature_matrix.xlsx`
- `literature/research_lineage.md`
- `literature/chronological_lineage.md`
- `literature/method_taxonomy.md`
- `literature/experimental_pattern_summary.md`
- `literature/novelty_threats.md`

## Validation

- Total paper cards: 50.
- Matrix rows: 50.
- XLSX generated: yes.
- Year distribution: 2012: 1, 2014: 1, 2015: 1, 2016: 1, 2017: 2, 2019: 4, 2020: 7, 2021: 1, 2023: 5, 2024: 10, 2025: 12, 2026: 5.
- 2023-2024 key precursor papers: 15.
- Earlier foundations: 18.
- P0 closest/threat papers: 13.

## Key Literature Decision

Reverse Edit Reconstruction should be downgraded to an L1 edit-correspondence / leakage diagnostic. The strongest surviving paper direction is Counterfactual Edit Simulatability for model-produced GEC edits, with rule/evidence grounding as an L3 auxiliary signal.

## Closest Work

- GEE and Prompt Insertion already cover natural-language GEC explanation generation from erroneous/corrected pairs.
- EXCGEC already covers edit-wise explainable GEC as a benchmark in Chinese.
- CLEME2.0 already covers decomposed correction behaviors: hit/correct, wrong, under/missed, and overcorrection.
- COCOGEC already covers GEC-specific counterfactuals for robustness.
- Hase and Bansal already define simulatability as helping users predict model behavior.
- Parcalabescu and Frank warn that many natural-language faithfulness tests measure output-level self-consistency rather than internal faithfulness.

## Consequence for Round 06

The next round must compare candidate ideas explicitly and choose a main/backup line. The candidate list must not preserve reverse reconstruction as the main contribution by inertia.

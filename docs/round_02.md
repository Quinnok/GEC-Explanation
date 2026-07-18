# Round 02: Real Pilot Pipeline

Last updated: 2026-07-18

## Actions

- Consolidated state under `docs/` and removed the duplicate `research/` directory.
- Initialized Git and committed the Bootstrap state.
- Added project ignores for local environments, TeX tools, downloaded corpora, and generated PDF output.
- Installed ERRANT 3.0.2 and spaCy `en_core_web_sm` in `.venv311`.
- Installed local TinyTeX under `.local-tex/` and compiled `paper/main.tex` with `latexmk`.
- Downloaded EXPECT from the public upstream repository and built a versioned real pilot sample.
- Extracted ERRANT edits, compared token diff against ERRANT, built automatic explanation variants, ran two baselines, and generated paper tables/sections from `results/`.

## Evidence

- Real sample count: 300.
- ERRANT edit count: 320.
- Explanation pilot records: 3000.
- Token diff vs ERRANT exact sample match before type labels: 94.7%.
- Structured explicit Full Edit Exact on explicit explanations: 99.7%.
- Structured explicit Full Edit Exact on raw edit strings: 100.0%.

## Next Single Action

Run a focused literature and human-validation design pass before upgrading automatic pilot labels into claims about real explanation faithfulness.

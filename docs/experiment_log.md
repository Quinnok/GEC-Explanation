# Experiment Log

Last updated: 2026-07-18

## Iteration 1

- Workspace: `/Users/bytedance/Documents/GEC可解释性`
- Git status: not a Git repository.
- Python: system Python 3.9.6; bundled Python also available.
- GPU: `nvidia-smi` not found.
- Disk: about 773GiB available on current volume.
- Real datasets found locally: none.
- Real GEC outputs found locally: none.
- Real explanation annotations found locally: none.
- Unit tests: `python3 -m unittest discover -s experiments/tests`, 5 tests passed.
- Toy sanity check: `bash experiments/run_pilot.sh`, completed successfully.
- Toy outputs: `results/predictions/toy_pilot_predictions.jsonl`, `results/summary.json`, `results/raw_results.json`, `results/tables/toy_summary.tex`.
- Toy macro full edit exact: 0.25. This number is not research evidence and must not be reported as a paper result.
- LaTeX compile attempt: `pdflatex` is not installed in this environment, so paper compilation is blocked until a TeX distribution or `tectonic` is available.


## Iteration 2

- EXPECT cloned from `https://github.com/lorafei/Explainable_GEC` at commit `6e44b68f6e4c199dd3b235cacb604a856bd3d133`.
- Real pilot sample: 300 EXPECT source/reference pairs in `data/processed/expect_v1_samples.jsonl`.
- ERRANT edits: 320 in `results/edit_extraction/expect_v1_errant_edits.jsonl`.
- ERRANT/token-diff check report: `results/edit_extraction/expect_errant_check_30.md`.
- Explanation pilot: 3000 automatic template records in `data/processed/expect_v1_explanation_pilot.jsonl`; not human gold.
- Baselines run: `surface_keyword`, `structured_explicit`.
- Leakage metrics: `results/real_pilot/condition_metrics.json`.
- Paper compile: `paper/main.tex` compiled successfully with local TinyTeX/latexmk; final grep found no LaTeX warnings, overfull/underfull boxes, unresolved citations, or fatal errors.


## Iteration 2

- EXPECT cloned from `https://github.com/lorafei/Explainable_GEC` at commit `6e44b68f6e4c199dd3b235cacb604a856bd3d133`.
- Real pilot sample: 300 EXPECT source/reference pairs in `data/processed/expect_v1_samples.jsonl`.
- ERRANT edits: 320 in `results/edit_extraction/expect_v1_errant_edits.jsonl`.
- ERRANT/token-diff check report: `results/edit_extraction/expect_errant_check_30.md`.
- Explanation pilot: 3000 automatic template records in `data/processed/expect_v1_explanation_pilot.jsonl`; not human gold.
- Baselines run: `surface_keyword`, `structured_explicit`.
- Leakage metrics: `results/real_pilot/condition_metrics.json`.
- Paper compile: `paper/main.tex` compiled successfully with local TinyTeX/latexmk; logs retained under `logs/`.

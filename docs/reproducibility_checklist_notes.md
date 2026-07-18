# Reproducibility Checklist Notes

These notes are source material for filling `AuthorKit27/ReproducibilityChecklist.tex`.

| Checklist Area | Current Evidence |
|---|---|
| Code for preprocessing | `experiments/src/real_pilot_pipeline.py`, `build_jfleg_samples.py`, `extract_edits.py`, `analyze_model_edits.py`. |
| Code for experiments | `run_faithfulness_methods.py`, `build_counterfactuals.py`, `run_counterfactual_simulators.py`, `run_reranking_experiment.py`. |
| Data splits/statistics | `data/faithfulness_benchmark/benchmark_stats.json`, `docs/benchmark_card.md`, `docs/data_statement.md`. |
| Model details | `results/model_predictions/*runtime_metadata.json`, `docs/model_data_downloads.md`. |
| Hyperparameters | Shell scripts expose sample size, counterfactual max per model, bootstrap samples, judge limit, and batch size. |
| Evaluation metrics | `paper/sections/experimental_setup.tex`, `results/round09/statistical_analysis.json`, `results/round11/reranking_metrics.json`. |
| Statistical tests | Grouped bootstrap with 200 samples in Round 09; paired bootstrap deltas stored in `results/round09/statistical_analysis.json`. |
| Compute | CPU-only local runs; runtime metadata stored for prediction and local judge stages. |
| Randomness | Deterministic stable hashes and fixed seed in statistical analysis where used. |
| Human evaluation | Annotation package exists, but completed human labels are 0; status is blocked. |
| Licenses | `docs/license_summary.md` and `docs/license_report.md`. |
| Artifact checksum | `results/round14/result_checksums.sha256`. |

Do not answer "yes" to human-evaluation reproducibility items until real annotator files exist.

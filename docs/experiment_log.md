# Experiment Log

Last updated: 2026-07-18

## Iteration 1

- Workspace: `/Users/bytedance/Documents/GEC可解释性`
- Git status at start: not a Git repository.
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
- LaTeX compile attempt: `pdflatex` was not installed.

## Iteration 2

- EXPECT cloned from `https://github.com/lorafei/Explainable_GEC` at commit `6e44b68f6e4c199dd3b235cacb604a856bd3d133`.
- Real pilot sample: 300 EXPECT source/reference pairs in `data/processed/expect_v1_samples.jsonl`.
- ERRANT edits: 320 in `results/edit_extraction/expect_v1_errant_edits.jsonl`.
- ERRANT/token-diff check report: `results/edit_extraction/expect_errant_check_30.md`.
- Explanation pilot: 3000 automatic template records in `data/processed/expect_v1_explanation_pilot.jsonl`; not human gold.
- Baselines run: `surface_keyword`, `structured_explicit`.
- Leakage metrics: `results/real_pilot/condition_metrics.json`.
- Paper compile: `paper/main.tex` compiled successfully with local TinyTeX/latexmk; final grep found no LaTeX warnings, overfull/underfull boxes, unresolved citations, or fatal errors.
- Round 02 committed as `1bb4c57 Round 02 real EXPECT ERRANT pilot`.

## Round 03

- Cleaned Round 02 workspace state, ignored or deleted non-research installation logs, and removed smoke prediction outputs.
- Model prediction command: `.venv311/bin/python experiments/src/run_model_predictions.py --sample-size 300 --overwrite --output results/model_predictions/expect_v1_model_predictions.jsonl --metadata results/model_predictions/runtime_metadata.json`.
- Sequence-to-edit model: `gotutiyan/gector-roberta-base-5k`, revision `adaac6fb919431fb5a038b1e449055ae638613a4`, non-commercial-only model card. Runtime: 300 samples, 247 changed, 39 copied reference, 13.511s CPU.
- Sequence-to-sequence model: `vennify/t5-base-grammar-correction`, revision `9e4a09d21dca1072a69302df9261289d03c3ed78`, CC-BY-NC-SA-4.0 model card. Runtime: 300 samples, 295 changed, 0 copied reference, 157.650s CPU.
- Prediction file: `results/model_predictions/expect_v1_model_predictions.jsonl`, 600 rows.
- Edit alignment command: `.venv311/bin/python experiments/src/analyze_model_edits.py --predictions results/model_predictions/expect_v1_model_predictions.jsonl --out-dir results/model_edits --check-size 30`.
- Model-produced edit dataset: `results/model_edits/model_edit_dataset.jsonl`, 1707 actual predicted edits.
- Missing-edit diagnosis: `results/model_edits/missing_edit_diagnosis.jsonl`, 319 missed reference edits.
- Behavior distribution: GECToR correct 142, wrong 37, overcorrection 493, missed 141; T5 correct 71, wrong 71, overcorrection 893, missed 178.
- Readable alignment report: `results/model_edits/model_edit_alignment_check_30.md`, balanced 15 GECToR and 15 T5 cases.
- Alignment failures: 6 ambiguous cases in `results/model_edits/alignment_failures.jsonl`.
- EXPECT field audit: EXPECT provides source, target, correction index, evidence index, error type, predicted parsing order, and origin; it does not provide natural-language explanations.
- Open-source explanation candidate command: `.venv311/bin/python experiments/src/generate_model_edit_explanations.py --limit 300 --batch-size 8 --output data/processed/model_edit_explanation_candidates.jsonl --stats data/processed/model_edit_explanation_candidate_stats.json`.
- Explanation candidates: 300 FLAN-T5-base candidates, balanced 150 per GEC model, generated from source, model prediction, and predicted edit span; not human gold.
- Explanation candidate audit: `results/model_explanations/explanation_candidate_check_30.md` and `results/model_explanations/explanation_candidate_quality_flags.json`.

## Round 04

- Round 03 committed as `8a8fedb Round 03 model-predicted edit pilot`.
- Explanation/edit audit command: `.venv311/bin/python experiments/src/build_round04_audit.py --count 60 --out-dir results/audit`.
- Explanation/edit audit outputs: `results/audit/round04_sample_audit.jsonl`, `results/audit/round04_sample_audit.md`, `results/audit/round04_audit_summary.json`.
- Model behavior audit command: `.venv311/bin/python experiments/src/build_model_behavior_audit.py --count 100 --out-dir results/audit`.
- Model behavior audit outputs: 100 rows in `results/audit/model_behavior_audit_100.jsonl`; behavior counts correct 24, wrong 24, over 28, missed 24.
- T5 normalization command: `.venv311/bin/python experiments/src/t5_normalization_ablation.py --out-dir results/model_edits`.
- T5 raw stats: correct 71, wrong 71, over 893, missed 178, precision 0.068599, recall 0.221875, F0.5 0.079596.
- T5 excluding ORTH+PUNCT stats: correct 71, wrong 49, over 345, missed 193, precision 0.152688, recall 0.226837, F0.5 0.163369.
- T5 substantive-only stats: correct 71, wrong 45, over 245, missed 195, precision 0.196676, recall 0.228296, F0.5 0.202279.
- Normalization changes: 297 T5 predictions changed under at least one normalization in `results/model_edits/normalization_changes.jsonl`.
- Alignment reliability command: `.venv311/bin/python experiments/src/audit_alignment_reliability.py --count 50 --out-dir results/audit`.
- Alignment reliability outputs: `results/audit/alignment_reliability_audit_50.md`, `results/audit/alignment_reliability_audit_50.jsonl`, `results/audit/alignment_reliability_summary.json`.
- Exact-only vs stable alignment over 600 sentences: exact-only correct 213, over 1494, missed 427; stable correct 213, wrong 90, over 1404, missed 337.

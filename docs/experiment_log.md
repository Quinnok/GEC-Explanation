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
- Round 04 committed as `2667862 Round 04 audit normalization alignment`.

## Round 05

- Installed `openpyxl` 3.1.5 in `.venv311` to generate `literature/literature_matrix.xlsx`.
- Literature package command: `.venv311/bin/python experiments/src/build_literature_package.py`.
- Literature package outputs: 50 paper cards in `literature/paper_cards/`, matrix files in CSV/Markdown/XLSX, and lineage/taxonomy/novelty documents under `literature/`.
- Literature validation: matrix rows 50, paper cards 50, XLSX exists.
- Year coverage: five 2026 papers, twelve 2025 papers, fifteen 2023-2024 papers, and eighteen earlier foundations.
- P0 closest/threat papers identified: COCOGEC, EXCGEC, CLEME2.0, GEE, Prompt Insertion, EXPECT, ERRANT, BEA-2019, Hase and Bansal simulatability, Jacovi and Goldberg faithfulness, Lyu et al. faithfulness survey, and Parcalabescu and Frank self-consistency.
- Verification: `.venv311/bin/python -m py_compile experiments/src/build_literature_package.py` passed.
- Verification: `.venv311/bin/python -m unittest discover -s experiments/tests` ran 5 tests, all passed.
- Paper compile verification: `../.local-tex/TinyTeX/bin/universal-darwin/latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in `paper/` reported `main.pdf` up to date.
- LaTeX log check found no warnings, undefined citations/references, fatal errors, overfull boxes, or underfull boxes.
- Round 05 committed as `fa2b7fc Round 05 literature package`.

## Round 06

- Idea restructuring outputs: `docs/idea_candidates.md`, `docs/idea_score_matrix.csv`, `docs/idea_review_panel.md`, `docs/final_idea_decision.md`, and `docs/round_06.md`.
- Six ideas compared: Reverse Edit Reconstruction, Leakage-adjusted Edit Simulatability, Counterfactual Edit Simulatability, Rule-grounded Faithfulness, Evidence-grounded Faithfulness, and Faithfulness-calibrated Explanation Reranking.
- Simulated five reviewer perspectives: GEC specialist, explainability/faithfulness specialist, evaluation specialist, counterfactual learning specialist, and educational NLP specialist.
- Decision: select Counterfactual Edit Simulatability as the main line; select Rule-grounded Faithfulness as backup; demote Reverse Edit Reconstruction to an L1 edit-correspondence/leakage diagnostic.
- Paper updated: title, abstract, introduction, problem formulation, method, related work, experimental setup, results wording, conclusion, and BibTeX.
- Verification: `.venv311/bin/python -m unittest discover -s experiments/tests` ran 5 tests, all passed.
- Paper compile verification: `PATH="$PWD/../.local-tex/TinyTeX/bin/universal-darwin:$PATH" ../.local-tex/TinyTeX/bin/universal-darwin/latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in `paper/` completed successfully.
- LaTeX log check found no warnings, undefined citations/references, fatal errors, overfull boxes, or underfull boxes.
- Round 06 committed as `1db85c8 Round 06 idea restructuring`.

## Round 07

- JFLEG cloned from `https://github.com/keisks/jfleg` and recorded at commit `ee06ff806a208aba815ac45313f4e750a48330a5`; upstream README states Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.
- JFLEG processing command: `.venv311/bin/python experiments/src/build_jfleg_samples.py --jfleg-root data/downloads/jfleg --sample-size 160`.
- JFLEG processed sample file: `data/processed/jfleg_v1_samples.jsonl`, 160 rows, all four references retained, `ref0` used as the primary ERRANT reference for this pilot.
- JFLEG model command: `.venv311/bin/python experiments/src/run_model_predictions.py --input data/processed/jfleg_v1_samples.jsonl --sample-size 80 --models gector_roberta_base t5_base_grammar --overwrite --output results/model_predictions/jfleg_v1_model_predictions.jsonl --metadata results/model_predictions/jfleg_v1_runtime_metadata.json`.
- JFLEG runtime: GECToR 80 samples, 71 changed, 7.436 CPU seconds; T5 80 samples, 80 changed, 23.322 CPU seconds.
- JFLEG edit analysis command: `.venv311/bin/python experiments/src/analyze_model_edits.py --predictions results/model_predictions/jfleg_v1_model_predictions.jsonl --out-dir results/model_edits_jfleg --check-size 30`.
- JFLEG model-produced edits: 540 in `results/model_edits_jfleg/model_edit_dataset.jsonl`; missed edits: 378 in `results/model_edits_jfleg/missing_edit_diagnosis.jsonl`.
- CoEdIT command: `.venv311/bin/python experiments/src/run_model_predictions.py --input data/processed/expect_v1_samples.jsonl --sample-size 20 --models coedit_large --overwrite --output results/model_predictions/expect_v1_coedit_predictions.jsonl --metadata results/model_predictions/expect_v1_coedit_runtime_metadata.json`.
- CoEdIT model: `grammarly/coedit-large`, revision `5637bcdf9d8d4419f97c8cfea36f7d35c79232b6`, CC-BY-NC-4.0 model card, instruction prefix `Fix grammatical errors in this sentence: `.
- CoEdIT runtime: 20 EXPECT samples, 20 changed, 0 copied reference, 90.428 CPU seconds; model weight download was about 3.13GB.
- CoEdIT edit analysis command: `.venv311/bin/python experiments/src/analyze_model_edits.py --predictions results/model_predictions/expect_v1_coedit_predictions.jsonl --out-dir results/model_edits_coedit_expect --check-size 20`.
- CoEdIT model-produced edits: 122 in `results/model_edits_coedit_expect/model_edit_dataset.jsonl`; missed edits: 8 in `results/model_edits_coedit_expect/missing_edit_diagnosis.jsonl`.
- Benchmark build command: `bash experiments/run_benchmark.sh`.
- Benchmark outputs: `data/faithfulness_benchmark/edit_records.jsonl` with 700 model-produced edits; `data/faithfulness_benchmark/explanation_instances.jsonl` with 12,754 explanation/control instances; `data/faithfulness_benchmark/missing_edit_diagnosis.jsonl` with 160 missed-edit diagnoses.
- Benchmark selected model counts: CoEdIT 122, GECToR 298, T5 280.
- Benchmark selected dataset counts: EXPECT 420, JFLEG 280.
- Benchmark selected behavior counts: correct 136, wrong 126, overcorrection 438.
- Benchmark selected operation counts: delete 58, insert 115, replace 527; ERRANT error-type count: 41.
- Documentation generated from JSON outputs: `docs/benchmark_card.md`, `docs/data_statement.md`, `docs/license_report.md`, and `data/faithfulness_benchmark/leakage_audit.json`.
- Leakage audit: 0 source texts cross train/dev/test splits; 32 predicted target strings cross splits, mostly common punctuation/function words.
- Verification: unit tests, Python compile checks, shell syntax checks, `git diff --check`, `bash experiments/run_benchmark.sh`, and final `latexmk` compile all passed; LaTeX log grep found no warnings, undefined citations/references, fatal errors, overfull boxes, or underfull boxes.
- Round 07 committed as `7b35499 Round 07 faithfulness benchmark`.

## Round 08

- Fixed structured parser to recognize `source span [s,e)` as well as `source token span [s,e)`.
- Added regression test for the Round 07 explicit-template span format; unit tests now run 6 tests.
- L1/L3 command: `.venv311/bin/python experiments/src/run_faithfulness_methods.py --benchmark-dir data/faithfulness_benchmark --out-dir results/round08`.
- L1/L3 evaluated examples: 11,764; skipped labels: `{"candidate_not_gold": 290, "pending_counterfactual_label": 700}`.
- L1/L3 methods implemented and run: random, majority, no-explanation majority, current-edit-only, surface keyword, structured explicit extraction, reverse reconstruction, no-source reconstruction, target-masked reconstruction, leakage-adjusted reconstruction, TF-IDF embedding similarity, NLI lexical proxy, rule/evidence verifier, no-rule verifier, no-evidence verifier.
- L1/L3 headline macro-F1: random 0.490; majority 0.396; surface keyword 0.579; structured explicit extraction 0.639; reverse reconstruction 0.640; target-masked reconstruction 0.439; leakage-adjusted reconstruction 0.496; TF-IDF similarity 0.703; NLI proxy 0.736; rule/evidence verifier 0.767.
- L1 reconstruction full exact: structured/reverse 0.098; target-masked 0.015; leakage-adjusted 0.035.
- Counterfactual source command: `.venv311/bin/python experiments/src/build_counterfactuals.py --benchmark data/faithfulness_benchmark/edit_records.jsonl --out-dir data/counterfactuals --max-per-model 8`.
- Counterfactual sources: 24 origin edits and 48 variants, split evenly into 24 error-irrelevant and 24 rule-relevant variants; model counts GECToR 8, T5 8, CoEdIT 8 origin edits.
- Counterfactual reruns: GECToR 16 samples in 5.890s CPU; T5 16 samples in 12.505s CPU; CoEdIT 16 samples in 52.096s CPU.
- Counterfactual labels from actual model reruns: preserve 23, competing_edit 20, cancel 3, change_span 2.
- Counterfactual baseline macro-F1: random 0.150, source-edit availability 0.161, variant-family prior 0.193.
- Round 08 report and tables generated from JSON: `docs/round_08.md`, `results/tables/round08_l1_methods.tex`, `results/tables/round08_counterfactual_methods.tex`.
- Added optional parallel chunked prediction entry point: `experiments/run_parallel_model_predictions.sh`; not used for Round 08 because the current counterfactual sample is small and CoEdIT multi-process loading may hurt CPU memory/runtime.
- End-to-end reproduction command passed: `CF_MAX_PER_MODEL=8 CHECK_SIZE=30 bash experiments/run_round08.sh`.

# Evidence Index

| Question | Evidence |
|---|---|
| Are predictions real model outputs? | `results/model_predictions/*_predictions.jsonl`, runtime metadata JSON files. |
| Are edits model-produced rather than reference edits? | `data/faithfulness_benchmark/edit_records.jsonl`; each row contains source, reference, prediction, model, and predicted edit. |
| Are labels human gold? | No. `data/faithfulness_benchmark/benchmark_stats.json` has `human_gold_count: 0`; `results/round10/human_annotation_status.json` is `blocked_no_human_annotation`. |
| Does reconstruction leak edit fields? | `results/round09/statistical_analysis.json`, `results/paper_assets/leakage_ablation_table.tex`, Round 11 reward-hacking report. |
| Are counterfactual labels actual model behavior? | `results/round09/counterfactual_labels.jsonl` records `label_source: actual_original_gec_model_rerun`. |
| How are competing edits handled? | `results/round09/counterfactual_labels.jsonl`; paper keeps `competing_edit` separate. |
| What are the main automatic results? | `results/round09/statistical_analysis.json`, `results/paper_assets/main_results_table.tex`. |
| Does reranking reward templates? | `results/round11/reward_hacking_report.json`; combined/surface/reconstruction top-1 edit-copy rates are 1.0. |
| Is there an LLM judge baseline? | `results/round11/local_llm_judge_metadata.json`; local FLAN-T5, no paid API. |
| Is the paper format checked? | `results/round12/paper_consistency_check.json`; `docs/aaai27_requirements_check.md`. |
| Are artifacts reproducible? | `docs/reproduction_commands.md`, `results/round14/result_checksums.sha256`. |


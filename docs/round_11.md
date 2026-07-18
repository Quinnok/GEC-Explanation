# Round 11: Explanation Candidate Reranking

## Completed

- Built reranking candidates for 80 model-produced edits.
- Candidate count: 880.
- Compared random, length, surface, local open-source LLM judge, reconstruction, counterfactual, rule/evidence, and combined rerankers.
- Evaluated pairwise ranking accuracy, MRR, automatic top-1 faithfulness, grammatical-validity proxy, helpfulness proxy, length, fluency proxy, and reward-hacking indicators.

## Key Result

- Best automatic pairwise ranking method: `combined_reranker` with 0.935 pairwise accuracy.
- This best score is reward-hacking prone: `combined_reranker`, `surface_score`, and `reconstruction_score` select template/edit-copy explanations as top-1 for 100.0% of the 80 edits.
- The local open-source FLAN-T5 judge covered all 880 candidates in 74.919 CPU seconds, but performed below random on the automatic pairwise ranking metric (0.455 vs. random 0.509).
- Human top-1 preference remains blocked because no human labels exist.

## Metrics

| Method | Pairwise | MRR | Auto Top-1 Faithfulness | Template Top-1 | Edit-Copy Top-1 |
|---|---:|---:|---:|---:|---:|
| combined_reranker | 0.935 | 1.000 | 0.978 | 1.000 | 1.000 |
| counterfactual_score | 0.548 | 0.754 | 0.455 | 0.250 | 0.275 |
| length_heuristic | 0.825 | 1.000 | 0.704 | 0.038 | 0.038 |
| local_llm_judge | 0.455 | 0.671 | 0.374 | 0.175 | 0.213 |
| random_selection | 0.509 | 0.705 | 0.391 | 0.200 | 0.225 |
| reconstruction_score | 0.729 | 1.000 | 0.957 | 1.000 | 1.000 |
| rule_evidence_score | 0.744 | 0.912 | 0.679 | 0.463 | 0.512 |
| surface_score | 0.760 | 1.000 | 0.970 | 1.000 | 1.000 |

## Interpretation

- Reranking can be used as an application of the evaluation suite, but current automatic labels reward explicit edit templates too strongly.
- The strongest automatic methods should be treated as leakage/ranking controls, not as evidence that the selected explanation is pedagogically useful or human-preferred.
- Human preference remains unavailable until real annotators complete the Round 10 package.

## Files

- `results/round11/reranking_candidates.jsonl`
- `results/round11/reranking_scored_candidates.jsonl`
- `results/round11/reranking_metrics.json`
- `results/round11/reward_hacking_report.json`
- `results/tables/round11_reranking.tex`

# Rebuttal Draft: Reviewer 3

## Likely Concern

The method does not outperform simple baselines, and reranking can be reward-hacked by template explanations.

## Response

This is a central empirical finding rather than an omitted weakness. The paper reports that current L2 simulators are weak: the best automatic L2 baseline reaches 0.297 Macro-F1. The reranking experiment shows that high automatic pairwise accuracy can select explanations that simply copy the edit. We therefore frame the contribution as an evaluation benchmark and diagnostic suite, not a solved explanation selection method.

## Evidence

- `paper/sections/results.tex`
- `paper/sections/ablation.tex`
- `results/round09/statistical_analysis.json`
- `results/round11/reranking_metrics.json`
- `results/round11/reward_hacking_report.json`

## Planned Revision If Space Allows

Emphasize the negative result in the conclusion: automatic metrics must be audited for edit-copy reward hacking before being used for learner-facing explanation selection.


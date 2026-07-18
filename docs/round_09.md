# Round 09: Scaled Pilot Statistics and Error Analysis

## Completed

- Grouped bootstrap with 200 resamples by source sentence/edit group.
- Paired bootstrap deltas with Holm correction for L1 methods.
- Grouped analysis by dataset, model, behavior, error type, operation, sentence length, edit multiplicity, explanation type, and negative type.
- Error-analysis packets for successes, failures, instability, invalid/competing counterfactuals, multi-reference candidates, ERRANT alignment issues, and simulator confusions.
- LaTeX tables generated under `results/tables/`.

## Scaled Counterfactual Run

- Counterfactual labels: `{"cancel": 7, "change_span": 3, "change_target": 1, "competing_edit": 52, "preserve": 57}`
- Counterfactual simulator instances: 1080 unique explanation-variant pairs; 6480 method prediction rows.
- Best automatic L1 method by grouped bootstrap macro-F1: `rule_evidence_verifier` = 0.767 [0.752, 0.785]
- Best automatic L2 simulator by grouped bootstrap macro-F1: `trained_explanation_type_prior` = 0.297 [0.277, 0.312]

## Claim Answers

- Closest metric to human faithfulness: unanswered because no human labels exist yet.
- Reverse reconstruction leakage: supported in the automatic benchmark by large drops under target masking and leakage adjustment.
- Counterfactual nontrivial gain: not supported yet; current explanation-conditioned simulator baselines remain weak.
- Rule-relevant counterfactuals: more likely to disrupt the original edit, but many become competing edits rather than clean cancellations.
- Model-family and behavior differences: analyzable in the produced grouped files, but CoEdIT is still small and labels are automatic.

## Key Files

- `results/round09/statistical_analysis.json`
- `results/round09/counterfactual_simulator_metrics.json`
- `results/round09/error_analysis/`
- `results/tables/round09_l1_bootstrap.tex`
- `results/tables/round09_counterfactual_bootstrap.tex`

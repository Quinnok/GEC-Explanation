# Post-Human-Eval Idea Decision

Updated: 2026-07-19

## Decision

Do not frame the current paper as a solved `Counterfactual Edit Simulatability` method paper or as a completed `RuleFaith-GEC` method paper.

The strongest defensible direction is now:

> **Human-grounded stress testing of GEC explanation metrics.**

Recommended title family:

> **Beyond Edit Reconstruction: A Human-Adjudicated Stress Test for GEC Explanation Faithfulness**

## Evidence

Round 15 finalized 160 adjudicated edit-explanation labels from two independent human annotators and a human third-party adjudicator, confirmed by the user on 2026-07-19. The set is a stress test, not a natural sample:

- Final faithfulness labels: `faithful=1`, `partially_faithful=57`, `unfaithful=102`.
- Final edit alignment labels: `correct=18`, `partially_correct=46`, `incorrect=96`.
- Final rule labels: `correct=4`, `partially_correct=18`, `incorrect=39`, `not_applicable=99`.
- Final evidence labels: `correct=1`, `partially_correct=15`, `incorrect=19`, `not_provided=125`.

Against these labels, the best full-coverage binary faithfulness metrics were:

| Method | Faithfulness Macro-F1 | AUROC | Notes |
|---|---:|---:|---|
| Surface leakage score | 0.800 | 0.820 | Strong because many stress-test labels reward/penalize explicit edit information. |
| Reverse reconstruction | 0.789 | 0.772 | Good for edit alignment, weak for rule/evidence quality. |
| Rule/evidence verifier | 0.695 | 0.720 | Better rule recall but low precision; not sufficient as a solved RuleFaith method. |
| Combined proxy | 0.713 | 0.880 | Strong ordinal separation but still mixes leakage, reconstruction, and rule heuristics. |

The local FLAN-T5 judge only covered 15 of the 160 items through Round 11 reranking outputs, so it cannot be used as the main LLM-judge result for this human set.

## Interpretation

The human-adjudicated stress test supports the following conservative claims:

1. Edit reconstruction and surface leakage scores are useful for **edit alignment**, but they do not validate grammar rules or evidence.
2. High reconstruction can coexist with `not_applicable` rules and `not_provided` evidence, especially for edit-copy templates.
3. Rule/evidence verification is directionally useful but currently too noisy to claim a solved RuleFaith evaluator.
4. The paper should separate `edit alignment`, `edit validity`, `rule correctness`, `evidence correctness`, and `overall faithfulness` rather than collapse them into a single metric.

## Chosen Main Line

Use the paper as a critical evaluation and benchmark paper:

> We build a model-edit-level GEC explanation stress test and show that automatic metrics that look strong on edit reconstruction can fail to capture rule and evidence quality under adjudicated labels.

## Downgraded Claims

- `Counterfactual Edit Simulatability` remains a useful future direction and diagnostic layer, but the current L2 simulator result is weak.
- `RuleFaith-GEC` remains the best method-development direction, but Round 15 does not yet show that the current verifier solves rule/evidence faithfulness.
- `Reverse Edit Reconstruction` should remain an L1 edit-identifiability diagnostic, not the main faithfulness claim.

## Required Next Step

Generate a stronger natural-explanation validation set:

1. Select 150--200 substantive non-ORTH/PUNCT model edits.
2. Generate natural post-hoc and rule-grounded explanations with GPT-5.5 and at least one open model.
3. Annotate a balanced subset using the V2 protocol.
4. Re-evaluate whether rule/evidence metrics still outperform reconstruction when templates are not dominant.

Until then, the current paper should avoid claiming broad real-world explanation quality.

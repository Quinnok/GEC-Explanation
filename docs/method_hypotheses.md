# RuleFaith-GEC Preregistered Hypotheses

Created: 2026-07-19

These hypotheses are frozen before GPT-5.5 teacher generation, verifier recalibration, student training, and method-pilot result inspection on the new natural explanation data.

## Primary Hypotheses

H1. Filtered SFT will achieve higher human Rule Correctness than Vanilla SFT on natural edit-level explanations.

H2. Preference Optimization after Filtered SFT will achieve higher human Overall Faithfulness than Filtered SFT alone.

H3. RuleFaith-GEC will reduce false rationalization rate relative to Vanilla SFT, especially for invalid, stylistic, and wrong-correction edits.

H4. Under target-masked evaluation, RuleFaith-GEC will still outperform Vanilla SFT in Rule Correctness and Overall Faithfulness.

H5. At the same explanation coverage, RuleFaith-GEC will have lower faithfulness risk than Direct Teacher, Vanilla SFT, and LLM Judge reranking.

H6. The RuleFaith-GEC improvement trend will hold on at least two corrector families.

## Secondary Hypotheses

H7. A verifier score with leakage and genericness penalties will reduce edit-copy explanations relative to reconstruction-only reranking.

H8. Rule/evidence verification will identify wrong-rule and wrong-evidence negatives better than reverse reconstruction.

H9. Selective abstention will improve risk at fixed coverage without merely rejecting all wrong-correction cases.

H10. A smaller student model trained with verifier-filtered preferences will reduce cost per faithful explanation relative to direct GPT-5.5 generation.

## Primary Metrics

- Edit Alignment Macro-F1 / AUROC.
- Edit Validity Awareness Macro-F1 / AUROC.
- Rule Correctness Macro-F1 / AUROC.
- Evidence Correctness Macro-F1 / AUROC.
- Overall Faithfulness Macro-F1 / AUROC.
- False Rationalization Rate.
- Target-Masked Rule Correctness.
- Risk at matched coverage.
- AURC and ECE for selective explanation.
- Cost and latency per 1,000 explanations.

## Locked Evaluation Rules

- The final natural-explanation test set must not be used to tune verifier weights.
- Weights are determined on train/dev only.
- Report equal-weight and learned-weight score variants.
- Do not collapse all dimensions into one score unless all component dimensions are separately reported.
- Report grouped bootstrap confidence intervals by source sentence or edit cluster.
- Report results by dataset, corrector, behavior, error type, operation, and valid/invalid edit.


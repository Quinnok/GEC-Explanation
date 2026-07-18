# Rebuttal Draft: Reviewer 2

## Likely Concern

Counterfactual Edit Simulatability may be too close to GEC robustness or counterfactual data augmentation, especially COCOGEC.

## Response

The goal differs from robustness evaluation. COCOGEC studies counterfactual generation for robust GEC; our diagnostic starts from a model-produced edit and asks whether an explanation predicts how the same GEC model behaves when the input is changed. Labels are not theoretical expectations: each counterfactual source is passed through the original model, and ERRANT is used to compare the resulting edit behavior. We also keep `competing_edit` as its own class to avoid overstating clean preservation or cancellation.

## Evidence

- `paper/sections/related_work.tex`
- `paper/sections/method.tex`
- `paper/supplementary/appendix.tex`
- `results/round09/counterfactual_labels.jsonl`
- `results/round09/error_analysis/counterfactual_invalid_or_competing_20.jsonl`

## Planned Revision If Space Allows

Add a compact table contrasting inputs/outputs of GEE, EXCGEC, COCOGEC, and this diagnostic in the supplement.


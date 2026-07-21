# Loop N: Qwen3 Ready-Candidate Codex Pseudo-Validation

Date: 2026-07-21

## Objective

Fill the 41-row Qwen3 ready-candidate validation package so the method loop can continue while preserving the distinction between real human validation and Codex/AI pseudo-validation.

## Input

- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_form.csv`
- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_key.csv`

## Implementation

- Added `experiments/rulefaith/complete_qwen3_ready_validation_codex.py`.
- Added `experiments/tests/test_qwen3_ready_validation_codex.py`.
- The script validates that the 41 validation IDs exactly match the label map, fills the six validator fields, merges the completed form with the hidden key, and writes summary/case reports.

## Commands

```bash
python3 experiments/rulefaith/complete_qwen3_ready_validation_codex.py --overwrite
```

## Outputs

- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_completed_by_codex.csv`
- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_completed_by_codex_merged_with_key.csv`
- `results/rulefaith/qwen3_ready_validation_codex_summary.json`
- `results/rulefaith/qwen3_ready_validation_codex_cases.md`

## Verified Results

- Candidate count: 41.
- Overall decisions: 17 `accept`, 13 `refine`, 11 `reject`.
- Edit alignment: 38 `pass`, 3 `partial`.
- Edit validity: 27 `valid`, 4 `acceptable_alternative`, 4 `stylistic`, 6 `invalid`.
- Rule plausibility: 22 `plausible`, 9 `weak`, 10 `implausible`.
- Evidence sufficiency: 22 `sufficient`, 18 `partial`, 1 `insufficient`.

## Scientific Interpretation

The pseudo-validation catches several failures that passed the automatic gates, including false rationalization of invalid edits, plausible-looking but wrong article explanations, insufficient implied-noun evidence, and punctuation rules that do not match the source structure. This supports the current RuleFaith design choice: automatic field-aware and target-masked gates are useful for narrowing candidate pools, but they are not sufficient to promote Qwen3 candidates into final positives.

## Boundary

These labels are `codex_ai_pseudo_validation`. They are not human labels, not human gold, and not suitable for final paper claims about human evaluation. They can be used for internal triage, prompt repair, candidate filtering, and selecting examples for a future real-human natural explanation evaluation.

## Decision

Use the 17 accepted pseudo-validated candidates only as provisional seed positives for a small internal method smoke test. Do not use them as final SFT/preference training positives until they are validated by real annotators or a stronger preregistered validation protocol.

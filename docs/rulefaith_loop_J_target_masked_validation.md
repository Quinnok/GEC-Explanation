# Loop J: Target-Masked RuleFaith Validation

Date: 2026-07-21

## Status

Round: Loop J

Main objective: test whether the field-aware Qwen3 accepted/refine pool still carries rule and evidence signals when the target edit string is hidden from rule, rationale, and applicability-condition text.

Highest risk: the validation is deterministic and heuristic. It reduces target-copy reward hacking risk but does not prove human rule correctness.

## Hypothesis

If field-aware selection recovers candidates for the right reason, then many candidates should keep grammar and source-evidence signals after target masking. Candidates whose quality depends on the target string, mismatched rule category, or generic wording should be routed to refine or rejected.

## Implemented

- Added `experiments/rulefaith/validate_qwen3_target_masked.py`.
- Added `experiments/tests/test_qwen3_target_masked_validation.py`.
- Installed `pytest` into the user Python environment because it was previously missing.
- Added target masking for `rule_text`, `rationale`, and `applicability_conditions`.
- Added exact-token masking so a target such as `go` does not mask substrings such as `going`.
- Added rule-category mismatch checks for common failure modes, including noun-number edits explained as subject-verb agreement.
- Kept the output boundary explicit: target-masked `validated` candidates are validation candidates only, not human gold and not SFT positives.

## Inputs

- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_refine.jsonl`

## Outputs

- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_validated.jsonl`
- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_refine.jsonl`
- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_rejected.jsonl`
- `results/rulefaith/qwen3_target_masked_validation_stats.json`
- `results/rulefaith/qwen3_target_masked_validation_report.md`
- `results/rulefaith/qwen3_target_masked_validation.csv`

## Commands Executed

```bash
python3 -m pip install --user pytest
python3 -m py_compile experiments/rulefaith/validate_qwen3_target_masked.py
python3 -m unittest experiments.tests.test_qwen3_target_masked_validation
python3 experiments/rulefaith/validate_qwen3_target_masked.py --overwrite
```

## Verified Results

- Input candidates: 58.
- Field-aware input buckets: 45 accepted, 13 refine.
- Target-masked buckets: 47 validated, 8 refine, 3 rejected.
- Previous accepted bucket retention: 39/45 validated, 5 refine, 1 rejected.
- Previous refine bucket retention: 8/13 validated, 3 refine, 2 rejected.
- Score mean/min/max: 0.8543 / 0.0 / 1.0.
- Output line counts: 47 validated JSONL rows, 8 refine JSONL rows, 3 rejected JSONL rows, and 58 CSV data rows.

Failure counts:

- `target_dependent_quality_text`: 7
- `masked_rule_lacks_grammar_signal`: 2
- `generic_after_target_mask`: 1
- `rule_category_mismatch:noun_number_explained_as_subject_verb_agreement`: 2
- `rule_category_mismatch:orthography_rule_lacks_spelling_signal`: 2
- `rule_category_mismatch:pronoun_rule_lacks_pronoun_signal`: 1
- `rule_category_mismatch:verb_rule_lacks_verb_signal`: 1

Warning counts:

- `rationale_edit_copy`: 13
- `specific_evidence_not_mentioned_in_rule_or_rationale`: 21

## Scientific Interpretation

Target-masked validation provides a stronger automatic filter than the field-aware gate alone. It shows that 47 candidates keep enough rule/evidence structure after hiding the target string, while 11 candidates need repair or rejection because target dependence, genericness, or category mismatch remains.

This result is useful for building a next-stage validation/refinement pool. It is not enough for paper claims about human faithfulness because the check is heuristic and can miss subtle rule errors.

## Claim-Evidence Update

Claim M-C19 is partially supported: target-masked validation can reduce target-copy and rule-category shortcuts before positive-data construction. Remaining evidence needed: Codex/manual rule plausibility audit, stronger verifier or real-human spot check, and natural explanation evaluation.

## Next Internal Action

Run a rule-plausibility and evidence-sufficiency audit over the 47 target-masked validated candidates. The audit should identify cases where the rule is linguistically plausible but mismatched, oversimplified, or not truly supported by the extracted evidence.

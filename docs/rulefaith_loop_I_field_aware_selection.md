# Loop I: Field-Aware RuleFaith Selection

Date: 2026-07-21

## Status

Round: Loop I

Main objective: avoid over-penalizing the required structured `edit_description` field while keeping leakage, alignment, validity, rule, and evidence gates strict.

Highest risk: field-aware accepted candidates are only suitable for target-masked validation and additional verification. They are automatic pseudo-label decisions, not human labels and not SFT positives.

## Hypothesis

The strict Loop H selection gate rejected every repaired Qwen3 candidate because it treated the required structured edit description as leakage. If edit-copy in `edit_description` is reported but not used as a hard failure, while edit-copy in `rule_text` and `rationale` remains penalized, the repaired pool should yield a usable validation pool without weakening hard alignment, validity, rule, and evidence gates.

## Implemented

- Added `experiments/rulefaith/select_qwen3_field_aware_rulefaith.py`.
- Added `experiments/tests/test_qwen3_field_aware_selection.py`.
- Split leakage checks by field:
  - `edit_description_edit_copy`
  - `edit_description_target_copy`
  - `rule_text_edit_copy`
  - `rule_text_target_copy`
  - `rationale_edit_copy`
  - `rationale_target_copy`
- Allowed edit-copy in `edit_description` because the method schema requires an explicit edit description.
- Kept hard rejection for parse failures, alignment errors, edit-validity risks, false rationalization, missing rule, rule edit-copy, missing evidence, wrong evidence, prediction-only evidence, and lack of specific source evidence.
- Kept `rationale_edit_copy`, generic explanations, and unsupported confidence as refine risks.

## Outputs

- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_refine.jsonl`
- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_rejected.jsonl`
- `results/rulefaith/qwen3_field_aware_rulefaith_selection_stats.json`
- `results/rulefaith/qwen3_field_aware_rulefaith_selection_report.md`
- `results/rulefaith/qwen3_field_aware_rulefaith_selection.csv`

## Commands Executed

```bash
python3 -m py_compile experiments/rulefaith/select_qwen3_field_aware_rulefaith.py
python3 -m unittest experiments.tests.test_qwen3_field_aware_selection
python3 experiments/rulefaith/select_qwen3_field_aware_rulefaith.py --overwrite
python3 -m py_compile experiments/rulefaith/select_qwen3_field_aware_rulefaith.py experiments/rulefaith/repair_qwen3_structured_evidence.py
python3 -m unittest discover -s experiments/tests
git diff --check
python3 -m pytest -q
```

## Verified Results

- Candidate count: 160.
- Previous strict Loop H buckets: 0 accepted, 58 refine, 102 rejected.
- Field-aware buckets: 45 accepted, 13 refine, 102 rejected.
- Output line counts: 45 accepted JSONL rows, 13 refine JSONL rows, 102 rejected JSONL rows, and 160 CSV data rows.
- Full unittest suite passed: 38 tests.
- `git diff --check` passed.
- Secret-pattern scan over `annotation`, `docs`, `results`, `experiments`, and `data` produced no matches.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

Field leakage counts:

- `edit_description_edit_copy`: 108
- `edit_description_target_copy`: 100
- `rationale_edit_copy`: 26
- `rationale_target_copy`: 86
- `rule_text_target_copy`: 40

Hard failure counts remain:

- `alignment_error`: 58
- `missing_rule`: 1
- `no_specific_source_evidence`: 36
- `parse_not_json`: 1
- `possible_false_rationalization`: 19
- `validity_error_auto`: 28

Active refine reasons:

- `generic_explanation`: 1
- `rationale_edit_copy`: 13

All refine triggers before hard-reject override:

- `generic_explanation`: 1
- `rationale_edit_copy`: 26
- `unsupported_confidence`: 70

## Scientific Interpretation

Loop I supports a narrower conclusion: the zero-accepted result in Loop H was partly an instrumentation problem caused by treating the schema-required `edit_description` as leakage. A field-aware gate recovers 45 candidates for target-masked validation while leaving 102 hard failures unchanged.

This does not prove final rule correctness or evidence correctness. Several accepted examples still contain plausible but linguistically questionable rules, so the accepted bucket must be used as a validation pool, not as positive training data.

## Claim-Evidence Update

Claim M-C18 is partially supported: a field-aware leakage gate avoids over-penalizing required edit descriptions and produces a usable validation pool. Remaining evidence needed: target-masked validation, stronger verifier or real-human audit, and downstream natural-explanation evaluation.

## Next Internal Action

Run target-masked validation over the 45 accepted and 13 refine candidates. The next gate should test whether rule and rationale quality survives when the target edit cannot be copied.

# Loop L: Ready-Candidate Blind Validation Package

Date: 2026-07-21

## Status

Round: Loop L

Main objective: package the 25 rule/evidence-ready Qwen3 candidates for blind validation and prepare targeted repair input for the 16 needs-refinement candidates.

Highest risk: the package is ready for validation but does not itself create human labels. The hidden key must not be shown to blind validators.

## Implemented

- Added `experiments/rulefaith/prepare_qwen3_validation_package.py`.
- Added `experiments/tests/test_qwen3_validation_package.py`.
- Generated anonymized validation IDs so the blind form does not expose `qwen3_8b`, model family, dataset, or automatic decisions.
- Generated a hidden key for later merge.
- Generated targeted repair instructions from automatic audit reasons.

## Inputs

- `data/rulefaith/filtering/qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl`
- `data/rulefaith/filtering/qwen3_rule_plausibility_needs_refinement.jsonl`

## Outputs

- `annotation/rulefaith_qwen3_ready_validation/guidelines.md`
- `annotation/rulefaith_qwen3_ready_validation/README.md`
- `annotation/rulefaith_qwen3_ready_validation/ready_validation_form.csv`
- `annotation/rulefaith_qwen3_ready_validation/ready_validation_key.csv`
- `annotation/rulefaith_qwen3_ready_validation/repair_instructions.csv`
- `annotation/rulefaith_qwen3_ready_validation/handoff_manifest.json`
- `annotation/rulefaith_qwen3_ready_validation/handoff_manifest.md`
- `annotation/rulefaith_qwen3_ready_validation/rulefaith_qwen3_ready_validation_package.zip`
- `results/rulefaith/qwen3_ready_validation_package_summary.json`
- `results/rulefaith/qwen3_ready_validation_package_report.md`

## Commands Executed

```bash
python3 -m py_compile experiments/rulefaith/prepare_qwen3_validation_package.py
python3 -m unittest experiments.tests.test_qwen3_validation_package
python3 experiments/rulefaith/prepare_qwen3_validation_package.py --overwrite
```

## Verified Results

- Blind validation form rows: 25.
- Hidden key rows: 25.
- Repair instruction rows: 16.
- Blind form excludes `candidate_id`, `model_key`, `model_family`, `dataset`, `automatic_decision`, and `automatic_reasons`.
- Zip SHA256: `4907c29a702a367d90afcde68b41756f2f9109ef3175e2bc361ef1080052e5ca`.
- Full validation after Loops J--L passed: `unittest` 47 tests and `pytest` 47 tests.
- Secret-pattern scan over project research artifacts produced no matches.

## Scientific Interpretation

The Qwen3 local-teacher path now has a reproducible validation handoff:

```text
160 repaired candidates
  -> 58 field-aware candidates
  -> 47 target-masked validated candidates
  -> 25 blind-validation candidates
  -> 16 targeted repair candidates
```

This closes the packaging step for the current open-teacher pool. It still does not satisfy the natural human-evaluation gate for AAAI method claims.

## Next Internal Action

Implement targeted repair for the 16 needs-refinement candidates, using the generated repair instructions as structured feedback.

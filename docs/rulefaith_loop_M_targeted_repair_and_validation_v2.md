# Loop M: Targeted Repair and Validation Package V2

Date: 2026-07-21

## Status

Round: Loop M

Main objective: repair the 16 needs-refinement Qwen3 candidates, re-run automatic gates, and regenerate a larger blind validation package.

Highest risk: deterministic repair can improve structural gate scores without proving human-perceived rule correctness or helpfulness.

## Implemented

- Added `experiments/rulefaith/repair_qwen3_needs_refinement.py`.
- Added `experiments/tests/test_qwen3_targeted_repair.py`.
- Updated `experiments/rulefaith/prepare_qwen3_validation_package.py` to support multiple ready inputs and empty refine inputs.
- Updated `experiments/tests/test_qwen3_validation_package.py`.

## Inputs

- `data/rulefaith/filtering/qwen3_rule_plausibility_needs_refinement.jsonl`
- `data/rulefaith/filtering/qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl`

## Outputs

Targeted repair:

- `results/rulefaith/qwen3_targeted_repaired_candidates.jsonl`
- `results/rulefaith/qwen3_targeted_repair_stats.json`
- `results/rulefaith/qwen3_targeted_repair_report.md`
- `results/rulefaith/qwen3_targeted_repair_before_after.csv`

Revalidation after repair:

- `data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_validated.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_refine.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_rejected.jsonl`
- `results/rulefaith/qwen3_targeted_repaired_target_masked_stats.json`
- `results/rulefaith/qwen3_targeted_repaired_target_masked_report.md`
- `results/rulefaith/qwen3_targeted_repaired_target_masked.csv`
- `data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_ready_for_human_spotcheck.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_needs_refinement.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_reject.jsonl`
- `results/rulefaith/qwen3_targeted_repaired_rule_plausibility_stats.json`
- `results/rulefaith/qwen3_targeted_repaired_rule_plausibility_report.md`
- `results/rulefaith/qwen3_targeted_repaired_rule_plausibility.csv`

Validation package v2:

- `annotation/rulefaith_qwen3_ready_validation_v2/guidelines.md`
- `annotation/rulefaith_qwen3_ready_validation_v2/README.md`
- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_form.csv`
- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_key.csv`
- `annotation/rulefaith_qwen3_ready_validation_v2/repair_instructions.csv`
- `annotation/rulefaith_qwen3_ready_validation_v2/handoff_manifest.json`
- `annotation/rulefaith_qwen3_ready_validation_v2/handoff_manifest.md`
- `annotation/rulefaith_qwen3_ready_validation_v2/rulefaith_qwen3_ready_validation_package.zip`
- `results/rulefaith/qwen3_ready_validation_package_v2_summary.json`
- `results/rulefaith/qwen3_ready_validation_package_v2_report.md`

## Commands Executed

```bash
python3 -m py_compile experiments/rulefaith/repair_qwen3_needs_refinement.py
python3 -m unittest experiments.tests.test_qwen3_targeted_repair
python3 experiments/rulefaith/repair_qwen3_needs_refinement.py --overwrite
python3 experiments/rulefaith/validate_qwen3_target_masked.py --inputs results/rulefaith/qwen3_targeted_repaired_candidates.jsonl --prefix qwen3_targeted_repaired_target_masked --stats-output results/rulefaith/qwen3_targeted_repaired_target_masked_stats.json --report-output results/rulefaith/qwen3_targeted_repaired_target_masked_report.md --csv-output results/rulefaith/qwen3_targeted_repaired_target_masked.csv --overwrite
python3 experiments/rulefaith/audit_qwen3_rule_plausibility.py --input data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_validated.jsonl --prefix qwen3_targeted_repaired_rule_plausibility --stats-output results/rulefaith/qwen3_targeted_repaired_rule_plausibility_stats.json --report-output results/rulefaith/qwen3_targeted_repaired_rule_plausibility_report.md --csv-output results/rulefaith/qwen3_targeted_repaired_rule_plausibility.csv --overwrite
python3 experiments/rulefaith/prepare_qwen3_validation_package.py --ready data/rulefaith/filtering/qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_ready_for_human_spotcheck.jsonl --refine data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_needs_refinement.jsonl --output-dir annotation/rulefaith_qwen3_ready_validation_v2 --summary-output results/rulefaith/qwen3_ready_validation_package_v2_summary.json --report-output results/rulefaith/qwen3_ready_validation_package_v2_report.md --overwrite
```

## Verified Results

Targeted repair:

- Input needs-refinement candidates: 16.
- Rationale edit-copy before/after: 8 -> 0.
- Evidence mentioned in rule/rationale before/after: 8 -> 16.
- Repair actions: 8 evidence appends, 8 rationale replacements, 14 confidence caps.

Revalidation after repair:

- Target-masked validation: 16/16 validated.
- Rule/evidence audit after repair: 16/16 ready-for-human-spotcheck.
- Remaining repaired needs-refinement: 0.
- Remaining repaired reject: 0.

Validation package v2:

- Blind validation form rows: 41.
- Hidden key rows: 41.
- Repair instruction rows: 0.
- Blind form excludes `candidate_id`, `model_key`, `model_family`, `dataset`, `automatic_decision`, and `automatic_reasons`.
- Zip SHA256: `31ce8d7735d57107b9271dd1202ba0cde4d1c0acbed489ec11c8e3d18938799d`.
- Full validation after Loop M passed: `unittest` 51 tests and `pytest` 51 tests.
- Secret-pattern scan over project research artifacts produced no matches.

## Scientific Interpretation

Targeted deterministic repair successfully fixes the two observed structural failure modes in the 16-candidate refinement bucket: missing evidence integration and rationale edit-copy. The local Qwen3 pool now has 41 candidates ready for blind human or stronger validation:

```text
25 originally ready candidates
+16 targeted-repaired ready candidates
=41 blind-validation candidates
```

This remains automatic evidence. The 41 candidates should not be used as final positives until the blind validation form is completed by real validators or an explicitly documented stronger-model pseudo-label process.

## Next Internal Action

Fill `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_form.csv` only if the label source is explicitly recorded as Codex/AI pseudo-validation, or hand it to real validators for human labels. In parallel, start preparing the method paper sections that describe the staged RuleFaith funnel with no human-claim overreach.

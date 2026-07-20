# Loop G: Complete Qwen3 Audit Forms with Codex Labels

Date: 2026-07-21

## Status

Completed.

## Main Objective

The user requested that Codex fill the remaining audit labels. This loop creates explicit Codex-completed audit files for both current Qwen3 audit packages.

These are AI/Codex annotations. They are not human annotations and must not be reported as human gold.

## Work Completed

### Canonicalized Audit

- Completed form: `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed_by_codex.csv`
- Merged with key: `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed_by_codex_merged_with_key.csv`
- Validation summary: `results/rulefaith/qwen3_canonicalized_codex_completed_validation_summary.json`
- Validation report: `results/rulefaith/qwen3_canonicalized_codex_completed_validation_report.md`

Results:

- Rows completed: 80/80
- Validation: `ready_to_merge_completed_audit`
- Decisions: 44 `refine`, 36 `reject`

### Pre-Canonicalization Audit

- Completed form: `annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex.csv`
- Merged with key: `annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex_merged_with_key.csv`
- Validation summary: `results/rulefaith/qwen3_precano_codex_completed_validation_summary.json`
- Validation report: `results/rulefaith/qwen3_precano_codex_completed_validation_report.md`

Results:

- Rows completed: 80/80
- Validation: `ready_to_merge_completed_audit`
- Decisions: 46 `refine`, 34 `reject`

## Round10 Boundary

`annotation/round10/annotation_form.csv` and `annotation/round10/adjudication_template.csv` are old blank templates. They were not overwritten because Round15 already contains the finalized adjudicated stress-test labels under `annotation/round15/`.

## Scientific Interpretation

The Codex annotations are conservative and accept no candidates directly. They are useful for identifying Qwen3 failure modes and selecting cases for refiner/verifier development, but they do not support human-evaluation claims.

## Validation

- `python3 -m py_compile experiments/rulefaith/prefill_qwen3_audit_codex.py experiments/rulefaith/summarize_qwen3_prelabeled_audit.py experiments/rulefaith/validate_qwen3_human_audit.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 29 tests.
- `git diff --check` passed.
- Canonicalized and pre-canonicalization Codex-completed audit CSVs each have 80 rows and no blank `human_*` cells.
- Secret-pattern scan produced no matches.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

## Next Action

Use the Codex-completed canonicalized audit form to redesign the verifier/refiner around missing evidence, edit-copy, unsupported confidence, wrong-rule, and false-rationalization risks.

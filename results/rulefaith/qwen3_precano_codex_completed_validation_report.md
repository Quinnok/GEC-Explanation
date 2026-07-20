# Qwen3 Human Audit Validation Report

## Summary

- `row_count`: `80`
- `completed_row_count`: `80`
- `incomplete_row_count`: `0`
- `is_complete`: `True`
- `uncertain_without_notes_count`: `0`
- `decision`: `ready_to_merge_completed_audit`

## Human Decisions

- `refine`: 46
- `reject`: 34

## Issue Counts

- `human_alignment_error`: `{'no': 65, 'yes': 15}`
- `human_validity_error`: `{'no': 55, 'yes': 25}`
- `human_wrong_rule`: `{'no': 55, 'yes': 25}`
- `human_inapplicable_rule`: `{'no': 55, 'yes': 25}`
- `human_missing_evidence`: `{'no': 1, 'yes': 79}`
- `human_wrong_evidence`: `{'yes': 80}`
- `human_generic_explanation`: `{'no': 80}`
- `human_edit_copy`: `{'no': 7, 'yes': 73}`
- `human_semantic_distortion`: `{'no': 55, 'yes': 25}`
- `human_unsupported_confidence`: `{'yes': 80}`

## Merged Output

- `/Users/bytedance/Documents/GEC可解释性/annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex_merged_with_key.csv`
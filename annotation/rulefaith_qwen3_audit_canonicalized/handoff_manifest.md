# Qwen3 Canonicalized Human Audit Handoff Manifest

This package is the blind human-audit handoff for Qwen3-8B teacher candidates after deterministic evidence-span canonicalization.

## Package

- Package directory: `/Users/bytedance/Documents/GEC可解释性/annotation/rulefaith_qwen3_audit_canonicalized/handoff_package`
- Zip file: `/Users/bytedance/Documents/GEC可解释性/annotation/rulefaith_qwen3_audit_canonicalized/qwen3_canonicalized_human_audit_package.zip`
- Zip SHA256: `5d0cd63b24e9590a306929201206e9ca532d3585f04c4a49afdafacdf3cf46ad`
- Zip size bytes: `16120`

## Validation

- `row_count`: `80`
- `candidate_id_count`: `80`
- `key_row_count`: `80`
- `hidden_key_columns_in_form`: `[]`
- `human_annotation_cells_filled`: `0`
- `human_annotation_cells_blank`: `960`

## Files Included For Auditor

- `README_FOR_AUDITOR.md`: 1731 bytes, sha256 `88ad50cc9a3c4ba907094c8316ac1a6c3751f97f827aee37360562d3cd175030`
- `guidelines.md`: 3074 bytes, sha256 `058c0a65997acf76427357aa07a821973fb822ab3caed3439453f46af2f9f400`
- `manual_audit_form.csv`: 82611 bytes, sha256 `5d9f42d973bd3de3c0e5ef5ae86b8709e4b716fdd3ddd1fecabe4e0c8947a4c7`

## Files Not Included

- Hidden key file: `/Users/bytedance/Documents/GEC可解释性/annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv`

## Next Step

Send only the zip file or package directory contents to a real human auditor. After the completed CSV returns, validate it with `experiments/rulefaith/validate_qwen3_human_audit.py`.
# Qwen3 Codex Annotation Data Card

Created: 2026-07-21

## Scope

This card documents Codex-assisted completion of the Qwen3 audit forms.

These annotations are AI-assisted pseudo-labels. They are not human annotations, not human gold labels, and must not be reported as human evaluation.

## Completed Files

### Canonicalized Qwen3 Audit

- Blank form: `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_form.csv`
- Codex completed form: `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed_by_codex.csv`
- Codex completed merged form: `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed_by_codex_merged_with_key.csv`
- Validation summary: `results/rulefaith/qwen3_canonicalized_codex_completed_validation_summary.json`
- Breakdown: `results/rulefaith/qwen3_codex_prelabeled_breakdown.md`

Decision counts:

| Decision | Count |
|---|---:|
| `refine` | 44 |
| `reject` | 36 |
| `accept` | 0 |
| `abstain` | 0 |

### Pre-Canonicalization Qwen3 Audit

- Blank form: `annotation/rulefaith_qwen3_audit/manual_audit_form.csv`
- Codex completed form: `annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex.csv`
- Codex completed merged form: `annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex_merged_with_key.csv`
- Validation summary: `results/rulefaith/qwen3_precano_codex_completed_validation_summary.json`
- Breakdown: `results/rulefaith/qwen3_precano_codex_prelabeled_breakdown.md`

Decision counts:

| Decision | Count |
|---|---:|
| `refine` | 46 |
| `reject` | 34 |
| `accept` | 0 |
| `abstain` | 0 |

## Label Source

`codex_ai_assisted_prelabelling_not_human_gold`

The labels were generated from existing automatic diagnostics using conservative rules:

- severe alignment, validity, rule, or semantic-distortion risks produce `reject`;
- repairable evidence, edit-copy, genericness, or unsupported-confidence risks produce `refine`;
- no current candidate was directly accepted.

## Intended Use

Allowed:

- internal triage;
- failure-mode analysis;
- verifier debugging;
- refiner prompt debugging;
- selecting cases for later human review.

Not allowed:

- reporting as human annotation;
- reporting as human agreement;
- constructing SFT positive data without further human or stronger validation;
- claiming Qwen3 candidates are ready for positive distillation.

## Historical Round10 Note

`annotation/round10/annotation_form.csv` and `annotation/round10/adjudication_template.csv` are preserved as historical blank templates. The usable Round 15 adjudicated labels live under `annotation/round15/`; these Round10 templates were not overwritten.

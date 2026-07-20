# Qwen3 Canonicalized Audit Handoff

This folder contains the blind human audit package for Qwen3-8B teacher candidates after deterministic evidence-span canonicalization.

## Files To Send To The Human Auditor

- `guidelines.md`
- `manual_audit_form.csv`

Do not send `manual_audit_key.csv` to the auditor.

## Scope

- Rows: 80 blind candidate explanations.
- Source: Qwen3-8B teacher candidates after deterministic evidence-span canonicalization.
- Label status: teacher-generated candidates only; not human gold and not accepted positives.

## Auditor Instructions

The auditor should fill issue columns with `yes`, `no`, or `uncertain`, and fill `human_decision` with one of:

- `accept`
- `refine`
- `reject`
- `abstain`

The auditor should not see:

- automatic accepted/refine/rejected buckets;
- automatic risk flags;
- prior model decisions;
- downstream training plans.

## Current Automatic Gate Status

Full-pool canonicalization improved strict evidence checks but did not close the quality gate:

- all evidence spans source-index matched: 20/160 -> 155/160
- contextual source evidence: 24/160 -> 82/160
- missing evidence: 136/160 -> 78/160
- prediction-only evidence: 87/160 -> 29/160
- wrong-evidence automatic flags: 141/160 -> 29/160

The follow-up 20-edit Qwen3 evidence-refinement probe did not improve contextual evidence:

- contextual source evidence: 7/20 -> 2/20 after refinement and canonicalization
- missing evidence: 13/20 -> 18/20
- prediction-only evidence: 20/20 -> 0/20
- wrong-evidence automatic flags: 20/20 -> 0/20

This means the refiner mostly removed evidence instead of adding contextual source evidence. Human audit is required before using any candidate as a positive training example.

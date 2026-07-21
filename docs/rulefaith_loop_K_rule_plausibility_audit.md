# Loop K: Rule Plausibility and Evidence Sufficiency Audit

Date: 2026-07-21

## Status

Round: Loop K

Main objective: audit the 47 target-masked validated Qwen3 candidates for rule plausibility and evidence sufficiency before any positive-data construction.

Highest risk: this is still a deterministic automatic audit. The ready bucket is suitable for blind human or stronger validation, not for final SFT/preference positives.

## Hypothesis

Target-masked validation removes many target-copy shortcuts, but some candidates may still have insufficient evidence or unsupported confidence. A rule-plausibility/evidence-sufficiency audit should identify a smaller, cleaner candidate pool for manual or stronger validation.

## Implemented

- Added `experiments/rulefaith/audit_qwen3_rule_plausibility.py`.
- Added `experiments/tests/test_qwen3_rule_plausibility_audit.py`.
- Added evidence requirements by edit type:
  - SVA: subject evidence.
  - Preposition: governor and complement evidence.
  - Determiner/article: head noun evidence.
  - Pronoun: antecedent/reference evidence.
  - Noun number: noun-number context or head noun evidence.
  - Verb form: verb/time/complement context evidence.
  - Orthography/punctuation: orthographic or punctuation context evidence.
- Added decision buckets:
  - `ready_for_human_spotcheck`
  - `needs_refinement`
  - `reject`

## Inputs

- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_validated.jsonl`

## Outputs

- `data/rulefaith/filtering/qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl`
- `data/rulefaith/filtering/qwen3_rule_plausibility_needs_refinement.jsonl`
- `data/rulefaith/filtering/qwen3_rule_plausibility_reject.jsonl`
- `results/rulefaith/qwen3_rule_plausibility_audit_stats.json`
- `results/rulefaith/qwen3_rule_plausibility_audit_report.md`
- `results/rulefaith/qwen3_rule_plausibility_audit.csv`

## Commands Executed

```bash
python3 -m py_compile experiments/rulefaith/audit_qwen3_rule_plausibility.py
python3 -m unittest experiments.tests.test_qwen3_rule_plausibility_audit
python3 experiments/rulefaith/audit_qwen3_rule_plausibility.py --overwrite
```

## Verified Results

- Input candidates: 47.
- Ready for human/stronger validation: 25.
- Needs refinement: 16.
- Rejected: 6.
- Evidence sufficiency: 41 sufficient, 6 insufficient.
- Rule plausibility: 47 plausible under current deterministic category checks.
- Output line counts: 25 ready JSONL rows, 16 refinement JSONL rows, 6 rejected JSONL rows, and 47 CSV data rows.

Reason counts:

- `evidence_not_mentioned_in_rule_or_rationale`: 14
- `rationale_edit_copy`: 8
- `unsupported_high_confidence`: 6
- `missing_required_evidence:specific_source_evidence`: 5
- `missing_required_evidence:noun_number_context`: 1

## Scientific Interpretation

The automatic RuleFaith funnel now separates Qwen3 candidates into a much cleaner triage structure:

```text
160 repaired Qwen3 candidates
  -> 58 field-aware accepted/refine candidates
  -> 47 target-masked validated candidates
  -> 25 rule/evidence ready-for-spotcheck candidates
```

The strongest remaining automatic failure mode is not rule-category mismatch, but evidence integration: 14 candidates cite source evidence structurally but do not explicitly use that evidence in the rule or rationale. These should be refined before training.

## Claim-Evidence Update

Claim M-C20 is partially supported: a staged automatic verifier can reduce a noisy Qwen3 teacher pool to a smaller candidate set with explicit rule/evidence checks. Remaining evidence needed: human or stronger validation of the 25 ready candidates and targeted refinement of the 16 repair candidates.

## Next Internal Action

Build a blind validation package for the 25 ready candidates and a targeted repair input for the 16 needs-refinement candidates. Keep all labels marked as automatic until real human or stronger validation is complete.

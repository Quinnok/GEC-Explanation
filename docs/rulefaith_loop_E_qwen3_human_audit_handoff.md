# Loop E: Qwen3 Canonicalized Human Audit Handoff

Date: 2026-07-20

## Status

- Loop ID: Loop E / Qwen3 canonicalized human audit handoff.
- Main objective: turn the canonicalized blind audit files into a safe, auditable handoff package and prepare validation/merge tooling for the completed human audit.
- Highest risk: accidentally exposing `manual_audit_key.csv` or automatic risk labels to the auditor.
- Git start commit: `e21c0cf`.

## Work Completed

Implemented:

- `experiments/rulefaith/prepare_qwen3_audit_handoff.py`
- `experiments/rulefaith/validate_qwen3_human_audit.py`
- `experiments/tests/test_qwen3_human_audit_tools.py`

Generated:

- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_package/README_FOR_AUDITOR.md`
- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_package/guidelines.md`
- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_package/manual_audit_form.csv`
- `annotation/rulefaith_qwen3_audit_canonicalized/qwen3_canonicalized_human_audit_package.zip`
- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_manifest.json`
- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_manifest.md`
- `results/rulefaith/qwen3_human_audit_validation_summary.json`
- `results/rulefaith/qwen3_human_audit_validation_report.md`

## Commands Executed

```bash
python3 -m py_compile experiments/rulefaith/prepare_qwen3_audit_handoff.py experiments/rulefaith/validate_qwen3_human_audit.py
python3 -m unittest experiments.tests.test_qwen3_human_audit_tools
python3 experiments/rulefaith/prepare_qwen3_audit_handoff.py --overwrite
python3 experiments/rulefaith/validate_qwen3_human_audit.py --allow-incomplete --skip-merged-output --overwrite
unzip -l annotation/rulefaith_qwen3_audit_canonicalized/qwen3_canonicalized_human_audit_package.zip
```

## Verified Results

- Handoff rows: 80.
- Candidate IDs in blind form and hidden key match exactly.
- Hidden key columns in blind form: none.
- Human annotation cells filled: 0.
- Human annotation cells blank: 960.
- Handoff zip SHA256: `5d0cd63b24e9590a306929201206e9ca532d3585f04c4a49afdafacdf3cf46ad`.
- Zip contents:
  - `README_FOR_AUDITOR.md`
  - `guidelines.md`
  - `manual_audit_form.csv`
- Hidden file intentionally excluded:
  - `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv`

Validation of the current blank form returns:

```json
{
  "decision": "waiting_for_human_completion",
  "is_complete": false,
  "row_count": 80
}
```

Additional validation:

- `python3 -m unittest discover -s experiments/tests` passed after this loop, 27 tests.
- `git diff --check` passed.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

## Scientific Interpretation

All non-human work needed to hand off the canonicalized Qwen3 audit is complete. The next step is a genuine hard blocker: a real human auditor must fill the blind form before these candidates can be used to revise the evidence verifier or construct positive SFT/preference examples.

## How To Resume After Human Audit

When the completed CSV is available, save it as:

```text
annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed.csv
```

Then run:

```bash
python3 experiments/rulefaith/validate_qwen3_human_audit.py \
  --form annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed.csv \
  --key annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv \
  --merged-output annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_merged_with_key.csv \
  --summary-output results/rulefaith/qwen3_human_audit_validation_summary.json \
  --report-output results/rulefaith/qwen3_human_audit_validation_report.md \
  --overwrite
```

If validation passes, use the merged output to update the evidence verifier and candidate-selection policy.

## Next Internal Action

Wait for the completed real-human audit. Do not train SFT or preference models on Qwen3 positives before this audit returns and passes validation.

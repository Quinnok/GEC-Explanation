# Loop A: Qwen3-8B Candidate Audit

## Loop Start

Loop ID: Loop A / Qwen3-8B candidate audit

Current bottleneck: Qwen3-8B generated the first non-trivial local teacher candidate pool, but accepted/refine candidates have not been audited for leakage, evidence grounding, edit-copy, or false rationalization.

Hypothesis: Qwen3-8B candidates are useful enough to continue, but automatic audit will reveal evidence and validity risks that must be addressed before targeted refinement and distillation.

Required evidence: full accepted/refine/rejected audit, stratified manual sample, automatic leakage/span/rule/evidence/genericness/rationalization flags.

Success criterion: no generator input leakage, edit spans match source, audit sample covers accepted/refine/rejected, EXPECT/JFLEG, GECToR/T5/CoEdIT, replace/insert/delete, and correct/wrong/overcorrection.

Failure criterion: reference or human-label leakage, broken edit spans, or pervasive evidence-span failures that invalidate candidates as positives.

Planned files:

- `experiments/rulefaith/build_qwen3_manual_audit.py`
- `experiments/tests/test_qwen3_manual_audit.py`
- `results/rulefaith/qwen3_manual_audit.csv`
- `results/rulefaith/qwen3_manual_audit_summary.json`
- `results/rulefaith/qwen3_manual_audit_cases.md`

## Loop Result

The audit covered all 160 Qwen3-8B candidates: 41 accepted, 63 refine, and 56 rejected. The generated CSV keeps all candidates and marks 80 rows for stratified manual audit.

## Commands Executed

- `git status --short --branch`
- `git log --oneline -10`
- `python3 -m py_compile experiments/rulefaith/build_qwen3_manual_audit.py`
- `python3 -m unittest experiments.tests.test_qwen3_manual_audit`
- `python3 experiments/rulefaith/build_qwen3_manual_audit.py --overwrite`
- `python3 -m unittest discover -s experiments/tests`
- `pytest -q` failed because `pytest` is not installed in the current shell.

## Artifacts Produced

- `results/rulefaith/qwen3_manual_audit.csv`
- `results/rulefaith/qwen3_manual_audit_summary.json`
- `results/rulefaith/qwen3_manual_audit_cases.md`

## Main Metrics

- Candidate count: 160
- Manual audit selected rows: 80
- No generator input leakage: 0/160 flagged
- Source span match: 160/160
- Target present in prediction: 160/160
- Evidence span index match: 48/160
- Contextual evidence present: 51/160
- Missing contextual evidence: 109/160
- Wrong evidence automatic flag: 108/160
- Possible false rationalization: 19/160
- Validity-error automatic risk: 28/160

## Important Cases

See `results/rulefaith/qwen3_manual_audit_cases.md` for high-risk cases, including wrong/overcorrection edits where Qwen3 marks an edit as valid and gives a fluent rationale without sufficient source-grounded evidence.

## Hypothesis Status

Revise. The Qwen3-8B candidate pool is useful, and there is no input leakage, but evidence grounding is not reliable enough to proceed directly to targeted refinement or SFT positives.

## Remaining Risks

- Evidence spans often quote source-like text but use invalid token indices.
- Some accepted candidates may rationalize wrong/overcorrection edits as valid.
- Edit-copy and target-copy rates are high enough that selection must include leakage penalties.
- Manual review is still required for the selected 80 rows.

## Next Highest-Priority Loop

Fix evidence verifier/prompt and rerun the Qwen3 audit before targeted refinement.

## Verification

- Python compile check passed for `experiments/rulefaith/build_qwen3_manual_audit.py`.
- Related unit tests passed: 6/6.
- Existing `experiments/tests` suite passed: 12/12.
- CSV consistency checks passed: 160 unique candidates, 80 selected manual-audit rows, 0 input leakage flags, 160 source-span matches.
- `pytest -q` was attempted but unavailable in this environment (`pytest: command not found`).

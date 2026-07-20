# Loop B: Evidence Gate Repair and Blind Audit Package

## Loop Start

Loop ID: Loop B / Evidence grounding repair

Current bottleneck: Qwen3-8B candidates often cite plausible evidence text but mix source spans, prediction-only target phrases, and incorrect token offsets. This makes them unsafe as SFT positives even when edit alignment looks good.

Hypothesis: tightening the evidence verifier and teacher prompt will separate three cases that were conflated in Loop A: source-index-matched evidence, prediction-only evidence, and edit-token-only evidence.

Required evidence: updated prompt constraints, stricter audit taxonomy, rerun audit statistics, and a blind human audit package.

Success criterion: audit package is complete, source/prediction leakage remains absent, evidence error types are explicitly counted, and annotators can audit selected rows without seeing accepted/refine/rejected labels or automatic flags.

Failure criterion: audit script cannot distinguish source evidence from prediction-only evidence, or selected audit rows do not cover the required strata.

Planned files:

- `experiments/rulefaith/build_qwen3_manual_audit.py`
- `experiments/rulefaith/generate_teacher_candidates.py`
- `configs/rulefaith/qwen3_8b_teacher.yaml`
- `docs/rulefaith_teacher_prompt.md`
- `annotation/rulefaith_qwen3_audit/manual_audit_form.csv`
- `annotation/rulefaith_qwen3_audit/manual_audit_key.csv`
- `annotation/rulefaith_qwen3_audit/guidelines.md`
- `results/rulefaith/qwen3_manual_audit_summary.json`

## Loop Result

The evidence gate now records whether evidence spans match source token indices, whether all evidence spans are source-index matched, whether any span is prediction-only, whether a span is only the edited token, and which evidence error types occurred.

The rerun audit still covers all 160 Qwen3-8B candidates and selects 80 blind-audit rows.

## Commands Executed

- `git status --short --branch`
- `git log --oneline -10`
- `python3 -m py_compile experiments/rulefaith/build_qwen3_manual_audit.py experiments/rulefaith/generate_teacher_candidates.py`
- `python3 -m unittest experiments.tests.test_qwen3_manual_audit`
- `python3 experiments/rulefaith/build_qwen3_manual_audit.py --overwrite`

## Artifacts Produced

- `annotation/rulefaith_qwen3_audit/manual_audit_form.csv`
- `annotation/rulefaith_qwen3_audit/manual_audit_key.csv`
- `annotation/rulefaith_qwen3_audit/guidelines.md`
- Updated `results/rulefaith/qwen3_manual_audit.csv`
- Updated `results/rulefaith/qwen3_manual_audit_summary.json`
- Updated `results/rulefaith/qwen3_manual_audit_cases.md`

## Main Metrics

- Candidate count: 160
- Blind manual audit rows: 80
- No generator input leakage: 0/160
- Source span match: 160/160
- Target present in prediction: 160/160
- At least one evidence span source-index matched: 48/160
- All evidence spans source-index matched: 20/160
- Contextual source evidence present: 24/160
- Missing contextual evidence: 136/160
- Prediction-only evidence present: 87/160
- Wrong evidence automatic flag: 141/160
- Possible false rationalization: 19/160

Evidence error types:

- `index_text_mismatch`: 121
- `prediction_only_text`: 62
- `prediction_or_target_role`: 29
- `invalid_indices`: 24
- `text_not_in_source`: 23
- `missing_evidence`: 1

## Important Cases

`results/rulefaith/qwen3_manual_audit_cases.md` now surfaces candidates where the explanation cites corrected phrases from `MODEL_PREDICTION` as evidence. These are precisely the cases the v2 prompt must prevent.

## Hypothesis Status

Keep/revise. The stricter gate successfully distinguishes source evidence from prediction-only evidence, but it shows that current Qwen3 candidates are less source-grounded than the earlier audit suggested.

## Remaining Risks

- Current Qwen3-8B candidates were generated with prompt v1, so they should not be treated as positive training data.
- A 1-candidate prompt-v2 smoke test completed successfully, but Qwen3 candidates have not yet been regenerated at useful scale under v2.
- Human audit is still needed for the 80 blind rows.
- Evidence verifier remains heuristic and must be calibrated on manual audit outcomes.

## Next Highest-Priority Loop

Apply targeted evidence refinement to Qwen3 prompt-v2 outputs or strengthen the evidence prompt further, then rerun the strict audit before using any candidates as positives.

## Prompt-v2 Smoke Test

- Output: `results/rulefaith/qwen3_v2_smoke_candidates.jsonl`
- Audit: `results/rulefaith/qwen3_v2_smoke_audit.json`
- Candidate count: 1
- Parse status: parsed JSON
- Evidence source-index match: true
- Prediction-only evidence: false
- Interpretation: prompt v2 can produce source-index-matched evidence on at least one punctuation/stylistic edit, but this is only a smoke test and does not establish broad quality.

## Prompt-v2 Smoke10 Test

- Output: `results/rulefaith/qwen3_v2_smoke10_candidates.jsonl`
- Audit: `results/rulefaith/qwen3_v2_smoke10_audit.json`
- Candidate count: 10
- Parse status: 10/10 parsed JSON
- Source span match: 10/10
- Target present in prediction: 10/10
- At least one source-index-matched evidence span: 6/10
- All evidence spans source-index matched: 4/10
- Contextual source evidence: 3/10
- Prediction-only evidence: 0/10
- Wrong-evidence automatic flag: 6/10
- Interpretation: prompt v2 removes the major prompt-v1 prediction-only evidence failure in this smoke sample, but contextual evidence remains too weak for positive training data.

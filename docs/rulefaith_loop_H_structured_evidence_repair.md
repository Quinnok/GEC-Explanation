# Loop H: Structured Evidence Repair for Qwen3 Candidates

Date: 2026-07-21

## Status

Completed.

## Main Objective

Use the Codex-completed Qwen3 audit failure modes to implement a non-LLM evidence repair pass that can add source-grounded evidence spans without querying a teacher model.

## Hypothesis

Many Qwen3 evidence failures are source-span and missing-context failures. A deterministic source-context repair pass should improve evidence grounding while avoiding prediction-only evidence.

## Implementation

- Script: `experiments/rulefaith/repair_qwen3_structured_evidence.py`
- Tests: `experiments/tests/test_qwen3_structured_evidence_repair.py`

The script:

- reads `data/rulefaith/teacher_candidates_qwen3_8b_canonicalized.jsonl`;
- keeps valid existing source evidence spans;
- adds source-grounded context spans from the edit, ERRANT type, and nearby source tokens;
- writes repaired candidates to `results/rulefaith/qwen3_structured_evidence_repaired_candidates.jsonl`;
- computes before/after audit flags;
- writes strict RuleFaith buckets under `data/rulefaith/filtering/`.

No reference correction, human label, or behavior label is used to generate evidence spans.

## Commands Executed

```bash
python3 experiments/rulefaith/repair_qwen3_structured_evidence.py --overwrite
python3 experiments/rulefaith/diagnose_teacher_candidates.py --input results/rulefaith/qwen3_structured_evidence_repaired_candidates.jsonl --json-output results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_metrics.json --md-output results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_report.md
python3 experiments/rulefaith/filter_teacher_candidates.py --candidates results/rulefaith/qwen3_structured_evidence_repaired_candidates.jsonl --diagnostics results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_metrics.json --output-dir data/rulefaith/filtering --stats results/rulefaith/qwen3_structured_evidence_repaired_filtering_statistics.json --prefix qwen3_structured_evidence_repaired
```

## Outputs

- `results/rulefaith/qwen3_structured_evidence_repaired_candidates.jsonl`
- `results/rulefaith/qwen3_structured_evidence_repair_stats.json`
- `results/rulefaith/qwen3_structured_evidence_repair_report.md`
- `results/rulefaith/qwen3_structured_evidence_repair_before_after.csv`
- `results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_metrics.json`
- `results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_report.md`
- `results/rulefaith/qwen3_structured_evidence_repaired_filtering_statistics.json`
- `data/rulefaith/filtering/qwen3_structured_evidence_repaired_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_structured_evidence_repaired_refine.jsonl`
- `data/rulefaith/filtering/qwen3_structured_evidence_repaired_rejected.jsonl`
- `data/rulefaith/filtering/qwen3_structured_rulefaith_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_structured_rulefaith_refine.jsonl`
- `data/rulefaith/filtering/qwen3_structured_rulefaith_rejected.jsonl`

## Verified Results

Automatic audit flags before and after structured evidence repair:

| Flag | Before | After | Delta |
|---|---:|---:|---:|
| `evidence_contextual` | 82 | 160 | +78 |
| `missing_evidence` | 78 | 0 | -78 |
| `wrong_evidence_auto` | 29 | 0 | -29 |
| `evidence_text_found_in_prediction_only` | 29 | 0 | -29 |
| `unsupported_confidence` | 131 | 70 | -61 |
| `alignment_error` | 58 | 58 | +0 |
| `edit_copy` | 112 | 112 | +0 |
| `possible_false_rationalization` | 19 | 19 | +0 |
| `validity_error_auto` | 28 | 28 | +0 |

Stricter evidence check:

- specific source evidence: 10/160 -> 124/160
- generic-context-only after repair: 36/160

Standard conservative prefilter after repair:

- accepted: 101
- refine: 0
- rejected: 59

Strict RuleFaith selection after repair:

- accepted: 0
- refine: 58
- rejected: 102

The difference shows why the stricter gate is needed: contextual source spans alone are not enough when alignment errors, edit-copy risk, false rationalization, and unsupported confidence remain.

## Interpretation

Structured evidence repair should be kept as a preprocessing/refiner-input step. It fixes source evidence coverage and eliminates prediction-only evidence under automatic checks.

It should not be used as a final scoring method or as a positive-data constructor by itself. The strict RuleFaith gate still accepts no candidates directly.

## Remaining Risks

- 36 candidates still have only generic context evidence.
- 58 candidates still have alignment errors.
- 112 candidates still trigger edit-copy risk.
- 19 candidates still trigger possible false rationalization.
- 28 candidates still trigger edit-validity risk.

## Validation

- `python3 -m py_compile experiments/rulefaith/repair_qwen3_structured_evidence.py experiments/rulefaith/prefill_qwen3_audit_codex.py experiments/rulefaith/summarize_qwen3_prelabeled_audit.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 35 tests.
- `git diff --check` passed.
- Output integrity check passed: 160 repaired candidates, 58 strict refine candidates, and 102 strict rejected candidates.
- Secret-pattern scan produced no matches.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

## Next Action

Implement an alignment and leakage-aware refinement/selection loop over the 58 strict `refine` candidates, with target-masked checks before any candidate can become positive data.

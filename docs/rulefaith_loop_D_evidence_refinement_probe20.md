# Loop D: Qwen3 Evidence Refinement Probe20

Date: 2026-07-20

## Status

- Loop ID: Loop D / 20-edit canonicalization-plus-refinement probe
- Main objective: test whether targeted Qwen3 evidence refinement can repair remaining evidence failures after deterministic evidence-span canonicalization.
- Highest risk: the model may remove risky evidence spans instead of adding source-grounded contextual evidence.
- Git start commit: `841317b`

## Hypothesis

Targeted Qwen3 evidence refinement, applied only after deterministic canonicalization, can increase contextual source evidence on remaining evidence-risk candidates without increasing prediction-only evidence.

## Commands Executed

```bash
python3 -m py_compile experiments/rulefaith/build_evidence_refinement_probe.py experiments/rulefaith/compare_evidence_refinement_probe.py experiments/rulefaith/refine_qwen3_evidence.py experiments/rulefaith/canonicalize_evidence_spans.py
python3 -m unittest experiments.tests.test_evidence_refinement_probe_selection experiments.tests.test_qwen3_evidence_refinement experiments.tests.test_evidence_span_canonicalizer
python3 experiments/rulefaith/build_evidence_refinement_probe.py --overwrite
HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/refine_qwen3_evidence.py --input data/rulefaith/qwen3_evidence_refinement_probe20.jsonl --output results/rulefaith/qwen3_evidence_refinement_probe20_refined_candidates.jsonl --stats-output results/rulefaith/qwen3_evidence_refinement_probe20_refinement_stats.json --audit-md-output results/rulefaith/qwen3_evidence_refinement_probe20_refinement_audit.md --raw-dir results/rulefaith/qwen3_evidence_refinement_probe20_raw --overwrite --max-input-length 1536 --max-new-tokens 320
python3 experiments/rulefaith/canonicalize_evidence_spans.py --input results/rulefaith/qwen3_evidence_refinement_probe20_refined_candidates.jsonl --output results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalized_candidates.jsonl --stats-output results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalization_stats.json --audit-md-output results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalization_audit.md --overwrite
python3 experiments/rulefaith/compare_evidence_refinement_probe.py --overwrite
```

## Artifacts Produced

- `experiments/rulefaith/build_evidence_refinement_probe.py`
- `experiments/rulefaith/compare_evidence_refinement_probe.py`
- `experiments/tests/test_evidence_refinement_probe_selection.py`
- `data/rulefaith/qwen3_evidence_refinement_probe20.jsonl`
- `results/rulefaith/qwen3_evidence_refinement_probe20_stats.json`
- `results/rulefaith/qwen3_evidence_refinement_probe20_card.md`
- `results/rulefaith/qwen3_evidence_refinement_probe20_refined_candidates.jsonl`
- `results/rulefaith/qwen3_evidence_refinement_probe20_refinement_stats.json`
- `results/rulefaith/qwen3_evidence_refinement_probe20_refinement_audit.md`
- `results/rulefaith/qwen3_evidence_refinement_probe20_raw/`
- `results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalized_candidates.jsonl`
- `results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalization_stats.json`
- `results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalization_audit.md`
- `results/rulefaith/qwen3_evidence_refinement_probe20_comparison.json`
- `results/rulefaith/qwen3_evidence_refinement_probe20_comparison.md`

## Verified Results

Probe selection:

- Input candidates: 160 canonicalized Qwen3 candidates.
- Eligible evidence-risk candidates: 89 candidates across 49 unique edit groups.
- Selected probe: 20 candidates across 20 unique edit groups.
- Selected breakdown:
  - dataset: EXPECT 18, JFLEG 2
  - model: CoEdIT 9, T5 6, GECToR 5
  - operation: replace 13, insert 5, delete 2
  - original candidate type: natural 9, rule-grounded 11
  - split: train 15, test 5

Refinement:

- Qwen3 refined outputs: 20/20.
- Parse status: 20/20 parsed JSON.
- Before refinement on selected probe:
  - contextual source evidence: 7/20
  - missing evidence: 13/20
  - prediction-only evidence: 20/20
  - wrong-evidence automatic flag: 20/20
- After Qwen3 refinement:
  - contextual source evidence: 2/20
  - missing evidence: 18/20
  - prediction-only evidence: 0/20
  - wrong-evidence automatic flag: 0/20
- After re-canonicalizing refined outputs:
  - contextual source evidence: 2/20
  - missing evidence: 18/20
  - prediction-only evidence: 0/20
  - wrong-evidence automatic flag: 0/20

## Scientific Interpretation

The evidence-only Qwen3 repair prompt is not ready to scale. It reliably parses JSON and removes prediction-only or wrong evidence flags, but mostly does so by dropping evidence rather than adding source-grounded contextual triggers. This weakens RuleFaith's evidence-grounding objective and risks creating a reward-hacking path where candidates avoid penalties by abstaining or leaving evidence empty.

## Validation

- Python compile checks passed for the new probe/compare scripts and the existing refinement/canonicalization scripts.
- `python3 -m unittest discover -s experiments/tests` passed after this loop, 24 tests.
- `git diff --check` passed.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

## Decision

Reject this Qwen3 evidence-refinement prompt for scaling. Keep deterministic evidence-span canonicalization as preprocessing. Do not use refined probe outputs as positive SFT or preference data. The next step is human review of the canonicalized blind audit package and then a stronger evidence verifier/refinement strategy.

## Next Internal Action

Hand off `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_form.csv` and `annotation/rulefaith_qwen3_audit_canonicalized/guidelines.md` to a human auditor, then use the audit to update the evidence verifier and decide whether any Qwen3 candidates can become positives.

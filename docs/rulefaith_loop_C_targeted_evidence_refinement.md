# Loop C: Targeted Evidence Refinement Smoke

Date: 2026-07-20

## Loop ID

Loop C / targeted evidence refinement and evidence-span canonicalization.

## Current Bottleneck

Qwen3 prompt-v2 removes prediction-only evidence in a 10-candidate smoke sample, but only 3/10 candidates contain contextual SOURCE evidence under the strict gate.

## Hypotheses

H-C1: A compact evidence-only Qwen3 repair prompt can improve contextual SOURCE evidence without introducing prediction-only evidence.

H-C2: Some apparent wrong-evidence failures are span-offset failures rather than substantive evidence failures, so a deterministic source-span canonicalizer can improve strict evidence scores without model regeneration.

## Required Evidence

- Qwen3 evidence-refinement outputs for the 7 smoke10 candidates with missing/wrong evidence.
- Strict evidence gate before/after metrics.
- Deterministic canonicalization outputs for the same smoke10 candidates.
- Unit tests for selection, prompt construction, JSON fallback parsing, and span canonicalization.

## Commands Executed

```bash
python3 -m py_compile experiments/rulefaith/refine_qwen3_evidence.py experiments/rulefaith/build_qwen3_manual_audit.py experiments/rulefaith/generate_teacher_candidates.py
python3 -m unittest discover -s experiments/tests
python3 experiments/rulefaith/refine_qwen3_evidence.py --dry-run --overwrite --stats-output results/rulefaith/qwen3_v2_smoke10_evidence_refinement_dryrun_stats.json --audit-md-output results/rulefaith/qwen3_v2_smoke10_evidence_refinement_dryrun_audit.md
HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/refine_qwen3_evidence.py --overwrite --max-input-length 1536 --max-new-tokens 320 --stats-output results/rulefaith/qwen3_v2_smoke10_evidence_refinement_stats.json --audit-md-output results/rulefaith/qwen3_v2_smoke10_evidence_refinement_audit.md --output results/rulefaith/qwen3_v2_smoke10_evidence_refined_candidates.jsonl --raw-dir results/rulefaith/qwen3_v2_smoke10_evidence_refinement_raw
python3 experiments/rulefaith/canonicalize_evidence_spans.py --overwrite
```

## Artifacts Produced

- `experiments/rulefaith/refine_qwen3_evidence.py`
- `experiments/rulefaith/canonicalize_evidence_spans.py`
- `experiments/tests/test_qwen3_evidence_refinement.py`
- `experiments/tests/test_evidence_span_canonicalizer.py`
- `results/rulefaith/qwen3_v2_smoke10_evidence_refined_candidates.jsonl`
- `results/rulefaith/qwen3_v2_smoke10_evidence_refinement_stats.json`
- `results/rulefaith/qwen3_v2_smoke10_evidence_refinement_audit.md`
- `results/rulefaith/qwen3_v2_smoke10_evidence_canonicalized_candidates.jsonl`
- `results/rulefaith/qwen3_v2_smoke10_evidence_canonicalization_stats.json`
- `results/rulefaith/qwen3_v2_smoke10_evidence_canonicalization_audit.md`

## Verified Results

Qwen3 evidence-only refinement selected 7/10 smoke candidates.

Before refinement on the selected 7:

- Contextual SOURCE evidence: 0/7
- Missing evidence: 7/7
- Prediction-only evidence: 0/7
- Wrong-evidence automatic flag: 6/7

After compact Qwen3 refinement:

- Parse status: 7/7 parsed JSON
- Contextual SOURCE evidence: 0/7
- Missing evidence: 7/7
- Prediction-only evidence: 0/7
- Wrong-evidence automatic flag: 0/7

Interpretation: the compact refinement prompt is JSON-stable and removes wrong indexed evidence, but it mostly does so by clearing evidence spans rather than adding contextual source evidence. This does not satisfy the evidence-grounding goal.

Deterministic evidence-span canonicalization on the 10 prompt-v2 smoke candidates:

- Contextual SOURCE evidence: 3/10 -> 8/10
- Missing evidence: 7/10 -> 2/10
- Prediction-only evidence: 0/10 -> 0/10
- Wrong-evidence automatic flag: 6/10 -> 0/10
- Corrected index actions: 7 exact plus 1 ambiguous index repair
- Dropped unlocatable spans: 1

Interpretation: many Qwen3 evidence failures in the smoke sample are source-span offset failures, not necessarily absence of source evidence. Evidence canonicalization should become a RuleFaith preprocessing step before scoring or model refinement.

Full-pool canonicalization over the original Qwen3 buckets:

Accepted bucket:

- Contextual source evidence: 0/41 -> 15/41
- Wrong-evidence flags: 39/41 -> 5/41

Refine bucket:

- Contextual source evidence: 10/63 -> 19/63
- Wrong-evidence flags: 52/63 -> 16/63

Rejected bucket:

- Contextual source evidence: 14/56 -> 48/56
- Wrong-evidence flags: 50/56 -> 8/56

Strict post-canonicalization audit across all 160 candidates:

- All evidence spans source-index matched: 20/160 -> 155/160
- Contextual source evidence: 24/160 -> 82/160
- Missing evidence: 136/160 -> 78/160
- Prediction-only evidence: 87/160 -> 29/160
- Wrong-evidence automatic flag: 141/160 -> 29/160

Interpretation: the original accepted/refine/rejected split was substantially affected by evidence offset errors. Canonicalized candidates should be re-prefiltered before selecting positives or refinement examples.

Canonicalized prefilter rerun:

- Merged canonicalized candidates: 160
- Parse JSON rate: 0.9938
- Alignment proxy pass rate: 0.6375
- Old diagnostic contextual-evidence rate: 0.3125
- New buckets: accepted 34, refine 67, rejected 59

Interpretation: strict evidence-span quality improves substantially after canonicalization, but the old prefilter still relies on rough alignment/contextual-evidence proxies. Positive construction should use post-canonicalization strict audit plus human review, not this prefilter alone.

## Hypothesis Status

- H-C1: rejected for now. Evidence-only Qwen3 refinement is parse-stable but does not add contextual evidence.
- H-C2: partially supported. Deterministic source-span canonicalization substantially improves strict evidence scores on smoke10 and the full 160-candidate pool without introducing prediction-only evidence, but it does not validate linguistic sufficiency.

## Remaining Risks

- Canonicalization fixes offsets but does not validate linguistic rule correctness.
- Some canonicalized spans may still be linguistically insufficient even if source-index matched.
- Human audit is still required before treating candidates as positives.
- 78/160 candidates still lack contextual evidence after canonicalization.

## Next Highest-Priority Loop

Run a 20-edit probe with canonicalization followed by targeted model refinement only for candidates that still lack contextual evidence, and send the canonicalized blind audit package for human review.

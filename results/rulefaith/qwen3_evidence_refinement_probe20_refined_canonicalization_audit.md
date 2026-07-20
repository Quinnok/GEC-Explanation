# Evidence Span Canonicalization Audit

This deterministic pass repairs evidence span offsets when the cited text can be located in SOURCE. It does not judge whether the rule is linguistically correct.

## Summary

- `generated_at`: `2026-07-20T13:10:38+00:00`
- `git_commit`: `841317b`
- `input_count`: `20`
- `canonicalized_count`: `20`
- `action_counts`: `{}`
- `before`: `{'contextual_source_evidence': 2, 'missing_evidence': 18, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `after`: `{'contextual_source_evidence': 2, 'missing_evidence': 18, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `improvement_counts`: `{'evidence_contextual_improved': 0, 'wrong_evidence_fixed': 0, 'prediction_only_evidence_regressed': 0}`
- `decision`: `canonicalizer_only_repairs_offsets_not_missing_contextual_evidence`
- `input_file`: `/Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_evidence_refinement_probe20_refined_candidates.jsonl`
- `output_file`: `/Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalized_candidates.jsonl`

## Changed Cases

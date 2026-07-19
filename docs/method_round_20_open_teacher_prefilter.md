# Method Round 20: Open-Teacher Prefilter

## Status

- Round: 20
- Main objective: test whether local open teachers can provide usable positive teacher candidates for RuleFaith-GEC.
- Highest risk: available small open teachers may produce edit-copy rationales rather than rule/evidence-grounded explanations.
- Git commit: pending
- Data version: `data/rulefaith/edit_pool.jsonl`
- Model versions:
  - `Qwen/Qwen2.5-0.5B-Instruct`
  - `Qwen/Qwen2.5-1.5B-Instruct` probe
  - `google/flan-t5-base`

## Work Completed

- Completed Qwen2.5-0.5B 80-edit pilot with 160 candidates using two local shards.
- Ran candidate quality audit and RuleFaith-specific teacher diagnostics.
- Added `experiments/rulefaith/diagnose_teacher_candidates.py`.
- Added `experiments/rulefaith/filter_teacher_candidates.py`.
- Ran conservative prefilter for Qwen2.5-0.5B, FLAN-T5-base, and Qwen2.5-1.5B probe outputs.
- Ran a Qwen2.5-1.5B non-punctuation probe with 20 candidates.

## Files Created or Modified

- `data/rulefaith/teacher_candidates_qwen_small_pilot.jsonl`
- `data/rulefaith/qwen_shards/teacher_candidates_qwen_small_pilot_shard_0.jsonl`
- `data/rulefaith/qwen_shards/teacher_candidates_qwen_small_pilot_shard_1.jsonl`
- `data/rulefaith/qwen15_probe_edits.jsonl`
- `data/rulefaith/filtering/qwen_small_accepted.jsonl`
- `data/rulefaith/filtering/qwen_small_refine.jsonl`
- `data/rulefaith/filtering/qwen_small_rejected.jsonl`
- `data/rulefaith/filtering/open_teacher_accepted.jsonl`
- `data/rulefaith/filtering/open_teacher_refine.jsonl`
- `data/rulefaith/filtering/open_teacher_rejected.jsonl`
- `data/rulefaith/filtering/qwen15_probe_accepted.jsonl`
- `data/rulefaith/filtering/qwen15_probe_refine.jsonl`
- `data/rulefaith/filtering/qwen15_probe_rejected.jsonl`
- `results/rulefaith/qwen_teacher_diagnostic_metrics.json`
- `results/rulefaith/qwen_teacher_diagnostic_cases.md`
- `results/rulefaith/qwen_filtering_statistics.json`
- `results/rulefaith/open_teacher_diagnostic_metrics.json`
- `results/rulefaith/open_teacher_diagnostic_cases.md`
- `results/rulefaith/open_teacher_filtering_statistics.json`
- `results/rulefaith/qwen15_probe_candidates.jsonl`
- `results/rulefaith/qwen15_probe_diagnostic_metrics.json`
- `results/rulefaith/qwen15_probe_diagnostic_cases.md`
- `results/rulefaith/qwen15_probe_filtering_statistics.json`

## Commands Executed

- `HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN_SHARDS=2 bash experiments/rulefaith/run_qwen_teacher_pilot.sh`
- `.venv311/bin/python experiments/rulefaith/diagnose_teacher_candidates.py --input data/rulefaith/teacher_candidates_qwen_small_pilot.jsonl --json-output results/rulefaith/qwen_teacher_diagnostic_metrics.json --md-output results/rulefaith/qwen_teacher_diagnostic_cases.md`
- `.venv311/bin/python experiments/rulefaith/filter_teacher_candidates.py --candidates data/rulefaith/teacher_candidates_qwen_small_pilot.jsonl --diagnostics results/rulefaith/qwen_teacher_diagnostic_metrics.json --output-dir data/rulefaith/filtering --stats results/rulefaith/qwen_filtering_statistics.json --prefix qwen_small`
- `.venv311/bin/python experiments/rulefaith/diagnose_teacher_candidates.py --input data/rulefaith/teacher_candidates_pilot.jsonl --json-output results/rulefaith/open_teacher_diagnostic_metrics.json --md-output results/rulefaith/open_teacher_diagnostic_cases.md`
- `.venv311/bin/python experiments/rulefaith/filter_teacher_candidates.py --candidates data/rulefaith/teacher_candidates_pilot.jsonl --diagnostics results/rulefaith/open_teacher_diagnostic_metrics.json --output-dir data/rulefaith/filtering --stats results/rulefaith/open_teacher_filtering_statistics.json --prefix open_teacher`
- `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --qwen-model Qwen/Qwen2.5-1.5B-Instruct --input data/rulefaith/qwen15_probe_edits.jsonl --limit 10 --candidate-types natural rule_grounded --output results/rulefaith/qwen15_probe_candidates.jsonl --stats results/rulefaith/qwen15_probe_stats.json --parse-failures results/rulefaith/qwen15_probe_parse_failures.jsonl --raw-dir results/rulefaith/qwen15_probe_raw`

## Verified Results

| Teacher | Candidates | Parse JSON | Alignment Proxy | Missing Rule | Rule Edit-Copy | Contextual Evidence | Accepted | Refine | Rejected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FLAN-T5-base | 160 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0 | 0 | 160 |
| Qwen2.5-0.5B | 160 | 0.975 | 0.769 | 0.025 | 0.887 | 0.037 | 1 | 15 | 144 |
| Qwen2.5-1.5B probe | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 0.350 | 0 | 0 | 20 |

## Scientific Interpretation

Qwen2.5-0.5B is substantially more parseable than FLAN-T5-base and can act as a local open direct baseline. However, most candidates restate the edit rather than giving a real grammatical rule or contextual evidence. Qwen2.5-1.5B improves edit alignment on the non-punctuation probe but fails to populate explicit `rule_text` under the current prompt. Neither open teacher currently provides enough positive examples for SFT or preference optimization.

## Go / No-Go

No-Go for student distillation with current open-teacher positives.

Proceeding to Vanilla SFT, Filtered SFT, DPO, or RuleFaith-GEC training with these candidates would train the student to copy edits and omit explicit rule/evidence grounding. The next viable path requires GPT-5.5 credentials, a stronger open model/prompting strategy, or a small manually validated positive seed set.

## Open Issues

- GPT-5.5 teacher generation remains blocked by missing `OPENAI_API_KEY`.
- Current open teachers are insufficient as positive teacher data.
- Qwen outputs often include markdown code fences despite prompt instructions.
- Qwen2.5-0.5B rarely provides contextual evidence.
- Qwen2.5-1.5B probe often places rule-like content in rationale while leaving `rule_text` missing.

## Next Internal Action

Obtain a stronger teacher source before constructing SFT/preference data. The preferred next action is to run GPT-5.5 teacher generation with budget controls; the fallback is to redesign the Qwen prompt and rerun a 20-edit probe before any larger local generation.

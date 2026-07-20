# Method Round 20 Qwen3-8B Addendum

## Status

- Round: 20 open-teacher prefilter extension
- Main objective: rerun the Qwen2.5-style open-teacher pilot with `Qwen/Qwen3-8B`
- Highest risk: stronger open-teacher generations may still fail evidence grounding or alignment checks
- Git commit before work: `68bf812`
- Model version: `Qwen/Qwen3-8B`, revision `b968826d9c46dd6066d109eabc6255188de91218`

## Work Completed

- Upgraded the local environment to `transformers==5.14.1`, `huggingface_hub==1.24.0`, and `tokenizers==0.22.2` so Qwen3 can load.
- Added provider-name support for Qwen-style causal chat models, preventing Qwen3 candidate IDs from colliding with Qwen2.5 outputs.
- Added Qwen3 no-thinking support through `tokenizer.apply_chat_template(..., enable_thinking=False)` when available and stripped any `<think>...</think>` blocks defensively.
- Added `configs/rulefaith/qwen3_8b_teacher.yaml`.
- Added `experiments/rulefaith/run_qwen3_8b_teacher_pilot.sh`.
- Ran a 1-candidate smoke test and then a full 80-edit pilot with 2 shards.
- Ran the same diagnostic and conservative prefilter used for FLAN-T5 and Qwen2.5.

## Files Created or Modified

- `configs/rulefaith/qwen3_8b_teacher.yaml`
- `experiments/rulefaith/run_qwen3_8b_teacher_pilot.sh`
- `experiments/rulefaith/generate_teacher_candidates.py`
- `requirements.txt`
- `data/rulefaith/teacher_candidates_qwen3_8b_pilot.jsonl`
- `data/rulefaith/qwen3_8b_shards/teacher_candidates_qwen3_8b_pilot_shard_0.jsonl`
- `data/rulefaith/qwen3_8b_shards/teacher_candidates_qwen3_8b_pilot_shard_1.jsonl`
- `data/rulefaith/filtering/qwen3_8b_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_8b_refine.jsonl`
- `data/rulefaith/filtering/qwen3_8b_rejected.jsonl`
- `results/rulefaith/qwen3_8b_teacher_generation_stats.json`
- `results/rulefaith/qwen3_8b_teacher_candidate_quality_flags.json`
- `results/rulefaith/qwen3_8b_teacher_candidate_quality_report.md`
- `results/rulefaith/qwen3_8b_teacher_diagnostic_metrics.json`
- `results/rulefaith/qwen3_8b_teacher_diagnostic_cases.md`
- `results/rulefaith/qwen3_8b_filtering_statistics.json`
- `results/rulefaith/qwen_open_teacher_comparison.csv`
- `results/rulefaith/qwen_open_teacher_comparison.tex`

## Commands Executed

- `.venv311/bin/python -m pip install 'transformers>=4.51.0'`
- `.venv311/bin/python -m py_compile experiments/rulefaith/generate_teacher_candidates.py experiments/rulefaith/diagnose_teacher_candidates.py experiments/rulefaith/filter_teacher_candidates.py experiments/rulefaith/merge_teacher_candidate_shards.py`
- `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --qwen-model Qwen/Qwen3-8B --qwen-provider-name qwen3_8b --qwen-config configs/rulefaith/qwen3_8b_teacher.yaml --limit 0 --output results/rulefaith/qwen3_8b_limit0_candidates.jsonl --stats results/rulefaith/qwen3_8b_limit0_stats.json --parse-failures results/rulefaith/qwen3_8b_limit0_parse_failures.jsonl --raw-dir results/rulefaith/qwen3_8b_limit0_raw`
- `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --qwen-model Qwen/Qwen3-8B --qwen-provider-name qwen3_8b --qwen-config configs/rulefaith/qwen3_8b_teacher.yaml --limit 1 --candidate-types natural --output results/rulefaith/qwen3_8b_smoke_candidates.jsonl --stats results/rulefaith/qwen3_8b_smoke_stats.json --parse-failures results/rulefaith/qwen3_8b_smoke_parse_failures.jsonl --raw-dir results/rulefaith/qwen3_8b_smoke_raw`
- `HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN3_SHARDS=2 bash experiments/rulefaith/run_qwen3_8b_teacher_pilot.sh`
- `.venv311/bin/python experiments/rulefaith/diagnose_teacher_candidates.py --input data/rulefaith/teacher_candidates_qwen3_8b_pilot.jsonl --json-output results/rulefaith/qwen3_8b_teacher_diagnostic_metrics.json --md-output results/rulefaith/qwen3_8b_teacher_diagnostic_cases.md`
- `.venv311/bin/python experiments/rulefaith/filter_teacher_candidates.py --candidates data/rulefaith/teacher_candidates_qwen3_8b_pilot.jsonl --diagnostics results/rulefaith/qwen3_8b_teacher_diagnostic_metrics.json --output-dir data/rulefaith/filtering --stats results/rulefaith/qwen3_8b_filtering_statistics.json --prefix qwen3_8b`

## Verified Results

| Model | N | Parse JSON | Alignment Proxy | Missing Rule | Rule Edit-Copy | Contextual Evidence | Accepted | Refine | Rejected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FLAN/open | 160 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0 | 0 | 160 |
| Qwen2.5-0.5B | 160 | 0.975 | 0.769 | 0.025 | 0.887 | 0.037 | 1 | 15 | 144 |
| Qwen2.5-1.5B probe | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 0.350 | 0 | 0 | 20 |
| Qwen3-8B | 160 | 0.994 | 0.656 | 0.006 | 0.006 | 0.388 | 41 | 63 | 56 |

The Qwen3-8B run is the first local open-teacher branch to produce a non-trivial accepted candidate set under the conservative RuleFaith prefilter. It reduces edit-copy behavior sharply compared with Qwen2.5-0.5B and produces explicit rule text in nearly all parsed candidates.

## Failed Runs

- No Qwen3-8B generation command failed.
- Initial Qwen3-8B download was slow because the environment used unauthenticated Hugging Face requests; final cache size is about 15GB and no incomplete blobs remain.

## Scientific Interpretation

Qwen3-8B should replace Qwen2.5-0.5B as the primary local open-teacher candidate source. However, 98/160 candidates still lack contextual evidence under the current heuristic and 55/160 fail the exact-string alignment proxy. These failures require refinement and targeted manual audit before using accepted candidates as SFT positives.

## Claim-Evidence Updates

- M-C12 should be revised: Qwen2.5 small is not adequate as positive teacher data.
- New evidence supports a stronger claim that Qwen3-8B can supply useful open-teacher candidates for RuleFaith refinement.

## Open Issues

- Qwen3-8B accepted candidates need manual spot-checking before they are treated as positive SFT data.
- The alignment proxy may be overly strict for paraphrased edit descriptions such as "change" vs. "replace"; do not tune it on final test labels without preregistration.
- Qwen3-8B still does not replace GPT-5.5 as a strong teacher; it is a viable local open branch.

## Next Internal Action

Run RuleFaith refinement on the 63 Qwen3-8B `refine` candidates, then manually audit a small accepted/refined sample before constructing preference pairs.

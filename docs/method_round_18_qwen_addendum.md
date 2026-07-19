# Method Round 18 Qwen Addendum

## Status

- Round: 18 addendum
- Main objective: add a stronger local open instruction teacher branch for RuleFaith-GEC.
- Highest risk: Hugging Face model-weight download is currently too slow to complete the first Qwen smoke test.
- Git commit: pending
- Data version: `data/rulefaith/edit_pool.jsonl`
- Model version: `Qwen/Qwen2.5-0.5B-Instruct` intended; weights not fully cached yet.

## Work Completed

- Added `qwen_small` provider to `experiments/rulefaith/generate_teacher_candidates.py`.
- Added strict JSON chat prompting through Qwen chat templates.
- Added token usage, raw response, parse-failure, latency, and zero-cost local inference logging for Qwen.
- Added provider-specific config in `configs/rulefaith/qwen_small_teacher.yaml`.
- Added `experiments/rulefaith/run_qwen_teacher_pilot.sh` with shard-level parallel execution controlled by `RULEFAITH_QWEN_SHARDS`.
- Added `experiments/rulefaith/merge_teacher_candidate_shards.py` to merge shard outputs without duplicate candidate IDs.
- Updated README and method logs to distinguish FLAN-T5 weak baseline, Qwen local open teacher, and GPT-5.5 strong API teacher.

## Commands Executed

- `.venv311/bin/python -m py_compile experiments/rulefaith/generate_teacher_candidates.py experiments/rulefaith/audit_teacher_candidates.py experiments/rulefaith/merge_teacher_candidate_shards.py`
- `.venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --limit 0 --output results/rulefaith/qwen_limit0_candidates.jsonl --stats results/rulefaith/qwen_limit0_stats.json --parse-failures results/rulefaith/qwen_limit0_parse_failures.jsonl --raw-dir results/rulefaith/qwen_limit0_raw`
- `.venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --limit 1 --candidate-types natural --output results/rulefaith/qwen_smoke_candidates.jsonl --stats results/rulefaith/qwen_smoke_stats.json --parse-failures results/rulefaith/qwen_smoke_parse_failures.jsonl --raw-dir results/rulefaith/qwen_smoke_raw`
- `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --limit 1 --candidate-types natural --output results/rulefaith/qwen_smoke_candidates.jsonl --stats results/rulefaith/qwen_smoke_stats.json --parse-failures results/rulefaith/qwen_smoke_parse_failures.jsonl --raw-dir results/rulefaith/qwen_smoke_raw --resume`

## Verified Results

- Python compile checks passed.
- `qwen_small --limit 0` passed and wrote scheduler/summary metadata without triggering model loading.
- Hugging Face cache for `Qwen/Qwen2.5-0.5B-Instruct` was created.
- Smoke generation did not complete because the model-weight download stalled at about 37 MB and was manually interrupted.
- No Qwen explanation candidate has been produced yet.

## Failed Runs

- Qwen smoke attempt 1: interrupted during Hugging Face Xet-backed weight download.
- Qwen smoke attempt 2: retried with `HF_HUB_DISABLE_XET=1`; interrupted after ordinary HTTP weight download also stalled.

## Scientific Interpretation

Adding Qwen small is methodologically correct because the FLAN-T5-base branch is too weak to serve as a useful open teacher, while Qwen2.5-0.5B-Instruct is a small instruction model that can diversify teacher candidates without API cost. This addendum does not provide evidence that Qwen candidates are high quality; that claim remains unverified until the pilot completes.

## Claim-Evidence Updates

- Added M-C12 to the method claim-evidence matrix: Qwen small as a stronger local open-teacher source remains unverified.

## Open Issues

- Qwen model weights are not fully cached.
- GPT-5.5 teacher branch remains blocked by missing API credentials.
- No method-pilot filtering or preference-data construction should use Qwen until candidate quality is audited.

## Next Internal Action

Run:

```bash
HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN_SHARDS=2 bash experiments/rulefaith/run_qwen_teacher_pilot.sh
```

after the Qwen model download is stable or the model has been pre-cached.

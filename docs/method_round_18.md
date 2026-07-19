# Method Round 18

## Status

Teacher candidate scaffolding complete; GPT-5.5 generation blocked by missing API credentials.

## Main Objective

Prepare GPT-5.5 and open-teacher generation for the 80-edit natural explanation pilot.

## Highest Risk

No `OPENAI_API_KEY` is visible, so the required GPT-5.5 teacher pilot cannot run. The local open teacher is too weak to replace it.

## Git Commit

Recorded in Git history as `Round 18 teacher candidate scaffolding`.

## Data Version

- Input edit pool: `data/rulefaith/edit_pool.jsonl`
- Output candidates: `data/rulefaith/teacher_candidates_pilot.jsonl`

## Model Version

- Open teacher: `google/flan-t5-base`
- GPT-5.5: not run; blocked by missing `OPENAI_API_KEY`.

## Work Completed

- Created GPT-5.5 and open-teacher configs.
- Created strict teacher prompt and data card.
- Implemented `experiments/rulefaith/generate_teacher_candidates.py`.
- Implemented budget/key checks for GPT generation.
- Implemented raw-response, parse-failure, stats, resume, and optional OpenAI import handling.
- Ran open-teacher pilot on 80 edits with 160 candidates.
- Preserved failed/weak FLAN-T5 runs under `results/rulefaith/failed_runs/`.
- Added teacher candidate quality audit.

## Files Created or Modified

- `configs/rulefaith/gpt55_teacher.yaml`
- `configs/rulefaith/open_teacher.yaml`
- `docs/rulefaith_teacher_prompt.md`
- `docs/rulefaith_teacher_data_card.md`
- `experiments/rulefaith/generate_teacher_candidates.py`
- `experiments/rulefaith/audit_teacher_candidates.py`
- `experiments/rulefaith/run_teacher_pilot.sh`
- `data/rulefaith/teacher_candidates_pilot.jsonl`
- `results/rulefaith/teacher_generation_stats.json`
- `results/rulefaith/teacher_parse_failures.jsonl`
- `results/rulefaith/teacher_raw_responses/`
- `results/rulefaith/teacher_candidate_quality_flags.json`
- `results/rulefaith/teacher_candidate_quality_report.md`
- `results/rulefaith/failed_runs/`

## Commands Executed

- `.venv311/bin/python -m py_compile experiments/rulefaith/generate_teacher_candidates.py`
- `RULEFAITH_TEACHER_PROVIDER=open_teacher RULEFAITH_TEACHER_LIMIT=80 bash experiments/rulefaith/run_teacher_pilot.sh`
- `.venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider all --limit 80 --resume`
- `.venv311/bin/python -m py_compile experiments/rulefaith/audit_teacher_candidates.py`
- `.venv311/bin/python experiments/rulefaith/audit_teacher_candidates.py`

## Verified Results

- Open-teacher candidates: 160.
- Candidate types: 80 natural, 80 rule-grounded.
- Model coverage: CoEdIT 56, GECToR 52, T5 52 candidates.
- GPT-5.5 candidates: 0.
- API spend: 0.0 USD.
- GPT blocker: `gpt55_failed:missing_OPENAI_API_KEY`.
- Open-teacher low-quality flags: 98/160, rate 0.6125.

## Failed Runs

- JSON prompt with FLAN-T5-small produced mostly invalid fragments.
- Plain-text prompt with FLAN-T5-small initially exposed a candidate-type loop bug and then weak outputs.
- Both are preserved under `results/rulefaith/failed_runs/`.

## Scientific Interpretation

Round 18 proves the teacher-generation infrastructure is ready and safe, but does not yet provide the required strong natural teacher candidates. FLAN-T5-base is a weak open baseline, not a substitute for GPT-5.5.

## Claim-Evidence Updates

- M-C11 is currently not supported: FLAN-T5-base does not provide sufficiently reliable natural explanations.

## Open Issues

- `OPENAI_API_KEY` is required for the GPT-5.5 teacher pilot.
- A stronger open instruction model may be needed if GPT outputs cannot be used.

## Next Internal Action

Use existing Round 15 human labels to calibrate the verifier stack while waiting for GPT credentials.

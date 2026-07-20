# RuleFaith-GEC Method Experiment Log

## Round 16: Branch and Preregistration

- Date: 2026-07-19
- Branch: `method/rulefaith-gec`
- Starting commit: `4519543060cbaff49806fd9963412f4ca4ab83c0`
- Created method directories under `configs/rulefaith/`, `experiments/rulefaith/`, `data/rulefaith/`, `results/rulefaith/`, and `logs/rulefaith/`.
- Frozen Round 15 stress-test snapshot in `docs/method_snapshots/round15_stress_test_snapshot.md`.
- Preregistered primary hypotheses and metric mappings before new method results.

No GPT-5.5 calls or student training were run in Round 16.

## Round 17: Substantive Edit Pool

- Date: 2026-07-19
- Script: `.venv311/bin/python experiments/rulefaith/build_edit_pool.py`
- Input: `data/faithfulness_benchmark/edit_records.jsonl`
- Output pool: `data/rulefaith/edit_pool.jsonl`
- Split files: `data/rulefaith/train_edits.jsonl`, `data/rulefaith/dev_edits.jsonl`, `data/rulefaith/test_edits.jsonl`
- Selected edits: 300
- Model counts: `gector_roberta_base=120`, `t5_base_grammar=120`, `coedit_large=60`
- Dataset counts: `EXPECT=165`, `JFLEG=135`
- Behavior counts: `correct_correction=77`, `wrong_correction=72`, `overcorrection=151`
- Operation counts: `replace=237`, `insert=30`, `delete=33`
- Excluded obvious detokenization/format artifacts: 251
- Source keys crossing splits: 0
- Target strings crossing splits: 13
- Near-duplicate source pairs at >=0.92 similarity: 0

Interpretation: the pool is suitable for natural teacher generation and method development, but later target-masked and leakage-aware evaluation is mandatory.

## Round 18: Teacher Candidate Pilot Scaffolding

- Date: 2026-07-19
- Scripts:
  - `.venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider all --limit 80 --resume`
  - `.venv311/bin/python experiments/rulefaith/audit_teacher_candidates.py`
- Configs:
  - `configs/rulefaith/gpt55_teacher.yaml`
  - `configs/rulefaith/open_teacher.yaml`
- Prompt doc: `docs/rulefaith_teacher_prompt.md`
- Open teacher model: `google/flan-t5-base`
- Open teacher candidates: 160 candidates for 80 edits, 80 natural and 80 rule-grounded.
- GPT-5.5 candidates: 0; blocked by missing `OPENAI_API_KEY`.
- Estimated API cost: 0.0 USD.
- Parse status: all 160 open-teacher candidates are wrapped non-JSON responses.
- Quality audit: 98/160 candidates flagged low quality, low-quality rate 0.6125.
- Failed/weak runs preserved under `results/rulefaith/failed_runs/`.

Interpretation: the open teacher is usable as a weak baseline/failure signal but is not strong enough to replace the GPT-5.5 teacher pilot.

## Round 19: Verifier Calibration

- Date: 2026-07-19
- Script: `.venv311/bin/python experiments/rulefaith/calibrate_verifiers.py`
- Calibration source: `results/human_gold/main_metric_table.csv`
- Output:
  - `results/rulefaith/verifier_metrics.json`
  - `results/rulefaith/verifier_calibration.csv`
  - `results/rulefaith/verifier_error_cases.md`
  - `docs/rulefaith_verifier_design.md`
- Gate A status: `conditional_pass`.
- Rule/Evidence verifier AUROC:
  - Edit Alignment: 0.75
  - Rule Correctness: 0.7562582345191041
  - Evidence Correctness: 0.6666666666666666
  - Target-masked edit alignment: 0.7582194010416666
- Delta over reverse reconstruction:
  - Rule AUROC: +0.3280632411067194
  - Evidence AUROC: +0.2530381944444444

Interpretation: verifier calibration is adequate for method-pilot filtering, but it is not final evidence for natural explanation generation quality.

## Environment Check After Round 19

- `git diff --check`: passed.
- Python compile checks for Round 18/19 scripts: passed.
- Paper compile rerun: failed because `pdflatex`/`latexmk` are not available in the current shell and `.local-tools/tectonic` cannot compile `aaai2027.sty`, which requires pdfTeX.
- Paper sources were not changed in Rounds 18/19; the previous `paper/main.pdf` remains available.

## Qwen Small Teacher Addendum and Open-Teacher Prefilter

- Date: 2026-07-19
- Added provider: `qwen_small`
- Default model: `Qwen/Qwen2.5-0.5B-Instruct`
- Config: `configs/rulefaith/qwen_small_teacher.yaml`
- Runner: `experiments/rulefaith/run_qwen_teacher_pilot.sh`
- Parallel support: `RULEFAITH_QWEN_SHARDS=N` launches N independent generation shards and merges them with `experiments/rulefaith/merge_teacher_candidate_shards.py`.
- Validation commands:
  - `.venv311/bin/python -m py_compile experiments/rulefaith/generate_teacher_candidates.py experiments/rulefaith/audit_teacher_candidates.py experiments/rulefaith/merge_teacher_candidate_shards.py`
  - `.venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --limit 0 --output results/rulefaith/qwen_limit0_candidates.jsonl --stats results/rulefaith/qwen_limit0_stats.json --parse-failures results/rulefaith/qwen_limit0_parse_failures.jsonl --raw-dir results/rulefaith/qwen_limit0_raw`
  - `.venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --limit 1 --candidate-types natural --output results/rulefaith/qwen_smoke_candidates.jsonl --stats results/rulefaith/qwen_smoke_stats.json --parse-failures results/rulefaith/qwen_smoke_parse_failures.jsonl --raw-dir results/rulefaith/qwen_smoke_raw`
  - `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --limit 1 --candidate-types natural --output results/rulefaith/qwen_smoke_candidates.jsonl --stats results/rulefaith/qwen_smoke_stats.json --parse-failures results/rulefaith/qwen_smoke_parse_failures.jsonl --raw-dir results/rulefaith/qwen_smoke_raw --resume`
- Qwen2.5-0.5B full pilot:
  - Command: `HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN_SHARDS=2 bash experiments/rulefaith/run_qwen_teacher_pilot.sh`
  - Output: `data/rulefaith/teacher_candidates_qwen_small_pilot.jsonl`
  - Candidates: 160 for 80 edits, 80 natural and 80 rule-grounded.
  - Parse JSON rate: 0.975.
  - Alignment proxy pass: 0.7688.
  - Rule edit-copy rate: 0.8875.
  - Contextual evidence rate: 0.0375.
  - Conservative prefilter: 1 accepted, 15 refine, 144 rejected.
- Qwen2.5-1.5B probe:
  - Model size in local cache: about 2.9GB.
  - Output: `results/rulefaith/qwen15_probe_candidates.jsonl`
  - Candidates: 20 for 10 non-punctuation edits.
  - Parse JSON rate: 1.0.
  - Alignment proxy pass: 1.0.
  - Missing rule text rate: 1.0.
  - Conservative prefilter: 0 accepted, 0 refine, 20 rejected.
- FLAN-T5-base prefilter:
  - Conservative prefilter: 0 accepted, 0 refine, 160 rejected.
- Interpretation: current open teachers are useful as direct baselines, negative candidates, and refinement stress cases, but not as positive teacher data for RuleFaith SFT/preference training.

## Qwen3-8B Teacher Pilot Addendum

- Date: 2026-07-20
- Model: `Qwen/Qwen3-8B`
- Provider name: `qwen3_8b`
- Config: `configs/rulefaith/qwen3_8b_teacher.yaml`
- Runner: `experiments/rulefaith/run_qwen3_8b_teacher_pilot.sh`
- Thinking mode: disabled via Qwen chat template when supported; decoded `<think>...</think>` blocks are stripped defensively.
- Dependency update:
  - `transformers==5.14.1`
  - `huggingface_hub==1.24.0`
  - `tokenizers==0.22.2`
- Validation and generation commands:
  - `.venv311/bin/python -m py_compile experiments/rulefaith/generate_teacher_candidates.py experiments/rulefaith/diagnose_teacher_candidates.py experiments/rulefaith/filter_teacher_candidates.py experiments/rulefaith/merge_teacher_candidate_shards.py`
  - `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --qwen-model Qwen/Qwen3-8B --qwen-provider-name qwen3_8b --qwen-config configs/rulefaith/qwen3_8b_teacher.yaml --limit 0 --output results/rulefaith/qwen3_8b_limit0_candidates.jsonl --stats results/rulefaith/qwen3_8b_limit0_stats.json --parse-failures results/rulefaith/qwen3_8b_limit0_parse_failures.jsonl --raw-dir results/rulefaith/qwen3_8b_limit0_raw`
  - `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --qwen-model Qwen/Qwen3-8B --qwen-provider-name qwen3_8b --qwen-config configs/rulefaith/qwen3_8b_teacher.yaml --limit 1 --candidate-types natural --output results/rulefaith/qwen3_8b_smoke_candidates.jsonl --stats results/rulefaith/qwen3_8b_smoke_stats.json --parse-failures results/rulefaith/qwen3_8b_smoke_parse_failures.jsonl --raw-dir results/rulefaith/qwen3_8b_smoke_raw`
  - `HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN3_SHARDS=2 bash experiments/rulefaith/run_qwen3_8b_teacher_pilot.sh`
  - `.venv311/bin/python experiments/rulefaith/diagnose_teacher_candidates.py --input data/rulefaith/teacher_candidates_qwen3_8b_pilot.jsonl --json-output results/rulefaith/qwen3_8b_teacher_diagnostic_metrics.json --md-output results/rulefaith/qwen3_8b_teacher_diagnostic_cases.md`
  - `.venv311/bin/python experiments/rulefaith/filter_teacher_candidates.py --candidates data/rulefaith/teacher_candidates_qwen3_8b_pilot.jsonl --diagnostics results/rulefaith/qwen3_8b_teacher_diagnostic_metrics.json --output-dir data/rulefaith/filtering --stats results/rulefaith/qwen3_8b_filtering_statistics.json --prefix qwen3_8b`
- Qwen3-8B full pilot:
  - Output: `data/rulefaith/teacher_candidates_qwen3_8b_pilot.jsonl`
  - Candidates: 160 for 80 edits, 80 natural and 80 rule-grounded.
  - Parse JSON rate: 0.9938.
  - Alignment proxy pass: 0.6562.
  - Missing rule text rate: 0.0063.
  - Rule edit-copy rate: 0.0063.
  - Contextual evidence rate: 0.3875.
  - Conservative prefilter: 41 accepted, 63 refine, 56 rejected.
- Comparison table:
  - `results/rulefaith/qwen_open_teacher_comparison.csv`
  - `results/rulefaith/qwen_open_teacher_comparison.tex`

Interpretation: Qwen3-8B should replace Qwen2.5 as the primary local open-teacher branch. It still needs verifier-guided refinement and manual spot-checking before any student SFT/preference training.

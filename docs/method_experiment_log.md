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
## 2026-07-20 Loop A Qwen3-8B Candidate Audit

Objective: audit Qwen3-8B accepted/refine/rejected candidates before targeted refinement or SFT positives.

Inputs:

- `data/rulefaith/filtering/qwen3_8b_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_8b_refine.jsonl`
- `data/rulefaith/filtering/qwen3_8b_rejected.jsonl`
- `data/rulefaith/edit_pool.jsonl`

Outputs:

- `results/rulefaith/qwen3_manual_audit.csv`
- `results/rulefaith/qwen3_manual_audit_summary.json`
- `results/rulefaith/qwen3_manual_audit_cases.md`

Verified results:

- 160 candidates audited.
- 80 rows selected for stratified manual audit.
- 0/160 generator input leakage flags.
- 160/160 source edit spans match the source tokenization.
- 160/160 target texts are present in predictions when applicable.
- 48/160 evidence spans match source token indices.
- 51/160 have contextual evidence under automatic checks.
- 109/160 are missing contextual evidence.
- 19/160 are possible false rationalizations.
- 28/160 have edit-validity risk.

Validation:

- `python3 -m py_compile experiments/rulefaith/build_qwen3_manual_audit.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 12 tests.
- `pytest -q` was attempted but unavailable: `pytest: command not found`.

Decision: revise evidence verifier and evidence-generation prompt before targeted refinement. Do not treat Qwen3 accepted/refine candidates as SFT positives yet.

## 2026-07-20 Loop B Evidence Gate Repair

Objective: tighten Qwen3 evidence-span validation and create a blind human audit package before targeted refinement.

Code/config changes:

- Updated `experiments/rulefaith/build_qwen3_manual_audit.py` with stricter source-only evidence diagnostics.
- Updated `experiments/rulefaith/generate_teacher_candidates.py` Qwen prompt with source-only evidence-span requirements.
- Updated `configs/rulefaith/qwen3_8b_teacher.yaml` prompt version to `rulefaith_qwen3_8b_teacher_v2_source_evidence_no_think_json`.

Outputs:

- `annotation/rulefaith_qwen3_audit/manual_audit_form.csv`
- `annotation/rulefaith_qwen3_audit/manual_audit_key.csv`
- `annotation/rulefaith_qwen3_audit/guidelines.md`
- Updated `results/rulefaith/qwen3_manual_audit.csv`
- Updated `results/rulefaith/qwen3_manual_audit_summary.json`
- Updated `results/rulefaith/qwen3_manual_audit_cases.md`

Verified results:

- 160 candidates audited.
- 80 blind rows selected for human audit.
- 0/160 generator input leakage flags.
- 160/160 source edit spans match the source tokenization.
- 160/160 target texts are present in predictions when applicable.
- 48/160 candidates have at least one source-index-matched evidence span.
- 20/160 candidates have all evidence spans source-index matched.
- 24/160 candidates have contextual source evidence.
- 87/160 candidates include prediction-only evidence.
- 141/160 candidates receive an automatic wrong-evidence flag.
- Evidence error types: index_text_mismatch 121, prediction_only_text 62, prediction_or_target_role 29, invalid_indices 24, text_not_in_source 23, missing_evidence 1.

Validation:

- `python3 -m py_compile experiments/rulefaith/build_qwen3_manual_audit.py experiments/rulefaith/generate_teacher_candidates.py` passed.
- `python3 -m unittest experiments.tests.test_qwen3_manual_audit` passed, 8 tests.

Decision: keep Qwen3-8B as the primary local teacher branch, but treat v1 candidates as audit/refinement material only. Regenerate or refine with prompt v2 before training data construction.

Prompt-v2 smoke tests:

- Command: `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --qwen-model Qwen/Qwen3-8B --qwen-provider-name qwen3_8b --qwen-config configs/rulefaith/qwen3_8b_teacher.yaml --limit 1 --candidate-types natural --output results/rulefaith/qwen3_v2_smoke_candidates.jsonl --stats results/rulefaith/qwen3_v2_smoke_stats.json --parse-failures results/rulefaith/qwen3_v2_smoke_parse_failures.jsonl --raw-dir results/rulefaith/qwen3_v2_smoke_raw --resume`
- Output: `results/rulefaith/qwen3_v2_smoke_candidates.jsonl`
- Audit: `results/rulefaith/qwen3_v2_smoke_audit.json`
- Candidate count: 1
- Parse status: parsed JSON
- Latency: 22.9837 seconds after model load
- Evidence source-index match: true
- Prediction-only evidence: false
- Interpretation: promising smoke result only; not enough to claim prompt-v2 solves evidence grounding.

Smoke10:

- Command: `HF_HUB_DISABLE_XET=1 .venv311/bin/python experiments/rulefaith/generate_teacher_candidates.py --provider qwen_small --qwen-model Qwen/Qwen3-8B --qwen-provider-name qwen3_8b --qwen-config configs/rulefaith/qwen3_8b_teacher.yaml --limit 10 --candidate-types natural --output results/rulefaith/qwen3_v2_smoke10_candidates.jsonl --stats results/rulefaith/qwen3_v2_smoke10_stats.json --parse-failures results/rulefaith/qwen3_v2_smoke10_parse_failures.jsonl --raw-dir results/rulefaith/qwen3_v2_smoke10_raw --resume`
- Output: `results/rulefaith/qwen3_v2_smoke10_candidates.jsonl`
- Audit: `results/rulefaith/qwen3_v2_smoke10_audit.json`
- Candidate count: 10
- Parse status: 10/10 parsed JSON
- Source span match: 10/10
- Target present in prediction: 10/10
- At least one evidence span source-index matched: 6/10
- All evidence spans source-index matched: 4/10
- Contextual source evidence: 3/10
- Prediction-only evidence: 0/10
- Wrong-evidence automatic flag: 6/10
- Interpretation: prompt-v2 removed prediction-only evidence in this smoke sample, but it still under-produces contextual source evidence. Targeted evidence refinement or a stronger prompt is needed before scaling.

## 2026-07-20 Loop C Targeted Evidence Refinement Smoke

Objective: test whether evidence-only repair can improve Qwen3 prompt-v2 evidence grounding on the 10-candidate smoke sample.

Model-only refinement:

- Script: `experiments/rulefaith/refine_qwen3_evidence.py`
- Input: `results/rulefaith/qwen3_v2_smoke10_candidates.jsonl`
- Output: `results/rulefaith/qwen3_v2_smoke10_evidence_refined_candidates.jsonl`
- Audit: `results/rulefaith/qwen3_v2_smoke10_evidence_refinement_audit.md`
- Selected for refinement: 7/10 candidates.
- Parse status after compact prompt v2: 7/7 parsed JSON.
- Selected-before contextual evidence: 0/7.
- Selected-after contextual evidence: 0/7.
- Selected-before wrong-evidence flags: 6/7.
- Selected-after wrong-evidence flags: 0/7.
- Prediction-only evidence regression: 0/7.

Interpretation: compact model-only refinement is JSON-stable and removes invalid evidence spans, but it mostly clears evidence rather than adding contextual source evidence. This does not support using model-only refinement as the evidence repair mechanism.

Deterministic canonicalization:

- Script: `experiments/rulefaith/canonicalize_evidence_spans.py`
- Output: `results/rulefaith/qwen3_v2_smoke10_evidence_canonicalized_candidates.jsonl`
- Audit: `results/rulefaith/qwen3_v2_smoke10_evidence_canonicalization_audit.md`
- Contextual source evidence: 3/10 -> 8/10.
- Missing evidence: 7/10 -> 2/10.
- Prediction-only evidence: 0/10 -> 0/10.
- Wrong-evidence automatic flags: 6/10 -> 0/10.
- Actions: 7 exact index corrections, 1 ambiguous index correction, 1 dropped unlocatable span.

Interpretation: many Qwen3 prompt-v2 evidence failures are span-offset failures. Evidence-span canonicalization should be added before RuleFaith scoring and before deciding which candidates need model refinement.

Validation:

- `python3 -m py_compile experiments/rulefaith/canonicalize_evidence_spans.py experiments/rulefaith/refine_qwen3_evidence.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 23 tests.

Full Qwen3 bucket canonicalization:

- Accepted bucket: contextual source evidence 0/41 -> 15/41; wrong-evidence flags 39/41 -> 5/41.
- Refine bucket: contextual source evidence 10/63 -> 19/63; wrong-evidence flags 52/63 -> 16/63.
- Rejected bucket: contextual source evidence 14/56 -> 48/56; wrong-evidence flags 50/56 -> 8/56.
- Outputs:
  - `data/rulefaith/filtering/qwen3_8b_accepted_canonicalized.jsonl`
  - `data/rulefaith/filtering/qwen3_8b_refine_canonicalized.jsonl`
  - `data/rulefaith/filtering/qwen3_8b_rejected_canonicalized.jsonl`

Strict post-canonicalization audit:

- Command: `python3 experiments/rulefaith/build_qwen3_manual_audit.py --accepted data/rulefaith/filtering/qwen3_8b_accepted_canonicalized.jsonl --refine data/rulefaith/filtering/qwen3_8b_refine_canonicalized.jsonl --rejected data/rulefaith/filtering/qwen3_8b_rejected_canonicalized.jsonl --csv-output results/rulefaith/qwen3_manual_audit_after_canonicalization.csv --summary-output results/rulefaith/qwen3_manual_audit_after_canonicalization_summary.json --cases-output results/rulefaith/qwen3_manual_audit_after_canonicalization_cases.md --blind-form-output annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_form.csv --blind-key-output annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv --guidelines-output annotation/rulefaith_qwen3_audit_canonicalized/guidelines.md --overwrite`
- Candidate count: 160.
- All evidence spans source-index matched: 20/160 -> 155/160.
- Contextual source evidence: 24/160 -> 82/160.
- Missing evidence: 136/160 -> 78/160.
- Prediction-only evidence: 87/160 -> 29/160.
- Wrong-evidence automatic flags: 141/160 -> 29/160.
- Selected manual-audit rows: 80.

Interpretation: the previous Qwen3 prefilter was substantially distorted by span-offset errors. Canonicalized candidates should be re-prefiltered before any 20-edit refinement probe or positive-data construction.

Canonicalized prefilter rerun:

- Merged file: `data/rulefaith/teacher_candidates_qwen3_8b_canonicalized.jsonl`
- Diagnostics: `results/rulefaith/qwen3_8b_canonicalized_diagnostic_metrics.json`
- Filter stats: `results/rulefaith/qwen3_8b_canonicalized_filtering_statistics.json`
- Candidate count: 160.
- Parse JSON rate: 0.9938.
- Alignment proxy pass rate: 0.6375.
- Old diagnostic contextual-evidence rate: 0.3125.
- New prefilter buckets: accepted 34, refine 67, rejected 59.

Interpretation: deterministic canonicalization improves strict evidence-span checks, but the old prefilter is still limited by its rough alignment/contextual-evidence heuristics. Positive selection should not rely on this prefilter alone; use the post-canonicalization strict audit and human blind audit.

## 2026-07-20 Loop D Evidence Refinement Probe20

Objective: test whether targeted Qwen3 evidence refinement can repair the remaining evidence-risk candidates after deterministic evidence-span canonicalization.

Probe construction:

- Script: `experiments/rulefaith/build_evidence_refinement_probe.py`
- Input: `data/rulefaith/teacher_candidates_qwen3_8b_canonicalized.jsonl`
- Output: `data/rulefaith/qwen3_evidence_refinement_probe20.jsonl`
- Eligible evidence-risk candidates: 89 candidates across 49 unique edit groups.
- Selected probe: 20 candidates across 20 unique edit groups.
- Breakdown:
  - dataset: EXPECT 18, JFLEG 2
  - model: CoEdIT 9, T5 6, GECToR 5
  - operation: replace 13, insert 5, delete 2
  - original candidate type: natural 9, rule-grounded 11
  - split: train 15, test 5

Qwen3 targeted refinement:

- Script: `experiments/rulefaith/refine_qwen3_evidence.py`
- Input: `data/rulefaith/qwen3_evidence_refinement_probe20.jsonl`
- Output: `results/rulefaith/qwen3_evidence_refinement_probe20_refined_candidates.jsonl`
- Raw responses: `results/rulefaith/qwen3_evidence_refinement_probe20_raw/`
- Parse status: 20/20 parsed JSON.
- Selected-before contextual source evidence: 7/20.
- Selected-after contextual source evidence: 2/20.
- Selected-before missing evidence: 13/20.
- Selected-after missing evidence: 18/20.
- Selected-before prediction-only evidence: 20/20.
- Selected-after prediction-only evidence: 0/20.
- Selected-before wrong-evidence flags: 20/20.
- Selected-after wrong-evidence flags: 0/20.

Refined-output canonicalization:

- Script: `experiments/rulefaith/canonicalize_evidence_spans.py`
- Output: `results/rulefaith/qwen3_evidence_refinement_probe20_refined_canonicalized_candidates.jsonl`
- Contextual source evidence stayed 2/20 after canonicalization.
- Missing evidence stayed 18/20 after canonicalization.
- No prediction-only or wrong-evidence flags were reintroduced.

Comparison:

- Script: `experiments/rulefaith/compare_evidence_refinement_probe.py`
- Output: `results/rulefaith/qwen3_evidence_refinement_probe20_comparison.json`
- Markdown: `results/rulefaith/qwen3_evidence_refinement_probe20_comparison.md`
- Aligned triples: 20/20.
- Transition counts:
  - contextual 0 -> 0 -> 0 and wrong 1 -> 0 -> 0: 13 cases
  - contextual 1 -> 0 -> 0 and wrong 1 -> 0 -> 0: 5 cases
  - contextual 1 -> 1 -> 1 and wrong 1 -> 0 -> 0: 2 cases

Interpretation: this Qwen3 evidence-only repair prompt mostly clears risky evidence spans instead of adding source-grounded contextual evidence. It removes automatic wrong-evidence flags but worsens the actual evidence-grounding objective.

Decision: reject this evidence-refinement prompt for scaling. Keep deterministic canonicalization as preprocessing, but do not use Qwen3 refined probe outputs as positives. Hand off the canonicalized blind audit package before constructing SFT or preference data.

Validation:

- `python3 -m py_compile experiments/rulefaith/build_evidence_refinement_probe.py experiments/rulefaith/compare_evidence_refinement_probe.py experiments/rulefaith/refine_qwen3_evidence.py experiments/rulefaith/canonicalize_evidence_spans.py` passed.
- `python3 -m unittest experiments.tests.test_evidence_refinement_probe_selection experiments.tests.test_qwen3_evidence_refinement experiments.tests.test_evidence_span_canonicalizer` passed, 9 tests.

## 2026-07-20 Loop E Qwen3 Human Audit Handoff

Objective: prepare a safe blind package for the real-human audit and add tooling to validate and merge the completed audit.

Implemented:

- `experiments/rulefaith/prepare_qwen3_audit_handoff.py`
- `experiments/rulefaith/validate_qwen3_human_audit.py`
- `experiments/tests/test_qwen3_human_audit_tools.py`

Generated:

- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_package/`
- `annotation/rulefaith_qwen3_audit_canonicalized/qwen3_canonicalized_human_audit_package.zip`
- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_manifest.json`
- `annotation/rulefaith_qwen3_audit_canonicalized/handoff_manifest.md`
- `results/rulefaith/qwen3_human_audit_validation_summary.json`
- `results/rulefaith/qwen3_human_audit_validation_report.md`
- `docs/rulefaith_loop_E_qwen3_human_audit_handoff.md`

Verified handoff package:

- Rows in blind form: 80.
- Candidate IDs match hidden key: yes.
- Hidden key columns in blind form: none.
- Human annotation cells filled before handoff: 0.
- Human annotation cells blank before handoff: 960.
- Zip contents: `README_FOR_AUDITOR.md`, `guidelines.md`, `manual_audit_form.csv`.
- Zip SHA256: `5d0cd63b24e9590a306929201206e9ca532d3585f04c4a49afdafacdf3cf46ad`.
- `manual_audit_key.csv` is intentionally excluded from the package.

Validation:

- `python3 -m py_compile experiments/rulefaith/prepare_qwen3_audit_handoff.py experiments/rulefaith/validate_qwen3_human_audit.py` passed.
- `python3 -m unittest experiments.tests.test_qwen3_human_audit_tools` passed, 3 tests.
- `python3 -m unittest discover -s experiments/tests` passed, 27 tests.
- `git diff --check` passed.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.
- Current blank form validation returns `waiting_for_human_completion`.

Decision: all non-human handoff work is complete. Qwen3 positive-data construction is now blocked on the real human audit.

## 2026-07-21 Loop F Codex-Assisted Qwen3 Audit Prelabelling

Objective: fill a separate copy of the canonicalized Qwen3 blind audit form with Codex-assisted prelabels so internal verifier/refiner debugging can continue without overwriting or misrepresenting the real-human audit package.

Important boundary:

- These labels are AI-assisted pseudo-labels generated from automatic diagnostics.
- They are not human labels, not human gold, and must not be reported as human evaluation.
- They must not be used to construct SFT positives or preference positives without real human confirmation.

Implemented:

- `experiments/rulefaith/prefill_qwen3_audit_codex.py`
- `experiments/rulefaith/summarize_qwen3_prelabeled_audit.py`
- `experiments/tests/test_qwen3_codex_prelabelling.py`

Inputs:

- `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_form.csv`
- `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv`
- `results/rulefaith/qwen3_manual_audit_after_canonicalization.csv`

Outputs:

- `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_codex_prelabeled.csv`
- `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_codex_prelabeled_merged_with_key.csv`
- `results/rulefaith/qwen3_codex_prelabeled_audit_summary.json`
- `results/rulefaith/qwen3_codex_prelabeled_audit_report.md`
- `results/rulefaith/qwen3_codex_prelabeled_validation_summary.json`
- `results/rulefaith/qwen3_codex_prelabeled_validation_report.md`
- `results/rulefaith/qwen3_codex_prelabeled_breakdown.json`
- `results/rulefaith/qwen3_codex_prelabeled_breakdown.md`
- `docs/rulefaith_loop_F_codex_audit_prelabelling.md`

Commands:

- `python3 experiments/rulefaith/prefill_qwen3_audit_codex.py --overwrite`
- `python3 experiments/rulefaith/validate_qwen3_human_audit.py --form annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_codex_prelabeled.csv --key annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv --merged-output annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_codex_prelabeled_merged_with_key.csv --summary-output results/rulefaith/qwen3_codex_prelabeled_validation_summary.json --report-output results/rulefaith/qwen3_codex_prelabeled_validation_report.md --overwrite`
- `python3 experiments/rulefaith/summarize_qwen3_prelabeled_audit.py --overwrite`

Verified results:

- Rows filled: 80/80.
- Validation status: `ready_to_merge_completed_audit`.
- Decision counts: 44 `refine`, 36 `reject`, 0 `accept`, 0 `abstain`.
- Main issue counts:
  - `human_edit_copy`: 71
  - `human_missing_evidence`: 60
  - `human_unsupported_confidence`: 79
  - `human_wrong_rule`: 28
  - `human_inapplicable_rule`: 28
  - `human_validity_error`: 28
  - `human_semantic_distortion`: 28
  - `human_wrong_evidence`: 24
  - `human_alignment_error`: 17

Validation:

- `python3 -m py_compile experiments/rulefaith/prefill_qwen3_audit_codex.py experiments/rulefaith/summarize_qwen3_prelabeled_audit.py experiments/rulefaith/validate_qwen3_human_audit.py` passed.
- `python3 -m unittest experiments.tests.test_qwen3_codex_prelabelling experiments.tests.test_qwen3_human_audit_tools` passed, 5 tests.
- `python3 -m unittest discover -s experiments/tests` passed, 29 tests.
- `git diff --check` passed.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.
- Secret-pattern scan produced only a false positive on the text `risk-coverage`; no actual API key/token assignment was found.

Interpretation: the prelabelled audit copy reinforces that the canonicalized Qwen3 pool is useful as a repair/risk source, not a positive training source. The next verifier/refiner loop should focus on missing contextual evidence, edit-copy penalties, unsupported confidence, and false rationalization.

Decision: keep the real-human audit gate open. Use Codex prelabels only for internal triage and prompt/verifier debugging.

## 2026-07-21 Loop G Complete Qwen3 Codex Audit Forms

Objective: fill all current Qwen3 audit packages with explicit Codex-completed forms, without overwriting the original blank blind forms or misrepresenting AI labels as human labels.

Generated:

- `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed_by_codex.csv`
- `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed_by_codex_merged_with_key.csv`
- `annotation/rulefaith_qwen3_audit/manual_audit_codex_prelabeled.csv`
- `annotation/rulefaith_qwen3_audit/manual_audit_codex_prelabeled_merged_with_key.csv`
- `annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex.csv`
- `annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex_merged_with_key.csv`
- `annotation/qwen3_codex_annotation_data_card.md`
- `results/rulefaith/qwen3_precano_codex_prelabeled_audit_summary.json`
- `results/rulefaith/qwen3_precano_codex_prelabeled_audit_report.md`
- `results/rulefaith/qwen3_precano_codex_prelabeled_validation_summary.json`
- `results/rulefaith/qwen3_precano_codex_prelabeled_validation_report.md`
- `results/rulefaith/qwen3_precano_codex_prelabeled_breakdown.json`
- `results/rulefaith/qwen3_precano_codex_prelabeled_breakdown.md`
- `results/rulefaith/qwen3_canonicalized_codex_completed_validation_summary.json`
- `results/rulefaith/qwen3_canonicalized_codex_completed_validation_report.md`
- `results/rulefaith/qwen3_precano_codex_completed_validation_summary.json`
- `results/rulefaith/qwen3_precano_codex_completed_validation_report.md`

Commands:

- `python3 experiments/rulefaith/prefill_qwen3_audit_codex.py --form annotation/rulefaith_qwen3_audit/manual_audit_form.csv --diagnostics results/rulefaith/qwen3_manual_audit.csv --output annotation/rulefaith_qwen3_audit/manual_audit_codex_prelabeled.csv --summary-output results/rulefaith/qwen3_precano_codex_prelabeled_audit_summary.json --report-output results/rulefaith/qwen3_precano_codex_prelabeled_audit_report.md --overwrite`
- `python3 experiments/rulefaith/validate_qwen3_human_audit.py --form annotation/rulefaith_qwen3_audit/manual_audit_codex_prelabeled.csv --key annotation/rulefaith_qwen3_audit/manual_audit_key.csv --merged-output annotation/rulefaith_qwen3_audit/manual_audit_codex_prelabeled_merged_with_key.csv --summary-output results/rulefaith/qwen3_precano_codex_prelabeled_validation_summary.json --report-output results/rulefaith/qwen3_precano_codex_prelabeled_validation_report.md --overwrite`
- `python3 experiments/rulefaith/summarize_qwen3_prelabeled_audit.py --merged annotation/rulefaith_qwen3_audit/manual_audit_codex_prelabeled_merged_with_key.csv --json-output results/rulefaith/qwen3_precano_codex_prelabeled_breakdown.json --md-output results/rulefaith/qwen3_precano_codex_prelabeled_breakdown.md --overwrite`

Verified results:

- Canonicalized audit: 80/80 rows complete, validation status `ready_to_merge_completed_audit`, decisions 44 `refine`, 36 `reject`.
- Pre-canonicalization audit: 80/80 rows complete, validation status `ready_to_merge_completed_audit`, decisions 46 `refine`, 34 `reject`.
- No direct accepts in either Codex-completed audit package.

Validation:

- `python3 -m py_compile experiments/rulefaith/prefill_qwen3_audit_codex.py experiments/rulefaith/summarize_qwen3_prelabeled_audit.py experiments/rulefaith/validate_qwen3_human_audit.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 29 tests.
- `git diff --check` passed.
- Both Codex-completed audit CSVs have 80 rows and 0 blank `human_*` cells.
- Secret-pattern scan over `annotation`, `docs`, `results`, and `experiments` produced no matches.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

Round10 boundary:

- `annotation/round10/annotation_form.csv` and `annotation/round10/adjudication_template.csv` remain blank historical templates.
- Usable stress-test labels are already finalized under `annotation/round15/`.
- These templates were not overwritten with Codex labels.

Decision: current Qwen3 audit blanks are filled by Codex-completed counterparts. Use them for internal triage only; do not use them as human evidence.

## 2026-07-21 Loop H Structured Evidence Repair

Objective: convert the Codex audit failure mode around missing/wrong evidence into an executable deterministic repair pass and test it on the full canonicalized Qwen3 pool.

Implemented:

- `experiments/rulefaith/repair_qwen3_structured_evidence.py`
- `experiments/tests/test_qwen3_structured_evidence_repair.py`

Outputs:

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
- `docs/rulefaith_loop_H_structured_evidence_repair.md`

Commands:

- `python3 experiments/rulefaith/repair_qwen3_structured_evidence.py --overwrite`
- `python3 experiments/rulefaith/diagnose_teacher_candidates.py --input results/rulefaith/qwen3_structured_evidence_repaired_candidates.jsonl --json-output results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_metrics.json --md-output results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_report.md`
- `python3 experiments/rulefaith/filter_teacher_candidates.py --candidates results/rulefaith/qwen3_structured_evidence_repaired_candidates.jsonl --diagnostics results/rulefaith/qwen3_structured_evidence_repaired_diagnostic_metrics.json --output-dir data/rulefaith/filtering --stats results/rulefaith/qwen3_structured_evidence_repaired_filtering_statistics.json --prefix qwen3_structured_evidence_repaired`

Verified results:

- Candidate count: 160.
- Automatic contextual evidence: 82/160 -> 160/160.
- Missing evidence: 78/160 -> 0/160.
- Prediction-only evidence: 29/160 -> 0/160.
- Wrong-evidence automatic flag: 29/160 -> 0/160.
- Unsupported confidence: 131/160 -> 70/160.
- Specific source evidence: 10/160 -> 124/160.
- Generic-context-only after repair: 36/160.
- Alignment errors unchanged: 58/160.
- Edit-copy risk unchanged: 112/160.
- Possible false rationalization unchanged: 19/160.
- Edit-validity risk unchanged: 28/160.

Selection results:

- Old conservative prefilter after repair: 101 accepted, 0 refine, 59 rejected.
- Strict RuleFaith gate after repair: 0 accepted, 58 refine, 102 rejected.

Interpretation:

Structured source-evidence repair is useful as a preprocessing/refiner-input step and should replace model-only evidence repair for this failure mode. It should not be used as final selection, because source evidence coverage alone hides alignment, leakage, and false-rationalization risks.

Validation:

- `python3 -m py_compile experiments/rulefaith/repair_qwen3_structured_evidence.py` passed.
- `python3 -m unittest experiments.tests.test_qwen3_structured_evidence_repair` passed, 6 tests.
- `python3 -m unittest discover -s experiments/tests` passed, 35 tests.
- `git diff --check` passed.
- Output integrity check passed: 160 repaired candidates, 58 strict refine candidates, 102 strict rejected candidates.
- Secret-pattern scan over `annotation`, `docs`, `results`, `experiments`, and `data` produced no matches.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

Decision: keep structured evidence repair, keep strict RuleFaith selection, and use the 58 strict `refine` candidates for the next alignment/leakage-aware loop.

## 2026-07-21 Loop I Field-Aware RuleFaith Selection

Objective: fix an over-strict leakage policy that treated required structured `edit_description` text as the same kind of leakage as rule/rationale answer copying.

Implemented:

- `experiments/rulefaith/select_qwen3_field_aware_rulefaith.py`
- `experiments/tests/test_qwen3_field_aware_selection.py`

Outputs:

- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_refine.jsonl`
- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_rejected.jsonl`
- `results/rulefaith/qwen3_field_aware_rulefaith_selection_stats.json`
- `results/rulefaith/qwen3_field_aware_rulefaith_selection_report.md`
- `results/rulefaith/qwen3_field_aware_rulefaith_selection.csv`
- `docs/rulefaith_loop_I_field_aware_selection.md`

Commands:

- `python3 -m py_compile experiments/rulefaith/select_qwen3_field_aware_rulefaith.py`
- `python3 -m unittest experiments.tests.test_qwen3_field_aware_selection`
- `python3 experiments/rulefaith/select_qwen3_field_aware_rulefaith.py --overwrite`

Verified results:

- Candidate count: 160.
- Previous strict buckets: 0 accepted, 58 refine, 102 rejected.
- Field-aware buckets: 45 accepted, 13 refine, 102 rejected.
- Output integrity: 45 accepted JSONL rows, 13 refine JSONL rows, 102 rejected JSONL rows, and 160 CSV data rows.
- Field leakage counts: `edit_description_edit_copy` 108, `edit_description_target_copy` 100, `rationale_edit_copy` 26, `rationale_target_copy` 86, `rule_text_target_copy` 40.
- Active refine reasons: `rationale_edit_copy` 13 and `generic_explanation` 1.
- Hard failure reasons remain: `alignment_error` 58, `validity_error_auto` 28, `possible_false_rationalization` 19, `no_specific_source_evidence` 36, `missing_rule` 1, and `parse_not_json` 1.

Validation:

- `python3 -m py_compile experiments/rulefaith/select_qwen3_field_aware_rulefaith.py experiments/rulefaith/repair_qwen3_structured_evidence.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 38 tests.
- `git diff --check` passed.
- Output integrity check passed for all three JSONL buckets and the 160-row CSV.
- Secret-pattern scan over `annotation`, `docs`, `results`, `experiments`, and `data` produced no matches.
- `python3 -m pytest -q` could not run because `pytest` is not installed in the current shell.

Interpretation:

Field-aware selection recovers a useful target-masked validation pool from the repaired Qwen3 candidates without relaxing hard failures. The result should not be treated as positive SFT/preference data, because it is automatic and rule correctness remains unverified.

Decision: use the 45 accepted and 13 refine candidates for target-masked validation. Keep all pseudo-label and human-evidence boundaries explicit.

## 2026-07-21 Loop J Target-Masked RuleFaith Validation

Objective: validate the field-aware Qwen3 candidate pool under a target-masked condition so rule/rationale quality is not rewarded merely for copying the target edit string.

Implemented:

- `experiments/rulefaith/validate_qwen3_target_masked.py`
- `experiments/tests/test_qwen3_target_masked_validation.py`

Dependency fix:

- Installed `pytest` with `python3 -m pip install --user pytest`.

Inputs:

- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_accepted.jsonl`
- `data/rulefaith/filtering/qwen3_field_aware_rulefaith_refine.jsonl`

Outputs:

- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_validated.jsonl`
- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_refine.jsonl`
- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_rejected.jsonl`
- `results/rulefaith/qwen3_target_masked_validation_stats.json`
- `results/rulefaith/qwen3_target_masked_validation_report.md`
- `results/rulefaith/qwen3_target_masked_validation.csv`
- `docs/rulefaith_loop_J_target_masked_validation.md`

Commands:

- `python3 -m pip install --user pytest`
- `python3 -m py_compile experiments/rulefaith/validate_qwen3_target_masked.py`
- `python3 -m unittest experiments.tests.test_qwen3_target_masked_validation`
- `python3 experiments/rulefaith/validate_qwen3_target_masked.py --overwrite`

Verified results:

- Input candidates: 58.
- Field-aware input buckets: 45 accepted, 13 refine.
- Target-masked buckets: 47 validated, 8 refine, 3 rejected.
- Previous accepted bucket: 39 validated, 5 refine, 1 rejected.
- Previous refine bucket: 8 validated, 3 refine, 2 rejected.
- Score mean/min/max: 0.8543 / 0.0 / 1.0.
- Failure counts: 7 target-dependent quality texts, 2 masked grammar-signal failures, 1 generic-after-mask case, and 6 rule-category mismatches.
- Warning counts: 13 rationale edit-copy cases and 21 cases where specific evidence is not mentioned in rule/rationale.

Interpretation:

Target-masked validation is a useful second automatic gate. It catches target-copy dependence and obvious category shortcuts missed by field-aware selection. It does not certify human rule correctness, so the 47 validated candidates should be used as an audit pool rather than training positives.

Decision: run a rule-plausibility and evidence-sufficiency audit over the 47 target-masked validated candidates before constructing SFT or preference data.

## 2026-07-21 Loop K Rule Plausibility and Evidence Sufficiency Audit

Objective: audit the 47 target-masked validated Qwen3 candidates for rule plausibility and evidence sufficiency before any positive-data construction.

Implemented:

- `experiments/rulefaith/audit_qwen3_rule_plausibility.py`
- `experiments/tests/test_qwen3_rule_plausibility_audit.py`

Inputs:

- `data/rulefaith/filtering/qwen3_target_masked_rulefaith_validated.jsonl`

Outputs:

- `data/rulefaith/filtering/qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl`
- `data/rulefaith/filtering/qwen3_rule_plausibility_needs_refinement.jsonl`
- `data/rulefaith/filtering/qwen3_rule_plausibility_reject.jsonl`
- `results/rulefaith/qwen3_rule_plausibility_audit_stats.json`
- `results/rulefaith/qwen3_rule_plausibility_audit_report.md`
- `results/rulefaith/qwen3_rule_plausibility_audit.csv`
- `docs/rulefaith_loop_K_rule_plausibility_audit.md`

Commands:

- `python3 -m py_compile experiments/rulefaith/audit_qwen3_rule_plausibility.py`
- `python3 -m unittest experiments.tests.test_qwen3_rule_plausibility_audit`
- `python3 experiments/rulefaith/audit_qwen3_rule_plausibility.py --overwrite`

Verified results:

- Input candidates: 47.
- Ready for human/stronger validation: 25.
- Needs refinement: 16.
- Rejected: 6.
- Evidence sufficiency: 41 sufficient, 6 insufficient.
- Rule plausibility: 47 plausible under current deterministic checks.
- Output integrity: 25 ready JSONL rows, 16 refinement JSONL rows, 6 rejected JSONL rows, and 47 CSV data rows.
- Main reasons: evidence not mentioned in rule/rationale (14), rationale edit-copy (8), unsupported high confidence (6), missing required specific source evidence (5), and missing noun-number context (1).

Interpretation:

The staged automatic RuleFaith funnel now narrows Qwen3 candidates from 160 repaired outputs to 25 ready-for-spotcheck candidates. The largest remaining automatic failure is evidence integration, not JSON format or target leakage.

Decision: build a blind validation package for the 25 ready candidates and targeted repair inputs for the 16 refinement candidates. Keep all labels marked as automatic until real human or stronger validation is complete.

## 2026-07-21 Loop L Ready-Candidate Blind Validation Package

Objective: package the 25 ready Qwen3 candidates for blind validation and prepare targeted repair input for the 16 needs-refinement candidates.

Implemented:

- `experiments/rulefaith/prepare_qwen3_validation_package.py`
- `experiments/tests/test_qwen3_validation_package.py`

Inputs:

- `data/rulefaith/filtering/qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl`
- `data/rulefaith/filtering/qwen3_rule_plausibility_needs_refinement.jsonl`

Outputs:

- `annotation/rulefaith_qwen3_ready_validation/guidelines.md`
- `annotation/rulefaith_qwen3_ready_validation/README.md`
- `annotation/rulefaith_qwen3_ready_validation/ready_validation_form.csv`
- `annotation/rulefaith_qwen3_ready_validation/ready_validation_key.csv`
- `annotation/rulefaith_qwen3_ready_validation/repair_instructions.csv`
- `annotation/rulefaith_qwen3_ready_validation/handoff_manifest.json`
- `annotation/rulefaith_qwen3_ready_validation/handoff_manifest.md`
- `annotation/rulefaith_qwen3_ready_validation/rulefaith_qwen3_ready_validation_package.zip`
- `results/rulefaith/qwen3_ready_validation_package_summary.json`
- `results/rulefaith/qwen3_ready_validation_package_report.md`
- `docs/rulefaith_loop_L_ready_validation_package.md`

Commands:

- `python3 -m py_compile experiments/rulefaith/prepare_qwen3_validation_package.py`
- `python3 -m unittest experiments.tests.test_qwen3_validation_package`
- `python3 experiments/rulefaith/prepare_qwen3_validation_package.py --overwrite`

Verified results:

- Blind validation form rows: 25.
- Hidden key rows: 25.
- Repair instruction rows: 16.
- Blind form excludes `candidate_id`, `model_key`, `model_family`, `dataset`, `automatic_decision`, and `automatic_reasons`.
- Zip SHA256: `4907c29a702a367d90afcde68b41756f2f9109ef3175e2bc361ef1080052e5ca`.

Interpretation:

The local Qwen3 teacher pool now has a reproducible validation handoff. The package supports a future human or stronger-model validation step, but it does not itself provide human evidence.

Decision: run targeted repair on the 16 needs-refinement candidates using the generated repair instructions, then re-run target-masked and rule/evidence gates.

## 2026-07-21 Loop M Targeted Repair and Validation Package V2

Objective: repair the 16 needs-refinement Qwen3 candidates, re-run automatic gates, and regenerate a larger blind validation package.

Implemented:

- `experiments/rulefaith/repair_qwen3_needs_refinement.py`
- `experiments/tests/test_qwen3_targeted_repair.py`
- Extended `experiments/rulefaith/prepare_qwen3_validation_package.py` to support multiple ready inputs and empty refine inputs.
- Extended `experiments/tests/test_qwen3_validation_package.py`.

Commands:

- `python3 -m py_compile experiments/rulefaith/repair_qwen3_needs_refinement.py`
- `python3 -m unittest experiments.tests.test_qwen3_targeted_repair`
- `python3 experiments/rulefaith/repair_qwen3_needs_refinement.py --overwrite`
- `python3 experiments/rulefaith/validate_qwen3_target_masked.py --inputs results/rulefaith/qwen3_targeted_repaired_candidates.jsonl --prefix qwen3_targeted_repaired_target_masked --stats-output results/rulefaith/qwen3_targeted_repaired_target_masked_stats.json --report-output results/rulefaith/qwen3_targeted_repaired_target_masked_report.md --csv-output results/rulefaith/qwen3_targeted_repaired_target_masked.csv --overwrite`
- `python3 experiments/rulefaith/audit_qwen3_rule_plausibility.py --input data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_validated.jsonl --prefix qwen3_targeted_repaired_rule_plausibility --stats-output results/rulefaith/qwen3_targeted_repaired_rule_plausibility_stats.json --report-output results/rulefaith/qwen3_targeted_repaired_rule_plausibility_report.md --csv-output results/rulefaith/qwen3_targeted_repaired_rule_plausibility.csv --overwrite`
- `python3 experiments/rulefaith/prepare_qwen3_validation_package.py --ready data/rulefaith/filtering/qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_ready_for_human_spotcheck.jsonl --refine data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_needs_refinement.jsonl --output-dir annotation/rulefaith_qwen3_ready_validation_v2 --summary-output results/rulefaith/qwen3_ready_validation_package_v2_summary.json --report-output results/rulefaith/qwen3_ready_validation_package_v2_report.md --overwrite`

Outputs:

- `results/rulefaith/qwen3_targeted_repaired_candidates.jsonl`
- `results/rulefaith/qwen3_targeted_repair_stats.json`
- `results/rulefaith/qwen3_targeted_repair_report.md`
- `results/rulefaith/qwen3_targeted_repair_before_after.csv`
- `data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_validated.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_refine.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_target_masked_rejected.jsonl`
- `results/rulefaith/qwen3_targeted_repaired_target_masked_stats.json`
- `results/rulefaith/qwen3_targeted_repaired_target_masked_report.md`
- `results/rulefaith/qwen3_targeted_repaired_target_masked.csv`
- `data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_ready_for_human_spotcheck.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_needs_refinement.jsonl`
- `data/rulefaith/filtering/qwen3_targeted_repaired_rule_plausibility_reject.jsonl`
- `results/rulefaith/qwen3_targeted_repaired_rule_plausibility_stats.json`
- `results/rulefaith/qwen3_targeted_repaired_rule_plausibility_report.md`
- `results/rulefaith/qwen3_targeted_repaired_rule_plausibility.csv`
- `annotation/rulefaith_qwen3_ready_validation_v2/`
- `results/rulefaith/qwen3_ready_validation_package_v2_summary.json`
- `results/rulefaith/qwen3_ready_validation_package_v2_report.md`
- `docs/rulefaith_loop_M_targeted_repair_and_validation_v2.md`

Verified results:

- Targeted repair candidates: 16.
- Rationale edit-copy before/after: 8 -> 0.
- Evidence mentioned in rule/rationale before/after: 8 -> 16.
- Repair actions: 8 evidence appends, 8 rationale replacements, 14 confidence caps.
- Target-masked revalidation: 16/16 validated.
- Rule/evidence re-audit: 16/16 ready-for-human-spotcheck.
- V2 blind validation package: 41 blind rows, 41 hidden key rows, 0 repair rows.
- V2 zip SHA256: `31ce8d7735d57107b9271dd1202ba0cde4d1c0acbed489ec11c8e3d18938799d`.

Interpretation:

Targeted repair fixes the structural failure modes it was designed for, but it may also optimize to deterministic gate heuristics. The repaired candidates should enter blind validation, not training data.

Decision: use the v2 package as the current validation package. The next loop should either fill it as explicitly marked Codex/AI pseudo-validation or hand it to real validators.

Validation after Loop M:

- `python3 -m py_compile experiments/rulefaith/validate_qwen3_target_masked.py experiments/rulefaith/audit_qwen3_rule_plausibility.py experiments/rulefaith/prepare_qwen3_validation_package.py experiments/rulefaith/repair_qwen3_needs_refinement.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 51 tests.
- `python3 -m pytest -q` passed, 51 tests.
- `git diff --check` passed.
- Output integrity check passed for targeted-repair outputs, target-masked revalidation buckets, rule-plausibility re-audit buckets, and v2 blind package counts.
- Secret-pattern scan over `annotation`, `docs`, `results`, `experiments`, and `data` produced no matches.

Validation after Loops J--L:

- `python3 -m py_compile experiments/rulefaith/validate_qwen3_target_masked.py experiments/rulefaith/audit_qwen3_rule_plausibility.py experiments/rulefaith/prepare_qwen3_validation_package.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 47 tests.
- `python3 -m pytest -q` passed, 47 tests.
- `git diff --check` passed.
- Output integrity check passed for target-masked buckets, rule-plausibility buckets, blind form, hidden key, and repair instructions.
- Secret-pattern scan over `annotation`, `docs`, `results`, `experiments`, and `data` produced no matches.

## 2026-07-21 Loop N Codex Ready-Candidate Pseudo-Validation

Objective: fill the 41-row Qwen3 v2 ready validation package with explicitly marked Codex/AI pseudo-validation labels so the internal RuleFaith loop can continue without claiming human evidence.

Implemented:

- `experiments/rulefaith/complete_qwen3_ready_validation_codex.py`
- `experiments/tests/test_qwen3_ready_validation_codex.py`

Command:

- `python3 experiments/rulefaith/complete_qwen3_ready_validation_codex.py --overwrite`

Outputs:

- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_completed_by_codex.csv`
- `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_completed_by_codex_merged_with_key.csv`
- `results/rulefaith/qwen3_ready_validation_codex_summary.json`
- `results/rulefaith/qwen3_ready_validation_codex_cases.md`
- `docs/rulefaith_loop_N_codex_ready_validation.md`

Verified results:

- Candidate count: 41.
- Overall decisions: 17 `accept`, 13 `refine`, 11 `reject`.
- Edit alignment: 38 `pass`, 3 `partial`.
- Edit validity: 27 `valid`, 4 `acceptable_alternative`, 4 `stylistic`, 6 `invalid`.
- Rule plausibility: 22 `plausible`, 9 `weak`, 10 `implausible`.
- Evidence sufficiency: 22 `sufficient`, 18 `partial`, 1 `insufficient`.

Interpretation:

The pseudo-validation shows that automatic target-masked and rule/evidence gates are useful but still over-admit linguistically weak candidates. The 17 accepts can seed a small internal smoke test, while the 13 refine and 11 reject rows should drive the next repair and verifier-hardening loop.

Validation after Loop N:

- Installed user-local TinyTeX under `/Users/bytedance/Library/TinyTeX` after no system `pdflatex`, `latexmk`, or `tectonic` pdfTeX-compatible path was available.
- Installed LaTeX dependencies with `tlmgr`: `newtx`, `xpatch`, `xstring`, `mweights`, `carlisle`, `fontaxes`, `placeins`, `caption`, `algorithms`, `tex-gyre`, and `courier`.
- `python3 -m py_compile experiments/rulefaith/complete_qwen3_ready_validation_codex.py experiments/rulefaith/generate_rulefaith_paper_assets.py` passed.
- `python3 -m unittest discover -s experiments/tests` passed, 54 tests.
- `python3 -m pytest -q` passed, 54 tests.
- `git diff --check` passed.
- `pdflatex -interaction=nonstopmode main.tex` passed twice under TinyTeX and generated `paper/main.pdf` with 8 pages.

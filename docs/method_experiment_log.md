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

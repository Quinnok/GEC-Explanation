# RuleFaith-GEC Method Loop State

Last updated: 2026-07-21

## Current Branch

`main`

## Frozen Baseline

Stress-test paper frozen at commit `4519543060cbaff49806fd9963412f4ca4ab83c0`.

## Current Round

Loop P deployable selector diagnostic: verifier calibration conditionally passed on the Round 15 human-adjudicated pressure-test set. FLAN-T5 and Qwen2.5 open-teacher pilots were too weak for positive distillation data, while the Qwen3-8B no-thinking pilot produced the first non-trivial local open-teacher candidate pool. The Qwen3 pool now has Codex-completed audit forms, deterministic structured evidence repair, field-aware selection, target-masked validation, targeted repair, a 41-candidate blind validation handoff package, an explicitly marked Codex/AI pseudo-validation copy, generated same-setting baseline/selection tables, and a fixed deployable ready-pool scorer that is useful diagnostically but not yet strong enough as the final selector.

## Highest-Priority Problem

Move from human-grounded metric stress testing to a method that produces and selectively abstains from edit-level GEC explanations.

## Current Known Blockers

- `OPENAI_API_KEY` is not visible in the current environment, so GPT-5.5 teacher generation cannot run yet.
- `openai` Python SDK is not visible in the current environment; installation attempts were interrupted by very slow package download, so the GPT branch remains optional-import guarded.
- Qwen3-8B accepted 41/160 candidates under the conservative RuleFaith prefilter. Loop B found no generator input leakage and 160/160 source-span matches, but only 20/160 candidates had all evidence spans source-index matched, 24/160 had contextual source evidence, and 87/160 included prediction-only evidence. Loop C smoke10 canonicalization improved contextual evidence from 3/10 to 8/10, but model-only refinement did not add contextual evidence. Full-pool canonicalization improved contextual source evidence from 24/160 to 82/160 and wrong-evidence flags from 141/160 to 29/160. Loop D 20-edit targeted Qwen3 refinement parsed 20/20 outputs but worsened contextual source evidence from 7/20 to 2/20, confirming that this refiner mostly removes evidence rather than grounding it.
- Codex-completed audit forms cover both Qwen3 blind audit packages and validate cleanly, but they are pseudo-labels and cannot satisfy the real-human audit gate.
- Structured evidence repair fixes automatic source-evidence coverage but leaves alignment, edit-copy, false-rationalization, and validity risks.
- Field-aware selection separates required `edit_description` copy from leakage, but the 45 accepted candidates are not SFT positives and still need target-masked and human/stronger validation.
- Target-masked validation reduces target-copy and rule-category shortcuts, but the 47 validated candidates are not SFT positives and still need rule plausibility plus human/stronger validation.
- Rule/evidence audit reduces the target-masked validated pool to 25 ready-for-spotcheck candidates, but they remain automatic candidates until human or stronger validation.
- The ready validation package hides model/system identity and automatic decisions. Loop N filled a separate Codex/AI pseudo-validation copy, but this is not human validation.
- Validation package v2 contains 41 candidates after adding 16 successfully repaired candidates; no v2 repair rows remain. Codex pseudo-validation marks 17 accept, 13 refine, and 11 reject.
- Student model training may require GPU/model downloads and later user confirmation if a model exceeds 10GB.
- New natural explanation human evaluation will require real annotators later.

## Latest Completed Work

- Round 16 method branch and preregistration.
- Round 17 substantive edit pool: 300 selected edits, source-level train/dev/test split, model-family coverage, dataset coverage, and leakage audits.
- Round 18 teacher-generation scaffolding and open-teacher pilot: 160 FLAN-T5-base candidates for 80 edits, with quality audit showing a 61.25% low-quality rate; GPT-5.5 branch blocked by missing `OPENAI_API_KEY`.
- Round 19 verifier calibration: Rule/Evidence verifier conditionally passes Gate A on stress-test labels, with rule/evidence AUROC above reverse reconstruction.
- Qwen small teacher addendum: implemented `qwen_small` provider, config, raw-response logging, parse-failure logging, and parallel shard runner.
- Round 20 open-teacher prefilter: Qwen2.5-0.5B generated 160 candidates; parse JSON rate 0.975, alignment proxy pass 0.769, rule edit-copy rate 0.887, contextual evidence rate 0.037, accepted 1/160. FLAN-T5 accepted 0/160. Qwen2.5-1.5B non-punctuation probe accepted 0/20 because all candidates lacked explicit rule text. Qwen3-8B generated 160 candidates with thinking disabled; parse JSON rate 0.994, rule edit-copy rate 0.006, contextual evidence rate 0.388, and conservative prefilter accepted 41/160 with 63 candidates marked for refinement.
- Loop A Qwen3 audit: `results/rulefaith/qwen3_manual_audit.csv` contains all 160 candidates and selects 80 for stratified manual audit. Automatic checks found 0 input leakage, 160/160 source span matches, 48/160 evidence index matches, 51/160 contextual-evidence candidates, 109/160 missing contextual evidence, 19 possible false rationalizations, and 28 validity-error risks.
- Loop B evidence gate repair: prompt v2 now requires source-only evidence spans with exact whitespace-token offsets; stricter audit finds all-spans source index match 20/160, contextual source evidence 24/160, prediction-only evidence 87/160, and wrong-evidence flags 141/160. Blind human-audit files are under `annotation/rulefaith_qwen3_audit/`.
- Qwen3 prompt-v2 smoke tests: the 1-candidate smoke and 10-candidate smoke both parsed successfully. Smoke10 has 0/10 prediction-only evidence, but only 3/10 contextual source-evidence candidates and 6/10 wrong-evidence flags.
- Loop C targeted evidence refinement: compact Qwen3 evidence-only repair parsed 7/7 selected smoke outputs but improved contextual evidence 0/7 -> 0/7, mostly clearing evidence spans. Deterministic evidence-span canonicalization on smoke10 improved contextual source evidence 3/10 -> 8/10 and wrong-evidence flags 6/10 -> 0/10 without prediction-only regression. Full-pool post-canonicalization strict audit improved all-spans source-index match 20/160 -> 155/160, contextual source evidence 24/160 -> 82/160, and wrong-evidence flags 141/160 -> 29/160. Canonicalized prefilter buckets are accepted 34, refine 67, rejected 59.
- Loop D evidence refinement probe20: selected 20 evidence-risk candidates across 20 unique edits from the canonicalized pool and ran Qwen3 targeted repair. Outputs parsed 20/20, but contextual evidence fell 7/20 -> 2/20 and missing evidence rose 13/20 -> 18/20. Refined-output canonicalization did not recover contextual evidence.
- Loop E Qwen3 human-audit handoff: packaged `qwen3_canonicalized_human_audit_package.zip` with only README, guidelines, and blind form; excluded `manual_audit_key.csv`; added validation/merge tooling for the completed human audit.
- Loop F Codex-assisted audit prelabelling: generated `manual_audit_codex_prelabeled.csv`, merged it with the hidden key, and summarized 44 `refine` and 36 `reject` decisions for internal triage only.
- Loop G Qwen3 Codex audit completion: generated explicit `manual_audit_completed_by_codex.csv` files for both canonicalized and pre-canonicalization Qwen3 packages. The pre-canonicalization package has 46 `refine` and 34 `reject`; the canonicalized package has 44 `refine` and 36 `reject`.
- Loop H structured evidence repair: automatic contextual evidence 82/160 -> 160/160, specific source evidence 10/160 -> 124/160, prediction-only evidence 29/160 -> 0/160, wrong-evidence flags 29/160 -> 0/160. Strict RuleFaith buckets are 0 accepted, 58 refine, 102 rejected.
- Loop I field-aware RuleFaith selection: previous strict buckets were 0 accepted, 58 refine, 102 rejected. After excluding schema-required `edit_description` copy from leakage failure while retaining hard alignment/validity/rule/evidence gates, buckets are 45 accepted, 13 refine, 102 rejected.
- Loop J target-masked validation: over the 45 field-aware accepted and 13 field-aware refine candidates, target-masked buckets are 47 validated, 8 refine, and 3 rejected. The validator flags 7 target-dependent explanations, 2 grammar-signal failures, 1 generic-after-mask case, and 6 rule-category mismatches.
- Loop K rule/evidence audit: over 47 target-masked validated candidates, decisions are 25 ready-for-human-spotcheck, 16 needs-refinement, and 6 reject. The main reasons are evidence not mentioned in rule/rationale (14), rationale edit-copy (8), unsupported high confidence (6), and missing required evidence (6).
- Loop L ready validation package: 25 blind validation rows, 25 hidden key rows, 16 repair-instruction rows, and zip SHA256 `4907c29a702a367d90afcde68b41756f2f9109ef3175e2bc361ef1080052e5ca`.
- Loop M targeted repair and package v2: repaired 16/16 refinement candidates; rationale edit-copy 8 -> 0; evidence mentioned 8 -> 16; 16/16 pass target-masked and rule/evidence re-audit; validation package v2 has 41 blind rows and zip SHA256 `31ce8d7735d57107b9271dd1202ba0cde4d1c0acbed489ec11c8e3d18938799d`.
- Loop N Codex ready-candidate pseudo-validation: filled `ready_validation_completed_by_codex.csv` for all 41 v2 candidates. Decisions are 17 `accept`, 13 `refine`, and 11 `reject`; rule plausibility labels are 22 `plausible`, 9 `weak`, and 10 `implausible`; evidence sufficiency labels are 22 `sufficient`, 18 `partial`, and 1 `insufficient`.
- Loop O baseline result fill-in: generated `results/rulefaith/rulefaith_teacher_baselines.csv`, `results/rulefaith/rulefaith_method_gate_funnel.csv`, `results/rulefaith/rulefaith_selection_baselines.csv`, and paper tables under `results/paper_assets/`. Same-setting teacher baselines show FLAN-T5-base accepted 0/160, Qwen2.5-0.5B accepted 1/160, Qwen2.5-1.5B probe accepted 0/20, and Qwen3-8B accepted 41/160. On the 41-row pseudo-validation pool, rule-grounded candidate selection is the best simple non-oracle selector with 0.435 accept rate and 0.739 non-reject rate, while a pseudo-validator selective upper-bound covers 11/23 edit groups.
- Loop P deployable ready-pool selector: added `experiments/rulefaith/score_rulefaith_ready_candidates.py`, which scores candidates without reading `validator_*` labels. Against Codex/AI pseudo-validation for diagnostics, top-1 accept rate is 0.391 and non-reject rate is 0.739; selective mode covers 18/23 edit groups with accept rate 0.389 and non-reject rate 0.778. This partially beats first/highest-confidence selectors but does not beat the rule-grounded simple selector.

## Next Internal Action

Use the 17 Codex-pseudo-accepted candidates as provisional seeds for a small internal RuleFaith smoke test only. Prepare a real-human natural explanation validation package before any paper-quality method claim or final SFT/preference construction. Do not tune the Loop P deployable scorer thresholds on pseudo-validation labels.

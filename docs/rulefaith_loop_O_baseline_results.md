# RuleFaith Loop O: Baseline Result Fill-In

## Status

- Loop ID: O
- Current bottleneck: paper method section had Qwen3 pilot results but lacked a compact baseline comparison and candidate-selection ablation.
- Hypothesis: under the same 80-edit teacher setting, Qwen3-8B is a stronger local teacher than FLAN-T5 and Qwen2.5, but simple candidate-selection rules remain weak under pseudo-validation.
- Required evidence: same-setting teacher diagnostic files, frozen RuleFaith gate statistics, and the 41-row Codex/AI pseudo-validation package.
- Success criterion: generated tables are fully derived from repository result files and do not claim human validation for pseudo labels.
- Failure criterion: missing result provenance, unlabeled pseudo-validation boundaries, or table numbers not matching JSON/CSV sources.

## Teacher Baselines

| system | n | parse_json_rate | alignment_proxy_pass_rate | missing_rule_text_rate | rule_edit_copy_rate | contextual_evidence_rate | high_risk_rate | accepted | refine | rejected | accepted_rate | non_rejected_rate | label_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FLAN-T5-base direct | 160 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0 | 0 | 160 | 0.000 | 0.000 | automatic_prefilter |
| Qwen2.5-0.5B direct | 160 | 0.975 | 0.769 | 0.025 | 0.887 | 0.037 | 0.994 | 1 | 15 | 144 | 0.006 | 0.100 | automatic_prefilter |
| Qwen2.5-1.5B probe | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 0.350 | 1.000 | 0 | 0 | 20 | 0.000 | 0.000 | automatic_prefilter_probe20 |
| Qwen3-8B direct | 160 | 0.994 | 0.656 | 0.006 | 0.006 | 0.388 | 0.744 | 41 | 63 | 56 | 0.256 | 0.650 | automatic_prefilter |

## RuleFaith Gate Funnel

| stage | source_file | n | accepted_or_ready | refine | rejected | accepted_or_ready_rate | non_rejected_rate | label_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3 direct prefilter | qwen3_8b_filtering_statistics.json | 160 | 41 | 63 | 56 | 0.256 | 0.650 | automatic_prefilter |
| Field-aware RuleFaith gate | qwen3_field_aware_rulefaith_selection_stats.json | 160 | 45 | 13 | 102 | 0.281 | 0.362 | automatic_gate |
| Target-masked validation | qwen3_target_masked_validation_stats.json | 58 | 47 | 8 | 3 | 0.810 | 0.948 | automatic_gate |
| Rule/evidence audit | qwen3_rule_plausibility_audit_stats.json | 47 | 25 | 16 | 6 | 0.532 | 0.872 | automatic_rule_evidence_audit |
| Targeted deterministic repair | qwen3_targeted_repair_stats.json | 16 | 16 | 0 | 0 | 1.000 | 1.000 | deterministic_repair_revalidated |
| Codex pseudo-validation | qwen3_ready_validation_codex_summary.json | 41 | 17 | 13 | 11 | 0.415 | 0.732 | codex_ai_pseudo_validation_not_human |

## Candidate-Selection Baselines

| strategy | edit_groups | covered_groups | abstained_groups | coverage | accept_selected | refine_selected | reject_selected | accept_rate | non_reject_rate | mean_utility | label_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Random candidate (expected) | 23 | 23 | 0 | 1.000 | 9.5 | 7.0 | 6.5 | 0.413 | 0.717 | 0.565 | codex_ai_pseudo_validation_expected_value |
| First candidate | 23 | 23 | 0 | 1.000 | 8.0 | 8.0 | 7.0 | 0.348 | 0.696 | 0.522 | codex_ai_pseudo_validation |
| Natural candidate | 23 | 23 | 0 | 1.000 | 9.0 | 7.0 | 7.0 | 0.391 | 0.696 | 0.543 | codex_ai_pseudo_validation |
| Rule-grounded candidate | 23 | 23 | 0 | 1.000 | 10.0 | 7.0 | 6.0 | 0.435 | 0.739 | 0.587 | codex_ai_pseudo_validation |
| Highest confidence | 23 | 23 | 0 | 1.000 | 8.0 | 8.0 | 7.0 | 0.348 | 0.696 | 0.522 | codex_ai_pseudo_validation |
| Longest rationale | 23 | 23 | 0 | 1.000 | 8.0 | 9.0 | 6.0 | 0.348 | 0.739 | 0.543 | codex_ai_pseudo_validation |
| Shortest rationale | 23 | 23 | 0 | 1.000 | 10.0 | 6.0 | 7.0 | 0.435 | 0.696 | 0.565 | codex_ai_pseudo_validation |
| Pseudo-validator selective accept | 23 | 11 | 12 | 0.478 | 11.0 | 0.0 | 0.0 | 1.000 | 1.000 | 1.000 | codex_ai_pseudo_validation_upper_bound |

## Interpretation

- Qwen2.5-0.5B ran in the same setting but produced only 1 accepted candidate out of 160 under the conservative prefilter; it is therefore a weak baseline/negative source, not a positive-teacher source.
- Qwen3-8B produced a non-trivial direct accepted pool, but later pseudo-validation still rejected 11 of the 41 automatically ready candidates.
- Rule-grounded candidate choice is the best simple non-oracle top-1 strategy in this ready pool by accept rate, but the selective pseudo-validator diagnostic shows that many edit groups still need abstention or further refinement.
- These results can fill the method-pilot baseline section. They are not a replacement for real-human natural explanation evaluation.

## Artifacts Produced

- `results/rulefaith/rulefaith_teacher_baselines.csv`
- `results/rulefaith/rulefaith_method_gate_funnel.csv`
- `results/rulefaith/rulefaith_selection_baselines.csv`
- `results/rulefaith/rulefaith_selection_baselines.json`
- `results/paper_assets/rulefaith_open_teacher_baselines.tex`
- `results/paper_assets/rulefaith_selection_baselines.tex`

## Provenance

- Generated at: `2026-07-21T09:51:33.177596+00:00`
- Git commit at generation time: `dcfe6f0`
- Label boundary: `codex_ai_pseudo_validation` is AI pseudo-validation for internal triage only.

## Next Highest-Priority Loop

Prepare the next natural-explanation validation package or add a non-oracle deployable scorer for the 41-row ready pool; do not treat the pseudo-selective diagnostic as a final method result.

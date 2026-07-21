# Current Status

Last updated: 2026-07-21

## Current Branch

`main`

## Current Commit

Loop F Codex-assisted audit prelabel commit; use `git log --oneline -1` as the authoritative hash. The loop started from `473b5a7`.

## Current Method Version

RuleFaith-GEC method line, Qwen3-8B local open-teacher pilot, after deterministic evidence-span canonicalization, a 20-edit canonicalization-plus-refinement probe, human-audit handoff packaging, Codex-assisted completion of both Qwen3 audit forms, structured source-evidence repair, field-aware RuleFaith selection, target-masked validation, rule-plausibility/evidence-sufficiency audit, targeted deterministic repair, blind validation package v2 generation, and Codex/AI pseudo-validation for internal triage only.

## Completed Loops

- Round 15 human-grounded metric stress test is merged into `main`.
- Round 16--20 method scaffolding, edit pool, verifier calibration, Qwen2.5/Qwen3 teacher pilots are merged into `main`.
- Loop A / Qwen3-8B candidate audit generated an automatic audit package over all 160 Qwen3 candidates and selected 80 stratified rows for manual review.
- Loop B / evidence gate repair tightened evidence-span validation, updated the Qwen3 prompt constraints, and generated a blind 80-row human audit package.
- Loop C / targeted evidence refinement showed that model-only evidence repair is JSON-stable but mostly clears evidence instead of adding contextual evidence; deterministic span canonicalization improves smoke10 and full-pool evidence scores.
- Loop D / 20-edit evidence refinement probe confirmed that targeted Qwen3 evidence repair after canonicalization is not ready to scale: 20/20 parsed, but contextual source evidence dropped from 7/20 to 2/20.
- Loop E / Qwen3 human-audit handoff packaged the canonicalized 80-row blind audit form, produced checksums, and added validation/merge tooling for the completed human audit.
- Loop F / Codex-assisted prelabelling filled a separate copy of the 80-row blind audit form from automatic diagnostics, validated it, and generated breakdown reports. These labels are AI-assisted pseudo-labels, not real human audit labels.
- Loop G / Complete Qwen3 Codex audit coverage added `completed_by_codex` forms for both canonicalized and pre-canonicalization Qwen3 audit packages and documented the label-source boundary in `annotation/qwen3_codex_annotation_data_card.md`.
- Loop H / Structured evidence repair added deterministic source-context evidence spans, improved automatic contextual evidence from 82/160 to 160/160, and introduced a stricter RuleFaith selection gate that keeps 58 candidates in `refine` and rejects 102.
- Loop I / Field-aware RuleFaith selection separated required `edit_description` copy from leakage in `rule_text` and `rationale`, yielding 45 accepted, 13 refine, and 102 rejected candidates for target-masked validation.
- Loop J / Target-masked validation hid target strings from rule/rationale/conditions, added rule-category mismatch checks, and produced 47 validated, 8 refine, and 3 rejected candidates from the 58-candidate field-aware pool.
- Loop K / Rule plausibility and evidence sufficiency audit checked the 47 target-masked validated candidates and produced 25 ready-for-spotcheck, 16 needs-refinement, and 6 rejected candidates.
- Loop L / Ready-candidate validation packaging produced a 25-row blind validation form, 25-row hidden key, 16-row targeted repair instruction file, and handoff zip.
- Loop M / Targeted repair fixed the 16 needs-refinement candidates structurally, revalidated all 16, and generated a v2 blind validation package with 41 rows and no remaining repair rows.
- Loop N / Codex ready-candidate pseudo-validation filled the 41-row v2 validation package as explicitly marked AI pseudo-labels, yielding 17 accept, 13 refine, and 11 reject decisions for internal triage only.

## Running Loops

- No long-running command is active. The field-aware selection loop completed and produced validation buckets for the repaired Qwen3 candidates.

## Blocked Loops

- GPT-5.5 teacher generation is blocked until API credentials and budget are available.
- Natural explanation human evaluation is blocked until a new blinded package is prepared and real annotators are available.
- Student training is blocked until teacher candidates pass the stricter evidence gate, manual audit, and refinement.
- Qwen3 positive-data construction remains blocked for human-evidence claims. Codex-completed forms, field-aware automatic selection, and v2 ready-candidate pseudo-validation exist, but they must not be used as human gold or final positive labels.
- Full `pytest` verification is now available after installing `pytest` with `python3 -m pip install --user pytest`.

## Best Verified Result

The Qwen3-8B pilot produced 160 parsed teacher candidates with no generator-input leakage detected by the audit. Source edit spans and target presence in predictions passed for all 160 candidates. Deterministic evidence-span canonicalization improved all-spans source-index match from 20/160 to 155/160, contextual source evidence from 24/160 to 82/160, and wrong-evidence flags from 141/160 to 29/160. The Loop D 20-edit Qwen3 model-refinement probe was rejected because contextual source evidence dropped from 7/20 to 2/20. Codex-completed canonicalized audit decisions are 44 `refine` and 36 `reject`; pre-canonicalization audit decisions are 46 `refine` and 34 `reject`. Loop H structured evidence repair improves automatic contextual source evidence from 82/160 to 160/160, removes 29 prediction-only/wrong-evidence flags, and raises strict specific-source-evidence coverage from 10/160 to 124/160. Loop I field-aware selection fixes an over-strict leakage policy by allowing required edit-copy in `edit_description` while still penalizing `rule_text` and `rationale` leakage: previous strict buckets were 0 accepted, 58 refine, 102 rejected; field-aware buckets are 45 accepted, 13 refine, 102 rejected. Loop J target-masked validation over the 58 field-aware candidates produces 47 validated, 8 refine, and 3 rejected candidates, while flagging 7 target-dependent explanations and 6 rule-category mismatches. Loop K rule/evidence audit over the 47 target-masked validated candidates produces 25 ready-for-spotcheck, 16 needs-refinement, and 6 rejected candidates. Loop L packages the 25 ready candidates into a blind validation form and the 16 refinement candidates into targeted repair instructions. Loop M repairs all 16 refinement candidates structurally, revalidates all 16 under target-masked and rule/evidence gates, and generates a v2 blind package with 41 candidates. Loop N Codex/AI pseudo-validation labels those 41 candidates as 17 accept, 13 refine, and 11 reject, showing that automatic gates still miss linguistic issues.

## Largest Scientific Risk

Structured repair, field-aware selection, target-masked validation, rule/evidence audit, deterministic targeted repair, and Codex pseudo-validation fix several instrumentation bottlenecks but do not prove human-rated linguistic rule correctness. The largest remaining risks are alignment errors (58/160), possible false rationalization (19/160), edit-validity risk (28/160), and the lack of real-human or stronger preregistered validation for the 41 v2 ready candidates.

## Next Highest-Value Action

Use the 17 Codex-pseudo-accepted Qwen3 candidates only for a small internal RuleFaith selection/refinement smoke test, while preparing a real-human natural explanation validation package before any paper-quality method claim.

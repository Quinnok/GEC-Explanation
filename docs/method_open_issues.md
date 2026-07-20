# RuleFaith-GEC Method Open Issues

Last updated: 2026-07-20

## P0

| Issue | Impact | Needed Evidence | Status |
|---|---|---|---|
| GPT-5.5 API key is not visible in the environment. | Round 18 GPT-5.5 teacher generation cannot run. | `OPENAI_API_KEY` or compatible API credentials, plus budget confirmation. | Open |
| GPT-5.5 teacher pilot has not run. | No strong natural teacher candidates for RuleFaith filtering or distillation. | API-backed 80-edit pilot after credentials are available. | Blocked |
| Qwen3-8B accepted/refine candidates have not been manually spot-checked. | Student SFT/preference training could still learn weak evidence grounding or alignment errors. | `annotation/rulefaith_qwen3_audit/manual_audit_form.csv` selects 80 blind rows for human audit. Complete the audit before constructing positives. | Open |
| Qwen3-8B evidence spans are not reliable enough for positives. | Teacher candidates may cite plausible text with incorrect source token indices, prediction-only target phrases, or non-contextual evidence. | Loop B strict audit: all-spans source index match 20/160, contextual source evidence 24/160, prediction-only evidence 87/160. | Open |
| Natural explanation test data does not exist yet. | Cannot prove method improves real generated explanations. | New balanced natural-explanation set and human evaluation. | Open |

## P1

| Issue | Impact | Needed Evidence | Status |
|---|---|---|---|
| CoEdIT/instruction-corrector pool is small. | Cross-family trend could be underpowered. | Round 17 edit-pool stats and possible additional corrector. | Open |
| FLAN-T5-base open teacher is weak. | Open-source teacher candidates may add noise rather than useful preference positives. | Treat as weak baseline unless a stronger open model is approved or available locally. | Open |
| Qwen2.5-0.5B is too weak for positive teacher data under the current prompt. | Only 1/160 candidates passed the conservative RuleFaith prefilter. | Treat as weak baseline/negative source unless prompt refinement improves rule/evidence quality. | Open |
| Qwen2.5-1.5B probe did not solve explicit rule generation. | 20/20 probe candidates lacked explicit rule_text and were rejected. | Try a stronger prompt, a larger model, or GPT-5.5; do not train on this probe as positives. | Open |
| Qwen3-8B evidence grounding remains partial. | 136/160 candidates lack contextual source evidence under Loop B strict checks. | Run larger prompt-v2 regeneration or targeted refinement, rerun audit, then manually inspect selected candidates. | Open |
| Qwen3 prompt-v2 still under-produces contextual evidence. | Prompt-v2 removes prediction-only evidence in the smoke10 sample but often cites only the edited token or has bad source offsets. | Smoke10: contextual source evidence 3/10 and wrong-evidence flags 6/10. | Open |
| Verifier calibration is pressure-test-only. | Gate A conditional pass may not transfer to natural teacher outputs. | Re-run verifier calibration after GPT/open natural candidates exist. | Open |
| Large student model download may exceed 10GB. | Requires user confirmation before Round 23/24. | Student model selection report. | Open |
| `pdflatex`/`latexmk` unavailable in current shell. | Paper compile gate cannot be rerun after method-paper rewrite. | Restore TinyTeX/pdfTeX PATH or install a pdfTeX-compatible LaTeX toolchain. | Open |
| Agreement-inherited Round 15 labels lack blind audit. | Calibration labels may include shared bias. | Optional audit or robust sensitivity analysis. | Open |
| Thirteen target strings cross RuleFaith train/dev/test split. | Student/verifier evaluation could exploit target lexical shortcuts. | Target-masked evaluation and leakage-aware analysis. | Open |
| JFLEG multi-reference equivalence remains partial. | Some valid alternatives may be mislabeled as wrong or overcorrection. | Accept-if-any-reference alignment or manual audit before final claims. | Open |

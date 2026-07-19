# RuleFaith-GEC Method Open Issues

Last updated: 2026-07-19

## P0

| Issue | Impact | Needed Evidence | Status |
|---|---|---|---|
| GPT-5.5 API key is not visible in the environment. | Round 18 GPT-5.5 teacher generation cannot run. | `OPENAI_API_KEY` or compatible API credentials, plus budget confirmation. | Open |
| GPT-5.5 teacher pilot has not run. | No strong natural teacher candidates for RuleFaith filtering or distillation. | API-backed 80-edit pilot after credentials are available. | Blocked |
| Natural explanation test data does not exist yet. | Cannot prove method improves real generated explanations. | New balanced natural-explanation set and human evaluation. | Open |

## P1

| Issue | Impact | Needed Evidence | Status |
|---|---|---|---|
| CoEdIT/instruction-corrector pool is small. | Cross-family trend could be underpowered. | Round 17 edit-pool stats and possible additional corrector. | Open |
| FLAN-T5-base open teacher is weak. | Open-source teacher candidates may add noise rather than useful preference positives. | Treat as weak baseline unless a stronger open model is approved or available locally. | Open |
| Qwen small model weights did not finish downloading in the current network. | The stronger local open-teacher branch is implemented but has not produced candidates yet. | Re-run `HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN_SHARDS=2 bash experiments/rulefaith/run_qwen_teacher_pilot.sh` when Hugging Face download is stable or the model is pre-cached. | Open |
| Verifier calibration is pressure-test-only. | Gate A conditional pass may not transfer to natural teacher outputs. | Re-run verifier calibration after GPT/open natural candidates exist. | Open |
| Large student model download may exceed 10GB. | Requires user confirmation before Round 23/24. | Student model selection report. | Open |
| `pdflatex`/`latexmk` unavailable in current shell. | Paper compile gate cannot be rerun after method-paper rewrite. | Restore TinyTeX/pdfTeX PATH or install a pdfTeX-compatible LaTeX toolchain. | Open |
| Agreement-inherited Round 15 labels lack blind audit. | Calibration labels may include shared bias. | Optional audit or robust sensitivity analysis. | Open |
| Thirteen target strings cross RuleFaith train/dev/test split. | Student/verifier evaluation could exploit target lexical shortcuts. | Target-masked evaluation and leakage-aware analysis. | Open |
| JFLEG multi-reference equivalence remains partial. | Some valid alternatives may be mislabeled as wrong or overcorrection. | Accept-if-any-reference alignment or manual audit before final claims. | Open |

# RuleFaith-GEC Method Open Issues

Last updated: 2026-07-19

## P0

| Issue | Impact | Needed Evidence | Status |
|---|---|---|---|
| GPT-5.5 API key is not visible in the environment. | Round 18 GPT-5.5 teacher generation cannot run. | `OPENAI_API_KEY` or compatible API credentials, plus budget confirmation. | Open |
| Current verifier is too weak for a solved RuleFaith claim. | Filtering could fail to improve rule/evidence faithfulness. | Round 19 verifier calibration meeting Gate A. | Open |
| Natural explanation test data does not exist yet. | Cannot prove method improves real generated explanations. | New balanced natural-explanation set and human evaluation. | Open |

## P1

| Issue | Impact | Needed Evidence | Status |
|---|---|---|---|
| CoEdIT/instruction-corrector pool is small. | Cross-family trend could be underpowered. | Round 17 edit-pool stats and possible additional corrector. | Open |
| Large student model download may exceed 10GB. | Requires user confirmation before Round 23/24. | Student model selection report. | Open |
| Agreement-inherited Round 15 labels lack blind audit. | Calibration labels may include shared bias. | Optional audit or robust sensitivity analysis. | Open |


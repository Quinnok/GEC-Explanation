# RuleFaith Teacher Candidate Data Card

Created: 2026-07-19

## Status

Round 18 prepares GPT-5.5, FLAN-T5, and Qwen open-teacher generation. GPT-5.5 generation requires `OPENAI_API_KEY` and a valid `RULEFAITH_GPT55_MODEL` or accessible default model alias. Qwen generation uses Hugging Face local inference and has no API cost, but candidate quality must pass RuleFaith filtering before use as positives.

## Source Data

- Edit pool: `data/rulefaith/edit_pool.jsonl`
- Pilot size target: 80 edits
- GPT candidate target: 5 candidates per edit
- FLAN-T5 open teacher candidate target: 2 candidates per edit
- Qwen small open teacher candidate target: 2 candidates per edit
- Qwen3-8B open teacher candidate target: 2 candidates per edit

## Generation Inputs

Only source, model prediction, atomic model edit, and edit span are used. Reference corrections, aligned reference edits, model behavior labels, and human labels are excluded from teacher prompts.

## Intended Use

The outputs are natural explanation candidates for verifier filtering, refinement, and preference-data construction. They are not gold annotations.

## Current Known Blockers

- `OPENAI_API_KEY` is not visible in the current environment.
- The local OpenAI SDK install attempt was interrupted because package download was too slow; the generation script keeps OpenAI as an optional import.
- Qwen2.5-0.5B-Instruct completed an 80-edit, 160-candidate pilot. It is parseable but weak as teacher-positive data: only 1/160 candidates passed the conservative prefilter.
- Qwen2.5-1.5B-Instruct completed a 20-candidate probe. It had better alignment but did not provide explicit rule text under the current prompt, so 0/20 candidates passed the conservative prefilter.
- Qwen3-8B completed an 80-edit, 160-candidate no-thinking pilot. It is the first local open teacher with a usable accepted/refine pool: 41/160 accepted and 63/160 marked for refinement under the conservative prefilter.

## Safety Controls

- Budget limit is read from `RULEFAITH_API_BUDGET_USD`, defaulting to 30 USD.
- Raw responses and parse errors are saved.
- The script supports resume mode and will not silently overwrite previous candidates.
- Cost estimates are recorded separately from actual API usage.
- Qwen raw responses, parse failures, and quality reports are saved separately from FLAN-T5 outputs.
- Current FLAN and Qwen2.5 candidates should be used as weak baselines, rejected examples, and refinement stress cases, not as SFT positives.
- Qwen3-8B accepted/refine candidates may be used for RuleFaith refinement and preference construction only after manual spot-checking or an additional verifier quality gate.

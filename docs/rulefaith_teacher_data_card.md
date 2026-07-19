# RuleFaith Teacher Candidate Data Card

Created: 2026-07-19

## Status

Round 18 prepares GPT-5.5, FLAN-T5, and Qwen small open-teacher generation. GPT-5.5 generation requires `OPENAI_API_KEY` and a valid `RULEFAITH_GPT55_MODEL` or accessible default model alias. Qwen small generation uses Hugging Face local inference and has no API cost, but requires downloading model weights.

## Source Data

- Edit pool: `data/rulefaith/edit_pool.jsonl`
- Pilot size target: 80 edits
- GPT candidate target: 5 candidates per edit
- FLAN-T5 open teacher candidate target: 2 candidates per edit
- Qwen small open teacher candidate target: 2 candidates per edit

## Generation Inputs

Only source, model prediction, atomic model edit, and edit span are used. Reference corrections, aligned reference edits, model behavior labels, and human labels are excluded from teacher prompts.

## Intended Use

The outputs are natural explanation candidates for verifier filtering, refinement, and preference-data construction. They are not gold annotations.

## Current Known Blockers

- `OPENAI_API_KEY` is not visible in the current environment.
- The local OpenAI SDK install attempt was interrupted because package download was too slow; the generation script keeps OpenAI as an optional import.
- Qwen small provider is implemented with `Qwen/Qwen2.5-0.5B-Instruct`; initial smoke test reached Hugging Face weight download but was interrupted because the download stalled at about 37 MB in the current network.

## Safety Controls

- Budget limit is read from `RULEFAITH_API_BUDGET_USD`, defaulting to 30 USD.
- Raw responses and parse errors are saved.
- The script supports resume mode and will not silently overwrite previous candidates.
- Cost estimates are recorded separately from actual API usage.
- Qwen small raw responses, parse failures, and quality reports are saved separately from FLAN-T5 outputs.

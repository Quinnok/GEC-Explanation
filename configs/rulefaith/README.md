# RuleFaith Configs

This directory contains frozen method-branch configs. Do not tune test-set mappings or metric definitions after seeing RuleFaith method results.

- `open_teacher.yaml`: FLAN-T5-base weak open-teacher baseline.
- `qwen_small_teacher.yaml`: Qwen2.5-0.5B-Instruct local instruction-teacher branch.
- `qwen3_8b_teacher.yaml`: Qwen3-8B local open-teacher branch with thinking disabled.
- `gpt55_teacher.yaml`: API-backed strong teacher branch, gated by credentials and budget.

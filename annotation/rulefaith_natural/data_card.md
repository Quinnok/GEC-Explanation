# RuleFaith Natural Explanation Validation Data Card

Generated: 2026-07-21T13:02:26+00:00
Git commit: a381827
Seed: 20260721

## Purpose

This package supports blinded evaluation of natural GEC edit explanations. It compares Qwen3 direct natural explanations with RuleFaith deployable top-1 outputs for the same model-produced edits.

## Scope

- Items: 46
- Edit groups: 23
- Systems per group: 2
- System identities are hidden from annotators and stored only in `hidden_system_key.csv`.

## Counts

- Systems: {'qwen3_direct_natural': 22, 'rulefaith_score_top1': 23, 'qwen3_direct_rule_grounded': 1}
- Datasets: {'EXPECT': 36, 'JFLEG': 10}
- Correctors: {'gector_roberta_base': 14, 'coedit_large': 18, 't5_base_grammar': 14}
- Operations: {'replace': 28, 'delete': 10, 'insert': 8}

## Label Boundary

This package contains model-generated explanations. It does not contain human labels yet. It does not expose Codex/AI pseudo-validation decisions to annotators.

## Known Limitations

This is a small validation package derived from the current 41-row Qwen3 ready pool and 23 edit groups. It is suitable for a method-pilot validation pass, not for final AAAI-scale human evaluation by itself.

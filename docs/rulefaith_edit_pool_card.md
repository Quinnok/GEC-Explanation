# RuleFaith Edit Pool Card

Created: 2026-07-19

## Purpose

This pool selects substantive model-produced edits for natural teacher explanation generation and RuleFaith-GEC method development.

## Sources

- `data/faithfulness_benchmark/edit_records.jsonl`

## Selection Rules

- Exclude obvious detokenization, punctuation-spacing, and case/whitespace-only artifacts.
- Preserve all three model families with minimum quotas.
- Preserve EXPECT and JFLEG coverage.
- Preserve correct, wrong, and overcorrection behaviors.
- Preserve replace, insert, and delete operations.
- Retain ORTH/PUNCT only when not an obvious formatting artifact.
- Use source-level splits so the same source sentence does not cross train/dev/test.

## Key Statistics

- Selected edits: 300
- Train/dev/test: {'dev': 39, 'test': 55, 'train': 206}
- By model: {'coedit_large': 60, 'gector_roberta_base': 120, 't5_base_grammar': 120}
- By dataset: {'EXPECT': 165, 'JFLEG': 135}
- By behavior: {'correct_correction': 77, 'overcorrection': 151, 'wrong_correction': 72}
- By operation: {'delete': 33, 'insert': 30, 'replace': 237}

## Known Risks

- Target strings crossing splits: 13.
- Near-duplicate source pairs at >=0.92 similarity: 0.
- CoEdIT remains smaller than GECToR/T5 because the existing CoEdIT pilot is smaller.
- JFLEG multi-reference equivalence is not fully solved in this pool.

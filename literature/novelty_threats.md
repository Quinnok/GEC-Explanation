# Novelty Threats

## P0 Threats

1. GEE and Prompt Insertion already generate natural-language explanations for GEC edits from erroneous/corrected pairs.
2. EXCGEC already frames edit-wise explainable GEC as a benchmark, with human evaluation and free-text metrics, albeit in Chinese.
3. CLEME2.0 already decomposes GEC correction behavior into hit/wrong/under/over aspects.
4. COCOGEC already brings GEC-specific counterfactuals to robustness evaluation.
5. Hase and Bansal already define simulatability as predicting model behavior.
6. Parcalabescu and Frank already caution that explanation faithfulness tests may be output self-consistency.

## Surviving Innovation Space

The paper can remain viable if it makes a narrower claim:

- English model-produced edit-level explanation benchmark, not reference-edit template generation.
- Explicit separation of edit correspondence, output self-consistency, behavioral faithfulness, grammatical validity, and helpfulness.
- Counterfactual Edit Simulatability where labels are rerun model behavior under GEC-specific counterfactuals.
- Leakage-adjusted controls that show when reverse reconstruction is copying explicit edit content.
- Rule/evidence grounding as a secondary signal, not the sole contribution.

## Claims to Avoid Until More Evidence Exists

- "First edit-wise GEC explanation benchmark."
- "Reverse reconstruction measures faithfulness."
- "Generated explanations are gold."
- "Automatic metrics are equivalent to human judgments."

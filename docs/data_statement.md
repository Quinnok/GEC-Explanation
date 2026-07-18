# Data Statement

Generated: `2026-07-18T05:42:47+00:00`

## EXPECT

- Source: `https://github.com/lorafei/Explainable_GEC`
- Commit: `6e44b68f6e4c199dd3b235cacb604a856bd3d133`
- License: `MIT`
- Processed sample count: 300
- Source-reference ERRANT edit count: 320
- Split counts: `{"test": 300}`

EXPECT provides source/reference sentence pairs plus explanation-adjacent labels such as evidence indices and error types. The local audit found no natural-language explanation field for model-produced edits.

## JFLEG

- Source: `https://github.com/keisks/jfleg`
- Commit: `ee06ff806a208aba815ac45313f4e750a48330a5`
- License: `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International`
- Processed sample count: 160
- Split counts: `{"dev": 160, "test": 0}`
- Reference policy: The benchmark pilot uses ref0 as the primary reference for single-reference ERRANT extraction and retains all four JFLEG references in each row.

## Benchmark Construction

The benchmark aligns source-reference ERRANT edits with source-prediction ERRANT edits. Predicted edits are labeled as correct, wrong, or overcorrection by automatic alignment; unmatched reference edits are stored as missed-correction diagnoses. Labels are automatic and are not human adjudications.

## Splitting

Train/dev/test splits are deterministic hashes of dataset, sample id, and source text. The leakage audit found 0 source texts crossing splits. Template families are repeated across splits by design, so aggregate metrics must be reported by explanation type.

## Annotation Status

No double-human annotation has been collected. Round 10 must prepare annotation packets and adjudication guidelines before any human-gold claim.

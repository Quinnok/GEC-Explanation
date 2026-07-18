# Data Sources

Last updated: 2026-07-18

## EXPECT

- Source: https://github.com/lorafei/Explainable_GEC
- Paper: Enhancing Grammatical Error Correction Systems with Explanations, ACL 2023.
- License: MIT, as stated in the upstream repository README and LICENSE.
- Local download: `data/downloads/Explainable_GEC`.
- Download command: `git clone --depth 1 https://github.com/lorafei/Explainable_GEC.git data/downloads/Explainable_GEC`.
- Recorded commit: `6e44b68f6e4c199dd3b235cacb604a856bd3d133`.
- Pilot sample file: `data/processed/expect_v1_samples.jsonl`.
- Pilot sample count: 300.
- ERRANT edit count in pilot: 320.
- Split counts: `{"test": 300}`.
- Operation counts: `{"delete": 39, "insert": 51, "replace": 230}`.

The versioned pilot uses real source/reference sentence pairs from EXPECT. The generated explanations in this project are automatic template constructions for pilot diagnostics, not human gold explanations.

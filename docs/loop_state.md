# Loop State

Last updated: 2026-07-18

## Current Round

Round 08 methods and counterfactual pilot are complete and awaiting commit. Round 03 is committed as `8a8fedb`; Round 04 is committed as `2667862`; Round 05 is committed as `fa2b7fc`; Round 06 is committed as `1db85c8`; Round 07 is committed as `7b35499`.

## Latest Completed Work

- 100-row model behavior audit: `results/audit/model_behavior_audit_100.jsonl`.
- 60-row explanation/edit audit: `results/audit/round04_sample_audit.jsonl`.
- T5 normalization ablation: `results/model_edits/normalized_behavior_stats.json`.
- ERRANT alignment reliability audit: `results/audit/alignment_reliability_audit_50.md`.
- 50-paper literature package: `literature/`.
- Round 06 idea decision: main line is Counterfactual Edit Simulatability; backup is Rule-grounded Faithfulness.
- Round 07 benchmark candidate: 700 model-produced edits, 12,754 automatic explanation/control instances, 160 missed-edit diagnoses, two datasets, and three model families.
- Round 08 methods: 15 L1/L3 methods/ablations over 11,764 labeled automatic instances.
- Round 08 counterfactual pilot: 48 variants with labels from actual GEC model reruns across GECToR, T5, and CoEdIT.

## Current Highest-Priority Problem

Round 09 must scale the counterfactual pilot, add grouped statistics/error analysis, and avoid treating automatic template results as final human faithfulness evidence.

## Active Constraints

- No automatic audit output is human annotation.
- Round 02 template reconstruction remains a leakage upper control only.
- Raw T5 behavior must be retained alongside normalized and substantive views.
- Reverse reconstruction should be described as edit correspondence or output self-consistency, not internal model faithfulness.
- Counterfactual labels must come from rerunning the original GEC models, not from grammar-theory expectations.
- CoEdIT Round 07 evidence is a small 20-source CPU pilot; treat it as third-family coverage, not a full-scale comparison.
- JFLEG Round 07 labels use `ref0` as primary reference while retaining all four references for later multi-reference alignment.
- Round 08 rule/evidence verifier is a lexical automatic baseline, not semantic proof.
- Round 08 counterfactual labels are real model reruns, but the sample is small and many rule-relevant variants become competing edits.
- Optional parallel chunked prediction tooling exists in `experiments/run_parallel_model_predictions.sh`; benchmark parallel settings before using it for large CoEdIT runs.

# Loop State

Last updated: 2026-07-18

## Current Round

Round 10 human evaluation preparation is complete and awaiting commit. Round 03 is committed as `8a8fedb`; Round 04 is committed as `2667862`; Round 05 is committed as `fa2b7fc`; Round 06 is committed as `1db85c8`; Round 07 is committed as `7b35499`; Round 08 is committed as `4ebd5e4`; Round 09 is committed as `e288227`.

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
- Round 09 scaled pilot: 120 counterfactual variants, 1,080 explanation-variant pairs, grouped bootstrap statistics, and error-analysis packets.
- Round 10 annotation package: 240 public annotation items, guidelines, adjudication template, hidden auto-label metadata, and human annotation status checker.

## Current Highest-Priority Problem

The next nondependent work is simulated review/rebuttal and paper tightening. Human-faithfulness validation is blocked until real double annotation is completed.

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
- Round 09 does not support a nontrivial counterfactual simulator gain; best automatic L2 simulator macro-F1 is only 0.297.
- Preserve `competing_edit` as its own L2 behavior class.
- No human gold labels exist; `results/round10/human_annotation_status.json` records `blocked_no_human_annotation`.

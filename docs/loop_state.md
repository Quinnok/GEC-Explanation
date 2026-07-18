# Loop State

Last updated: 2026-07-18

## Current Round

Round 06 in progress. Round 03 is committed as `8a8fedb`; Round 04 is committed as `2667862`; Round 05 literature packaging is complete.

## Latest Completed Work

- 100-row model behavior audit: `results/audit/model_behavior_audit_100.jsonl`.
- 60-row explanation/edit audit: `results/audit/round04_sample_audit.jsonl`.
- T5 normalization ablation: `results/model_edits/normalized_behavior_stats.json`.
- ERRANT alignment reliability audit: `results/audit/alignment_reliability_audit_50.md`.
- 50-paper literature package: `literature/`.

## Current Highest-Priority Problem

Round 06 must choose a defensible main idea and backup. Reverse reconstruction is now only an L1 correspondence/leakage diagnostic, not the main contribution.

## Active Constraints

- No automatic audit output is human annotation.
- Round 02 template reconstruction remains a leakage upper control only.
- Raw T5 behavior must be retained alongside normalized and substantive views.
- Reverse reconstruction should be described as edit correspondence or output self-consistency, not internal model faithfulness.

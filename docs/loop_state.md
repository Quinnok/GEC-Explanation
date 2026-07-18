# Loop State

Last updated: 2026-07-18

## Current Round

Round 05 in progress. Round 03 is committed as `8a8fedb`. Round 04 audit/normalization/alignment work is complete and pending commit.

## Latest Completed Work

- 100-row model behavior audit: `results/audit/model_behavior_audit_100.jsonl`.
- 60-row explanation/edit audit: `results/audit/round04_sample_audit.jsonl`.
- T5 normalization ablation: `results/model_edits/normalized_behavior_stats.json`.
- ERRANT alignment reliability audit: `results/audit/alignment_reliability_audit_50.md`.

## Current Highest-Priority Problem

Novelty and framing remain the highest risk. The next round must build the systematic literature package and novelty-threat map before finalizing the research direction.

## Active Constraints

- No automatic audit output is human annotation.
- Round 02 template reconstruction remains a leakage upper control only.
- Raw T5 behavior must be retained alongside normalized and substantive views.
- Reverse reconstruction should be described as edit correspondence or output self-consistency, not internal model faithfulness.

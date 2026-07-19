# Loop State

Last updated: 2026-07-19

## Current Round

Round 15 human-grounded metric evaluation is complete and committed as `24f7b13`; annotation provenance was later confirmed by the user as two independent human annotators plus a human adjudicator. Round 03 is committed as `8a8fedb`; Round 04 is committed as `2667862`; Round 05 is committed as `fa2b7fc`; Round 06 is committed as `1db85c8`; Round 07 is committed as `7b35499`; Round 08 is committed as `4ebd5e4`; Round 09 is committed as `e288227`; Round 10 is committed as `a7cffc9`; Round 11 is committed as `f8529af`; Round 12 is committed as `62c51cd`; Round 13 is committed as `1b219c5`; Round 14 is committed as `e88aebc`.

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
- Round 11 reranking application: 880 candidates for 80 model-produced edits, eight automatic rerankers, local FLAN-T5 judge over all candidates, and reward-hacking audit.
- Round 12 complete draft: `paper/main.pdf` compiles cleanly; after Round 13 it is 8 total pages with references starting on page 7. `paper/supplementary/appendix.pdf` compiles to 4 clean pages, and 11 generated paper assets are tracked under `results/paper_assets/`.
- Round 13 simulated reviews: three rounds, nine roles per round, title/framing revised, close-work boundary strengthened, automatic P0s closed for draft.
- Round 14 rebuttal/artifacts: rebuttal drafts, evidence index, README, environment files, reproduction commands, model/data download notes, license summary, artifact checklist, reproducibility notes, and checksum index.
- Round 15 human-grounded metric evaluation: 160 human-adjudicated edit-explanation labels, human-gold metric tables, stress-test breakdowns, error cases, and a paper reframe around human-adjudicated metric stress testing.

## Current Highest-Priority Problem

All nondependent requested automatic work through Round 15 is complete. The next highest-priority task is a balanced natural-explanation validation set, ideally using GPT-5.5 plus at least one open model and the V2 human protocol.

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
- Round 15 has 160 human-adjudicated stress-test labels. The older Round 10 status file remains a historical pre-annotation status record, not the current project state.
- Round 11 reranking shows high automatic scores can be produced by template/edit-copy selection; do not frame reranking as solving explanation selection.
- The local FLAN-T5 judge is a no-paid-API baseline only; it scored below random on the current automatic pairwise ranking task.
- The main paper is at the AAAI main-content limit and uses two reference pages; further changes must be length-neutral or move details to the supplementary appendix.
- Official AAAI-27 requirements were checked on 2026-07-18 and must be rechecked immediately before final upload.
- Round 15 closes the missing-human-label risk for the stress-test subset, but natural-explanation coverage and learner-helpfulness claims remain future work.
- Round 14 checksums must be regenerated after any future result, paper, or artifact changes.

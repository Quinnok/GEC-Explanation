# Round 10: Human Evaluation Preparation

## Completed

- Built a human annotation package with 240 public items:
  - 160 edit explanation faithfulness items.
  - 80 counterfactual edit simulatability items.
- Created annotator-facing files under `annotation/round10/`:
  - `guidelines.md`
  - `annotation_items.jsonl`
  - `annotation_form.csv`
  - `adjudication_template.csv`
  - `README.md`
- Created hidden audit metadata in `annotation/round10/annotation_metadata_with_auto_labels.jsonl`.
- Created `experiments/src/evaluate_human_annotations.py` for Cohen's kappa after two annotators complete independent CSVs.
- Ran the status check and saved `results/round10/human_annotation_status.json`.

## Current Status

- Human gold labels: 0.
- Double-human annotation: blocked until real annotators fill independent annotation files.
- This is a genuine hard dependency for any claim about closest-to-human faithfulness.

## Package Stats

- Public items: 240.
- EXPECT/JFLEG items: 176 / 64.
- CoEdIT/GECToR/T5 items: 62 / 88 / 90.
- Human annotation status: `blocked_no_human_annotation`.

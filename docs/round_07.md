# Round 07: GEC Explanation Faithfulness Benchmark

## Completed

- Added JFLEG as a second license-clear GEC data source and retained all four references per row.
- Ran GECToR and T5 over 80 JFLEG samples each, producing 540 JFLEG model edits and 378 missed-edit diagnoses.
- Ran CoEdIT-large over 20 EXPECT samples as an instruction-following open generation/editor branch, producing 122 predicted edits and 8 missed-edit diagnoses.
- Built a 700-edit benchmark with 12,754 explanation/control instances and 160 missing-edit diagnoses.
- Included three model families in the selected benchmark: sequence-to-edit, sequence-to-sequence, and instruction-following text editor.
- Generated benchmark card, data statement, license report, and leakage audit from JSON outputs.

## Key Stats

- Dataset counts: `{"EXPECT": 420, "JFLEG": 280}`
- Model counts: `{"coedit_large": 122, "gector_roberta_base": 298, "t5_base_grammar": 280}`
- Behavior counts: `{"correct_correction": 136, "overcorrection": 438, "wrong_correction": 126}`
- Operation counts: `{"delete": 58, "insert": 115, "replace": 527}`
- Error types: 41
- Human gold labels: 0

## Caveats

- CoEdIT is a small 20-sentence CPU pilot because the model is 770M parameters / about 3.13GB of weights.
- Automatic explanations and negatives are not human gold.
- Explicit templates remain leakage upper controls only.
- Counterfactual labels are pending Round 08 reruns of the original GEC models.

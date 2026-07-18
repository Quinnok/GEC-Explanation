# Round 04: Data, Label, and Model Behavior Audit

Last updated: 2026-07-18

## Scope

Round 04 audits the reliability of the Round 03 model-produced edit pilot. It does not introduce human labels. All audit labels are researcher-readable automatic screening flags.

## 4.1 Model Behavior Audit

Command:

```bash
.venv311/bin/python experiments/src/build_model_behavior_audit.py --count 100 --out-dir results/audit
```

Outputs:

- `results/audit/model_behavior_audit_100.jsonl`
- `results/audit/model_behavior_audit_100.md`
- `results/audit/model_behavior_audit_summary.json`

Summary:

- Audited rows: 100.
- Model counts: `{"gector_roberta_base": 52, "t5_base_grammar": 48}`.
- Behavior counts: `{"correct_correction": 24, "missed_correction": 24, "overcorrection": 28, "wrong_correction": 24}`.
- Operation counts: `{"delete": 12, "insert": 21, "replace": 67}`.
- Error types covered: 25.
- Sentence length buckets: `{"long": 31, "medium": 55, "short": 14}`.
- Single/multi edit counts: `{"multi_edit": 84, "single_edit": 16}`.
- Automatic model-format-noise flags: 24.
- Automatically suitable-for-explanation flags: 58.

Important limitation: multi-reference equivalence cannot be adjudicated from the single EXPECT reference. The audit explicitly marks this as unknown rather than pretending it is resolved.

## 4.2 T5 Normalization Ablation

Command:

```bash
.venv311/bin/python experiments/src/t5_normalization_ablation.py --out-dir results/model_edits
```

Outputs:

- `results/model_edits/raw_behavior_stats.json`
- `results/model_edits/normalized_behavior_stats.json`
- `results/model_edits/substantive_behavior_stats.json`
- `results/model_edits/normalization_changes.jsonl`
- `results/model_edits/normalization_variant_events.jsonl`

T5 behavior by condition:

| Condition | Correct | Wrong | Over | Missed | Precision | Recall | F0.5 | Pred edits | Avg pred edits/sent |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Raw | 71 | 71 | 893 | 178 | 0.068599 | 0.221875 | 0.079596 | 1035 | 3.450000 |
| Normalized spacing | 71 | 71 | 897 | 178 | 0.068335 | 0.221875 | 0.079312 | 1039 | 3.463333 |
| Normalized punctuation | 71 | 68 | 854 | 181 | 0.071501 | 0.221875 | 0.082712 | 993 | 3.310000 |
| Normalized case | 71 | 67 | 814 | 182 | 0.074580 | 0.221875 | 0.085998 | 952 | 3.173333 |
| Excluding ORTH | 71 | 50 | 384 | 198 | 0.140594 | 0.222571 | 0.151774 | 505 | 1.683333 |
| Excluding PUNCT | 71 | 70 | 854 | 173 | 0.071357 | 0.226115 | 0.082673 | 995 | 3.316667 |
| Excluding ORTH+PUNCT | 71 | 49 | 345 | 193 | 0.152688 | 0.226837 | 0.163369 | 465 | 1.550000 |
| Substantive only | 71 | 45 | 245 | 195 | 0.196676 | 0.228296 | 0.202279 | 361 | 1.203333 |

Conclusion: the raw T5 result is heavily dominated by orthographic and punctuation/detokenization edits. Removing ORTH+PUNCT changes precision from 0.068599 to 0.152688 and reduces predicted edits from 1035 to 465. This does not delete the raw result; it shows why future main experiments must report both raw and normalized/substantive views.

## 4.3 ERRANT Alignment Reliability

Command:

```bash
.venv311/bin/python experiments/src/audit_alignment_reliability.py --count 50 --out-dir results/audit
```

Outputs:

- `results/audit/alignment_reliability_audit_50.jsonl`
- `results/audit/alignment_reliability_audit_50.md`
- `results/audit/alignment_reliability_summary.json`

Comparison over all 600 model-output sentences:

| Strategy | Correct | Wrong | Over | Missed |
|---|---:|---:|---:|---:|
| Exact-only | 213 | 0 | 1494 | 427 |
| Stable partial-overlap | 213 | 90 | 1404 | 337 |

The stable strategy greedily matches predicted/reference edits by span F1, source text, target text, operation, type, and same-start bonuses. Exact signatures remain correct corrections; non-exact but related matches become wrong corrections. Compared with exact-only matching, this recovers 90 non-exact related edits as wrong corrections instead of double-counting them as both overcorrections and missed corrections.

## Explanation Candidate Audit

Command:

```bash
.venv311/bin/python experiments/src/build_round04_audit.py --count 60 --out-dir results/audit
```

Outputs:

- `results/audit/round04_sample_audit.jsonl`
- `results/audit/round04_sample_audit.md`
- `results/audit/round04_audit_summary.json`

Summary: 60 explanation/edit rows, 31 GECToR and 29 T5; 19 correct, 15 wrong, 26 overcorrection; 17 ORTH/PUNCT noise flags; 7 generic explanation flags; 12 prediction-clause repeat flags. These are automatic screening flags, not human explanation judgments.

## Next Single Action

Build the Round 05 literature package with at least 35 paper cards and a novelty-threat matrix before finalizing the paper's research direction.

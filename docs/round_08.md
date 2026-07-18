# Round 08: Methods and Counterfactual Pilot

## Completed

- Implemented L1 edit-correspondence/leakage methods over the Round 07 benchmark.
- Implemented L3-style rule/evidence lexical verifier and ablations.
- Built 48 counterfactual source variants from 24 model-produced edits across GECToR, T5, and CoEdIT.
- Reran the original public GEC models on counterfactual sources and assigned labels from actual model behavior.
- Added regression coverage for `source span` parsing.

## L1/L3 Method Results

- Evaluated examples: 11764
- Skipped labels: `{"candidate_not_gold": 290, "pending_counterfactual_label": 700}`
- TF-IDF similarity threshold selected on train split: 0.1

| Method | N | Accuracy | Macro-F1 | Positive F1 | Negative F1 |
|---|---:|---:|---:|---:|---:|
| `random` | 11764 | 0.504 | 0.490 | 0.406 | 0.574 |
| `majority_train` | 11764 | 0.655 | 0.396 | 0.000 | 0.791 |
| `current_edit_only` | 11764 | 0.345 | 0.257 | 0.514 | 0.000 |
| `surface_keyword` | 11764 | 0.723 | 0.579 | 0.334 | 0.825 |
| `structured_explicit_extraction` | 11764 | 0.751 | 0.639 | 0.439 | 0.840 |
| `reverse_reconstruction` | 11764 | 0.751 | 0.640 | 0.440 | 0.840 |
| `target_masked_reconstruction` | 11764 | 0.669 | 0.439 | 0.081 | 0.798 |
| `leakage_adjusted_reconstruction` | 11764 | 0.689 | 0.496 | 0.183 | 0.808 |
| `tfidf_embedding_similarity` | 11764 | 0.741 | 0.703 | 0.598 | 0.809 |
| `nli_lexical_proxy` | 11764 | 0.740 | 0.736 | 0.704 | 0.768 |
| `rule_evidence_verifier` | 11764 | 0.783 | 0.767 | 0.705 | 0.828 |
| `no_rule_verifier` | 11764 | 0.654 | 0.641 | 0.573 | 0.709 |
| `no_evidence_verifier` | 11764 | 0.775 | 0.761 | 0.702 | 0.820 |
| `no_source_reconstruction` | 11764 | 0.717 | 0.564 | 0.306 | 0.822 |
| `no_explanation_majority` | 11764 | 0.655 | 0.396 | 0.000 | 0.791 |

## Reconstruction Metrics

| Method | Full Exact | Span F1 | Target Match | Operation Acc. |
|---|---:|---:|---:|---:|
| `leakage_adjusted_reconstruction` | 0.035 | 0.035 | 0.035 | 0.035 |
| `no_source_reconstruction` | 0.062 | 0.114 | 0.071 | 0.136 |
| `reverse_reconstruction` | 0.098 | 0.151 | 0.113 | 0.180 |
| `structured_explicit_extraction` | 0.098 | 0.151 | 0.113 | 0.180 |
| `target_masked_reconstruction` | 0.015 | 0.147 | 0.026 | 0.176 |

## Counterfactual Pilot

- Counterfactual instances: 48
- Model counts: `{"coedit_large": 16, "gector_roberta_base": 16, "t5_base_grammar": 16}`
- Variant family counts: `{"error_irrelevant": 24, "rule_relevant": 24}`
- Actual behavior counts: `{"cancel": 3, "change_span": 2, "competing_edit": 20, "preserve": 23}`

| Method | N | Accuracy | Macro-F1 |
|---|---:|---:|---:|
| `random` | 48 | 0.271 | 0.150 |
| `source_edit_availability` | 48 | 0.438 | 0.161 |
| `variant_family_prior` | 48 | 0.521 | 0.193 |

## Interpretation Guardrails

- These numbers use automatic labels and synthetic/open-model explanations; they are not human-gold faithfulness scores.
- Explicit templates remain leakage upper controls.
- The L2 pilot is small but real: labels come from rerunning the same public GEC models on counterfactual inputs.
- Many rule-relevant variants become `competing_edit`, so Round 09 must analyze this class instead of treating all non-preserve labels as clean cancellation.

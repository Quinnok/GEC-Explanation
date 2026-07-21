# RuleFaith Ready Candidate Deployable Selector Cases

These cases use Codex/AI pseudo-validation only for diagnostic comparison. The deployable scorer does not use `validator_*` fields when assigning scores.

## Metrics

- candidate count: `41`
- edit groups: `23`
- score buckets: `{'accept': 28, 'refine': 9, 'reject': 4}`
- top-1 selection: `{'strategy': 'RuleFaith deployable score top-1', 'edit_groups': 23, 'covered_groups': 23, 'coverage': 1.0, 'accept_selected': 9, 'refine_selected': 8, 'reject_selected': 6, 'accept_rate': 0.3913, 'non_reject_rate': 0.7391, 'mean_utility': 0.5652}`
- selective selection: `{'strategy': 'RuleFaith deployable score selective', 'edit_groups': 23, 'covered_groups': 18, 'coverage': 0.7826, 'accept_selected': 7, 'refine_selected': 7, 'reject_selected': 4, 'accept_rate': 0.3889, 'non_reject_rate': 0.7778, 'mean_utility': 0.5833}`
- pairwise accuracy: `0.5` over `4` comparisons

## High-Scoring Pseudo-Rejects

- `rf-edit-0058::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired` score=0.97 bucket=accept pseudo=reject category=lexical_choice features: evidence=1, target_copy=False, false_rat=False
- `rf-edit-0138::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired` score=0.97 bucket=accept pseudo=reject category=lexical_choice features: evidence=2, target_copy=False, false_rat=False
- `rf-edit-0138::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired` score=0.97 bucket=accept pseudo=reject category=lexical_choice features: evidence=2, target_copy=False, false_rat=False
- `rf-edit-0276::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired` score=0.97 bucket=accept pseudo=reject category=articles_determiners features: evidence=1, target_copy=False, false_rat=False
- `rf-edit-0276::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired` score=0.97 bucket=accept pseudo=reject category=articles_determiners features: evidence=1, target_copy=False, false_rat=False

## Low-Scoring Pseudo-Accepts

- `rf-edit-0292::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.42 bucket=reject pseudo=accept category=lexical_choice features: evidence=2, target_copy=False, false_rat=True
- `rf-edit-0023::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` score=0.57 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=True, false_rat=True
- `rf-edit-0023::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.57 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=True, false_rat=True
- `rf-edit-0016::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.66 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=False, false_rat=True
- `rf-edit-0191::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.66 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=False, false_rat=True

## False-Rationalization Flags

- `rf-edit-0016::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.66 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=False, false_rat=True
- `rf-edit-0023::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` score=0.57 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=True, false_rat=True
- `rf-edit-0023::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.57 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=True, false_rat=True
- `rf-edit-0191::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.66 bucket=refine pseudo=accept category=articles_determiners features: evidence=1, target_copy=False, false_rat=True
- `rf-edit-0225::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` score=0.52 bucket=reject pseudo=reject category=lexical_choice features: evidence=1, target_copy=True, false_rat=True
- `rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.5172 bucket=reject pseudo=refine category=articles_determiners features: evidence=1, target_copy=True, false_rat=True
- `rf-edit-0268::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.66 bucket=refine pseudo=refine category=lexical_choice features: evidence=2, target_copy=False, false_rat=True
- `rf-edit-0292::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=0.42 bucket=reject pseudo=accept category=lexical_choice features: evidence=2, target_copy=False, false_rat=True
- `rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired` score=0.66 bucket=refine pseudo=reject category=lexical_choice features: evidence=1, target_copy=False, false_rat=True
- `rf-edit-0255::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired` score=0.66 bucket=refine pseudo=accept category=lexical_choice features: evidence=2, target_copy=False, false_rat=True

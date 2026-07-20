# Qwen3 Codex Prelabel Breakdown

These results are Codex-assisted prelabels for internal triage. They are not human labels and must not be used as human-gold evidence.

## Overall Decisions

- `refine`: 46
- `reject`: 34

## Issue Counts

- `human_alignment_error`: 15
- `human_edit_copy`: 73
- `human_generic_explanation`: 0
- `human_inapplicable_rule`: 25
- `human_missing_evidence`: 79
- `human_semantic_distortion`: 25
- `human_unsupported_confidence`: 80
- `human_validity_error`: 25
- `human_wrong_evidence`: 80
- `human_wrong_rule`: 25

## Decision Breakdown

### bucket

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| accepted | 0 | 21 | 10 | 0 |
| refine | 0 | 25 | 9 | 0 |
| rejected | 0 | 0 | 15 | 0 |

### audit_priority

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| risk | 0 | 46 | 29 | 0 |
| stratum:behavior=correct_correction | 0 | 0 | 1 | 0 |
| stratum:behavior=overcorrection | 0 | 0 | 1 | 0 |
| stratum:behavior=wrong_correction | 0 | 0 | 1 | 0 |
| stratum:bucket=rejected | 0 | 0 | 1 | 0 |
| stratum:model_key=t5_base_grammar | 0 | 0 | 1 | 0 |

### candidate_type

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| natural | 0 | 20 | 17 | 0 |
| rule_grounded | 0 | 26 | 17 | 0 |

### dataset

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| EXPECT | 0 | 28 | 20 | 0 |
| JFLEG | 0 | 18 | 14 | 0 |

### model_key

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| coedit_large | 0 | 9 | 7 | 0 |
| gector_roberta_base | 0 | 23 | 17 | 0 |
| t5_base_grammar | 0 | 14 | 10 | 0 |

### behavior

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| correct_correction | 0 | 24 | 4 | 0 |
| overcorrection | 0 | 15 | 17 | 0 |
| wrong_correction | 0 | 7 | 13 | 0 |

### operation

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| delete | 0 | 5 | 4 | 0 |
| insert | 0 | 6 | 6 | 0 |
| replace | 0 | 35 | 24 | 0 |

### error_type

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| M:DET | 0 | 3 | 2 | 0 |
| M:NOUN:POSS | 0 | 1 | 0 | 0 |
| M:OTHER | 0 | 0 | 2 | 0 |
| M:PUNCT | 0 | 2 | 0 | 0 |
| M:VERB:TENSE | 0 | 0 | 2 | 0 |
| R:ADJ | 0 | 1 | 1 | 0 |
| R:ADV | 0 | 2 | 0 | 0 |
| R:DET | 0 | 0 | 2 | 0 |
| R:MORPH | 0 | 2 | 0 | 0 |
| R:NOUN | 0 | 3 | 4 | 0 |
| R:NOUN:NUM | 0 | 2 | 0 | 0 |
| R:OTHER | 0 | 11 | 4 | 0 |
| R:PREP | 0 | 9 | 2 | 0 |
| R:PRON | 0 | 3 | 0 | 0 |
| R:SPELL | 0 | 0 | 5 | 0 |
| R:VERB:FORM | 0 | 2 | 4 | 0 |
| R:VERB:SVA | 0 | 0 | 2 | 0 |
| U:CONJ | 0 | 0 | 1 | 0 |
| U:DET | 0 | 5 | 3 | 0 |

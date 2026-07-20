# Qwen3 Codex Prelabel Breakdown

These results are Codex-assisted prelabels for internal triage. They are not human labels and must not be used as human-gold evidence.

## Overall Decisions

- `refine`: 44
- `reject`: 36

## Issue Counts

- `human_alignment_error`: 17
- `human_edit_copy`: 71
- `human_generic_explanation`: 0
- `human_inapplicable_rule`: 28
- `human_missing_evidence`: 60
- `human_semantic_distortion`: 28
- `human_unsupported_confidence`: 79
- `human_validity_error`: 28
- `human_wrong_evidence`: 24
- `human_wrong_rule`: 28

## Decision Breakdown

### bucket

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| accepted | 0 | 15 | 10 | 0 |
| refine | 0 | 28 | 9 | 0 |
| rejected | 0 | 1 | 17 | 0 |

### audit_priority

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| risk | 0 | 44 | 31 | 0 |
| stratum:behavior=correct_correction | 0 | 0 | 1 | 0 |
| stratum:behavior=overcorrection | 0 | 0 | 1 | 0 |
| stratum:behavior=wrong_correction | 0 | 0 | 1 | 0 |
| stratum:model_key=coedit_large | 0 | 0 | 1 | 0 |
| stratum:model_key=t5_base_grammar | 0 | 0 | 1 | 0 |

### candidate_type

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| evidence_canonicalized | 0 | 44 | 36 | 0 |

### dataset

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| EXPECT | 0 | 28 | 20 | 0 |
| JFLEG | 0 | 16 | 16 | 0 |

### model_key

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| coedit_large | 0 | 10 | 4 | 0 |
| gector_roberta_base | 0 | 22 | 19 | 0 |
| t5_base_grammar | 0 | 12 | 13 | 0 |

### behavior

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| correct_correction | 0 | 17 | 4 | 0 |
| overcorrection | 0 | 15 | 16 | 0 |
| wrong_correction | 0 | 12 | 16 | 0 |

### operation

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| delete | 0 | 3 | 6 | 0 |
| insert | 0 | 9 | 6 | 0 |
| replace | 0 | 32 | 24 | 0 |

### error_type

| Group | accept | refine | reject | abstain |
|---|---:|---:|---:|---:|
| M:DET | 0 | 5 | 2 | 0 |
| M:NOUN:POSS | 0 | 2 | 0 | 0 |
| M:OTHER | 0 | 2 | 2 | 0 |
| M:PUNCT | 0 | 2 | 0 | 0 |
| M:VERB:TENSE | 0 | 0 | 2 | 0 |
| R:ADJ | 0 | 1 | 1 | 0 |
| R:ADV | 0 | 2 | 0 | 0 |
| R:DET | 0 | 0 | 2 | 0 |
| R:MORPH | 0 | 2 | 0 | 0 |
| R:NOUN | 0 | 2 | 1 | 0 |
| R:OTHER | 0 | 7 | 4 | 0 |
| R:PREP | 0 | 10 | 2 | 0 |
| R:PRON | 0 | 2 | 0 | 0 |
| R:SPELL | 0 | 0 | 8 | 0 |
| R:VERB:FORM | 0 | 2 | 4 | 0 |
| R:VERB:SVA | 0 | 0 | 2 | 0 |
| R:WO | 0 | 2 | 0 | 0 |
| U:CONJ | 0 | 0 | 3 | 0 |
| U:DET | 0 | 3 | 3 | 0 |

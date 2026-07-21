# Qwen3 Structured Evidence Repair

This deterministic repair pass adds source-grounded evidence spans inferred from the edit, error type, and nearby source context. It uses no reference correction, no behavior label for generation, and no human label.

## Summary

- Candidate count: 160
- Decision: `keep_structured_evidence_repair_for_refiner_inputs_not_final_scoring`
- Label source: `deterministic_structured_evidence_repair_not_human_gold`

## Before / After Flag Counts

| Flag | Before | After | Delta |
|---|---:|---:|---:|
| `evidence_contextual` | 82 | 160 | +78 |
| `missing_evidence` | 78 | 0 | -78 |
| `wrong_evidence_auto` | 29 | 0 | -29 |
| `evidence_text_found_in_prediction_only` | 29 | 0 | -29 |
| `edit_copy` | 112 | 112 | +0 |
| `rule_edit_copy` | 0 | 0 | +0 |
| `possible_false_rationalization` | 19 | 19 | +0 |
| `unsupported_confidence` | 131 | 70 | -61 |
| `alignment_error` | 58 | 58 | +0 |
| `validity_error_auto` | 28 | 28 | +0 |

## Repair Actions

- `added_determiner_head_noun`: 24
- `added_left_clause_context`: 4
- `added_left_context`: 68
- `added_modified_token_evidence`: 64
- `added_noun_left_context`: 26
- `added_noun_right_context`: 28
- `added_preposition_complement`: 12
- `added_preposition_governor`: 12
- `added_pronoun_context`: 4
- `added_right_clause_context`: 4
- `added_right_context`: 60
- `added_sva_subject`: 2
- `added_sva_verb`: 2
- `added_verb_left_context`: 12
- `added_verb_right_context`: 12
- `kept_existing_valid_source_spans`: 147

## Stricter Evidence Check

- `specific_source_evidence_before`: 10
- `specific_source_evidence_after`: 124
- `specific_source_evidence_delta`: +114
- `after_generic_context_only`: 36

The stricter count excludes generic left/right context roles. It is the safer number to use when deciding whether a repaired candidate is suitable for a later human audit or positive-data construction.

## Strict RuleFaith Selection

- bucket counts: `{'accepted': 0, 'refine': 58, 'rejected': 102}`
- reason counts: `{'alignment_error': 58, 'edit_copy': 58, 'generic_explanation': 1, 'missing_rule': 1, 'no_specific_source_evidence': 36, 'parse_not_json': 1, 'possible_false_rationalization': 19, 'validity_error_auto': 28}`

This stricter gate is intentionally more conservative than `filter_teacher_candidates.py`: it treats false rationalization, validity errors, alignment errors, and lack of specific source evidence as hard failures. Edit-copy and unsupported-confidence risks are routed to `refine`, not direct `accepted`.


## Examples With Improved Contextual Evidence

### rf-edit-0016::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- error type: `U:DET`
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 12, "text": "and they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`
- actions: `{'added_determiner_head_noun': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0016::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- error type: `U:DET`
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 13, "text": "they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`
- actions: `{'added_determiner_head_noun': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0021::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I was very fast , my best time was 5 5 seconds in 4 0 0 hundred meters is a good time in or country . 
- edit: `replace` `or` -> `the`
- error type: `R:OTHER`
- evidence: `[{"end": 25, "role": "error", "source": "kept_existing", "start": 23, "text": "or country"}, {"end": 22, "role": "left_context", "source": "structured_heuristic", "start": 21, "text": "time"}, {"end": 25, "role": "right_context", "source": "structured_heuristic", "start": 24, "text": "country"}]`
- actions: `{'added_left_context': 1, 'added_right_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0021::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: I was very fast , my best time was 5 5 seconds in 4 0 0 hundred meters is a good time in or country . 
- edit: `replace` `or` -> `the`
- error type: `R:OTHER`
- evidence: `[{"end": 25, "role": "error_span", "source": "kept_existing", "start": 22, "text": "in or country"}, {"end": 22, "role": "left_context", "source": "structured_heuristic", "start": 21, "text": "time"}, {"end": 25, "role": "right_context", "source": "structured_heuristic", "start": 24, "text": "country"}]`
- actions: `{'added_left_context': 1, 'added_right_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0023::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- error type: `R:WO`
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`
- actions: `{'added_determiner_head_noun': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0023::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- error type: `R:WO`
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`
- actions: `{'added_determiner_head_noun': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0024::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer cars in use than there are today . 
- edit: `insert` `` -> `,`
- error type: `M:PUNCT`
- evidence: `[{"end": 26, "role": "source", "source": "kept_existing", "start": 0, "text": "Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer cars in use than there are today ."}, {"end": 1, "role": "left_context", "source": "structured_heuristic", "start": 0, "text": "Thus"}, {"end": 3, "role": "right_context", "source": "structured_heuristic", "start": 2, "text": "concordance"}]`
- actions: `{'added_left_context': 1, 'added_right_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0024::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer cars in use than there are today . 
- edit: `insert` `` -> `,`
- error type: `M:PUNCT`
- evidence: `[{"end": 26, "role": "source", "source": "kept_existing", "start": 0, "text": "Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer cars in use than there are today ."}, {"end": 1, "role": "left_context", "source": "structured_heuristic", "start": 0, "text": "Thus"}, {"end": 3, "role": "right_context", "source": "structured_heuristic", "start": 2, "text": "concordance"}]`
- actions: `{'added_left_context': 1, 'added_right_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0025::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- edit: `delete` `the` -> ``
- error type: `U:DET`
- evidence: `[{"end": 10, "role": "head_noun", "source": "structured_heuristic", "start": 9, "text": "people"}]`
- actions: `{'added_determiner_head_noun': 1}`

### rf-edit-0025::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- edit: `delete` `the` -> ``
- error type: `U:DET`
- evidence: `[{"end": 10, "role": "head_noun", "source": "structured_heuristic", "start": 9, "text": "people"}]`
- actions: `{'added_determiner_head_noun': 1}`

### rf-edit-0026::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: It is true that consumers preffer to buy a product that has a lower price , but when international companies that has already the certification begins to send its market , people will preffer to consume theirs because the difference between prices is probbably not going to affect them to much . 
- edit: `replace` `its` -> `their`
- error type: `R:DET`
- evidence: `[{"end": 29, "role": "pronoun", "source": "kept_existing", "start": 28, "text": "its"}, {"end": 30, "role": "head_noun", "source": "structured_heuristic", "start": 29, "text": "market"}]`
- actions: `{'added_determiner_head_noun': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0033::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- edit: `delete` `the` -> ``
- error type: `U:DET`
- evidence: `[{"end": 36, "role": "head_noun", "source": "structured_heuristic", "start": 35, "text": "pollution"}]`
- actions: `{'added_determiner_head_noun': 1}`

### rf-edit-0033::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- edit: `delete` `the` -> ``
- error type: `U:DET`
- evidence: `[{"end": 36, "role": "head_noun", "source": "structured_heuristic", "start": 35, "text": "pollution"}]`
- actions: `{'added_determiner_head_noun': 1}`

### rf-edit-0034::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car . 
- edit: `replace` `pot` -> `potting`
- error type: `R:VERB:FORM`
- evidence: `[{"end": 15, "role": "error", "source": "kept_existing", "start": 14, "text": "pot"}, {"end": 14, "role": "verb_context", "source": "structured_heuristic", "start": 13, "text": "like"}, {"end": 16, "role": "verb_complement_or_time_context", "source": "structured_heuristic", "start": 15, "text": "taire"}]`
- actions: `{'added_verb_left_context': 1, 'added_verb_right_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0034::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car . 
- edit: `replace` `pot` -> `potting`
- error type: `R:VERB:FORM`
- evidence: `[{"end": 15, "role": "error", "source": "kept_existing", "start": 14, "text": "pot"}, {"end": 14, "role": "verb_context", "source": "structured_heuristic", "start": 13, "text": "like"}, {"end": 16, "role": "verb_complement_or_time_context", "source": "structured_heuristic", "start": 15, "text": "taire"}]`
- actions: `{'added_verb_left_context': 1, 'added_verb_right_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .
- edit: `insert` `` -> `'`
- error type: `M:NOUN:POSS`
- evidence: `[{"end": 17, "role": "noun_number_context", "source": "structured_heuristic", "start": 16, "text": "peoples"}, {"end": 18, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 17, "text": "lives"}]`
- actions: `{'added_noun_left_context': 1, 'added_noun_right_context': 1}`

### rf-edit-0035::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .
- edit: `insert` `` -> `'`
- error type: `M:NOUN:POSS`
- evidence: `[{"end": 17, "role": "noun_number_context", "source": "structured_heuristic", "start": 16, "text": "peoples"}, {"end": 18, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 17, "text": "lives"}]`
- actions: `{'added_noun_left_context': 1, 'added_noun_right_context': 1}`

### rf-edit-0039::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I took the sun a very long time and then I went to a cafe and and I drank a drink .
- edit: `delete` `and` -> ``
- error type: `U:CONJ`
- evidence: `[{"end": 16, "role": "redundant_conjunction", "source": "kept_existing", "start": 15, "text": "and"}, {"end": 15, "role": "left_clause_context", "source": "structured_heuristic", "start": 14, "text": "cafe"}, {"end": 18, "role": "right_clause_context", "source": "structured_heuristic", "start": 17, "text": "I"}]`
- actions: `{'added_left_clause_context': 1, 'added_right_clause_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0039::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: I took the sun a very long time and then I went to a cafe and and I drank a drink .
- edit: `delete` `and` -> ``
- error type: `U:CONJ`
- evidence: `[{"end": 16, "role": "redundant_conjunction", "source": "kept_existing", "start": 15, "text": "and"}, {"end": 15, "role": "left_clause_context", "source": "structured_heuristic", "start": 14, "text": "cafe"}, {"end": 18, "role": "right_clause_context", "source": "structured_heuristic", "start": 17, "text": "I"}]`
- actions: `{'added_left_clause_context': 1, 'added_right_clause_context': 1, 'kept_existing_valid_source_spans': 1}`

### rf-edit-0051::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- error type: `R:PREP`
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`
- actions: `{'added_preposition_governor': 1, 'added_preposition_complement': 1}`

Additional improved cases are available in the JSONL output.

## Limitations

- Automatic source evidence repair does not prove the rule is linguistically correct.
- The repaired candidates remain pseudo-labelled artifacts, not human-gold data.
- Edit-validity and false-rationalization risks require a separate verifier.

# Round 04 Model Edit and Explanation Audit

This is a researcher-readable automatic audit, not human annotation. It flags likely extraction, alignment, detokenization, and explanation-quality issues for manual review.

## Summary

- Audited rows: 60
- Model counts: `{"gector_roberta_base": 31, "t5_base_grammar": 29}`
- Behavior counts: `{"correct_correction": 19, "overcorrection": 26, "wrong_correction": 15}`
- Operation counts: `{"delete": 8, "insert": 12, "replace": 40}`
- ORTH/PUNCT noise flags: 17
- Generic explanation flags: 7

## 1. expect-test-00000::gector_roberta_base::0::8-9

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Reference: `In my community , we are very interested in the environment and ecological things .`
- Prediction: `In my community , we are very interested in the environment and ecological things .`
- Predicted edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- Aligned reference edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- FLAN explanation: `The verb ' syllable '' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": false, "orth_or_punct_noise_auto": false}`

## 2. expect-test-00001::gector_roberta_base::11::70-71

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- Aligned reference edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 3. expect-test-00002::gector_roberta_base::12::3-4

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Predicted edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- Aligned reference edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- FLAN explanation: `The word ' car' refers to a vehicle that has a lot of cars in it .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 4. expect-test-00003::gector_roberta_base::18::10-11

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `Although there are many positive points about private cars , they are also negative ones .`
- Reference: `Although there are many positive points about private cars , there are also negative ones .`
- Prediction: `Although there are many positive points about private cars , there are also negative ones .`
- Predicted edit: `{"end": 11, "error_type": "R:PRON", "operation": "replace", "source_text": "they", "start": 10, "target_text": "there"}`
- Aligned reference edit: `{"end": 11, "error_type": "R:PRON", "operation": "replace", "source_text": "they", "start": 10, "target_text": "there"}`
- FLAN explanation: `The word ' , ' " , is a syllable meaning '' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": false, "orth_or_punct_noise_auto": false}`

## 5. expect-test-00004::gector_roberta_base::19::22-23

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting travel for then to see more action .`
- Reference: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey for then to see more action .`
- Prediction: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey , then to see more action .`
- Predicted edit: `{"end": 23, "error_type": "R:NOUN", "operation": "replace", "source_text": "travel", "start": 22, "target_text": "journey"}`
- Aligned reference edit: `{"end": 23, "error_type": "R:NOUN", "operation": "replace", "source_text": "travel", "start": 22, "target_text": "journey"}`
- FLAN explanation: `The following is a list of public transportation in the United States :`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": true, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 6. expect-test-00006::gector_roberta_base::23::7-8

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `I hope my house will win the champion next year .`
- Reference: `I hope my house will win the championship next year .`
- Prediction: `I hope my house will win the championship next year .`
- Predicted edit: `{"end": 8, "error_type": "R:MORPH", "operation": "replace", "source_text": "champion", "start": 7, "target_text": "championship"}`
- Aligned reference edit: `{"end": 8, "error_type": "R:MORPH", "operation": "replace", "source_text": "champion", "start": 7, "target_text": "championship"}`
- FLAN explanation: `The verb should agree with the singular subject.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": true, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": false, "orth_or_punct_noise_auto": false}`

## 7. expect-test-00011::gector_roberta_base::40::5-6

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `What a wonderful day ! There is April now and finally spring has come .`
- Reference: `What a wonderful day ! It is April now and finally spring has come .`
- Prediction: `What a wonderful day ! It is April now and finally spring has come .`
- Predicted edit: `{"end": 6, "error_type": "R:PRON", "operation": "replace", "source_text": "There", "start": 5, "target_text": "It"}`
- Aligned reference edit: `{"end": 6, "error_type": "R:PRON", "operation": "replace", "source_text": "There", "start": 5, "target_text": "It"}`
- FLAN explanation: `The sentence ' ' is a rephrasing of the phrase '' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": false, "orth_or_punct_noise_auto": false}`

## 8. expect-test-00012::gector_roberta_base::41::7-8

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `The traffic can affect cars and buses at the same extent .`
- Reference: `The traffic can affect cars and buses to the same extent .`
- Prediction: `The traffic can affect cars and buses to the same extent .`
- Predicted edit: `{"end": 8, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 7, "target_text": "to"}`
- Aligned reference edit: `{"end": 8, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 7, "target_text": "to"}`
- FLAN explanation: `The sentence ' ' is a rephrasing of the original sentence " .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": false, "orth_or_punct_noise_auto": false}`

## 9. expect-test-00013::gector_roberta_base::43::8-9

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .`
- Reference: `Computers have had a most significant impact on people in the latter 1/2 of the 20th century .`
- Prediction: `Computers have had the most significant impact on people in the latter 1/2 of the 20th century .`
- Predicted edit: `{"end": 9, "error_type": "U:DET", "operation": "delete", "source_text": "the", "start": 8, "target_text": ""}`
- Aligned reference edit: `{"end": 9, "error_type": "U:DET", "operation": "delete", "source_text": "the", "start": 8, "target_text": ""}`
- FLAN explanation: `The word ' , ' or ' " , comes from the Greek word .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 10. expect-test-00014::gector_roberta_base::47::10-11

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Source: `i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Reference: `i love my family especially my little sister , she is sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Prediction: `I love my family , especially my little sister . She is sixteen years old . I consider her my best friend because I usually tell her everything about my life .`
- Predicted edit: `{"end": 11, "error_type": "R:VERB", "operation": "replace", "source_text": "has", "start": 10, "target_text": "is"}`
- Aligned reference edit: `{"end": 11, "error_type": "R:VERB", "operation": "replace", "source_text": "has", "start": 10, "target_text": "is"}`
- FLAN explanation: `The sentence ' ' I love my family , especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 11. expect-test-00005::gector_roberta_base::21::10-10

- Model: `gector_roberta_base`
- Behavior: `wrong_correction`
- Source: `They were planning to steal a very precious thing from Museum tonight .`
- Reference: `They were planning to steal a very precious thing from a Museum tonight .`
- Prediction: `They were planning to steal a very precious thing from the museum tonight .`
- Predicted edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "the"}`
- Aligned reference edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "a"}`
- FLAN explanation: `The word ' , ' or ' " , is a syllable meaning '' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 12. expect-test-00008::gector_roberta_base::27::10-11

- Model: `gector_roberta_base`
- Behavior: `wrong_correction`
- Source: `I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Reference: `I 'd like to tell you about my favorite restaurant . It 's name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Prediction: `I 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Predicted edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "replace", "source_text": "its", "start": 10, "target_text": ". Its"}`
- Aligned reference edit: `{"end": 10, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 10, "target_text": "."}`
- FLAN explanation: `A restaurant is a place to eat .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 13. expect-test-00021::gector_roberta_base::63::8-9

- Model: `gector_roberta_base`
- Behavior: `wrong_correction`
- Source: `Additionally , people now continue to destroy more agricultures and forest in order to satisfy all their needs , which will distory the ecosystem diversity and biodiversity especially the endangered species .`
- Reference: `Additionally , people now continue to destroy more agricultural land and forest in order to satisfy all their needs , which will distory the ecosystem diversity and biodiversity especially the endangered species .`
- Prediction: `Additionally , people now continue to destroy more agriculture and forests in order to satisfy all their needs , which will distory the ecosystem diversity and biodiversity , especially the endangered species .`
- Predicted edit: `{"end": 9, "error_type": "R:NOUN:INFL", "operation": "replace", "source_text": "agricultures", "start": 8, "target_text": "agriculture"}`
- Aligned reference edit: `{"end": 9, "error_type": "R:SPELL", "operation": "replace", "source_text": "agricultures", "start": 8, "target_text": "agricultural"}`
- FLAN explanation: `The sentence ' ' is a rephrasing of the original sentence " .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 14. expect-test-00028::gector_roberta_base::76::19-23

- Model: `gector_roberta_base`
- Behavior: `wrong_correction`
- Source: `A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .`
- Reference: `A worldwide war is the only case in which we would see a dramatic change in peoples lives in the period of 50 years from now .`
- Prediction: `A worldwide war is the only case in which we will see a dramatic change in peoples ' lives in 50 years from now .`
- Predicted edit: `{"end": 23, "error_type": "U:OTHER", "operation": "delete", "source_text": "the time length of", "start": 19, "target_text": ""}`
- Aligned reference edit: `{"end": 22, "error_type": "R:NOUN", "operation": "replace", "source_text": "time length", "start": 20, "target_text": "period"}`
- FLAN explanation: `The word " change " is a syllable that refers to a change in a person 's lives in the time span of 50 years from now .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 15. expect-test-00059::gector_roberta_base::145::3-4

- Model: `gector_roberta_base`
- Behavior: `wrong_correction`
- Source: `If I have not mobile I will not be able to work .`
- Reference: `If I have no mobile I will not be able to work .`
- Prediction: `If I had a mobile , I would not be able to work .`
- Predicted edit: `{"end": 4, "error_type": "R:OTHER", "operation": "replace", "source_text": "not", "start": 3, "target_text": "a"}`
- Aligned reference edit: `{"end": 4, "error_type": "R:OTHER", "operation": "replace", "source_text": "not", "start": 3, "target_text": "no"}`
- FLAN explanation: `The word ' mobile ' is a grammatical form of the verb ' work ' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 16. expect-test-00001::gector_roberta_base::1::2-3

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 3, "error_type": "R:SPELL", "operation": "replace", "source_text": "chanched", "start": 2, "target_text": "changed"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 17. expect-test-00001::gector_roberta_base::2::11-11

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 11, "target_text": ","}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 18. expect-test-00001::gector_roberta_base::3::14-14

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 14, "error_type": "M:PREP", "operation": "insert", "source_text": "", "start": 14, "target_text": "about"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 19. expect-test-00001::gector_roberta_base::4::16-17

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 17, "error_type": "U:VERB", "operation": "delete", "source_text": "is", "start": 16, "target_text": ""}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 20. expect-test-00001::gector_roberta_base::5::18-19

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 19, "error_type": "R:OTHER", "operation": "replace", "source_text": "life", "start": 18, "target_text": "lives are"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 21. expect-test-00001::gector_roberta_base::6::33-33

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 33, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 33, "target_text": ","}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 22. expect-test-00001::gector_roberta_base::7::38-39

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 39, "error_type": "R:ORTH", "operation": "replace", "source_text": "tv", "start": 38, "target_text": "TV"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 23. expect-test-00001::gector_roberta_base::8::45-46

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 46, "error_type": "R:ORTH", "operation": "replace", "source_text": "tv", "start": 45, "target_text": "TV"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 24. expect-test-00001::gector_roberta_base::9::52-52

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 52, "error_type": "M:NOUN", "operation": "insert", "source_text": "", "start": 52, "target_text": "children"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 25. expect-test-00001::gector_roberta_base::10::52-54

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Predicted edit: `{"end": 54, "error_type": "R:OTHER", "operation": "replace", "source_text": "young.but that", "start": 52, "target_text": ". That"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people 's lives a lot .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": true, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 26. expect-test-00000::t5_base_grammar::673::8-9

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Reference: `In my community , we are very interested in the environment and ecological things .`
- Prediction: `In my community, we are very interested in the environment and ecological things.`
- Predicted edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- Aligned reference edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- FLAN explanation: `The word ' , ' or ' " , is a grammatical form of the verb '' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 27. expect-test-00001::t5_base_grammar::691::70-71

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- Aligned reference edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 28. expect-test-00002::t5_base_grammar::693::3-4

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transportation because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world.`
- Predicted edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- Aligned reference edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- FLAN explanation: `The first sentence of a sentence refers to a single word.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 29. expect-test-00006::t5_base_grammar::705::7-8

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `I hope my house will win the champion next year .`
- Reference: `I hope my house will win the championship next year .`
- Prediction: `I hope my house will win the championship next year.`
- Predicted edit: `{"end": 8, "error_type": "R:MORPH", "operation": "replace", "source_text": "champion", "start": 7, "target_text": "championship"}`
- Aligned reference edit: `{"end": 8, "error_type": "R:MORPH", "operation": "replace", "source_text": "champion", "start": 7, "target_text": "championship"}`
- FLAN explanation: `The verb should agree with the singular subject.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": true, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 30. expect-test-00009::t5_base_grammar::720::17-17

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `But such a high level of development of Egyptian civilization has a negative side as well as positive .`
- Reference: `But such a high level of development of Egyptian civilization has a negative side as well as a positive .`
- Prediction: `There is a high level of development of Egyptian civilization, but there is a negative side as well as a positive side.`
- Predicted edit: `{"end": 17, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 17, "target_text": "a"}`
- Aligned reference edit: `{"end": 17, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 17, "target_text": "a"}`
- FLAN explanation: `The first sentence of the second sentence is a description of a person.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 31. expect-test-00014::t5_base_grammar::742::10-11

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Reference: `i love my family especially my little sister , she is sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Prediction: `i love my family, especially my little sister, who is sixteen years old, and I consider her my best friend because I usually tell her everything about my life.`
- Predicted edit: `{"end": 11, "error_type": "R:VERB", "operation": "replace", "source_text": "has", "start": 10, "target_text": "is"}`
- Aligned reference edit: `{"end": 11, "error_type": "R:VERB", "operation": "replace", "source_text": "has", "start": 10, "target_text": "is"}`
- FLAN explanation: `The first sentence of the sentence refers to a person or group of people .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 32. expect-test-00018::t5_base_grammar::759::25-26

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .`
- Reference: `I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring for the environment is very important and in my village they take different actions to care for it .`
- Prediction: `I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring for the environment is very important and in my village they take different actions to care for it.`
- Predicted edit: `{"end": 26, "error_type": "R:PREP", "operation": "replace", "source_text": "of", "start": 25, "target_text": "for"}`
- Aligned reference edit: `{"end": 26, "error_type": "R:PREP", "operation": "replace", "source_text": "of", "start": 25, "target_text": "for"}`
- FLAN explanation: `The first sentence of the second sentence is a rephrasing of the first sentence: " I live in San Miguel Almoloyan " .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 33. expect-test-00022::t5_base_grammar::771::14-15

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `The city has many projects such as " Keep it clean , keep it beauty " , the goal of which is to promote proper disposal in the public areas .`
- Reference: `The city has many projects such as " Keep it clean , keep it beautiful " , the goal of which is to promote proper disposal in the public areas .`
- Prediction: `The city has many projects such as " Keep it clean , keep it beautiful ", the goal of which is to promote proper disposal in the public areas.`
- Predicted edit: `{"end": 15, "error_type": "R:MORPH", "operation": "replace", "source_text": "beauty", "start": 14, "target_text": "beautiful"}`
- Aligned reference edit: `{"end": 15, "error_type": "R:MORPH", "operation": "replace", "source_text": "beauty", "start": 14, "target_text": "beautiful"}`
- FLAN explanation: `The sentence "Keep it clean , keep it beautiful " , the goal of which is to promote proper disposal in the public areas .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 34. expect-test-00038::t5_base_grammar::812::5-6

- Model: `t5_base_grammar`
- Behavior: `correct_correction`
- Source: `which play an important role to giving tough competition to the government . as a result of this consumer gets more benefits , like lower faire , privacy , freedom and safe travelling.in addition many automobile companies launcing new cars at affordable prices , which encourages people to use more and more private vechile .`
- Reference: `which play an important role in giving tough competition to the government . as a result of this consumer gets more benefits , like lower faire , privacy , freedom and safe travelling.in addition many automobile companies launcing new cars at affordable prices , which encourages people to use more and more private vechile .`
- Prediction: `which play an important role in giving tough competition to the government . as a result of this consumer gets more benefits, like lower faire , privacy , freedom and safe travelling.in addition, many automobile companies are launcing new cars at affordable prices, which encourages people to use more and more private vehicles.`
- Predicted edit: `{"end": 6, "error_type": "R:PREP", "operation": "replace", "source_text": "to", "start": 5, "target_text": "in"}`
- Aligned reference edit: `{"end": 6, "error_type": "R:PREP", "operation": "replace", "source_text": "to", "start": 5, "target_text": "in"}`
- FLAN explanation: `The first sentence of the second sentence is a rephrasing of the first sentence.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 35. expect-test-00005::t5_base_grammar::703::10-10

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `They were planning to steal a very precious thing from Museum tonight .`
- Reference: `They were planning to steal a very precious thing from a Museum tonight .`
- Prediction: `Then, they were planning to steal a very precious thing from the museum tonight.`
- Predicted edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "the"}`
- Aligned reference edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "a"}`
- FLAN explanation: `The word 'symbol' is a contraction of the verb ''.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 36. expect-test-00011::t5_base_grammar::727::4-6

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `What a wonderful day ! There is April now and finally spring has come .`
- Reference: `What a wonderful day ! It is April now and finally spring has come .`
- Prediction: `Then, there is April now, and finally spring has come.`
- Predicted edit: `{"end": 6, "error_type": "U:PUNCT", "operation": "replace", "source_text": "! There", "start": 4, "target_text": "there"}`
- Aligned reference edit: `{"end": 6, "error_type": "R:PRON", "operation": "replace", "source_text": "There", "start": 5, "target_text": "It"}`
- FLAN explanation: `The word ' spring ' is a syllable meaning ' now ' or ' then ' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 37. expect-test-00016::t5_base_grammar::753::13-14

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `In the end I think if many people want the Monarchy to be ablished a general election should be called and then see if the Monarchy should be abolished .`
- Reference: `In the end I think if many people want the Monarchy to be abolished , a general election should be called and then see if the Monarchy should be abolished .`
- Prediction: `In the end, I think if many people want the monarchy to be established, a general election should be called and then see if the monarchy should be abolished.`
- Predicted edit: `{"end": 14, "error_type": "R:SPELL", "operation": "replace", "source_text": "ablished", "start": 13, "target_text": "established,"}`
- Aligned reference edit: `{"end": 14, "error_type": "R:SPELL", "operation": "replace", "source_text": "ablished", "start": 13, "target_text": "abolished"}`
- FLAN explanation: `A general election should be called and then see if the monarchy should be abolished.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 38. expect-test-00020::t5_base_grammar::764::19-21

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `First , the scene that described the murder makes readers unable to stop themselves imagining the images in their mind .`
- Reference: `First , the scene that described the murder makes readers unable to stop themselves imagining the images in their minds .`
- Prediction: `First, the scene that described the murder makes readers unable to stop themselves imagining the images in their mind.`
- Predicted edit: `{"end": 21, "error_type": "R:ORTH", "operation": "replace", "source_text": "mind .", "start": 19, "target_text": "mind."}`
- Aligned reference edit: `{"end": 20, "error_type": "R:NOUN:NUM", "operation": "replace", "source_text": "mind", "start": 19, "target_text": "minds"}`
- FLAN explanation: `The sentence that describes the murder makes readers unable to stop themselves imagining the images in their mind .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 39. expect-test-00021::t5_base_grammar::766::8-9

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `Additionally , people now continue to destroy more agricultures and forest in order to satisfy all their needs , which will distory the ecosystem diversity and biodiversity especially the endangered species .`
- Reference: `Additionally , people now continue to destroy more agricultural land and forest in order to satisfy all their needs , which will distory the ecosystem diversity and biodiversity especially the endangered species .`
- Prediction: `Additionally, people now continue to destroy more agriculture and forest in order to satisfy all their needs, which will discredit the ecosystem diversity and biodiversity, especially the endangered species.`
- Predicted edit: `{"end": 9, "error_type": "R:NOUN:INFL", "operation": "replace", "source_text": "agricultures", "start": 8, "target_text": "agriculture"}`
- Aligned reference edit: `{"end": 9, "error_type": "R:SPELL", "operation": "replace", "source_text": "agricultures", "start": 8, "target_text": "agricultural"}`
- FLAN explanation: `The word 'symbol' is derived from the Greek word .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 40. expect-test-00027::t5_base_grammar::784::7-9

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `Everyone should develop their awareness of public manner .`
- Reference: `Everyone should develop their awareness of public manners .`
- Prediction: `The goal is to develop their awareness of the public manner.`
- Predicted edit: `{"end": 9, "error_type": "R:ORTH", "operation": "replace", "source_text": "manner .", "start": 7, "target_text": "manner."}`
- Aligned reference edit: `{"end": 8, "error_type": "R:NOUN:NUM", "operation": "replace", "source_text": "manner", "start": 7, "target_text": "manners"}`
- FLAN explanation: `The sentence ' , ' the , is a contraction of the verb '' .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 41. expect-test-00028::t5_base_grammar::785::21-22

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .`
- Reference: `A worldwide war is the only case in which we would see a dramatic change in peoples lives in the period of 50 years from now .`
- Prediction: `A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time period of 50 years from now.`
- Predicted edit: `{"end": 22, "error_type": "R:NOUN", "operation": "replace", "source_text": "length", "start": 21, "target_text": "period"}`
- Aligned reference edit: `{"end": 22, "error_type": "R:NOUN", "operation": "replace", "source_text": "time length", "start": 20, "target_text": "period"}`
- FLAN explanation: `The first sentence of the sentence refers to a person or group of people who are living in a particular area of the world .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 42. expect-test-00030::t5_base_grammar::790::0-4

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `You can it the best burgers you have ever eaten .`
- Reference: `You can eat the best burgers you have ever eaten .`
- Prediction: `The best burgers you have ever eaten.`
- Predicted edit: `{"end": 4, "error_type": "U:OTHER", "operation": "replace", "source_text": "You can it the", "start": 0, "target_text": "The"}`
- Aligned reference edit: `{"end": 3, "error_type": "R:OTHER", "operation": "replace", "source_text": "it", "start": 2, "target_text": "eat"}`
- FLAN explanation: `The word 'b' is a contraction of the verb 'c' and 'd 'e '.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 43. expect-test-00031::t5_base_grammar::792::0-1

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `Being back to our everyday life .`
- Reference: `Coming back to our everyday life .`
- Prediction: `We are back to our everyday life.`
- Predicted edit: `{"end": 1, "error_type": "R:OTHER", "operation": "replace", "source_text": "Being", "start": 0, "target_text": "We are"}`
- Aligned reference edit: `{"end": 1, "error_type": "R:VERB", "operation": "replace", "source_text": "Being", "start": 0, "target_text": "Coming"}`
- FLAN explanation: `The word 'return' refers to a change in the meaning of the verb 'to return '.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 44. expect-test-00035::t5_base_grammar::801::9-10

- Model: `t5_base_grammar`
- Behavior: `wrong_correction`
- Source: `The last time who I was there I have eat the best pizza that I have ever eaten in my life .`
- Reference: `The last time who I was there I ate the best pizza that I have ever eaten in my life .`
- Prediction: `The last time I was there, I have eaten the best pizza that I have ever eaten in my life.`
- Predicted edit: `{"end": 10, "error_type": "R:VERB:FORM", "operation": "replace", "source_text": "eat", "start": 9, "target_text": "eaten"}`
- Aligned reference edit: `{"end": 10, "error_type": "R:VERB:TENSE", "operation": "replace", "source_text": "have eat", "start": 8, "target_text": "ate"}`
- FLAN explanation: `The verb should agree with the singular subject.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": true, "explanation_mentions_error_type_hint": true, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 45. expect-test-00000::t5_base_grammar::672::2-4

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Reference: `In my community , we are very interested in the environment and ecological things .`
- Prediction: `In my community, we are very interested in the environment and ecological things.`
- Predicted edit: `{"end": 4, "error_type": "R:ORTH", "operation": "replace", "source_text": "community ,", "start": 2, "target_text": "community,"}`
- Aligned reference edit: `null`
- FLAN explanation: `The verb should agree with the singular subject .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": true, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 46. expect-test-00000::t5_base_grammar::674::13-15

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Reference: `In my community , we are very interested in the environment and ecological things .`
- Prediction: `In my community, we are very interested in the environment and ecological things.`
- Predicted edit: `{"end": 15, "error_type": "R:ORTH", "operation": "replace", "source_text": "things .", "start": 13, "target_text": "things."}`
- Aligned reference edit: `null`
- FLAN explanation: `The verb ' syllable '' , ' " , is a noun .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 47. expect-test-00001::t5_base_grammar::675::2-3

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 3, "error_type": "R:SPELL", "operation": "replace", "source_text": "chanched", "start": 2, "target_text": "changed"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 48. expect-test-00001::t5_base_grammar::676::3-5

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 5, "error_type": "R:ORTH", "operation": "replace", "source_text": "people 's", "start": 3, "target_text": "people's"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 49. expect-test-00001::t5_base_grammar::677::7-9

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 9, "error_type": "R:ORTH", "operation": "replace", "source_text": "lot .", "start": 7, "target_text": "lot."}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 50. expect-test-00001::t5_base_grammar::678::10-11

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 11, "error_type": "R:NOUN", "operation": "replace", "source_text": "fact", "start": 10, "target_text": "fact,"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 51. expect-test-00001::t5_base_grammar::679::14-14

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 14, "error_type": "M:PREP", "operation": "insert", "source_text": "", "start": 14, "target_text": "about"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 52. expect-test-00001::t5_base_grammar::680::16-17

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 17, "error_type": "U:VERB", "operation": "delete", "source_text": "is", "start": 16, "target_text": ""}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 53. expect-test-00001::t5_base_grammar::681::18-19

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 19, "error_type": "R:OTHER", "operation": "replace", "source_text": "life", "start": 18, "target_text": "lives are"}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 54. expect-test-00001::t5_base_grammar::682::20-21

- Model: `t5_base_grammar`
- Behavior: `overcorrection`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Predicted edit: `{"end": 21, "error_type": "U:CONJ", "operation": "delete", "source_text": "either", "start": 20, "target_text": ""}`
- Aligned reference edit: `null`
- FLAN explanation: `Technology has changed people's lives a lot.`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 55. expect-test-00002::gector_roberta_base::13::7-7

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Predicted edit: `{"end": 7, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 7, "target_text": ","}`
- Aligned reference edit: `null`
- FLAN explanation: `The word ' car' refers to a vehicle that has a lot of cars in it .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 56. expect-test-00002::gector_roberta_base::14::8-9

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Predicted edit: `{"end": 9, "error_type": "U:DET", "operation": "delete", "source_text": "the", "start": 8, "target_text": ""}`
- Aligned reference edit: `null`
- FLAN explanation: `The word ' car ' is a grammatical term for a car .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`

## 57. expect-test-00002::gector_roberta_base::15::10-10

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Predicted edit: `{"end": 10, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 10, "target_text": ","}`
- Aligned reference edit: `null`
- FLAN explanation: `The word ' car' refers to a vehicle that has a lot of cars in it .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 58. expect-test-00002::gector_roberta_base::16::22-22

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Predicted edit: `{"end": 22, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 22, "target_text": ","}`
- Aligned reference edit: `null`
- FLAN explanation: `The following is a list of words that have the same meaning :`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": true, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 59. expect-test-00002::gector_roberta_base::17::23-23

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Predicted edit: `{"end": 23, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 23, "target_text": ","}`
- Aligned reference edit: `null`
- FLAN explanation: `The following is a list of words that have the same meaning:`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": false, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": true, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": false, "explanation_mentions_target_text": false, "explanation_omits_key_condition_auto": true, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": true}`

## 60. expect-test-00004::gector_roberta_base::20::23-24

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Source: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting travel for then to see more action .`
- Reference: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey for then to see more action .`
- Prediction: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey , then to see more action .`
- Predicted edit: `{"end": 24, "error_type": "R:OTHER", "operation": "replace", "source_text": "for", "start": 23, "target_text": ","}`
- Aligned reference edit: `null`
- FLAN explanation: `Public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey , then to see more action .`
- Automatic audit flags: `{"audit_type": "researcher_readable_automatic_audit_not_human_annotation", "behavior_label_auto_consistent": true, "edit_boundary_auto_check": "pass", "edit_extraction_source_span_matches_auto": true, "explanation_corresponds_to_current_edit_auto": true, "explanation_directly_restates_target_auto": false, "explanation_generic_auto": false, "explanation_mentions_error_type_hint": false, "explanation_mentions_operation_hint": false, "explanation_mentions_source_text": true, "explanation_mentions_target_text": true, "explanation_omits_key_condition_auto": false, "explanation_repeats_prediction_clause_auto": false, "explanation_rule_correctness_auto": "unknown_requires_human", "multi_edit_sentence": true, "orth_or_punct_noise_auto": false}`


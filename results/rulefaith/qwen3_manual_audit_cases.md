# Qwen3-8B Manual Audit Cases

## Loop Setup

- Loop ID: Loop A / Qwen3-8B candidate audit
- Current bottleneck: evidence grounding and false-rationalization risk in natural teacher candidates.
- Hypothesis: the current prefilter accepts some useful Qwen3 candidates, but automatic flags will reveal evidence-span and validity risks that must be audited before targeted refinement.
- Required evidence: stratified manual audit file plus automatic leakage/span/rule/evidence/rationalization checks.
- Success criterion: no generator-input leakage; audit file covers accepted/refine/rejected, EXPECT/JFLEG, all corrector families, operations, and behaviors.
- Failure criterion: reference/human-label leakage or pervasive span/evidence failures that make candidates unusable without prompt/verifier repair.

## Summary

- Candidate count: 160
- Selected for manual audit: 80
- Bucket counts: `{'accepted': 41, 'refine': 63, 'rejected': 56}`
- Flag counts: `{'leakage_input_violation': 0, 'source_span_match': 160, 'target_present_in_prediction': 160, 'evidence_span_index_match': 48, 'evidence_all_spans_source_index_match': 20, 'evidence_text_found_in_source': 144, 'evidence_text_found_in_prediction_only': 87, 'evidence_contextual': 24, 'missing_evidence': 136, 'wrong_evidence_auto': 141, 'missing_rule': 1, 'rule_edit_copy': 0, 'target_copy': 111, 'edit_copy': 121, 'generic_explanation': 1, 'possible_false_rationalization': 19, 'unsupported_confidence': 145, 'alignment_error': 55, 'validity_error_auto': 28, 'semantic_distortion_auto': 28}`
- Evidence error type counts: `{'index_text_mismatch': 121, 'prediction_only_text': 62, 'invalid_indices': 24, 'prediction_or_target_role': 29, 'text_not_in_source': 23, 'missing_evidence': 1}`
- Decision: `fix_evidence_verifier_and_evidence_prompt_before_targeted_refinement`

## High-Risk Selected Cases

### rf-edit-0026::qwen3_8b::natural

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: It is true that consumers preffer to buy a product that has a lower price , but when international companies that has already the certification begins to send its market , people will preffer to consume theirs because the difference between prices is probbably not going to affect them to much .
- Prediction: It is true that consumers prefer to buy a product that has a lower price , but when international companies that have already the certification begin to send their market , people will prefer to consume theirs because the difference between prices is probably not going to affect them too much .
- Edit: `replace` `its` -> `their` at 28:29
- Rule: Pronouns must agree with their antecedents in number (singular/plural) and gender (if applicable).
- Evidence: `[{"end": 40, "role": "antecedent", "start": 16, "text": "international companies that have already the certification"}, {"end": 30, "role": "pronoun", "start": 28, "text": "its"}]`
- Rationale: The pronoun 'its' is singular and does not match the plural antecedent 'international companies'. Replacing 'its' with 'their' ensures grammatical agreement between the subject and the possessive pronoun.

### rf-edit-0074::qwen3_8b::rule_grounded

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `insert`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: which play an important role to giving tough competition to the government . as a result of this consumer gets more benefits , like lower faire , privacy , freedom and safe travelling.in addition many automobile companies launcing new cars at affordable prices , which encourages people to use more and more private vechile .
- Prediction: which play an important role in giving tough competition to the government . As a result of this , consumers get more benefits , like lower faire , privacy , freedom and safe journeys . In addition , many automobile companies are launcing new cars at affordable prices , which encourages people to use more and more private vegetables .
- Edit: `insert` `` -> `are` at 37:37
- Rule: A subject must agree with its verb in number (singular/plural).
- Evidence: `[{"end": 45, "role": "target", "start": 37, "text": "many automobile companies launcing"}]`
- Rationale: The subject 'many automobile companies' is plural, so the verb should be 'are launcing' instead of just 'launcing' to maintain subject-verb agreement. This ensures grammatical correctness in the sentence structure.

### rf-edit-0141::qwen3_8b::natural

- Bucket: `refine`; dataset: `JFLEG`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I want to talk about nocive or bad products like alcohol , hair spray and cigarrets .
- Prediction: I want to talk about harmful or bad products like alcohol, hair spray and cigarettes.
- Edit: `replace` `nocive` -> `harmful` at 5:6
- Rule: Use the correct spelling of words to ensure clarity and correctness in communication.
- Evidence: `[{"end": 10, "role": "error", "start": 5, "text": "nocive"}, {"end": 11, "role": "correction", "start": 5, "text": "harmful"}]`
- Rationale: The word 'nocive' is not a standard English word. The intended word is likely 'harmful', which is a commonly used adjective to describe something that causes harm. Replacing 'nocive' with 'harmful' corrects the spelling and improves the clarity of the sentence.

### rf-edit-0151::qwen3_8b::natural

- Bucket: `accepted`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `insert`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: public transportation . day by day folk are more crazy about own vehicles which leads dark future for public transportation
- Prediction: Public transportation. Day by day people are more crazy about own vehicles, which leads to a dark future for public transportation.
- Edit: `insert` `` -> `to a` at 15:15
- Rule: A preposition such as 'lead to' requires a complement (noun phrase) to complete its meaning.
- Evidence: `[{"end": 26, "role": "affected_span", "start": 15, "text": "leads dark future"}, {"end": 30, "role": "corrected_span", "start": 15, "text": "leads to a dark future"}]`
- Rationale: The original sentence contains an incomplete prepositional phrase 'leads dark future'. The verb 'lead' in this context requires the preposition 'to' followed by a noun phrase. Inserting 'to a' completes the phrase correctly as 'leads to a dark future', making the sentence grammatically accurate.

### rf-edit-0151::qwen3_8b::rule_grounded

- Bucket: `accepted`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `insert`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: public transportation . day by day folk are more crazy about own vehicles which leads dark future for public transportation
- Prediction: Public transportation. Day by day people are more crazy about own vehicles, which leads to a dark future for public transportation.
- Edit: `insert` `` -> `to a` at 15:15
- Rule: A preposition such as 'lead to' requires a complement (noun phrase) to complete its meaning.
- Evidence: `[{"end": 26, "role": "affected_span", "start": 15, "text": "leads dark future"}, {"end": 30, "role": "corrected_span", "start": 15, "text": "leads to a dark future"}]`
- Rationale: The original sentence contains an incomplete prepositional phrase 'leads dark future'. The verb 'lead' in this context requires the preposition 'to' followed by a noun phrase. Inserting 'to a' completes the phrase correctly as 'leads to a dark future', making the sentence grammatically accurate.

### rf-edit-0021::qwen3_8b::natural

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I was very fast , my best time was 5 5 seconds in 4 0 0 hundred meters is a good time in or country .
- Prediction: I was very fast . My best time was 5 5 5 seconds in 4 0 0 hundred meters , which is a good time in the country .
- Edit: `replace` `or` -> `the` at 23:24
- Rule: Use 'the' before a noun when referring to a specific or previously mentioned entity.
- Evidence: `[{"end": 27, "role": "error", "start": 23, "text": "or country"}, {"end": 27, "role": "correction", "start": 23, "text": "the country"}]`
- Rationale: The phrase 'in or country' is grammatically incorrect because 'or' is a conjunction, not an article. The correct article to use before 'country' is 'the', as it refers to a specific country (likely the speaker's own country) in the context.

### rf-edit-0021::qwen3_8b::rule_grounded

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I was very fast , my best time was 5 5 seconds in 4 0 0 hundred meters is a good time in or country .
- Prediction: I was very fast . My best time was 5 5 5 seconds in 4 0 0 hundred meters , which is a good time in the country .
- Edit: `replace` `or` -> `the` at 23:24
- Rule: Use 'the' before a noun when referring to a specific or previously mentioned entity.
- Evidence: `[{"end": 27, "role": "error_span", "start": 23, "text": "in or country"}, {"end": 27, "role": "corrected_span", "start": 23, "text": "in the country"}]`
- Rationale: The word 'or' is incorrect in this context because it is not a determiner. The correct definite article 'the' should be used before 'country' to indicate a specific reference.

### rf-edit-0026::qwen3_8b::rule_grounded

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: It is true that consumers preffer to buy a product that has a lower price , but when international companies that has already the certification begins to send its market , people will preffer to consume theirs because the difference between prices is probbably not going to affect them to much .
- Prediction: It is true that consumers prefer to buy a product that has a lower price , but when international companies that have already the certification begin to send their market , people will prefer to consume theirs because the difference between prices is probably not going to affect them too much .
- Edit: `replace` `its` -> `their` at 28:29
- Rule: Pronouns must agree with their antecedents in number (singular/plural) and gender (if applicable).
- Evidence: `[{"end": 26, "role": "antecedent", "start": 14, "text": "international companies"}, {"end": 30, "role": "pronoun", "start": 28, "text": "its"}]`
- Rationale: The pronoun 'its' is singular and does not agree with the plural antecedent 'international companies'. The correct pronoun to use in this context is 'their', which agrees in number with the plural subject.

### rf-edit-0034::qwen3_8b::natural

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 14:15
- Rule: Use the correct verb form based on context and grammatical structure.
- Evidence: `[{"end": 15, "role": "error", "start": 14, "text": "pot"}, {"end": 20, "role": "correction", "start": 14, "text": "potting"}]`
- Rationale: The word 'pot' is a noun or a base form of the verb, but in this context, the correct form should be 'potting', which is the present participle form of the verb 'pot'. This form is necessary to describe the ongoing action of potting tires on a car.

### rf-edit-0034::qwen3_8b::rule_grounded

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 14:15
- Rule: Verbs should be correctly inflected to match the context and intended meaning.
- Evidence: `[{"end": 15, "role": "error", "start": 14, "text": "pot"}, {"end": 20, "role": "correction", "start": 14, "text": "potting"}]`
- Rationale: The word 'pot' is a base verb, but in this context, the correct form should be 'potting' to indicate the ongoing action of potting tires on a car. This change ensures grammatical accuracy and clarity.

### rf-edit-0074::qwen3_8b::natural

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `insert`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: which play an important role to giving tough competition to the government . as a result of this consumer gets more benefits , like lower faire , privacy , freedom and safe travelling.in addition many automobile companies launcing new cars at affordable prices , which encourages people to use more and more private vechile .
- Prediction: which play an important role in giving tough competition to the government . As a result of this , consumers get more benefits , like lower faire , privacy , freedom and safe journeys . In addition , many automobile companies are launcing new cars at affordable prices , which encourages people to use more and more private vegetables .
- Edit: `insert` `` -> `are` at 37:37
- Rule: The subject and verb must agree in number (singular/plural).
- Evidence: `[{"end": 45, "role": "source", "start": 37, "text": "many automobile companies launcing"}, {"end": 45, "role": "target", "start": 37, "text": "many automobile companies are launcing"}]`
- Rationale: The subject 'many automobile companies' is plural, so the verb must also be plural. The original sentence used 'launcing' without a helping verb, which is incorrect. Inserting 'are' before 'launcing' ensures subject-verb agreement.

### rf-edit-0092::qwen3_8b::natural

- Bucket: `accepted`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Prediction: I 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Edit: `replace` `to` -> `than` at 25:26
- Rule: Use 'than' to compare two things.
- Evidence: `[{"end": 26, "role": "error", "start": 25, "text": "It has different food to other restaurants"}, {"end": 26, "role": "correction", "start": 25, "text": "It has different food than other restaurants"}]`
- Rationale: The original sentence uses 'to' in the phrase 'different food to other restaurants', which is incorrect. The correct comparative conjunction to use in this context is 'than', making the sentence grammatically accurate by comparing the food at the restaurant to that of other restaurants.

### rf-edit-0092::qwen3_8b::rule_grounded

- Bucket: `accepted`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Prediction: I 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Edit: `replace` `to` -> `than` at 25:26
- Rule: Use 'than' to compare two things, such as 'different from' or 'more than'.
- Evidence: `[{"end": 26, "role": "error", "start": 25, "text": "It has different food to other restaurants"}, {"end": 26, "role": "correction", "start": 25, "text": "It has different food than other restaurants"}]`
- Rationale: The original sentence uses 'to' incorrectly in the phrase 'different food to other restaurants'. The correct comparative conjunction is 'than', which is used to compare two things. This edit corrects the grammatical structure by replacing 'to' with 'than'.

### rf-edit-0107::qwen3_8b::natural

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 32:33
- Rule: Use the correct verb form based on context and grammatical structure.
- Evidence: `[{"end": 33, "role": "error", "start": 32, "text": "pot"}, {"end": 37, "role": "correction", "start": 32, "text": "potting"}]`
- Rationale: The word 'pot' is a base form of the verb, but in this context, the correct form should be 'potting', which is a present participle. This change ensures grammatical accuracy and clarity in describing the action of applying tires to a car.

### rf-edit-0107::qwen3_8b::rule_grounded

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 32:33
- Rule: Verbs should be correctly inflected to match context and meaning.
- Evidence: `[{"end": 33, "role": "error", "start": 32, "text": "pot"}, {"end": 37, "role": "corrected", "start": 32, "text": "potting"}]`
- Rationale: The word 'pot' is a base form of the verb, but in this context, the correct form should be 'potting' to indicate the ongoing action of potting tires on a car. This aligns with standard English grammar rules regarding verb forms in participial phrases.

### rf-edit-0170::qwen3_8b::natural

- Bucket: `accepted`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `wrong_correction`; operation: `insert`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: They were planning to steal a very precious thing from Museum tonight .
- Prediction: Then, they were planning to steal a very precious thing from the museum tonight.
- Edit: `insert` `` -> `the` at 10:10
- Rule: Definite articles ('the') should be used when referring to specific, known entities.
- Evidence: `[{"end": 14, "role": "noun", "start": 10, "text": "Museum"}]`
- Rationale: The noun 'Museum' in the original sentence is used without an article, which makes it unclear whether it refers to a specific museum or a general concept. Adding 'the' clarifies that the sentence is referring to a particular museum, making the sentence more precise and grammatically correct.

### rf-edit-0170::qwen3_8b::rule_grounded

- Bucket: `accepted`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `wrong_correction`; operation: `insert`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: They were planning to steal a very precious thing from Museum tonight .
- Prediction: Then, they were planning to steal a very precious thing from the museum tonight.
- Edit: `insert` `` -> `the` at 10:10
- Rule: Definite articles ('the') should be used when referring to specific, known entities.
- Evidence: `[{"end": 13, "role": "noun", "start": 10, "text": "Museum"}]`
- Rationale: The noun 'Museum' in the original sentence is used without an article, which makes it unclear which specific museum is being referenced. Adding 'the' clarifies that the sentence is referring to a particular, known museum.

### rf-edit-0207::qwen3_8b::natural

- Bucket: `refine`; dataset: `JFLEG`; model: `t5_base_grammar`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: One person if do n't have good health that means so many things they could lost .
- Prediction: One person if they don't have good health, that means so many things they could lose.
- Edit: `replace` `do` -> `they` at 3:4
- Rule: Subject-verb agreement requires the verb form to match the subject in number and person.
- Evidence: `[{"end": 4, "role": "source", "start": 3, "text": "One person if do n't have good health that means so many things they could lost ."}, {"end": 4, "role": "target", "start": 3, "text": "One person if they don't have good health, that means so many things they could lose."}]`
- Rationale: The original sentence contains a grammatical error where the subject 'one person' is incorrectly paired with the verb 'do'. Replacing 'do' with 'they' ensures proper subject-verb agreement and makes the sentence syntactically correct.

### rf-edit-0207::qwen3_8b::rule_grounded

- Bucket: `refine`; dataset: `JFLEG`; model: `t5_base_grammar`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: One person if do n't have good health that means so many things they could lost .
- Prediction: One person if they don't have good health, that means so many things they could lose.
- Edit: `replace` `do` -> `they` at 3:4
- Rule: A subject and its corresponding verb must agree in number (singular/plural) and person (first/second/third).
- Evidence: `[{"end": 6, "role": "source", "start": 3, "text": "One person if do n't have good health that means so many things they could lost ."}, {"end": 7, "role": "target", "start": 3, "text": "One person if they don't have good health, that means so many things they could lose."}]`
- Rationale: The original sentence contains a grammatical error where the subject 'One person' is paired with the incorrect verb 'do'. Replacing 'do' with 'they' ensures subject-verb agreement and creates a coherent conditional clause. This edit aligns with standard English grammar rules regarding subject-verb agreement and proper clause formation.

### rf-edit-0242::qwen3_8b::rule_grounded

- Bucket: `rejected`; dataset: `EXPECT`; model: `coedit_large`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;unsupported_confidence;alignment_error;validity_error_auto;semantic_distortion_auto`
- Source: Sometimes we go to partyies in the city , I dance in the parties with my friends .
- Prediction: Sometimes we go to parties in the city; I dance in the parties with my friends.
- Edit: `replace` `partyies` -> `parties` at 4:5
- Rule: Correct misspelled words to their standard form.
- Evidence: `[{"end": 9, "role": "error", "start": 4, "text": "partyies"}, {"end": 9, "role": "corrected", "start": 4, "text": "parties"}]`
- Rationale: The word 'partyies' contains an incorrect double 'i', which is a common spelling mistake. The correct spelling is 'parties', which is a standard English word referring to social gatherings. This correction aligns the text with proper spelling conventions.

### rf-edit-0251::qwen3_8b::natural

- Bucket: `rejected`; dataset: `EXPECT`; model: `coedit_large`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;alignment_error`
- Source: Technology will have advanced and maybe the cars will fly above streets and computers will have totally changed .
- Prediction: Technology will have advanced, and maybe cars will fly above the streets, and computers will have totally changed.
- Edit: `replace` `streets` -> `streets,` at 11:12
- Rule: A comma should be used to separate independent clauses or items in a list when clarity is needed.
- Evidence: `[{"end": 12, "role": "modified", "start": 11, "text": "and maybe cars will fly above the streets, and computers will have totally changed"}]`
- Rationale: The addition of a comma after 'streets' serves to separate the clause 'cars will fly above the streets' from the following clause 'computers will have totally changed', improving readability and adhering to standard punctuation rules for compound sentences.

### rf-edit-0251::qwen3_8b::rule_grounded

- Bucket: `rejected`; dataset: `EXPECT`; model: `coedit_large`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence;alignment_error`
- Source: Technology will have advanced and maybe the cars will fly above streets and computers will have totally changed .
- Prediction: Technology will have advanced, and maybe cars will fly above the streets, and computers will have totally changed.
- Edit: `replace` `streets` -> `streets,` at 11:12
- Rule: Use commas to separate independent clauses or to set off non-restrictive clauses.
- Evidence: `[{"end": 12, "role": "target", "start": 11, "text": "and maybe cars will fly above streets, and computers will have totally changed"}, {"end": 12, "role": "source", "start": 11, "text": "and maybe cars will fly above streets and computers will have totally changed"}]`
- Rationale: The addition of a comma after 'streets' improves readability by separating the independent clause 'cars will fly above streets' from the following clause 'computers will have totally changed'. While not strictly required, it is a stylistic choice that enhances clarity and adheres to standard punctuation conventions.

### rf-edit-0025::qwen3_8b::natural

- Bucket: `rejected`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `correct_correction`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;edit_copy;unsupported_confidence;alignment_error`
- Source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- Prediction: Computers have had the most significant impact on people in the latter 1/2 of the 20th century .
- Edit: `delete` `the` -> `` at 8:9
- Rule: Articles like 'the' may be omitted when the noun phrase is clearly defined or when the context makes the reference unambiguous.
- Evidence: `[{"end": 13, "role": "modified_noun_phrase", "start": 8, "text": "the most significant impact"}]`
- Rationale: The article 'the' is stylistically optional before 'most significant impact' because the phrase is already clearly defined in the context of the sentence. Removing it results in a more concise and natural phrasing.

### rf-edit-0025::qwen3_8b::rule_grounded

- Bucket: `rejected`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `correct_correction`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;edit_copy;unsupported_confidence;alignment_error`
- Source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- Prediction: Computers have had the most significant impact on people in the latter 1/2 of the 20th century .
- Edit: `delete` `the` -> `` at 8:9
- Rule: Articles like 'the' may be omitted when the noun phrase is clearly defined or when the context makes the reference unambiguous.
- Evidence: `[{"end": 13, "role": "modified_noun_phrase", "start": 8, "text": "the most significant impact"}]`
- Rationale: The article 'the' is stylistically redundant before 'most significant impact' because the phrase is already clearly defined in the context of the sentence, making the article unnecessary for clarity or specificity.

### rf-edit-0033::qwen3_8b::rule_grounded

- Bucket: `rejected`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;edit_copy;unsupported_confidence;alignment_error`
- Source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- Prediction: I think about transport that the government should help public transport , for example buses , trains , the metro and more , for a single reason : the quality of life against pollution .
- Edit: `delete` `the` -> `` at 34:35
- Rule: Avoid unnecessary articles before nouns that are clearly defined by context.
- Evidence: `[{"end": 38, "role": "target", "start": 34, "text": "the quality of life against pollution"}]`
- Rationale: The article 'the' before 'pollution' is unnecessary because the prepositional phrase 'against pollution' already provides sufficient context, making the article redundant and stylistically optional.

### rf-edit-0125::qwen3_8b::rule_grounded

- Bucket: `rejected`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;edit_copy;unsupported_confidence;alignment_error`
- Source: Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .
- Prediction: Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.
- Edit: `delete` `either` -> `` at 20:21
- Rule: When comparing two items in a list, the conjunction 'either' is often redundant if the list is already clear without it.
- Evidence: `[{"end": 25, "role": "target", "start": 20, "text": "compared either to our parents' or our grandparents' lives"}]`
- Rationale: The word 'either' is redundant in this context because the sentence already uses 'or' to introduce the two options. Removing 'either' makes the sentence more concise and natural.

### rf-edit-0147::qwen3_8b::rule_grounded

- Bucket: `rejected`; dataset: `JFLEG`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;missing_evidence;wrong_evidence_auto;possible_false_rationalization;unsupported_confidence;alignment_error;validity_error_auto;semantic_distortion_auto`
- Source: Specializing in one particular subject does not suit our life in this era which is characterized by diversity and innovation
- Prediction: Specializing in one particular subject does not suit our life in this era, which is characterized by diversity and innovation.
- Edit: `replace` `era` -> `era,` at 12:13
- Rule: A comma should be used after introductory clauses or phrases that are not essential to the meaning of the sentence.
- Evidence: `[{"end": 34, "role": "relative_clause", "start": 13, "text": "which is characterized by diversity and innovation"}]`
- Rationale: The phrase 'which is characterized by diversity and innovation' is a non-restrictive relative clause that adds additional context to the main clause. A comma is required after 'era' to properly separate the main clause from this relative clause, ensuring clarity and proper punctuation.

### rf-edit-0236::qwen3_8b::natural

- Bucket: `refine`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- Prediction: Using the Internet for the first time since the beginning of the 20th century.
- Edit: `replace` `latter 1/2` -> `beginning` at 12:14
- Rule: Replacements should maintain semantic coherence and logical consistency within the context.
- Evidence: `[{"end": 14, "role": "source", "start": 12, "text": "Computers have had a most significant impact on the people in the latter 1/2 of the 20th century."}, {"end": 14, "role": "target", "start": 12, "text": "Using the Internet for the first time since the beginning of the 20th century."}]`
- Rationale: Replacing 'latter 1/2' with 'beginning' creates a logical inconsistency because 'latter 1/2 of the 20th century' refers to the second half of the century, while 'beginning of the 20th century' refers to its early years. This substitution disrupts the temporal relationship and introduces a contradiction in meaning.

### rf-edit-0236::qwen3_8b::rule_grounded

- Bucket: `refine`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- Prediction: Using the Internet for the first time since the beginning of the 20th century.
- Edit: `replace` `latter 1/2` -> `beginning` at 12:14
- Rule: Replacements must maintain semantic coherence and temporal consistency within the context.
- Evidence: `[{"end": 14, "role": "source", "start": 12, "text": "Computers have had a most significant impact on the people in the latter 1/2 of the 20th century."}, {"end": 14, "role": "target", "start": 12, "text": "Using the Internet for the first time since the beginning of the 20th century."}]`
- Rationale: The phrase 'latter 1/2' refers to the second half of the 20th century, while 'beginning' refers to the early part of the century. These two phrases are semantically inconsistent and do not align with the original context of the sentence, which discusses the impact of computers during the latter half of the century. Replacing 'latter 1/2' with 'beginning' creates a logical inconsistency in the timeline.

### rf-edit-0242::qwen3_8b::natural

- Bucket: `rejected`; dataset: `EXPECT`; model: `coedit_large`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;missing_evidence;wrong_evidence_auto;target_copy;unsupported_confidence;alignment_error;validity_error_auto;semantic_distortion_auto`
- Source: Sometimes we go to partyies in the city , I dance in the parties with my friends .
- Prediction: Sometimes we go to parties in the city; I dance in the parties with my friends.
- Edit: `replace` `partyies` -> `parties` at 4:5
- Rule: Ensure correct spelling of words.
- Evidence: `[{"end": 9, "role": "error", "start": 4, "text": "partyies"}, {"end": 9, "role": "correct", "start": 4, "text": "parties"}]`
- Rationale: The word 'partyies' contains an incorrect double 'i', which is not part of the standard spelling of the word 'parties'. Correcting this spelling error ensures clarity and proper communication.

## Loop Result

- Commands executed: see `docs/rulefaith_loop_A_qwen3_audit.md`.
- Artifacts produced: `results/rulefaith/qwen3_manual_audit.csv`, `results/rulefaith/qwen3_manual_audit_summary.json`, and this case report.
- Hypothesis status: `revise` because the selected audit file is usable, but the automatic evidence-span checks show that the evidence verifier/prompt should be tightened before using accepted candidates as final positives.
- Next highest-priority loop: implement targeted refinement only after adding stricter evidence-span validation and manual spot-checking the selected rows.

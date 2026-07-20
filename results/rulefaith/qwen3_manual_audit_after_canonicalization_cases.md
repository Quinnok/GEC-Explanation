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
- Flag counts: `{'leakage_input_violation': 0, 'source_span_match': 160, 'target_present_in_prediction': 160, 'evidence_span_index_match': 155, 'evidence_all_spans_source_index_match': 155, 'evidence_text_found_in_source': 155, 'evidence_text_found_in_prediction_only': 29, 'evidence_contextual': 82, 'missing_evidence': 78, 'wrong_evidence_auto': 29, 'missing_rule': 1, 'rule_edit_copy': 0, 'target_copy': 102, 'edit_copy': 112, 'generic_explanation': 1, 'possible_false_rationalization': 19, 'unsupported_confidence': 131, 'alignment_error': 58, 'validity_error_auto': 28, 'semantic_distortion_auto': 28}`
- Evidence error type counts: `{'missing_evidence': 5, 'prediction_or_target_role': 29}`
- Decision: `fix_evidence_verifier_and_evidence_prompt_before_targeted_refinement`

## High-Risk Selected Cases

### rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `insert`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: which play an important role to giving tough competition to the government . as a result of this consumer gets more benefits , like lower faire , privacy , freedom and safe travelling.in addition many automobile companies launcing new cars at affordable prices , which encourages people to use more and more private vechile .
- Prediction: which play an important role in giving tough competition to the government . As a result of this , consumers get more benefits , like lower faire , privacy , freedom and safe journeys . In addition , many automobile companies are launcing new cars at affordable prices , which encourages people to use more and more private vegetables .
- Edit: `insert` `` -> `are` at 37:37
- Rule: A subject must agree with its verb in number (singular/plural).
- Evidence: `[{"end": 38, "role": "target", "start": 34, "text": "many automobile companies launcing"}]`
- Rationale: The subject 'many automobile companies' is plural, so the verb should be 'are launcing' instead of just 'launcing' to maintain subject-verb agreement. This ensures grammatical correctness in the sentence structure.

### rf-edit-0025::qwen3_8b::natural::evidence_canonicalized

- Bucket: `rejected`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `correct_correction`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;missing_evidence;edit_copy;unsupported_confidence;alignment_error`
- Source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- Prediction: Computers have had the most significant impact on people in the latter 1/2 of the 20th century .
- Edit: `delete` `the` -> `` at 8:9
- Rule: Articles like 'the' may be omitted when the noun phrase is clearly defined or when the context makes the reference unambiguous.
- Evidence: `[]`
- Rationale: The article 'the' is stylistically optional before 'most significant impact' because the phrase is already clearly defined in the context of the sentence. Removing it results in a more concise and natural phrasing.

### rf-edit-0025::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `rejected`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `correct_correction`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;missing_evidence;edit_copy;unsupported_confidence;alignment_error`
- Source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- Prediction: Computers have had the most significant impact on people in the latter 1/2 of the 20th century .
- Edit: `delete` `the` -> `` at 8:9
- Rule: Articles like 'the' may be omitted when the noun phrase is clearly defined or when the context makes the reference unambiguous.
- Evidence: `[]`
- Rationale: The article 'the' is stylistically redundant before 'most significant impact' because the phrase is already clearly defined in the context of the sentence, making the article unnecessary for clarity or specificity.

### rf-edit-0026::qwen3_8b::natural::evidence_canonicalized

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: It is true that consumers preffer to buy a product that has a lower price , but when international companies that has already the certification begins to send its market , people will preffer to consume theirs because the difference between prices is probbably not going to affect them to much .
- Prediction: It is true that consumers prefer to buy a product that has a lower price , but when international companies that have already the certification begin to send their market , people will prefer to consume theirs because the difference between prices is probably not going to affect them too much .
- Edit: `replace` `its` -> `their` at 28:29
- Rule: Pronouns must agree with their antecedents in number (singular/plural) and gender (if applicable).
- Evidence: `[{"end": 29, "role": "pronoun", "start": 28, "text": "its"}]`
- Rationale: The pronoun 'its' is singular and does not match the plural antecedent 'international companies'. Replacing 'its' with 'their' ensures grammatical agreement between the subject and the possessive pronoun.

### rf-edit-0033::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `rejected`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;missing_evidence;edit_copy;unsupported_confidence;alignment_error`
- Source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- Prediction: I think about transport that the government should help public transport , for example buses , trains , the metro and more , for a single reason : the quality of life against pollution .
- Edit: `delete` `the` -> `` at 34:35
- Rule: Avoid unnecessary articles before nouns that are clearly defined by context.
- Evidence: `[]`
- Rationale: The article 'the' before 'pollution' is unnecessary because the prepositional phrase 'against pollution' already provides sufficient context, making the article redundant and stylistically optional.

### rf-edit-0034::qwen3_8b::natural::evidence_canonicalized

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 14:15
- Rule: Use the correct verb form based on context and grammatical structure.
- Evidence: `[{"end": 15, "role": "error", "start": 14, "text": "pot"}]`
- Rationale: The word 'pot' is a noun or a base form of the verb, but in this context, the correct form should be 'potting', which is the present participle form of the verb 'pot'. This form is necessary to describe the ongoing action of potting tires on a car.

### rf-edit-0034::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 14:15
- Rule: Verbs should be correctly inflected to match the context and intended meaning.
- Evidence: `[{"end": 15, "role": "error", "start": 14, "text": "pot"}]`
- Rationale: The word 'pot' is a base verb, but in this context, the correct form should be 'potting' to indicate the ongoing action of potting tires on a car. This change ensures grammatical accuracy and clarity.

### rf-edit-0035::qwen3_8b::natural::evidence_canonicalized

- Bucket: `rejected`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `insert`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;missing_evidence;missing_rule;target_copy;edit_copy`
- Source: A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .
- Prediction: A worldwide war is the only case in which we will see a dramatic change in peoples ' lives in 50 years from now .
- Edit: `insert` `` -> `'` at 17:17
- Rule:
- Evidence: `[]`
- Rationale: { "edit_description": "Insert an apostrophe after 'peoples'", "edit_validity": "stylistic", "rule_id": "punctuation_apostrophe", "rule_text": "An apostrophe is used to indicate possession or contraction.", "evidence_spans": [ { "text": "peoples", "start": 17, "end": 23, "role": "target" } ], "applicability_conditions": [ "the word is a plural noun", "the word is being used to refer to people in general", "the word is not indicating possession" ], "rationale": "The word 'peoples' is a plural noun referring to groups of people, and does not require an apostrophe unless it is being used to indicate possession (e.g., 'peoples\' homes'). In this context, the apostrophe is unnecessary and stylistically incorrect.", "confidence": 0.95, "abstain": false, "abstain_reason": "" }

### rf-edit-0107::qwen3_8b::natural::evidence_canonicalized

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 32:33
- Rule: Use the correct verb form based on context and grammatical structure.
- Evidence: `[{"end": 33, "role": "error", "start": 32, "text": "pot"}]`
- Rationale: The word 'pot' is a base form of the verb, but in this context, the correct form should be 'potting', which is a present participle. This change ensures grammatical accuracy and clarity in describing the action of applying tires to a car.

### rf-edit-0107::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `refine`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: image you salf you are wark in factory just to do one thing like pot taire on car if they fire you you will destroy , becouse u dont know more than pot taire in car .
- Prediction: Imagine working in a factory just to do one thing , like potting taire on a car . If they fire you , you will destroy it , because you do know more than potting taire on a car .
- Edit: `replace` `pot` -> `potting` at 32:33
- Rule: Verbs should be correctly inflected to match context and meaning.
- Evidence: `[{"end": 33, "role": "error", "start": 32, "text": "pot"}]`
- Rationale: The word 'pot' is a base form of the verb, but in this context, the correct form should be 'potting' to indicate the ongoing action of potting tires on a car. This aligns with standard English grammar rules regarding verb forms in participial phrases.

### rf-edit-0141::qwen3_8b::natural::evidence_canonicalized

- Bucket: `refine`; dataset: `JFLEG`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I want to talk about nocive or bad products like alcohol , hair spray and cigarrets .
- Prediction: I want to talk about harmful or bad products like alcohol, hair spray and cigarettes.
- Edit: `replace` `nocive` -> `harmful` at 5:6
- Rule: Use the correct spelling of words to ensure clarity and correctness in communication.
- Evidence: `[{"end": 6, "role": "error", "start": 5, "text": "nocive"}]`
- Rationale: The word 'nocive' is not a standard English word. The intended word is likely 'harmful', which is a commonly used adjective to describe something that causes harm. Replacing 'nocive' with 'harmful' corrects the spelling and improves the clarity of the sentence.

### rf-edit-0217::qwen3_8b::natural::evidence_canonicalized

- Bucket: `rejected`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_prediction_only_text;wrong_evidence_auto;possible_false_rationalization;unsupported_confidence;alignment_error;validity_error_auto;semantic_distortion_auto`
- Source: In the end I think if many people want the Monarchy to be ablished a general election should be called and then see if the Monarchy should be abolished .
- Prediction: In the end, I think if many people want the monarchy to be established, a general election should be called and then see if the monarchy should be abolished.
- Edit: `replace` `ablished` -> `established,` at 13:14
- Rule: Correct spelling of words with common misspellings.
- Evidence: `[{"end": 14, "role": "error", "start": 13, "text": "ablished"}, {"end": 14, "role": "correction", "start": 13, "text": "ablished"}]`
- Rationale: The word 'ablished' is a common misspelling of 'established'. Correcting it ensures clarity and proper communication of the intended meaning.

### rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `rejected`; dataset: `EXPECT`; model: `coedit_large`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_prediction_only_text;wrong_evidence_auto;target_copy;unsupported_confidence;alignment_error;validity_error_auto;semantic_distortion_auto`
- Source: Sometimes we go to partyies in the city , I dance in the parties with my friends .
- Prediction: Sometimes we go to parties in the city; I dance in the parties with my friends.
- Edit: `replace` `partyies` -> `parties` at 4:5
- Rule: Correct misspelled words to their standard form.
- Evidence: `[{"end": 5, "role": "error", "start": 4, "text": "partyies"}, {"end": 14, "role": "corrected", "start": 13, "text": "parties"}]`
- Rationale: The word 'partyies' contains an incorrect double 'i', which is a common spelling mistake. The correct spelling is 'parties', which is a standard English word referring to social gatherings. This correction aligns the text with proper spelling conventions.

### rf-edit-0021::qwen3_8b::natural::evidence_canonicalized

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I was very fast , my best time was 5 5 seconds in 4 0 0 hundred meters is a good time in or country .
- Prediction: I was very fast . My best time was 5 5 5 seconds in 4 0 0 hundred meters , which is a good time in the country .
- Edit: `replace` `or` -> `the` at 23:24
- Rule: Use 'the' before a noun when referring to a specific or previously mentioned entity.
- Evidence: `[{"end": 25, "role": "error", "start": 23, "text": "or country"}]`
- Rationale: The phrase 'in or country' is grammatically incorrect because 'or' is a conjunction, not an article. The correct article to use before 'country' is 'the', as it refers to a specific country (likely the speaker's own country) in the context.

### rf-edit-0021::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I was very fast , my best time was 5 5 seconds in 4 0 0 hundred meters is a good time in or country .
- Prediction: I was very fast . My best time was 5 5 5 seconds in 4 0 0 hundred meters , which is a good time in the country .
- Edit: `replace` `or` -> `the` at 23:24
- Rule: Use 'the' before a noun when referring to a specific or previously mentioned entity.
- Evidence: `[{"end": 25, "role": "error_span", "start": 22, "text": "in or country"}]`
- Rationale: The word 'or' is incorrect in this context because it is not a determiner. The correct definite article 'the' should be used before 'country' to indicate a specific reference.

### rf-edit-0026::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `target_copy;edit_copy;possible_false_rationalization;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: It is true that consumers preffer to buy a product that has a lower price , but when international companies that has already the certification begins to send its market , people will preffer to consume theirs because the difference between prices is probbably not going to affect them to much .
- Prediction: It is true that consumers prefer to buy a product that has a lower price , but when international companies that have already the certification begin to send their market , people will prefer to consume theirs because the difference between prices is probably not going to affect them too much .
- Edit: `replace` `its` -> `their` at 28:29
- Rule: Pronouns must agree with their antecedents in number (singular/plural) and gender (if applicable).
- Evidence: `[{"end": 20, "role": "antecedent", "start": 18, "text": "international companies"}, {"end": 29, "role": "pronoun", "start": 28, "text": "its"}]`
- Rationale: The pronoun 'its' is singular and does not agree with the plural antecedent 'international companies'. The correct pronoun to use in this context is 'their', which agrees in number with the plural subject.

### rf-edit-0033::qwen3_8b::natural::evidence_canonicalized

- Bucket: `accepted`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `delete`
- Risks: `evidence_span_index_mismatch;evidence_not_all_source_index_matched;evidence_text_not_found_in_source;missing_evidence;edit_copy;unsupported_confidence`
- Source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- Prediction: I think about transport that the government should help public transport , for example buses , trains , the metro and more , for a single reason : the quality of life against pollution .
- Edit: `delete` `the` -> `` at 34:35
- Rule: Articles like 'the' may be omitted when they are redundant or when the noun phrase is clearly understood without them.
- Evidence: `[]`
- Rationale: The article 'the' before 'pollution' is stylistically unnecessary because it is already clear from context that the comparison is between quality of life and pollution, without requiring a definite article. Removing 'the' makes the sentence more concise and natural.

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `insert`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .
- Prediction: A worldwide war is the only case in which we will see a dramatic change in peoples ' lives in 50 years from now .
- Edit: `insert` `` -> `'` at 17:17
- Rule: Use an apostrophe to indicate possession in plural nouns.
- Evidence: `[{"end": 17, "role": "target", "start": 16, "text": "peoples"}]`
- Rationale: The word 'peoples' is a plural noun and requires an apostrophe to indicate possession. The insertion of the apostrophe is a stylistic choice to ensure grammatical correctness in the possessive form.

### rf-edit-0051::qwen3_8b::natural::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `correct_correction`; operation: `replace`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- Prediction: I live in San Miguel Almoloyan . This is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring for the environment is very important and in my village they take different actions to care for it .
- Edit: `replace` `of` -> `for` at 25:26
- Rule: The preposition 'for' is used to indicate purpose or relation to something, while 'of' indicates possession or composition.
- Evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`
- Rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its object (the environment). The correct preposition to use here is 'for', which indicates purpose or relation to something.

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `correct_correction`; operation: `replace`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- Prediction: I live in San Miguel Almoloyan . This is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring for the environment is very important and in my village they take different actions to care for it .
- Edit: `replace` `of` -> `for` at 25:26
- Rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- Evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`
- Rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its target (the environment). The correct preposition to use here is 'for', which indicates purpose or relation.

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `wrong_correction`; operation: `replace`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: Variety of buses are provided by the government in order to meet people 's financial means .
- Prediction: A variety of buses are provided by the government in order to meet people 's financial means .
- Edit: `replace` `Variety` -> `A variety` at 0:1
- Rule: Use of definite or indefinite articles for noun phrases
- Evidence: `[{"end": 1, "role": "modified", "start": 0, "text": "Variety"}]`
- Rationale: The original sentence begins with 'Variety', which is a non-count noun and does not require an article. Adding 'A' before 'variety' makes the noun phrase grammatically complete and more natural in standard English usage.

### rf-edit-0074::qwen3_8b::natural::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `insert`
- Risks: `missing_evidence;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: which play an important role to giving tough competition to the government . as a result of this consumer gets more benefits , like lower faire , privacy , freedom and safe travelling.in addition many automobile companies launcing new cars at affordable prices , which encourages people to use more and more private vechile .
- Prediction: which play an important role in giving tough competition to the government . As a result of this , consumers get more benefits , like lower faire , privacy , freedom and safe journeys . In addition , many automobile companies are launcing new cars at affordable prices , which encourages people to use more and more private vegetables .
- Edit: `insert` `` -> `are` at 37:37
- Rule: The subject and verb must agree in number (singular/plural).
- Evidence: `[{"end": 38, "role": "source", "start": 34, "text": "many automobile companies launcing"}]`
- Rationale: The subject 'many automobile companies' is plural, so the verb must also be plural. The original sentence used 'launcing' without a helping verb, which is incorrect. Inserting 'are' before 'launcing' ensures subject-verb agreement.

### rf-edit-0092::qwen3_8b::natural::evidence_canonicalized

- Bucket: `accepted`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Prediction: I 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Edit: `replace` `to` -> `than` at 25:26
- Rule: Use 'than' to compare two things.
- Evidence: `[{"end": 28, "role": "error", "start": 21, "text": "it has different food to other restaurants"}]`
- Rationale: The original sentence uses 'to' in the phrase 'different food to other restaurants', which is incorrect. The correct comparative conjunction to use in this context is 'than', making the sentence grammatically accurate by comparing the food at the restaurant to that of other restaurants.

### rf-edit-0092::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `accepted`; dataset: `EXPECT`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `replace`
- Risks: `missing_evidence;target_copy;edit_copy;unsupported_confidence;validity_error_auto;semantic_distortion_auto`
- Source: I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Prediction: I 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .
- Edit: `replace` `to` -> `than` at 25:26
- Rule: Use 'than' to compare two things, such as 'different from' or 'more than'.
- Evidence: `[{"end": 28, "role": "error", "start": 21, "text": "it has different food to other restaurants"}]`
- Rationale: The original sentence uses 'to' incorrectly in the phrase 'different food to other restaurants'. The correct comparative conjunction is 'than', which is used to compare two things. This edit corrects the grammatical structure by replacing 'to' with 'than'.

### rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `accepted`; dataset: `JFLEG`; model: `gector_roberta_base`; behavior: `overcorrection`; operation: `replace`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: If every people thinks to learn and understand lots of scientifc subjects , any person will do not do it and as a result of this any science is n't imporeved .
- Prediction: If everybody thinks about learning and understanding lots of scientific subjects , people will not do it and , as a result of this , any science will n't improve .
- Edit: `replace` `understand` -> `understanding` at 7:8
- Rule: Use noun forms in parallel structures for consistency and grammatical correctness.
- Evidence: `[{"end": 8, "role": "target", "start": 7, "text": "understand"}]`
- Rationale: The verb 'understand' is replaced with its noun form 'understanding' to maintain parallelism with 'learning', which is already in the noun form. This creates a more consistent and grammatically balanced structure in the sentence.

### rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `rejected`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `overcorrection`; operation: `delete`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;edit_copy;unsupported_confidence;alignment_error`
- Source: Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .
- Prediction: Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.
- Edit: `delete` `either` -> `` at 20:21
- Rule: When comparing two items in a list, the conjunction 'either' is often redundant if the list is already clear without it.
- Evidence: `[{"end": 25, "role": "target", "start": 20, "text": "either to our parents '"}]`
- Rationale: The word 'either' is redundant in this context because the sentence already uses 'or' to introduce the two options. Removing 'either' makes the sentence more concise and natural.

### rf-edit-0127::qwen3_8b::natural::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `correct_correction`; operation: `replace`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- Prediction: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring for the environment is very important and in my village they take different actions to care for it.
- Edit: `replace` `of` -> `for` at 25:26
- Rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- Evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`
- Rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its object (the environment). The correct preposition to use here is 'for', which indicates purpose or relation to something.

### rf-edit-0127::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `refine`; dataset: `EXPECT`; model: `t5_base_grammar`; behavior: `correct_correction`; operation: `replace`
- Risks: `evidence_prediction_only_text;missing_evidence;wrong_evidence_auto;target_copy;edit_copy;unsupported_confidence`
- Source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- Prediction: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring for the environment is very important and in my village they take different actions to care for it.
- Edit: `replace` `of` -> `for` at 25:26
- Rule: The preposition 'for' is used to indicate purpose or benefit, while 'of' indicates possession or association.
- Evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`
- Rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' implies possession or association, which does not fit the context. The correct preposition is 'for', which indicates purpose or benefit. Therefore, replacing 'of' with 'for' improves the grammatical accuracy and clarity of the sentence.

### rf-edit-0129::qwen3_8b::natural::evidence_canonicalized

- Bucket: `rejected`; dataset: `JFLEG`; model: `t5_base_grammar`; behavior: `wrong_correction`; operation: `replace`
- Risks: `target_copy;possible_false_rationalization;unsupported_confidence;alignment_error;validity_error_auto;semantic_distortion_auto`
- Source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study .
- Prediction: Because all those broad knowledge help them to understand their major in university as well as help them to make a correct choice in specializing study.
- Edit: `replace` `Beacuse` -> `Because` at 0:1
- Rule: Ensure correct spelling of words.
- Evidence: `[{"end": 1, "role": "error", "start": 0, "text": "Beacuse"}]`
- Rationale: The word 'Beacuse' is a misspelling of 'Because'. Correcting this spelling error ensures clarity and proper communication.

### rf-edit-0129::qwen3_8b::rule_grounded::evidence_canonicalized

- Bucket: `rejected`; dataset: `JFLEG`; model: `t5_base_grammar`; behavior: `wrong_correction`; operation: `replace`
- Risks: `target_copy;possible_false_rationalization;unsupported_confidence;alignment_error;validity_error_auto;semantic_distortion_auto`
- Source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study .
- Prediction: Because all those broad knowledge help them to understand their major in university as well as help them to make a correct choice in specializing study.
- Edit: `replace` `Beacuse` -> `Because` at 0:1
- Rule: Ensure correct spelling of words.
- Evidence: `[{"end": 1, "role": "error", "start": 0, "text": "Beacuse"}]`
- Rationale: The word 'Beacuse' is a clear spelling error of the correct word 'Because'. Correcting this spelling error improves the clarity and correctness of the sentence.

## Loop Result

- Commands executed: see `docs/rulefaith_loop_A_qwen3_audit.md`.
- Artifacts produced: `results/rulefaith/qwen3_manual_audit.csv`, `results/rulefaith/qwen3_manual_audit_summary.json`, and this case report.
- Hypothesis status: `revise` because the selected audit file is usable, but the automatic evidence-span checks show that the evidence verifier/prompt should be tightened before using accepted candidates as final positives.
- Next highest-priority loop: implement targeted refinement only after adding stricter evidence-span validation and manual spot-checking the selected rows.

# RuleFaith Teacher Candidate Diagnostics

Input: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/teacher_candidates_pilot.jsonl`

## Summary

- Candidate count: 160
- Provider counts: {'open_teacher': 160}
- Candidate type counts: {'natural': 80, 'rule_grounded': 80}
- Parse status counts: {'wrapped_non_json_response': 160}

## Provider Metrics

| Provider | N | Parse JSON | Alignment Proxy | Missing Rule | Rule Edit-Copy | Contextual Evidence | High Risk | Markdown JSON | Abstain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| open_teacher | 160 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |

## Highest-Risk Examples

- `rf-edit-0251::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "street" is a contraction of the verb "street".'
- `rf-edit-0251::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale="The word 'syllable' is a grammatical error."
- `rf-edit-0276::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "the" is a grammatical irregularity.'
- `rf-edit-0276::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "the" is a grammatical error.'
- `rf-edit-0277::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "the" is a grammatical rephrasing of the verb "the".'
- `rf-edit-0277::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "too" is a grammatical error.'
- `rf-edit-0248::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The name of a restaurant is the name of the food it serves.'
- `rf-edit-0248::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "it" is a grammatical or usage rule.'
- `rf-edit-0255::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "sister" is a grammatical contraction of the word "daughter".'
- `rf-edit-0255::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "sister" is a grammatical irregularity.'
- `rf-edit-0267::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='A grammatical error occurs when a word is spelled incorrectly.'
- `rf-edit-0267::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale="The word 'a' is a grammatical error."
- `rf-edit-0261::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "half" is a grammatical contraction of the verb "half".'
- `rf-edit-0261::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "half" is a contraction of the verb "half".'
- `rf-edit-0273::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='A general election should be called and then see if the Monarchy should be abolished.'
- `rf-edit-0273::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The grammatical or usage rule is that if a word is used in a sentence, it must be in the present tense.'
- `rf-edit-0289::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "finally" is a grammatical rephrasing of the word "now".'
- `rf-edit-0289::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "finally" is a grammatical error.'
- `rf-edit-0278::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "side" has a negative side and a positive side.'
- `rf-edit-0278::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The grammatical or usage rule is that if a word is used in a sentence, it must be in the present tense.'
- `rf-edit-0240::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='A restaurant is a place where food is served. The food is usually served in a dish that has a sauce on it. The sauce on the dish is usually garlic sauce. The service at a restauran'
- `rf-edit-0240::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The grammatical or usage rule is that if a word is used in a sentence, it must be in the present tense.'
- `rf-edit-0268::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale="We can think about the mobile phone, the computer, and finally the internet. Our grandparents couldn't have imagined a strange machine like the computer in their lives."
- `rf-edit-0268::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "computer" is a contraction of the verb "computer".'
- `rf-edit-0291::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "sausage" is a grammatical rephrasing of the word "cheese".'
- `rf-edit-0291::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "sausage" is a grammatical or usage rule.'
- `rf-edit-0292::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "sauce" is a grammatical rephrase of the word "sausage".'
- `rf-edit-0292::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "sauce" is a grammatical or usage rule.'
- `rf-edit-0265::open_teacher::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "is" is a misspelling of "is".'
- `rf-edit-0265::open_teacher::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule=''; rationale='The word "is" is a contraction of the verb "is".'

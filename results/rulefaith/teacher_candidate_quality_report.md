# Teacher Candidate Quality Report

Input: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/teacher_candidates_pilot.jsonl`

## Summary

- `candidate_count`: 160
- `provider_counts`: {'open_teacher': 160}
- `teacher_model_counts`: {'google/flan-t5-base': 160}
- `candidate_type_counts`: {'natural': 80, 'rule_grounded': 80}
- `parse_status_counts`: {'wrapped_non_json_response': 160}
- `generic_count`: 90
- `prompt_contamination_count`: 0
- `source_copy_like_count`: 8
- `too_short_count`: 0
- `low_quality_count`: 98
- `low_quality_rate`: 0.6125

## Highest-Risk Examples

- `rf-edit-0125::open_teacher::natural`: We can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents did n't watch tv because there wasn't any TV in the world when they were young.but that is n’t the only difference : we 
- `rf-edit-0125::open_teacher::rule_grounded`: We can think about how different our lives are compared to our parents' or grandparents' lives . For example, my parents didn't watch tv because there wasn't any TV in the world when they were young.but that isn't the only difference : we c
- `rf-edit-0257::open_teacher::natural`: We can think how different our lives are compared to either our parents' or our grandparents' lives. For example, my parents didn't watch tv because there wasn't any TV in the world when they were young. But that isn't the only difference: 
- `rf-edit-0257::open_teacher::rule_grounded`: We can think how different our lives are compared to either our parents' or our grandparents' lives. For example, my parents didn't watch tv because there wasn't any TV in the world when they were young. But that isn't the only difference: 
- `rf-edit-0033::open_teacher::natural`: The word "the" is a grammatical rephrase of the word "buses , trains , the metro and more , for a single reason : the quality of life against the pollution .
- `rf-edit-0098::open_teacher::rule_grounded`: The sentence " I was very fast , my best time was 5 5 5 seconds in 4 0 0 hundred meters is a good time in or country .
- `rf-edit-0150::open_teacher::natural`: If a person thinks to learn and understand lots of scientific subjects , any person will not do it and as a result of this any science isn't improved .
- `rf-edit-0268::open_teacher::natural`: We can think about the mobile phone, the computer, and finally the internet. Our grandparents couldn't have imagined a strange machine like the computer in their lives.
- `rf-edit-0287::open_teacher::natural`: The future of the planet will be in a bad condition and the trees will be dissappearing , after that we will have wars .
- `rf-edit-0035::open_teacher::natural`: The first sentence of a sentence is a grammatical error. The second sentence of the sentence is an error.
- `rf-edit-0021::open_teacher::natural`: The first sentence of a sentence is a grammatical error. The second sentence of the sentence is an error.
- `rf-edit-0129::open_teacher::natural`: The first sentence of a sentence is a grammatical error. The second sentence of the sentence is an error.
- `rf-edit-0056::open_teacher::natural`: The word "cigarettes" is a grammatical rephrasing of the word "alcohol , hair spray , and cigarrets .
- `rf-edit-0052::open_teacher::natural`: The first sentence of a sentence is a grammatical error. The second sentence is an error.
- `rf-edit-0170::open_teacher::natural`: The first sentence of a sentence is a grammatical error correction model edit.
- `rf-edit-0141::open_teacher::natural`: The word "harmful" is a grammatical rephrasing of the word "nocive" or "bad".
- `rf-edit-0034::open_teacher::natural`: The word 'pot' is a grammatical rephrasing of the verb 'tea '.
- `rf-edit-0107::open_teacher::natural`: The word 'pot' is a grammatical rephrasing of the verb 'tea '.
- `rf-edit-0068::open_teacher::rule_grounded`: The word " most " is a grammatical or usage rule .
- `rf-edit-0026::open_teacher::rule_grounded`: The word 'their' is a grammatical rephrasing of the verb 's' .

## Interpretation

The open-teacher candidates are useful as a weak baseline and failure signal, but they are not strong enough to replace the GPT-5.5 teacher pilot.

# RuleFaith Teacher Candidate Diagnostics

Input: `/Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen15_probe_candidates.jsonl`

## Summary

- Candidate count: 20
- Provider counts: {'qwen_small': 20}
- Candidate type counts: {'natural': 10, 'rule_grounded': 10}
- Parse status counts: {'parsed_json': 20}

## Provider Metrics

| Provider | N | Parse JSON | Alignment Proxy | Missing Rule | Rule Edit-Copy | Contextual Evidence | High Risk | Markdown JSON | Abstain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| qwen_small | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 0.350 | 1.000 | 0.950 | 0.000 |

## Highest-Risk Examples

- `rf-edit-0009::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=True; rule='None'; rationale="The edit replaces the verb 'try' with 'tries', which is a natural and grammatically correct alternative."
- `rf-edit-0009::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=True; rule='None'; rationale="The edit replaces the verb 'try' with 'tries', which is a valid grammatical change."
- `rf-edit-0001::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=True; rule='None'; rationale="The edit inserts 'about' at the specified span, which changes the meaning of the sentence but does not alter the structure or punctuation of the sentence."
- `rf-edit-0001::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale='The edit does not make sense grammatically or semantically within the context of the sentence.'
- `rf-edit-0004::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=True; rule='None'; rationale="Replacing 'to' with 'of' changes the meaning from 'to' (direction) to 'of' (possessive), which is a valid grammatical change."
- `rf-edit-0004::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=True; rule='None'; rationale="Replacing 'to' with 'of' changes the meaning from 'to' (direction) to 'of' (possessive), which is a valid grammatical change."
- `rf-edit-0003::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="Replacing 'that' with 'which' correctly introduces a non-restrictive relative clause."
- `rf-edit-0003::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="Replacing 'that' with 'which' correctly introduces a non-restrictive relative clause."
- `rf-edit-0006::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces a single word ('tree') with another single word ('trees'), which is a straightforward substitution."
- `rf-edit-0006::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces a single word ('tree') with another single word ('trees'), which is a straightforward replacement."
- `rf-edit-0010::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces the incorrect verb 'sacred' with the correct verb 'kept going', which improves the grammatical accuracy of the sentence."
- `rf-edit-0010::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces the incorrect verb 'sacred' with the correct verb 'kept going', which improves the grammatical accuracy of the sentence."
- `rf-edit-0011::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces the word 'lost' with 'lose', which is a natural and grammatically correct substitution."
- `rf-edit-0011::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces the word 'lost' with 'lose', which is a valid grammatical change."
- `rf-edit-0000::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=True; rule='None'; rationale="Deleting 'the' before 'consumers' and 'like me' does not change the meaning of the sentence."
- `rf-edit-0000::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=True; rule='None'; rationale="Deleting 'the' at the beginning of the sentence does not change the meaning or structure of the sentence."
- `rf-edit-0002::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces the pronoun 'they' with 'there', which is a valid grammatical change."
- `rf-edit-0002::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces the word 'they' with 'there', which is a valid replacement in this context."
- `rf-edit-0005::qwen_small::natural`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces 'people' with 'person' at the specified span, which is a straightforward replacement."
- `rf-edit-0005::qwen_small::rule_grounded`: alignment=True, missing_rule=True, rule_edit_copy=True, contextual_evidence=False; rule='None'; rationale="The edit replaces 'people' with 'person' at the specified span, which is a direct replacement of words."

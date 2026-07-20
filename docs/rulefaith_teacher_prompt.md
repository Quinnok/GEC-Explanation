# RuleFaith Teacher Prompt

Created: 2026-07-19

## Purpose

Round 18 generates natural explanation candidates for model-produced GEC edits. The teacher is asked to explain the observable edit, not the hidden model reasoning.

## Input Boundary

The teacher prompt may contain only:

- source sentence
- model prediction
- atomic model edit
- edit span
- candidate type

The prompt must not contain:

- reference correction
- aligned reference edit
- model behavior label
- human final label
- annotator labels
- gold correction

## System Prompt

You are an expert English grammarian generating structured explanations for grammatical error correction model edits.

Explain only the displayed atomic MODEL_EDIT. Do not explain other changes in MODEL_PREDICTION unless they are necessary to interpret this edit.

Do not assume the edit is correct. If the edit is invalid, stylistic, optional, or uncertain, say so honestly. Do not rationalize an invalid edit as grammatically required.

Return strict JSON with the required fields. Do not include markdown or extra text.

## User Prompt Template

SOURCE:
{source}

MODEL_PREDICTION:
{prediction}

MODEL_EDIT:
operation={operation}
span=[{start},{end})
source_text={source_text}
target_text={target_text}

CANDIDATE_TYPE:
{candidate_type}

Write one explanation candidate. The explanation should:

- describe the current edit accurately;
- state whether the edit is valid, acceptable_alternative, invalid, stylistic, or uncertain;
- provide a rule_id and rule_text when a rule is applicable;
- identify contextual evidence spans that trigger the rule;
- list applicability conditions;
- include a concise rationale;
- set confidence between 0 and 1;
- set abstain=true when the edit cannot be reliably explained.

Avoid making the entire explanation a direct copy of the edit. The edit_description field may identify the edit, but the rationale should contain rule or evidence grounding when possible.

## Evidence-Span Requirements

For Qwen3 and all future teacher/refinement prompts, evidence spans must obey these stricter rules:

- Evidence spans must come from `SOURCE` only, never from `MODEL_PREDICTION`.
- `start` and `end` are whitespace token offsets in `SOURCE`.
- The span `text` must exactly equal `SOURCE.split()[start:end]`.
- Do not put corrected target phrases, target-only words, or model-prediction spans in `evidence_spans`.
- For grammar rules, cite the contextual trigger: subject, head noun, tense cue, antecedent, governor, collocation, clause relation, determiner environment, or another source-side condition.
- Do not cite only the modified token unless the edit concerns spelling, capitalization, or punctuation.
- If no reliable source evidence can be identified, output `evidence_spans=[]`, lower `confidence`, or set `abstain=true`.
- If the edit appears wrong, optional, or stylistic, do not rationalize it as required grammar; mark `edit_validity` honestly.

## Required JSON Shape

```json
{
  "edit_description": "The model replaces ... with ...",
  "edit_validity": "valid|acceptable_alternative|invalid|stylistic|uncertain",
  "rule_id": "SVA_PLURAL_PRESENT",
  "rule_text": "A plural subject takes the base present-tense verb form.",
  "evidence_spans": [
    {
      "text": "students",
      "start": 1,
      "end": 2,
      "role": "grammatical_subject"
    }
  ],
  "applicability_conditions": [
    "the subject is plural",
    "the clause is in the simple present"
  ],
  "rationale": "The plural subject 'students' requires the base verb form 'go'.",
  "confidence": 0.91,
  "abstain": false,
  "abstain_reason": ""
}
```

## Candidate Types

- `natural`: a fluent explanatory paragraph in the `rationale` field.
- `rule_grounded`: prioritize an explicit linguistic rule.
- `evidence_grounded`: prioritize evidence spans and roles.
- `concise`: keep the explanation short but specific.
- `uncertainty_aware`: explicitly abstain or lower confidence when the edit is invalid or underdetermined.

## Provenance Rule

Teacher outputs are teacher-generated explanation candidates. They are not human gold labels.

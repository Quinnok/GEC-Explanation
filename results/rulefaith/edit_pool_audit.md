# RuleFaith Edit Pool Audit

Selected edits: 300
Excluded detokenization/format artifacts: 251

## Counts

### dataset

- `EXPECT`: 165
- `JFLEG`: 135

### model_key

- `coedit_large`: 60
- `gector_roberta_base`: 120
- `t5_base_grammar`: 120

### model_family

- `instruction-following text editor`: 60
- `sequence-to-edit`: 120
- `sequence-to-sequence`: 120

### behavior

- `correct_correction`: 77
- `overcorrection`: 151
- `wrong_correction`: 72

### operation

- `delete`: 33
- `insert`: 30
- `replace`: 237

### error_type

- `M:ADJ`: 1
- `M:ADV`: 1
- `M:DET`: 13
- `M:NOUN:POSS`: 1
- `M:OTHER`: 10
- `M:PREP`: 4
- `M:PUNCT`: 1
- `M:VERB`: 2
- `M:VERB:TENSE`: 4
- `R:ADJ`: 3
- `R:ADV`: 2
- `R:CONTR`: 2
- `R:DET`: 4
- `R:MORPH`: 4
- `R:NOUN`: 36
- `R:NOUN:INFL`: 1
- `R:NOUN:NUM`: 14
- `R:ORTH`: 1
- `R:OTHER`: 69
- `R:PART`: 2
- `R:PREP`: 14
- `R:PRON`: 8
- `R:SPELL`: 34
- `R:VERB`: 10
- `R:VERB:FORM`: 5
- `R:VERB:SVA`: 5
- `R:VERB:TENSE`: 5
- `R:WO`: 5
- `U:ADJ`: 1
- `U:CONJ`: 3
- `U:DET`: 10
- `U:NOUN`: 1
- `U:OTHER`: 11
- `U:PREP`: 5
- `U:PRON`: 3
- `U:PUNCT`: 1
- `U:VERB`: 2
- `U:VERB:TENSE`: 2

### error_category

- `articles_determiners`: 27
- `clause_structure`: 7
- `lexical_choice`: 137
- `noun_number`: 14
- `prepositions`: 23
- `pronouns`: 11
- `punctuation`: 2
- `spelling_orthography`: 39
- `subject_verb_agreement`: 5
- `verb_form`: 19
- `verb_tense`: 11
- `word_order`: 5

### split

- `dev`: 39
- `test`: 55
- `train`: 206

## Split Audits

- Source keys crossing splits: 0
- Target strings crossing splits: 13
- Near-duplicate source pairs at >=0.92 similarity: 0

Target strings crossing splits are recorded as an audit signal, not silently removed. Later target-masked experiments must report robustness to these repeats.

## Multi-Reference Handling

JFLEG examples retain the existing benchmark limitation: primary ERRANT extraction uses the selected reference stored in the record, while source/sample ids allow later accept-if-any-reference alignment. This pool does not claim final multi-reference equivalence.

## Scientific Boundary

The pool is selected for natural teacher generation and method development. It is not a new human-gold label set.

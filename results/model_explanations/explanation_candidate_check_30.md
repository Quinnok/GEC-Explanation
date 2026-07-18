# Open-Source Explanation Candidate Check

These are FLAN-T5-base candidates generated from source, model prediction, and the model edit span. They are not human gold and are not template explanations.

## 1. expect-test-00000::gector_roberta_base::0::8-9

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Predicted edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- Candidate: `The verb ' syllable '' .`
- Flags: `no_automatic_flag`

## 2. expect-test-00001::gector_roberta_base::1::2-3

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 3, "error_type": "R:SPELL", "operation": "replace", "source_text": "chanched", "start": 2, "target_text": "changed"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 3. expect-test-00001::gector_roberta_base::2::11-11

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 11, "target_text": ","}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 4. expect-test-00001::gector_roberta_base::3::14-14

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 14, "error_type": "M:PREP", "operation": "insert", "source_text": "", "start": 14, "target_text": "about"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 5. expect-test-00001::gector_roberta_base::4::16-17

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 17, "error_type": "U:VERB", "operation": "delete", "source_text": "is", "start": 16, "target_text": ""}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 6. expect-test-00001::gector_roberta_base::5::18-19

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 19, "error_type": "R:OTHER", "operation": "replace", "source_text": "life", "start": 18, "target_text": "lives are"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 7. expect-test-00001::gector_roberta_base::6::33-33

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 33, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 33, "target_text": ","}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 8. expect-test-00001::gector_roberta_base::7::38-39

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 39, "error_type": "R:ORTH", "operation": "replace", "source_text": "tv", "start": 38, "target_text": "TV"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 9. expect-test-00001::gector_roberta_base::8::45-46

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 46, "error_type": "R:ORTH", "operation": "replace", "source_text": "tv", "start": 45, "target_text": "TV"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 10. expect-test-00001::gector_roberta_base::9::52-52

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 52, "error_type": "M:NOUN", "operation": "insert", "source_text": "", "start": 52, "target_text": "children"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 11. expect-test-00001::gector_roberta_base::10::52-54

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 54, "error_type": "R:OTHER", "operation": "replace", "source_text": "young.but that", "start": 52, "target_text": ". That"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 12. expect-test-00001::gector_roberta_base::11::70-71

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Predicted edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- Candidate: `Technology has changed people 's lives a lot .`
- Flags: `no_automatic_flag`

## 13. expect-test-00002::gector_roberta_base::12::3-4

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Predicted edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- Candidate: `The word ' car' refers to a vehicle that has a lot of cars in it .`
- Flags: `no_automatic_flag`

## 14. expect-test-00002::gector_roberta_base::13::7-7

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 7, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 7, "target_text": ","}`
- Candidate: `The word ' car' refers to a vehicle that has a lot of cars in it .`
- Flags: `no_automatic_flag`

## 15. expect-test-00002::gector_roberta_base::14::8-9

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 9, "error_type": "U:DET", "operation": "delete", "source_text": "the", "start": 8, "target_text": ""}`
- Candidate: `The word ' car ' is a grammatical term for a car .`
- Flags: `no_automatic_flag`

## 16. expect-test-00002::gector_roberta_base::15::10-10

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 10, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 10, "target_text": ","}`
- Candidate: `The word ' car' refers to a vehicle that has a lot of cars in it .`
- Flags: `no_automatic_flag`

## 17. expect-test-00002::gector_roberta_base::16::22-22

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 22, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 22, "target_text": ","}`
- Candidate: `The following is a list of words that have the same meaning :`
- Flags: `generic_list_like`

## 18. expect-test-00002::gector_roberta_base::17::23-23

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 23, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 23, "target_text": ","}`
- Candidate: `The following is a list of words that have the same meaning:`
- Flags: `generic_list_like`

## 19. expect-test-00003::gector_roberta_base::18::10-11

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Predicted edit: `{"end": 11, "error_type": "R:PRON", "operation": "replace", "source_text": "they", "start": 10, "target_text": "there"}`
- Candidate: `The word ' , ' " , is a syllable meaning '' .`
- Flags: `no_automatic_flag`

## 20. expect-test-00004::gector_roberta_base::19::22-23

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Predicted edit: `{"end": 23, "error_type": "R:NOUN", "operation": "replace", "source_text": "travel", "start": 22, "target_text": "journey"}`
- Candidate: `The following is a list of public transportation in the United States :`
- Flags: `generic_list_like`

## 21. expect-test-00004::gector_roberta_base::20::23-24

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 24, "error_type": "R:OTHER", "operation": "replace", "source_text": "for", "start": 23, "target_text": ","}`
- Candidate: `Public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey , then to see more action .`
- Flags: `no_automatic_flag`

## 22. expect-test-00005::gector_roberta_base::21::10-10

- Model: `gector_roberta_base`
- Behavior: `wrong_correction`
- Predicted edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "the"}`
- Candidate: `The word ' , ' or ' " , is a syllable meaning '' .`
- Flags: `no_automatic_flag`

## 23. expect-test-00005::gector_roberta_base::22::10-11

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 11, "error_type": "R:ORTH", "operation": "replace", "source_text": "Museum", "start": 10, "target_text": "museum"}`
- Candidate: `The word ' , ' or ' " , refers to the same thing .`
- Flags: `no_automatic_flag`

## 24. expect-test-00006::gector_roberta_base::23::7-8

- Model: `gector_roberta_base`
- Behavior: `correct_correction`
- Predicted edit: `{"end": 8, "error_type": "R:MORPH", "operation": "replace", "source_text": "champion", "start": 7, "target_text": "championship"}`
- Candidate: `The verb should agree with the singular subject.`
- Flags: `few_shot_copy_like`

## 25. expect-test-00007::gector_roberta_base::24::13-14

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 14, "error_type": "R:OTHER", "operation": "replace", "source_text": "very", "start": 13, "target_text": "great"}`
- Candidate: `The following is a list of words that have the same meaning :`
- Flags: `generic_list_like`

## 26. expect-test-00007::gector_roberta_base::25::34-34

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 34, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 34, "target_text": ","}`
- Candidate: `The following is a list of words that have the same meaning :`
- Flags: `generic_list_like`

## 27. expect-test-00007::gector_roberta_base::26::52-53

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 53, "error_type": "R:NOUN", "operation": "replace", "source_text": "something", "start": 52, "target_text": "things"}`
- Candidate: `The following is a list of words that have the same meaning :`
- Flags: `generic_list_like`

## 28. expect-test-00008::gector_roberta_base::27::10-11

- Model: `gector_roberta_base`
- Behavior: `wrong_correction`
- Predicted edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "replace", "source_text": "its", "start": 10, "target_text": ". Its"}`
- Candidate: `A restaurant is a place to eat .`
- Flags: `no_automatic_flag`

## 29. expect-test-00008::gector_roberta_base::28::16-16

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 16, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 16, "target_text": "."}`
- Candidate: `The following is a list of restaurant names in the United States :`
- Flags: `generic_list_like`

## 30. expect-test-00008::gector_roberta_base::29::21-22

- Model: `gector_roberta_base`
- Behavior: `overcorrection`
- Predicted edit: `{"end": 22, "error_type": "M:PUNCT", "operation": "replace", "source_text": "it", "start": 21, "target_text": ". It"}`
- Candidate: `A restaurant is a place where people go to eat .`
- Flags: `no_automatic_flag`


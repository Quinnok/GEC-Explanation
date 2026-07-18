# Model Edit Alignment Check

This report compares source-reference ERRANT edits against source-prediction ERRANT edits for real model outputs.

## 1. gector_roberta_base::expect-test-00000

- Source: `In my community , we are very interested at the environment and ecological things .`
- Reference: `In my community , we are very interested in the environment and ecological things .`
- Prediction: `In my community , we are very interested in the environment and ecological things .`
- Reference edits: `[{"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}]`
- Predicted edits: `[{"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}]`
- Missed edits: `[]`

## 2. gector_roberta_base::expect-test-00001

- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference edits: `[{"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Predicted edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 11, "end": 11, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 14, "end": 14, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 33, "end": 33, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 38, "end": 39, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 45, "end": 46, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 52, "source_text": "", "target_text": "children", "operation": "insert", "error_type": "M:NOUN"}, {"start": 52, "end": 54, "source_text": "young.but that", "target_text": ". That", "operation": "replace", "error_type": "R:OTHER"}, {"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 6, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 7, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 8, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 9, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 10, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}]`
- Missed edits: `[]`

## 3. gector_roberta_base::expect-test-00002

- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Reference edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "U:PREP"}]`
- Predicted edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "U:PREP"}, {"start": 7, "end": 7, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}, {"start": 10, "end": 10, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 22, "end": 22, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 23, "end": 23, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 4. gector_roberta_base::expect-test-00003

- Source: `Although there are many positive points about private cars , they are also negative ones .`
- Reference: `Although there are many positive points about private cars , there are also negative ones .`
- Prediction: `Although there are many positive points about private cars , there are also negative ones .`
- Reference edits: `[{"start": 10, "end": 11, "source_text": "they", "target_text": "there", "operation": "replace", "error_type": "R:PRON"}]`
- Predicted edits: `[{"start": 10, "end": 11, "source_text": "they", "target_text": "there", "operation": "replace", "error_type": "R:PRON"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}]`
- Missed edits: `[]`

## 5. gector_roberta_base::expect-test-00004

- Source: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting travel for then to see more action .`
- Reference: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey for then to see more action .`
- Prediction: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey , then to see more action .`
- Reference edits: `[{"start": 22, "end": 23, "source_text": "travel", "target_text": "journey", "operation": "replace", "error_type": "R:NOUN"}]`
- Predicted edits: `[{"start": 22, "end": 23, "source_text": "travel", "target_text": "journey", "operation": "replace", "error_type": "R:NOUN"}, {"start": 23, "end": 24, "source_text": "for", "target_text": ",", "operation": "replace", "error_type": "R:OTHER"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 6. gector_roberta_base::expect-test-00005

- Source: `They were planning to steal a very precious thing from Museum tonight .`
- Reference: `They were planning to steal a very precious thing from a Museum tonight .`
- Prediction: `They were planning to steal a very precious thing from the museum tonight .`
- Reference edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}]`
- Predicted edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "M:DET"}, {"start": 10, "end": 11, "source_text": "Museum", "target_text": "museum", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "wrong_correction", "score": 1.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 7. gector_roberta_base::expect-test-00006

- Source: `I hope my house will win the champion next year .`
- Reference: `I hope my house will win the championship next year .`
- Prediction: `I hope my house will win the championship next year .`
- Reference edits: `[{"start": 7, "end": 8, "source_text": "champion", "target_text": "championship", "operation": "replace", "error_type": "R:MORPH"}]`
- Predicted edits: `[{"start": 7, "end": 8, "source_text": "champion", "target_text": "championship", "operation": "replace", "error_type": "R:MORPH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}]`
- Missed edits: `[]`

## 8. gector_roberta_base::expect-test-00007

- Source: `In conclusion , I think that this type of food and atmosphere is very for us , because normally we speak about books , work and studies , whereas with this type of environment we can speak about ourselves , our family , our hobbies and everyone will get to know new something about other classmates .`
- Reference: `In conclusion , I think that this type of food and atmosphere is very good for us , because normally we speak about books , work and studies , whereas with this type of environment we can speak about ourselves , our family , our hobbies and everyone will get to know new something about other classmates .`
- Prediction: `In conclusion , I think that this type of food and atmosphere is great for us , because normally we speak about books , work and studies , whereas with this type of environment , we can speak about ourselves , our family , our hobbies and everyone will get to know new things about other classmates .`
- Reference edits: `[{"start": 14, "end": 14, "source_text": "", "target_text": "good", "operation": "insert", "error_type": "M:ADJ"}]`
- Predicted edits: `[{"start": 13, "end": 14, "source_text": "very", "target_text": "great", "operation": "replace", "error_type": "R:OTHER"}, {"start": 34, "end": 34, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 52, "end": 53, "source_text": "something", "target_text": "things", "operation": "replace", "error_type": "R:NOUN"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 14, "end": 14, "source_text": "", "target_text": "good", "operation": "insert", "error_type": "M:ADJ"}}]`

## 9. gector_roberta_base::expect-test-00008

- Source: `I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Reference: `I 'd like to tell you about my favorite restaurant . It 's name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Prediction: `I 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Reference edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 10, "end": 11, "source_text": "its", "target_text": "It 's", "operation": "replace", "error_type": "R:OTHER"}]`
- Predicted edits: `[{"start": 10, "end": 11, "source_text": "its", "target_text": ". Its", "operation": "replace", "error_type": "M:PUNCT"}, {"start": 16, "end": 16, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 21, "end": 22, "source_text": "it", "target_text": ". It", "operation": "replace", "error_type": "M:PUNCT"}, {"start": 25, "end": 26, "source_text": "to", "target_text": "than", "operation": "replace", "error_type": "R:PREP"}, {"start": 28, "end": 28, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 36, "end": 36, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 39, "end": 40, "source_text": "Excellent", "target_text": "excellent", "operation": "replace", "error_type": "R:ORTH"}, {"start": 44, "end": 45, "source_text": "My", "target_text": "my", "operation": "replace", "error_type": "R:ORTH"}, {"start": 50, "end": 53, "source_text": "in order that", "target_text": "for", "operation": "replace", "error_type": "R:OTHER"}, {"start": 54, "end": 54, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 64, "end": 64, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "wrong_correction", "score": 1.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 6, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 7, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 8, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 9, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 10, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 1, "behavior": "missed_correction", "reference_edit": {"start": 10, "end": 11, "source_text": "its", "target_text": "It 's", "operation": "replace", "error_type": "R:OTHER"}}]`

## 10. gector_roberta_base::expect-test-00009

- Source: `But such a high level of development of Egyptian civilization has a negative side as well as positive .`
- Reference: `But such a high level of development of Egyptian civilization has a negative side as well as a positive .`
- Prediction: `But such a high level of development of Egyptian civilization has a negative side as well as positive .`
- Reference edits: `[{"start": 17, "end": 17, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}]`
- Predicted edits: `[]`
- Alignment: `[]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 17, "end": 17, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}}]`

## 11. gector_roberta_base::expect-test-00010

- Source: `Until dawn all of them had got out , so they sacred until they found a refuge .`
- Reference: `By dawn all of them had got out , so they sacred until they found a refuge .`
- Prediction: `Until dawn , all of them had got out , so they kept going until they found a refuge .`
- Reference edits: `[{"start": 0, "end": 1, "source_text": "Until", "target_text": "By", "operation": "replace", "error_type": "R:PREP"}]`
- Predicted edits: `[{"start": 2, "end": 2, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 11, "end": 12, "source_text": "sacred", "target_text": "kept going", "operation": "replace", "error_type": "R:VERB"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 0, "end": 1, "source_text": "Until", "target_text": "By", "operation": "replace", "error_type": "R:PREP"}}]`

## 12. gector_roberta_base::expect-test-00011

- Source: `What a wonderful day ! There is April now and finally spring has come .`
- Reference: `What a wonderful day ! It is April now and finally spring has come .`
- Prediction: `What a wonderful day ! It is April now and finally spring has come .`
- Reference edits: `[{"start": 5, "end": 6, "source_text": "There", "target_text": "It", "operation": "replace", "error_type": "R:PRON"}]`
- Predicted edits: `[{"start": 5, "end": 6, "source_text": "There", "target_text": "It", "operation": "replace", "error_type": "R:PRON"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}]`
- Missed edits: `[]`

## 13. gector_roberta_base::expect-test-00012

- Source: `The traffic can affect cars and buses at the same extent .`
- Reference: `The traffic can affect cars and buses to the same extent .`
- Prediction: `The traffic can affect cars and buses to the same extent .`
- Reference edits: `[{"start": 7, "end": 8, "source_text": "at", "target_text": "to", "operation": "replace", "error_type": "R:PREP"}]`
- Predicted edits: `[{"start": 7, "end": 8, "source_text": "at", "target_text": "to", "operation": "replace", "error_type": "R:PREP"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}]`
- Missed edits: `[]`

## 14. gector_roberta_base::expect-test-00013

- Source: `Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .`
- Reference: `Computers have had a most significant impact on people in the latter 1/2 of the 20th century .`
- Prediction: `Computers have had the most significant impact on people in the latter 1/2 of the 20th century .`
- Reference edits: `[{"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}]`
- Predicted edits: `[{"start": 3, "end": 4, "source_text": "a", "target_text": "the", "operation": "replace", "error_type": "R:DET"}, {"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}]`
- Missed edits: `[]`

## 15. gector_roberta_base::expect-test-00014

- Source: `i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Reference: `i love my family especially my little sister , she is sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Prediction: `I love my family , especially my little sister . She is sixteen years old . I consider her my best friend because I usually tell her everything about my life .`
- Reference edits: `[{"start": 10, "end": 11, "source_text": "has", "target_text": "is", "operation": "replace", "error_type": "R:VERB"}]`
- Predicted edits: `[{"start": 0, "end": 1, "source_text": "i", "target_text": "I", "operation": "replace", "error_type": "R:ORTH"}, {"start": 4, "end": 4, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 8, "end": 10, "source_text": ", she", "target_text": ". She", "operation": "replace", "error_type": "R:PUNCT"}, {"start": 10, "end": 11, "source_text": "has", "target_text": "is", "operation": "replace", "error_type": "R:VERB"}, {"start": 14, "end": 16, "source_text": ", i", "target_text": ". I", "operation": "replace", "error_type": "R:PUNCT"}, {"start": 22, "end": 23, "source_text": "i", "target_text": "I", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 16. t5_base_grammar::expect-test-00000

- Source: `In my community , we are very interested at the environment and ecological things .`
- Reference: `In my community , we are very interested in the environment and ecological things .`
- Prediction: `In my community, we are very interested in the environment and ecological things.`
- Reference edits: `[{"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}]`
- Predicted edits: `[{"start": 2, "end": 4, "source_text": "community ,", "target_text": "community,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}, {"start": 13, "end": 15, "source_text": "things .", "target_text": "things.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 17. t5_base_grammar::expect-test-00001

- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Prediction: `Technology has changed people's lives a lot. In fact, we can think about how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Reference edits: `[{"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Predicted edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 3, "end": 5, "source_text": "people 's", "target_text": "people's", "operation": "replace", "error_type": "R:ORTH"}, {"start": 7, "end": 9, "source_text": "lot .", "target_text": "lot.", "operation": "replace", "error_type": "R:ORTH"}, {"start": 10, "end": 11, "source_text": "fact", "target_text": "fact,", "operation": "replace", "error_type": "R:NOUN"}, {"start": 14, "end": 14, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 20, "end": 21, "source_text": "either", "target_text": "", "operation": "delete", "error_type": "U:CONJ"}, {"start": 23, "end": 25, "source_text": "parents '", "target_text": "parents'", "operation": "replace", "error_type": "R:ORTH"}, {"start": 26, "end": 27, "source_text": "our", "target_text": "", "operation": "delete", "error_type": "U:DET"}, {"start": 27, "end": 31, "source_text": "grandparents ' lives .", "target_text": "grandparents' lives.", "operation": "replace", "error_type": "R:ORTH"}, {"start": 32, "end": 33, "source_text": "example", "target_text": "example,", "operation": "replace", "error_type": "R:OTHER"}, {"start": 35, "end": 37, "source_text": "did n't", "target_text": "didn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 39, "end": 40, "source_text": ",", "target_text": "", "operation": "delete", "error_type": "U:PUNCT"}, {"start": 42, "end": 44, "source_text": "was n't", "target_text": "wasn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 54, "end": 56, "source_text": "is n't", "target_text": "isn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}, {"start": 87, "end": 89, "source_text": "lives .", "target_text": "lives.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 6, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 7, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 8, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 9, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 10, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 11, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 12, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 13, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 14, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 15, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 16, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 17, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 18. t5_base_grammar::expect-test-00002

- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Prediction: `We should use public transportation because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world.`
- Reference edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "U:PREP"}]`
- Predicted edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "U:PREP"}, {"start": 5, "end": 6, "source_text": "transport", "target_text": "transportation", "operation": "replace", "error_type": "R:MORPH"}, {"start": 30, "end": 32, "source_text": "world .", "target_text": "world.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 19. t5_base_grammar::expect-test-00003

- Source: `Although there are many positive points about private cars , they are also negative ones .`
- Reference: `Although there are many positive points about private cars , there are also negative ones .`
- Prediction: `There are many positive points about private cars, but they are also negative ones.`
- Reference edits: `[{"start": 10, "end": 11, "source_text": "they", "target_text": "there", "operation": "replace", "error_type": "R:PRON"}]`
- Predicted edits: `[{"start": 0, "end": 2, "source_text": "Although there", "target_text": "There", "operation": "replace", "error_type": "U:PREP"}, {"start": 8, "end": 9, "source_text": "cars", "target_text": "cars,", "operation": "replace", "error_type": "R:NOUN"}, {"start": 9, "end": 10, "source_text": ",", "target_text": "but", "operation": "replace", "error_type": "R:OTHER"}, {"start": 14, "end": 16, "source_text": "ones .", "target_text": "ones.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 10, "end": 11, "source_text": "they", "target_text": "there", "operation": "replace", "error_type": "R:PRON"}}]`

## 20. t5_base_grammar::expect-test-00004

- Source: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting travel for then to see more action .`
- Reference: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey for then to see more action .`
- Prediction: `However, public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting travel for then to see more action.`
- Reference edits: `[{"start": 22, "end": 23, "source_text": "travel", "target_text": "journey", "operation": "replace", "error_type": "R:NOUN"}]`
- Predicted edits: `[{"start": 0, "end": 2, "source_text": "However ,", "target_text": "However,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 28, "end": 30, "source_text": "action .", "target_text": "action.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 22, "end": 23, "source_text": "travel", "target_text": "journey", "operation": "replace", "error_type": "R:NOUN"}}]`

## 21. t5_base_grammar::expect-test-00005

- Source: `They were planning to steal a very precious thing from Museum tonight .`
- Reference: `They were planning to steal a very precious thing from a Museum tonight .`
- Prediction: `Then, they were planning to steal a very precious thing from the museum tonight.`
- Reference edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}]`
- Predicted edits: `[{"start": 0, "end": 1, "source_text": "They", "target_text": "Then, they", "operation": "replace", "error_type": "M:ADV"}, {"start": 10, "end": 10, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "M:DET"}, {"start": 10, "end": 13, "source_text": "Museum tonight .", "target_text": "museum tonight.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": 0, "behavior": "wrong_correction", "score": 1.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 22. t5_base_grammar::expect-test-00006

- Source: `I hope my house will win the champion next year .`
- Reference: `I hope my house will win the championship next year .`
- Prediction: `I hope my house will win the championship next year.`
- Reference edits: `[{"start": 7, "end": 8, "source_text": "champion", "target_text": "championship", "operation": "replace", "error_type": "R:MORPH"}]`
- Predicted edits: `[{"start": 7, "end": 8, "source_text": "champion", "target_text": "championship", "operation": "replace", "error_type": "R:MORPH"}, {"start": 9, "end": 11, "source_text": "year .", "target_text": "year.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 23. t5_base_grammar::expect-test-00007

- Source: `In conclusion , I think that this type of food and atmosphere is very for us , because normally we speak about books , work and studies , whereas with this type of environment we can speak about ourselves , our family , our hobbies and everyone will get to know new something about other classmates .`
- Reference: `In conclusion , I think that this type of food and atmosphere is very good for us , because normally we speak about books , work and studies , whereas with this type of environment we can speak about ourselves , our family , our hobbies and everyone will get to know new something about other classmates .`
- Prediction: `In conclusion, I think that this type of food and atmosphere is very for us, because normally we speak about books , work and studies , whereas with this type of environment we can speak about ourselves , our family , our hobbies and everyone will get to know new things about other classmates.`
- Reference edits: `[{"start": 14, "end": 14, "source_text": "", "target_text": "good", "operation": "insert", "error_type": "M:ADJ"}]`
- Predicted edits: `[{"start": 1, "end": 3, "source_text": "conclusion ,", "target_text": "conclusion,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 15, "end": 17, "source_text": "us ,", "target_text": "us,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 53, "source_text": "something", "target_text": "things", "operation": "replace", "error_type": "R:NOUN"}, {"start": 55, "end": 57, "source_text": "classmates .", "target_text": "classmates.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 14, "end": 14, "source_text": "", "target_text": "good", "operation": "insert", "error_type": "M:ADJ"}}]`

## 24. t5_base_grammar::expect-test-00008

- Source: `I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Reference: `I 'd like to tell you about my favorite restaurant . It 's name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Prediction: `I'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an excellent choice for me and my favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I can't imagine`
- Reference edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 10, "end": 11, "source_text": "its", "target_text": "It 's", "operation": "replace", "error_type": "R:OTHER"}]`
- Predicted edits: `[{"start": 0, "end": 2, "source_text": "I 'd", "target_text": "I'd", "operation": "replace", "error_type": "R:ORTH"}, {"start": 39, "end": 40, "source_text": "Excellent", "target_text": "excellent", "operation": "replace", "error_type": "R:ORTH"}, {"start": 44, "end": 45, "source_text": "My", "target_text": "my", "operation": "replace", "error_type": "R:ORTH"}, {"start": 93, "end": 95, "source_text": "ca n't", "target_text": "can't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 96, "end": 147, "source_text": "one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .", "target_text": "", "operation": "delete", "error_type": "U:OTHER"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 10, "end": 10, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}}, {"ref_index": 1, "behavior": "missed_correction", "reference_edit": {"start": 10, "end": 11, "source_text": "its", "target_text": "It 's", "operation": "replace", "error_type": "R:OTHER"}}]`

## 25. t5_base_grammar::expect-test-00009

- Source: `But such a high level of development of Egyptian civilization has a negative side as well as positive .`
- Reference: `But such a high level of development of Egyptian civilization has a negative side as well as a positive .`
- Prediction: `There is a high level of development of Egyptian civilization, but there is a negative side as well as a positive side.`
- Reference edits: `[{"start": 17, "end": 17, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}]`
- Predicted edits: `[{"start": 0, "end": 1, "source_text": "But", "target_text": "There", "operation": "replace", "error_type": "R:OTHER"}, {"start": 1, "end": 2, "source_text": "such", "target_text": "is", "operation": "replace", "error_type": "R:OTHER"}, {"start": 9, "end": 10, "source_text": "civilization", "target_text": "civilization,", "operation": "replace", "error_type": "R:NOUN"}, {"start": 10, "end": 11, "source_text": "has", "target_text": "but there is", "operation": "replace", "error_type": "R:OTHER"}, {"start": 17, "end": 17, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}, {"start": 18, "end": 19, "source_text": ".", "target_text": "side.", "operation": "replace", "error_type": "R:OTHER"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 4, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 26. t5_base_grammar::expect-test-00010

- Source: `Until dawn all of them had got out , so they sacred until they found a refuge .`
- Reference: `By dawn all of them had got out , so they sacred until they found a refuge .`
- Prediction: `Until dawn, all of them had got out, so they were sacred until they found a refuge.`
- Reference edits: `[{"start": 0, "end": 1, "source_text": "Until", "target_text": "By", "operation": "replace", "error_type": "R:PREP"}]`
- Predicted edits: `[{"start": 1, "end": 2, "source_text": "dawn", "target_text": "dawn,", "operation": "replace", "error_type": "R:OTHER"}, {"start": 7, "end": 9, "source_text": "out ,", "target_text": "out,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 11, "end": 11, "source_text": "", "target_text": "were", "operation": "insert", "error_type": "M:VERB"}, {"start": 16, "end": 18, "source_text": "refuge .", "target_text": "refuge.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 0, "end": 1, "source_text": "Until", "target_text": "By", "operation": "replace", "error_type": "R:PREP"}}]`

## 27. t5_base_grammar::expect-test-00011

- Source: `What a wonderful day ! There is April now and finally spring has come .`
- Reference: `What a wonderful day ! It is April now and finally spring has come .`
- Prediction: `Then, there is April now, and finally spring has come.`
- Reference edits: `[{"start": 5, "end": 6, "source_text": "There", "target_text": "It", "operation": "replace", "error_type": "R:PRON"}]`
- Predicted edits: `[{"start": 0, "end": 4, "source_text": "What a wonderful day", "target_text": "Then,", "operation": "replace", "error_type": "R:OTHER"}, {"start": 4, "end": 6, "source_text": "! There", "target_text": "there", "operation": "replace", "error_type": "U:PUNCT"}, {"start": 8, "end": 9, "source_text": "now", "target_text": "now,", "operation": "replace", "error_type": "R:OTHER"}, {"start": 13, "end": 15, "source_text": "come .", "target_text": "come.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": 0, "behavior": "wrong_correction", "score": 0.667}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`

## 28. t5_base_grammar::expect-test-00012

- Source: `The traffic can affect cars and buses at the same extent .`
- Reference: `The traffic can affect cars and buses to the same extent .`
- Prediction: `The traffic can affect cars and buses at the same extent.`
- Reference edits: `[{"start": 7, "end": 8, "source_text": "at", "target_text": "to", "operation": "replace", "error_type": "R:PREP"}]`
- Predicted edits: `[{"start": 10, "end": 12, "source_text": "extent .", "target_text": "extent.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 7, "end": 8, "source_text": "at", "target_text": "to", "operation": "replace", "error_type": "R:PREP"}}]`

## 29. t5_base_grammar::expect-test-00013

- Source: `Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .`
- Reference: `Computers have had a most significant impact on people in the latter 1/2 of the 20th century .`
- Prediction: `Using the Internet for the first time since the beginning of the 20th century.`
- Reference edits: `[{"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}]`
- Predicted edits: `[{"start": 0, "end": 1, "source_text": "Computers", "target_text": "", "operation": "delete", "error_type": "U:NOUN"}, {"start": 1, "end": 3, "source_text": "have had", "target_text": "Using", "operation": "replace", "error_type": "R:VERB"}, {"start": 3, "end": 7, "source_text": "a most significant impact", "target_text": "the Internet", "operation": "replace", "error_type": "R:OTHER"}, {"start": 7, "end": 8, "source_text": "on", "target_text": "for", "operation": "replace", "error_type": "R:PREP"}, {"start": 9, "end": 10, "source_text": "people", "target_text": "first time", "operation": "replace", "error_type": "R:OTHER"}, {"start": 10, "end": 11, "source_text": "in", "target_text": "since", "operation": "replace", "error_type": "R:PREP"}, {"start": 12, "end": 14, "source_text": "latter 1/2", "target_text": "beginning", "operation": "replace", "error_type": "R:OTHER"}, {"start": 17, "end": 19, "source_text": "century .", "target_text": "century.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 6, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 7, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[{"ref_index": 0, "behavior": "missed_correction", "reference_edit": {"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}}]`

## 30. t5_base_grammar::expect-test-00014

- Source: `i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Reference: `i love my family especially my little sister , she is sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Prediction: `i love my family, especially my little sister, who is sixteen years old, and I consider her my best friend because I usually tell her everything about my life.`
- Reference edits: `[{"start": 10, "end": 11, "source_text": "has", "target_text": "is", "operation": "replace", "error_type": "R:VERB"}]`
- Predicted edits: `[{"start": 3, "end": 4, "source_text": "family", "target_text": "family,", "operation": "replace", "error_type": "R:NOUN"}, {"start": 7, "end": 9, "source_text": "sister ,", "target_text": "sister,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 9, "end": 10, "source_text": "she", "target_text": "who", "operation": "replace", "error_type": "R:PRON"}, {"start": 10, "end": 11, "source_text": "has", "target_text": "is", "operation": "replace", "error_type": "R:VERB"}, {"start": 13, "end": 14, "source_text": "old", "target_text": "old,", "operation": "replace", "error_type": "R:ADJ"}, {"start": 14, "end": 16, "source_text": ", i", "target_text": "and I", "operation": "replace", "error_type": "R:OTHER"}, {"start": 22, "end": 23, "source_text": "i", "target_text": "I", "operation": "replace", "error_type": "R:ORTH"}, {"start": 29, "end": 31, "source_text": "life .", "target_text": "life.", "operation": "replace", "error_type": "R:ORTH"}]`
- Alignment: `[{"pred_index": 0, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 1, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 2, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 3, "ref_index": 0, "behavior": "correct_correction", "score": 1.0}, {"pred_index": 4, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 5, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 6, "ref_index": null, "behavior": "overcorrection", "score": 0.0}, {"pred_index": 7, "ref_index": null, "behavior": "overcorrection", "score": 0.0}]`
- Missed edits: `[]`


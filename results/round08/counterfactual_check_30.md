# Round 08 Counterfactual Check

Labels below are computed from actual GEC model predictions on counterfactual sources, not from grammar-theory expectations.

## 1. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00000::gector_roberta_base::00122::8-9::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In our community , we are very interested at the environment and ecological things .`
- Counterfactual prediction: `In our community , we are very interested in the environment and ecological things .`
- Original edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- Counterfactual edits: `[{"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}]`
- Actual label: `preserve`

## 2. gector_roberta_base::rule_relevant::EXPECT::expect-test-00000::gector_roberta_base::00122::8-9::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In my community , we are very interested in the environment and ecological things .`
- Counterfactual prediction: `In my community , we are very interested in the environment and ecological things .`
- Original edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- Counterfactual edits: `[]`
- Actual label: `cancel`

## 3. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00001::gector_roberta_base::00133::70-71::replace

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Science has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Science has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Original edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- Counterfactual edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 11, "end": 11, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 14, "end": 14, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 33, "end": 33, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 38, "end": 39, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 45, "end": 46, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 52, "source_text": "", "target_text": "children", "operation": "insert", "error_type": "M:NOUN"}, {"start": 52, "end": 54, "source_text": "young.but that", "target_text": ". That", "operation": "replace", "error_type": "R:OTHER"}, {"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Actual label: `preserve`

## 4. gector_roberta_base::rule_relevant::EXPECT::expect-test-00001::gector_roberta_base::00133::70-71::replace

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Original edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- Counterfactual edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 11, "end": 11, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 14, "end": 14, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 33, "end": 33, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 38, "end": 39, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 45, "end": 46, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 52, "source_text": "", "target_text": "children", "operation": "insert", "error_type": "M:NOUN"}, {"start": 52, "end": 54, "source_text": "young.but that", "target_text": ". That", "operation": "replace", "error_type": "R:OTHER"}]`
- Actual label: `competing_edit`

## 5. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00001::gector_roberta_base::00123::2-3::replace

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Science has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Science has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Original edit: `{"end": 3, "error_type": "R:SPELL", "operation": "replace", "source_text": "chanched", "start": 2, "target_text": "changed"}`
- Counterfactual edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 11, "end": 11, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 14, "end": 14, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 33, "end": 33, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 38, "end": 39, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 45, "end": 46, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 52, "source_text": "", "target_text": "children", "operation": "insert", "error_type": "M:NOUN"}, {"start": 52, "end": 54, "source_text": "young.but that", "target_text": ". That", "operation": "replace", "error_type": "R:OTHER"}, {"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Actual label: `preserve`

## 6. gector_roberta_base::rule_relevant::EXPECT::expect-test-00001::gector_roberta_base::00123::2-3::replace

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Technology has changed people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Original edit: `{"end": 3, "error_type": "R:SPELL", "operation": "replace", "source_text": "chanched", "start": 2, "target_text": "changed"}`
- Counterfactual edits: `[{"start": 11, "end": 11, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 14, "end": 14, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 33, "end": 33, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 38, "end": 39, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 45, "end": 46, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 52, "source_text": "", "target_text": "children", "operation": "insert", "error_type": "M:NOUN"}, {"start": 52, "end": 54, "source_text": "young.but that", "target_text": ". That", "operation": "replace", "error_type": "R:OTHER"}, {"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Actual label: `competing_edit`

## 7. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00001::gector_roberta_base::00124::11-11::insert

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Science has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Science has changed people 's lives a lot . In fact , we can think about how different our lives are compared either to our parents ' or our grandparents ' lives . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Original edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 11, "target_text": ","}`
- Counterfactual edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 11, "end": 11, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 14, "end": 14, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 33, "end": 33, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 38, "end": 39, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 45, "end": 46, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 52, "source_text": "", "target_text": "children", "operation": "insert", "error_type": "M:NOUN"}, {"start": 52, "end": 54, "source_text": "young.but that", "target_text": ". That", "operation": "replace", "error_type": "R:OTHER"}, {"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Actual label: `preserve`

## 8. gector_roberta_base::rule_relevant::EXPECT::expect-test-00001::gector_roberta_base::00124::11-11::insert

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Technology has chanched people 's lives a lot . In fact , we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Technology has changed people 's lives a lot . In fact , we can think about how different our lives are compared to our parents ' or our grandparents ' lives were . For example , my parents did n't watch TV , because there was n't any TV in the world when they were children . That is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Original edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "insert", "source_text": "", "start": 11, "target_text": ","}`
- Counterfactual edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 15, "end": 15, "source_text": "", "target_text": "about", "operation": "insert", "error_type": "M:PREP"}, {"start": 17, "end": 18, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 19, "end": 20, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 21, "end": 22, "source_text": "either", "target_text": "", "operation": "delete", "error_type": "U:CONJ"}, {"start": 31, "end": 31, "source_text": "", "target_text": "were", "operation": "insert", "error_type": "M:VERB"}, {"start": 34, "end": 34, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 39, "end": 40, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 46, "end": 47, "source_text": "tv", "target_text": "TV", "operation": "replace", "error_type": "R:ORTH"}, {"start": 53, "end": 53, "source_text": "", "target_text": "children", "operation": "insert", "error_type": "M:NOUN"}, {"start": 53, "end": 55, "source_text": "young.but that", "target_text": ". That", "operation": "replace", "error_type": "R:OTHER"}, {"start": 71, "end": 72, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Actual label: `preserve`

## 9. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00005::gector_roberta_base::00143::10-10::insert

- Original source: `They were planning to steal a very precious thing from Museum tonight .`
- Counterfactual source: `They were planning to steal a very precious thing from Gallery tonight .`
- Counterfactual prediction: `They were planning to steal a very precious thing from the gallery tonight .`
- Original edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "the"}`
- Counterfactual edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "M:DET"}, {"start": 10, "end": 11, "source_text": "Gallery", "target_text": "gallery", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `preserve`

## 10. gector_roberta_base::rule_relevant::EXPECT::expect-test-00005::gector_roberta_base::00143::10-10::insert

- Original source: `They were planning to steal a very precious thing from Museum tonight .`
- Counterfactual source: `They were planning to steal a very precious thing from the Museum tonight .`
- Counterfactual prediction: `They were planning to steal a very precious thing from the Museum tonight .`
- Original edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "the"}`
- Counterfactual edits: `[]`
- Actual label: `cancel`

## 11. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00008::gector_roberta_base::00149::10-11::replace

- Original source: `I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Counterfactual source: `We 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Counterfactual prediction: `We 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Original edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "replace", "source_text": "its", "start": 10, "target_text": ". Its"}`
- Counterfactual edits: `[{"start": 10, "end": 11, "source_text": "its", "target_text": ". Its", "operation": "replace", "error_type": "M:PUNCT"}, {"start": 16, "end": 16, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 21, "end": 22, "source_text": "it", "target_text": ". It", "operation": "replace", "error_type": "M:PUNCT"}, {"start": 25, "end": 26, "source_text": "to", "target_text": "than", "operation": "replace", "error_type": "R:PREP"}, {"start": 28, "end": 28, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 36, "end": 36, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 39, "end": 40, "source_text": "Excellent", "target_text": "excellent", "operation": "replace", "error_type": "R:ORTH"}, {"start": 44, "end": 45, "source_text": "My", "target_text": "my", "operation": "replace", "error_type": "R:ORTH"}, {"start": 50, "end": 53, "source_text": "in order that", "target_text": "for", "operation": "replace", "error_type": "R:OTHER"}, {"start": 54, "end": 54, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 64, "end": 64, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}]`
- Actual label: `preserve`

## 12. gector_roberta_base::rule_relevant::EXPECT::expect-test-00008::gector_roberta_base::00149::10-11::replace

- Original source: `I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Counterfactual source: `I 'd like to tell you about my favorite restaurant . Its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Counterfactual prediction: `I 'd like to tell you about my favorite restaurant . Its name is " Lemon " . I go there every week . It has different food than other restaurants . I 'd like chicken crispy with garlic sauce . It 's an excellent choice for me and my favorite appitizer is susage and for dessert , I 'd like " Vadge " cake with chocolate sauce . I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Original edit: `{"end": 11, "error_type": "M:PUNCT", "operation": "replace", "source_text": "its", "start": 10, "target_text": ". Its"}`
- Counterfactual edits: `[{"start": 17, "end": 17, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 22, "end": 23, "source_text": "it", "target_text": ". It", "operation": "replace", "error_type": "M:PUNCT"}, {"start": 26, "end": 27, "source_text": "to", "target_text": "than", "operation": "replace", "error_type": "R:PREP"}, {"start": 29, "end": 29, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 37, "end": 37, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 40, "end": 41, "source_text": "Excellent", "target_text": "excellent", "operation": "replace", "error_type": "R:ORTH"}, {"start": 45, "end": 46, "source_text": "My", "target_text": "my", "operation": "replace", "error_type": "R:ORTH"}, {"start": 51, "end": 54, "source_text": "in order that", "target_text": "for", "operation": "replace", "error_type": "R:OTHER"}, {"start": 55, "end": 55, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 65, "end": 65, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}]`
- Actual label: `competing_edit`

## 13. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00002::gector_roberta_base::00134::3-4::delete

- Original source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual source: `We should use of public transport because at the present there are a lot of vehicles in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual prediction: `We should use public transport because , at present , there are a lot of vehicles in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Original edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- Counterfactual edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "U:PREP"}, {"start": 7, "end": 7, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}, {"start": 10, "end": 10, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 22, "end": 22, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 23, "end": 23, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}]`
- Actual label: `preserve`

## 14. gector_roberta_base::rule_relevant::EXPECT::expect-test-00002::gector_roberta_base::00134::3-4::delete

- Original source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual source: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual prediction: `We should use public transport because , at present , there are a lot of cars in the world that pollute and , unfortunately , we are harming the environment and the world .`
- Original edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- Counterfactual edits: `[{"start": 6, "end": 6, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 7, "end": 8, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}, {"start": 9, "end": 9, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 21, "end": 21, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 22, "end": 22, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}]`
- Actual label: `change_span`

## 15. gector_roberta_base::error_irrelevant::EXPECT::expect-test-00003::gector_roberta_base::00140::10-11::replace

- Original source: `Although there are many positive points about private cars , they are also negative ones .`
- Counterfactual source: `Although there are many positive points about private vehicles , they are also negative ones .`
- Counterfactual prediction: `Although there are many positive points about private vehicles , there are also negative ones .`
- Original edit: `{"end": 11, "error_type": "R:PRON", "operation": "replace", "source_text": "they", "start": 10, "target_text": "there"}`
- Counterfactual edits: `[{"start": 10, "end": 11, "source_text": "they", "target_text": "there", "operation": "replace", "error_type": "R:PRON"}]`
- Actual label: `preserve`

## 16. gector_roberta_base::rule_relevant::EXPECT::expect-test-00003::gector_roberta_base::00140::10-11::replace

- Original source: `Although there are many positive points about private cars , they are also negative ones .`
- Counterfactual source: `Although there are many positive points about private cars , there are also negative ones .`
- Counterfactual prediction: `Although there are many positive points about private cars , there are also negative ones .`
- Original edit: `{"end": 11, "error_type": "R:PRON", "operation": "replace", "source_text": "they", "start": 10, "target_text": "there"}`
- Counterfactual edits: `[]`
- Actual label: `cancel`

## 17. t5_base_grammar::error_irrelevant::EXPECT::expect-test-00000::t5_base_grammar::00263::8-9::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In our community , we are very interested at the environment and ecological things .`
- Counterfactual prediction: `In our community, we are very interested in the environment and ecological things.`
- Original edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- Counterfactual edits: `[{"start": 2, "end": 4, "source_text": "community ,", "target_text": "community,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}, {"start": 13, "end": 15, "source_text": "things .", "target_text": "things.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `preserve`

## 18. t5_base_grammar::rule_relevant::EXPECT::expect-test-00000::t5_base_grammar::00263::8-9::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In my community , we are very interested in the environment and ecological things .`
- Counterfactual prediction: `In my community, we are very interested in the environment and ecological things.`
- Original edit: `{"end": 9, "error_type": "R:PREP", "operation": "replace", "source_text": "at", "start": 8, "target_text": "in"}`
- Counterfactual edits: `[{"start": 2, "end": 4, "source_text": "community ,", "target_text": "community,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 13, "end": 15, "source_text": "things .", "target_text": "things.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `competing_edit`

## 19. t5_base_grammar::error_irrelevant::EXPECT::expect-test-00001::t5_base_grammar::00281::70-71::replace

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Science has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Science has changed people's lives a lot . In fact, we can think how different our lives are compared to our parents' or grandparents' lives . For example, my parents didn't watch tv because there wasn't any tv in the world when they were young. but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Original edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- Counterfactual edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 3, "end": 5, "source_text": "people 's", "target_text": "people's", "operation": "replace", "error_type": "R:ORTH"}, {"start": 10, "end": 11, "source_text": "fact", "target_text": "fact,", "operation": "replace", "error_type": "R:NOUN"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 20, "end": 21, "source_text": "either", "target_text": "", "operation": "delete", "error_type": "U:CONJ"}, {"start": 23, "end": 25, "source_text": "parents '", "target_text": "parents'", "operation": "replace", "error_type": "R:ORTH"}, {"start": 26, "end": 27, "source_text": "our", "target_text": "", "operation": "delete", "error_type": "U:DET"}, {"start": 27, "end": 29, "source_text": "grandparents '", "target_text": "grandparents'", "operation": "replace", "error_type": "R:ORTH"}, {"start": 32, "end": 33, "source_text": "example", "target_text": "example,", "operation": "replace", "error_type": "R:OTHER"}, {"start": 35, "end": 37, "source_text": "did n't", "target_text": "didn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 39, "end": 40, "source_text": ",", "target_text": "", "operation": "delete", "error_type": "U:PUNCT"}, {"start": 42, "end": 44, "source_text": "was n't", "target_text": "wasn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 52, "end": 53, "source_text": "young.but", "target_text": "young. but", "operation": "replace", "error_type": "R:ORTH"}, {"start": 54, "end": 56, "source_text": "is n't", "target_text": "isn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}, {"start": 87, "end": 89, "source_text": "lives .", "target_text": "lives.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `preserve`

## 20. t5_base_grammar::rule_relevant::EXPECT::expect-test-00001::t5_base_grammar::00281::70-71::replace

- Original source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Counterfactual prediction: `Technology has changed people's lives a lot. In fact, we can think how different our lives are compared to our parents' or grandparents' lives. For example, my parents didn't watch tv because there wasn't any tv in the world when they were young.but that isn't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives.`
- Original edit: `{"end": 71, "error_type": "R:OTHER", "operation": "replace", "source_text": "ed", "start": 70, "target_text": "and"}`
- Counterfactual edits: `[{"start": 2, "end": 3, "source_text": "chanched", "target_text": "changed", "operation": "replace", "error_type": "R:SPELL"}, {"start": 3, "end": 5, "source_text": "people 's", "target_text": "people's", "operation": "replace", "error_type": "R:ORTH"}, {"start": 7, "end": 9, "source_text": "lot .", "target_text": "lot.", "operation": "replace", "error_type": "R:ORTH"}, {"start": 10, "end": 11, "source_text": "fact", "target_text": "fact,", "operation": "replace", "error_type": "R:NOUN"}, {"start": 16, "end": 17, "source_text": "is", "target_text": "", "operation": "delete", "error_type": "U:VERB"}, {"start": 18, "end": 19, "source_text": "life", "target_text": "lives are", "operation": "replace", "error_type": "R:OTHER"}, {"start": 20, "end": 21, "source_text": "either", "target_text": "", "operation": "delete", "error_type": "U:CONJ"}, {"start": 23, "end": 25, "source_text": "parents '", "target_text": "parents'", "operation": "replace", "error_type": "R:ORTH"}, {"start": 26, "end": 27, "source_text": "our", "target_text": "", "operation": "delete", "error_type": "U:DET"}, {"start": 27, "end": 31, "source_text": "grandparents ' lives .", "target_text": "grandparents' lives.", "operation": "replace", "error_type": "R:ORTH"}, {"start": 32, "end": 33, "source_text": "example", "target_text": "example,", "operation": "replace", "error_type": "R:OTHER"}, {"start": 35, "end": 37, "source_text": "did n't", "target_text": "didn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 39, "end": 40, "source_text": ",", "target_text": "", "operation": "delete", "error_type": "U:PUNCT"}, {"start": 42, "end": 44, "source_text": "was n't", "target_text": "wasn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 54, "end": 56, "source_text": "is n't", "target_text": "isn't", "operation": "replace", "error_type": "R:ORTH"}, {"start": 87, "end": 89, "source_text": "lives .", "target_text": "lives.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `competing_edit`

## 21. t5_base_grammar::error_irrelevant::EXPECT::expect-test-00000::t5_base_grammar::00262::2-4::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In our community , we are very interested at the environment and ecological things .`
- Counterfactual prediction: `In our community, we are very interested in the environment and ecological things.`
- Original edit: `{"end": 4, "error_type": "R:ORTH", "operation": "replace", "source_text": "community ,", "start": 2, "target_text": "community,"}`
- Counterfactual edits: `[{"start": 2, "end": 4, "source_text": "community ,", "target_text": "community,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}, {"start": 13, "end": 15, "source_text": "things .", "target_text": "things.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `preserve`

## 22. t5_base_grammar::rule_relevant::EXPECT::expect-test-00000::t5_base_grammar::00262::2-4::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In my community, we are very interested at the environment and ecological things .`
- Counterfactual prediction: `In my community, we are very interested in the environment and ecological things.`
- Original edit: `{"end": 4, "error_type": "R:ORTH", "operation": "replace", "source_text": "community ,", "start": 2, "target_text": "community,"}`
- Counterfactual edits: `[{"start": 7, "end": 8, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}, {"start": 12, "end": 14, "source_text": "things .", "target_text": "things.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `competing_edit`

## 23. t5_base_grammar::error_irrelevant::EXPECT::expect-test-00000::t5_base_grammar::00264::13-15::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In our community , we are very interested at the environment and ecological things .`
- Counterfactual prediction: `In our community, we are very interested in the environment and ecological things.`
- Original edit: `{"end": 15, "error_type": "R:ORTH", "operation": "replace", "source_text": "things .", "start": 13, "target_text": "things."}`
- Counterfactual edits: `[{"start": 2, "end": 4, "source_text": "community ,", "target_text": "community,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}, {"start": 13, "end": 15, "source_text": "things .", "target_text": "things.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `preserve`

## 24. t5_base_grammar::rule_relevant::EXPECT::expect-test-00000::t5_base_grammar::00264::13-15::replace

- Original source: `In my community , we are very interested at the environment and ecological things .`
- Counterfactual source: `In my community , we are very interested at the environment and ecological things.`
- Counterfactual prediction: `In my community, we are very interested in the environment and ecological things.`
- Original edit: `{"end": 15, "error_type": "R:ORTH", "operation": "replace", "source_text": "things .", "start": 13, "target_text": "things."}`
- Counterfactual edits: `[{"start": 2, "end": 4, "source_text": "community ,", "target_text": "community,", "operation": "replace", "error_type": "R:ORTH"}, {"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}]`
- Actual label: `competing_edit`

## 25. t5_base_grammar::error_irrelevant::EXPECT::expect-test-00005::t5_base_grammar::00293::10-10::insert

- Original source: `They were planning to steal a very precious thing from Museum tonight .`
- Counterfactual source: `They were planning to steal a very precious thing from Gallery tonight .`
- Counterfactual prediction: `They were planning to steal a very precious thing from the Gallery tonight.`
- Original edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "the"}`
- Counterfactual edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "M:DET"}, {"start": 11, "end": 13, "source_text": "tonight .", "target_text": "tonight.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `preserve`

## 26. t5_base_grammar::rule_relevant::EXPECT::expect-test-00005::t5_base_grammar::00293::10-10::insert

- Original source: `They were planning to steal a very precious thing from Museum tonight .`
- Counterfactual source: `They were planning to steal a very precious thing from the Museum tonight .`
- Counterfactual prediction: `They were planning to steal a very precious thing from the Museum tonight.`
- Original edit: `{"end": 10, "error_type": "M:DET", "operation": "insert", "source_text": "", "start": 10, "target_text": "the"}`
- Counterfactual edits: `[{"start": 12, "end": 14, "source_text": "tonight .", "target_text": "tonight.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `competing_edit`

## 27. t5_base_grammar::error_irrelevant::EXPECT::expect-test-00011::t5_base_grammar::00317::4-6::replace

- Original source: `What a wonderful day ! There is April now and finally spring has come .`
- Counterfactual source: `What a wonderful day ! There is April now and finally spring has come today .`
- Counterfactual prediction: `What a wonderful day! There is April now and finally spring has come today.`
- Original edit: `{"end": 6, "error_type": "U:PUNCT", "operation": "replace", "source_text": "! There", "start": 4, "target_text": "there"}`
- Counterfactual edits: `[{"start": 3, "end": 5, "source_text": "day !", "target_text": "day!", "operation": "replace", "error_type": "R:ORTH"}, {"start": 14, "end": 16, "source_text": "today .", "target_text": "today.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `competing_edit`

## 28. t5_base_grammar::rule_relevant::EXPECT::expect-test-00011::t5_base_grammar::00317::4-6::replace

- Original source: `What a wonderful day ! There is April now and finally spring has come .`
- Counterfactual source: `What a wonderful day there is April now and finally spring has come .`
- Counterfactual prediction: `What a wonderful day it is now April and finally spring has come.`
- Original edit: `{"end": 6, "error_type": "U:PUNCT", "operation": "replace", "source_text": "! There", "start": 4, "target_text": "there"}`
- Counterfactual edits: `[{"start": 4, "end": 5, "source_text": "there", "target_text": "it", "operation": "replace", "error_type": "R:PRON"}, {"start": 6, "end": 8, "source_text": "April now", "target_text": "now April", "operation": "replace", "error_type": "R:WO"}, {"start": 12, "end": 14, "source_text": "come .", "target_text": "come.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `competing_edit`

## 29. t5_base_grammar::error_irrelevant::EXPECT::expect-test-00002::t5_base_grammar::00283::3-4::delete

- Original source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual source: `We should use of public transport because at the present there are a lot of vehicles in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual prediction: `We should use public transport because at the present there are a lot of vehicles in the world that pollute and unfortunately we are harming the environment and the world.`
- Original edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- Counterfactual edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "U:PREP"}, {"start": 30, "end": 32, "source_text": "world .", "target_text": "world.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `preserve`

## 30. t5_base_grammar::rule_relevant::EXPECT::expect-test-00002::t5_base_grammar::00283::3-4::delete

- Original source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual source: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Counterfactual prediction: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world.`
- Original edit: `{"end": 4, "error_type": "U:PREP", "operation": "delete", "source_text": "of", "start": 3, "target_text": ""}`
- Counterfactual edits: `[{"start": 29, "end": 31, "source_text": "world .", "target_text": "world.", "operation": "replace", "error_type": "R:ORTH"}]`
- Actual label: `competing_edit`


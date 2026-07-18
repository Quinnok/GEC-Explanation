# Failure Cases

## 1. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The sentence should change from "community," back to "community ,".`

## 2. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_operation

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_operation`
- Gold/prediction: `False` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should insert the relevant phrase.`

## 3. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The sentence should change from "in" back to "at".`

## 4. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::partially_correct

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `partially_correct`
- Gold/prediction: `False` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The explanation identifies R:PREP but does not identify the edit target.`

## 5. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The sentence should change from "things." back to "things .".`

## 6. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::masked_target_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `masked_target_template`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace "chanched" with "[MASK]" at source span [2,3) for R:SPELL.`

## 7. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::rule_only

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `rule_only`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `Apply the grammar rule indicated by the local context. The explanation intentionally omits the target edit.`

## 8. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::gee_style_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `gee_style_automatic`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The phrase near span [2,3) violates R:SPELL; apply the grammar rule indicated by the local context.`

## 9. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::rule_grounded_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `rule_grounded_automatic`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `Apply the grammar rule indicated by the local context. In this sentence, the evidence is around "chanched".`

## 10. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::faithful_wrong_model_edit

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `faithful_wrong_model_edit`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The model actually decided to replace "chanched" with "changed", regardless of whether the correction is grammatically valid.`

## 11. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00004::3-5::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "people's" back to "people 's".`

## 12. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00005::7-9::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "lot." back to "lot .".`

## 13. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00006::10-11::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:NOUN`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "fact," back to "fact".`

## 14. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00006::10-11::replace::wrong_error_type

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:NOUN`
- Explanation type: `wrong_error_type`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This correction fixes R:VERB:SVA, not R:NOUN.`

## 15. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00006::10-11::replace::partially_correct

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:NOUN`
- Explanation type: `partially_correct`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The explanation identifies R:NOUN but does not identify the edit target.`

## 16. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00007::16-17::delete::wrong_source_token

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:VERB`
- Explanation type: `wrong_source_token`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The error is caused by the token "our".`

## 17. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00007::16-17::delete::wrong_target

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:VERB`
- Explanation type: `wrong_target`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should delete "the".`

## 18. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00007::16-17::delete::wrong_operation

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:VERB`
- Explanation type: `wrong_operation`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace the relevant phrase.`

## 19. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00007::16-17::delete::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:VERB`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "" back to "is".`

## 20. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00007::16-17::delete::wrong_error_type

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:VERB`
- Explanation type: `wrong_error_type`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This correction fixes R:VERB:SVA, not U:VERB.`

## 21. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00007::16-17::delete::swapped_across_sentence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:VERB`
- Explanation type: `swapped_across_sentence`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace "community ," with "community," for R:ORTH.`

## 22. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00007::16-17::delete::partially_correct

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:VERB`
- Explanation type: `partially_correct`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The explanation identifies U:VERB but does not identify the edit target.`

## 23. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00008::18-19::replace::masked_target_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `masked_target_template`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace "life" with "[MASK]" at source span [18,19) for R:OTHER.`

## 24. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00008::18-19::replace::rule_only

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `rule_only`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `Apply the grammar rule indicated by the local context. The explanation intentionally omits the target edit.`

## 25. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00008::18-19::replace::gee_style_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `gee_style_automatic`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The phrase near span [18,19) violates R:OTHER; apply the grammar rule indicated by the local context.`

## 26. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00008::18-19::replace::rule_grounded_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `rule_grounded_automatic`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `Apply the grammar rule indicated by the local context. In this sentence, the evidence is around "life".`

## 27. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00008::18-19::replace::faithful_wrong_model_edit

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `faithful_wrong_model_edit`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The model actually decided to replace "life" with "lives are", regardless of whether the correction is grammatically valid.`

## 28. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00009::20-22::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:WO`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "to either" back to "either to".`

## 29. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00010::23-25::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "parents'" back to "parents '".`

## 30. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00011::27-31::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "grandparents' lives." back to "grandparents ' lives .".`

## 31. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00012::32-33::replace::masked_target_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `masked_target_template`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace "example" with "[MASK]" at source span [32,33) for R:OTHER.`

## 32. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00012::32-33::replace::rule_only

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `rule_only`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `Apply the grammar rule indicated by the local context. The explanation intentionally omits the target edit.`

## 33. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00012::32-33::replace::gee_style_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `gee_style_automatic`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The phrase near span [32,33) violates R:OTHER; apply the grammar rule indicated by the local context.`

## 34. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00012::32-33::replace::rule_grounded_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `rule_grounded_automatic`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `Apply the grammar rule indicated by the local context. In this sentence, the evidence is around "example".`

## 35. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00012::32-33::replace::faithful_wrong_model_edit

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:OTHER`
- Explanation type: `faithful_wrong_model_edit`
- Gold/prediction: `True` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The model actually decided to replace "example" with "example,", regardless of whether the correction is grammatically valid.`

## 36. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00013::35-37::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "didn't" back to "did n't".`

## 37. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00014::39-40::delete::wrong_span

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:PUNCT`
- Explanation type: `wrong_span`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The edit applies to source span [40,41).`

## 38. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00014::39-40::delete::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:PUNCT`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "" back to ",".`

## 39. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00014::39-40::delete::wrong_error_type

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:PUNCT`
- Explanation type: `wrong_error_type`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This correction fixes R:VERB:SVA, not U:PUNCT.`

## 40. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00014::39-40::delete::wrong_rule

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:PUNCT`
- Explanation type: `wrong_rule`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `Use a comma because every grammar error here is punctuation-related.`

## 41. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00014::39-40::delete::swapped_across_sentence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `U:PUNCT`
- Explanation type: `swapped_across_sentence`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace "community ," with "community," for R:ORTH.`

## 42. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00015::42-44::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "wasn't" back to "was n't".`

## 43. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00016::45-46::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "TV" back to "tv".`

## 44. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00017::52-53::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "young. But" back to "young.but".`

## 45. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00018::54-56::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "isn't" back to "is n't".`

## 46. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00019::58-60::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "difference:" back to "difference :".`

## 47. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00020::66-68::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "phone," back to "phone ,".`

## 48. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00021::69-70::replace::wrong_direction

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:NOUN`
- Explanation type: `wrong_direction`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The sentence should change from "computer," back to "computer".`

## 49. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00021::69-70::replace::wrong_error_type

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:NOUN`
- Explanation type: `wrong_error_type`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This correction fixes R:VERB:SVA, not R:NOUN.`

## 50. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00021::69-70::replace::partially_correct

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:NOUN`
- Explanation type: `partially_correct`
- Gold/prediction: `False` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The explanation identifies R:NOUN but does not identify the edit target.`

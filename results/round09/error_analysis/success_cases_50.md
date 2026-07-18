# Success Cases

## 1. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::explicit_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `explicit_template`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "community ," with "community," at source span [2,4) for R:ORTH.`

## 2. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::masked_target_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `masked_target_template`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "community ," with "[MASK]" at source span [2,4) for R:ORTH.`

## 3. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::rule_only

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `rule_only`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Correct spelling, casing, spacing, or another orthographic form. The explanation intentionally omits the target edit.`

## 4. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::gee_style_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `gee_style_automatic`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The phrase near span [2,4) violates R:ORTH; correct spelling, casing, spacing, or another orthographic form.`

## 5. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::rule_grounded_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `rule_grounded_automatic`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Correct spelling, casing, spacing, or another orthographic form. In this sentence, the evidence is around "community".`

## 6. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_span

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_span`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The edit applies to source span [3,5).`

## 7. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_source_token

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_source_token`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The error is caused by the token ",".`

## 8. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_target

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_target`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "the".`

## 9. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_operation

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_operation`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should insert the relevant phrase.`

## 10. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_error_type

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_error_type`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This correction fixes R:VERB:SVA, not R:ORTH.`

## 11. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_rule

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_rule`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Use a comma because every grammar error here is punctuation-related.`

## 12. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::wrong_evidence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_evidence`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The evidence is the unrelated token "we".`

## 13. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::swapped_across_sentence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `swapped_across_sentence`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "chanched" with "changed" for R:SPELL.`

## 14. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::generic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `generic`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The sentence has a grammar issue and should be improved.`

## 15. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::partially_correct

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `partially_correct`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The explanation identifies R:ORTH but does not identify the edit target.`

## 16. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00000::2-4::replace::faithful_wrong_model_edit

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `faithful_wrong_model_edit`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The model actually decided to replace "community ," with "community,", regardless of whether the correction is grammatically valid.`

## 17. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::explicit_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `explicit_template`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "at" with "in" at source span [8,9) for R:PREP.`

## 18. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::masked_target_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `masked_target_template`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "at" with "[MASK]" at source span [8,9) for R:PREP.`

## 19. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::rule_only

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `rule_only`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Use the preposition required by the surrounding phrase. The explanation intentionally omits the target edit.`

## 20. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::gee_style_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `gee_style_automatic`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The phrase near span [8,9) violates R:PREP; use the preposition required by the surrounding phrase.`

## 21. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::rule_grounded_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `rule_grounded_automatic`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Use the preposition required by the surrounding phrase. In this sentence, the evidence is around "at".`

## 22. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_span

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_span`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The edit applies to source span [9,10).`

## 23. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_source_token

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_source_token`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The error is caused by the token "the".`

## 24. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_target

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_target`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "the".`

## 25. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_error_type

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_error_type`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This correction fixes R:VERB:SVA, not R:PREP.`

## 26. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_rule

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_rule`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Use a comma because every grammar error here is punctuation-related.`

## 27. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::wrong_evidence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `wrong_evidence`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The evidence is the unrelated token "environment".`

## 28. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::swapped_across_sentence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `swapped_across_sentence`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "chanched" with "changed" for R:SPELL.`

## 29. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00001::8-9::replace::generic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `correct_correction` / `R:PREP`
- Explanation type: `generic`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The sentence has a grammar issue and should be improved.`

## 30. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::explicit_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `explicit_template`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "things ." with "things." at source span [13,15) for R:ORTH.`

## 31. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::masked_target_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `masked_target_template`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "things ." with "[MASK]" at source span [13,15) for R:ORTH.`

## 32. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::rule_only

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `rule_only`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Correct spelling, casing, spacing, or another orthographic form. The explanation intentionally omits the target edit.`

## 33. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::gee_style_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `gee_style_automatic`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The phrase near span [13,15) violates R:ORTH; correct spelling, casing, spacing, or another orthographic form.`

## 34. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::rule_grounded_automatic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `rule_grounded_automatic`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Correct spelling, casing, spacing, or another orthographic form. In this sentence, the evidence is around "things".`

## 35. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_span

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_span`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The edit applies to source span [14,16).`

## 36. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_source_token

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_source_token`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The error is caused by the token ".".`

## 37. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_target

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_target`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "the".`

## 38. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_operation

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_operation`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should insert the relevant phrase.`

## 39. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_error_type

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_error_type`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This correction fixes R:VERB:SVA, not R:ORTH.`

## 40. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_rule

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_rule`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `Use a comma because every grammar error here is punctuation-related.`

## 41. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::wrong_evidence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `wrong_evidence`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The evidence is the unrelated token ".".`

## 42. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::swapped_across_sentence

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `swapped_across_sentence`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `This edit should replace "chanched" with "changed" for R:SPELL.`

## 43. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::generic

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `generic`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The sentence has a grammar issue and should be improved.`

## 44. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::partially_correct

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `partially_correct`
- Gold/prediction: `False` / `False`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The explanation identifies R:ORTH but does not identify the edit target.`

## 45. rule_evidence_verifier::EXPECT::expect-test-00000::coedit_large::00002::13-15::replace::faithful_wrong_model_edit

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:ORTH`
- Explanation type: `faithful_wrong_model_edit`
- Gold/prediction: `True` / `True`
- Source: `In my community , we are very interested at the environment and ecological things .`
- Explanation: `The model actually decided to replace "things ." with "things.", regardless of whether the correction is grammatically valid.`

## 46. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::explicit_template

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `explicit_template`
- Gold/prediction: `True` / `True`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace "chanched" with "changed" at source span [2,3) for R:SPELL.`

## 47. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::wrong_span

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `wrong_span`
- Gold/prediction: `False` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The edit applies to source span [3,4).`

## 48. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::wrong_source_token

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `wrong_source_token`
- Gold/prediction: `False` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `The error is caused by the token "people".`

## 49. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::wrong_target

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `wrong_target`
- Gold/prediction: `False` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should replace "the".`

## 50. rule_evidence_verifier::EXPECT::expect-test-00001::coedit_large::00003::2-3::replace::wrong_operation

- Dataset/model: `EXPECT` / `coedit_large`
- Behavior/type: `overcorrection` / `R:SPELL`
- Explanation type: `wrong_operation`
- Gold/prediction: `False` / `False`
- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Explanation: `This edit should insert the relevant phrase.`

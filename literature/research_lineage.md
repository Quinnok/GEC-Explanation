# Research Lineage

## From GEC Generation to Edit-Level Explanation

Classic English GEC evaluation began with shared tasks and edit scorers: M2, CoNLL-2014, ERRANT, BEA-2019, GLEU, and JFLEG. This line made edits explicit, but the object was correction quality, not explanation quality.

EXPECT moved English GEC toward explanation-adjacent supervision by adding evidence words and error types. GEE and Prompt Insertion moved further toward natural-language explanations for individual edits. EXCGEC then made edit-wise explainable GEC a benchmark task in Chinese. Therefore, this project must not claim to introduce edit-wise GEC explanations in general.

## From Whole-Sentence Metrics to Edit Behavior

Recent GEC evaluation work, especially CLEME2.0 and edit-level metric attribution, confirms that modern evaluation is shifting from aggregate F0.5 toward behavior decomposition: hit/correct correction, wrong correction, undercorrection/missed correction, and overcorrection. Our Round 03/04 behavior labels fit this line, but the contribution cannot be just behavior classification.

## From Explanation Quality to Faithfulness

Faithfulness work in NLP warns that explanations can be plausible or helpful without reflecting model behavior. Jacovi and Goldberg define the conceptual risk; Lyu et al. survey faithful explanation methods; Parcalabescu and Frank warn that many natural-language faithfulness tests measure self-consistency rather than internal faithfulness.

## Simulatability, Reconstruction, and Counterfactual Evaluation

Hase and Bansal define simulatability as helping users predict model behavior. Reverse reconstruction is one mechanized version of this idea, but Round 02 showed that explicit edit templates leak the answer. Counterfactual evaluation, from CheckList and contrast sets to COCOGEC, tests whether behavior changes appropriately under controlled input changes. The project's likely contribution is to specialize simulatability to GEC model-produced edits and separate leakage-prone correspondence from counterfactual behavioral faithfulness.

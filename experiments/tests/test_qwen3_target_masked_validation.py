import unittest

from experiments.rulefaith import validate_qwen3_target_masked as target_masked


class Qwen3TargetMaskedValidationTest(unittest.TestCase):
    def row(self, rule_text, rationale, target_text="go"):
        return {
            "candidate_id": "c1",
            "source": "The students goes to school .",
            "model_prediction": "The students go to school .",
            "model_edit": {
                "operation": "replace",
                "start": 2,
                "end": 3,
                "source_text": "goes",
                "target_text": target_text,
                "error_type": "R:VERB:SVA",
            },
            "parsed_output": {
                "edit_description": "Replace goes with go.",
                "edit_validity": "valid",
                "rule_text": rule_text,
                "evidence_spans": [
                    {"text": "students", "start": 1, "end": 2, "role": "grammatical_subject"},
                    {"text": "goes", "start": 2, "end": 3, "role": "finite_verb"},
                ],
                "rationale": rationale,
                "applicability_conditions": ["the subject is plural"],
                "confidence": 0.7,
                "abstain": False,
            },
            "rulefaith_field_aware_selection": {"bucket": "accepted"},
            "error_category": "subject_verb_agreement",
        }

    def test_word_target_mask_does_not_mask_substrings(self):
        masked, count = target_masked.mask_target("go going go.", "go")
        self.assertEqual(masked, "[TARGET_MASK] going [TARGET_MASK].")
        self.assertEqual(count, 2)

    def test_rule_and_evidence_survive_target_mask(self):
        row = self.row(
            "Plural subjects require the base present-tense verb form.",
            "The plural subject students requires the base verb form.",
        )
        result = target_masked.validate_row(row)
        self.assertEqual(result["target_masked_bucket"], "validated")
        self.assertTrue(result["masked_rule_has_grammar_signal"])
        self.assertTrue(result["specific_evidence_mentioned_after_mask"])

    def test_target_dependent_copy_requires_refinement(self):
        row = self.row("Use go here.", "Use go because go is correct.")
        result = target_masked.validate_row(row)
        self.assertEqual(result["target_masked_bucket"], "rejected")
        self.assertIn("target_dependent_quality_text", result["failures"])
        self.assertTrue(result["target_dependent"])

    def test_noun_number_rule_mismatch_requires_refinement(self):
        row = self.row(
            "Subjects and verbs must agree in number.",
            "The singular noun area should agree with the surrounding noun phrase.",
            target_text="areas",
        )
        row["model_edit"] = {
            "operation": "replace",
            "start": 9,
            "end": 10,
            "source_text": "area",
            "target_text": "areas",
            "error_type": "R:NOUN:NUM",
        }
        row["source"] = "The government prohibited smoking in public area ."
        row["model_prediction"] = "The government prohibited smoking in public areas ."
        row["parsed_output"]["evidence_spans"] = [
            {"text": "public", "start": 5, "end": 6, "role": "noun_number_context"},
            {"text": "area", "start": 6, "end": 7, "role": "head_noun"},
        ]
        row["error_category"] = "noun_number"
        result = target_masked.validate_row(row)
        self.assertEqual(result["target_masked_bucket"], "refine")
        self.assertEqual(result["rule_category_issue"], "noun_number_explained_as_subject_verb_agreement")


if __name__ == "__main__":
    unittest.main()

import unittest

from experiments.rulefaith import select_qwen3_field_aware_rulefaith as select


class Qwen3FieldAwareSelectionTest(unittest.TestCase):
    def row(self, rationale="The plural subject students requires the base verb form.", parse_status="parsed_json"):
        return {
            "candidate_id": "c1",
            "parse_status": parse_status,
            "source": "The students goes to school .",
            "model_prediction": "The students go to school .",
            "model_edit": {
                "operation": "replace",
                "start": 2,
                "end": 3,
                "source_text": "goes",
                "target_text": "go",
                "error_type": "R:VERB:SVA",
            },
            "parsed_output": {
                "edit_description": "Replace goes with go.",
                "edit_validity": "valid",
                "rule_text": "Plural subjects require the base verb form.",
                "evidence_spans": [
                    {"text": "students", "start": 1, "end": 2, "role": "grammatical_subject"},
                    {"text": "goes", "start": 2, "end": 3, "role": "finite_verb"},
                ],
                "rationale": rationale,
                "confidence": 0.7,
                "abstain": False,
            },
        }

    def clean_flags(self):
        return {
            "alignment_error": False,
            "validity_error_auto": False,
            "possible_false_rationalization": False,
            "missing_rule": False,
            "rule_edit_copy": False,
            "missing_evidence": False,
            "wrong_evidence_auto": False,
            "evidence_text_found_in_prediction_only": False,
            "unsupported_confidence": False,
            "generic_explanation": False,
        }

    def test_edit_description_copy_is_allowed(self):
        bucket, hard, refine, leakage = select.select_candidate(self.row(), self.clean_flags())
        self.assertEqual(bucket, "accepted")
        self.assertTrue(leakage["edit_description_edit_copy"])
        self.assertEqual(hard, [])
        self.assertEqual(refine, [])

    def test_rationale_edit_copy_goes_to_refine(self):
        row = self.row(rationale="Replace goes with go because the subject is plural.")
        bucket, hard, refine, leakage = select.select_candidate(row, self.clean_flags())
        self.assertEqual(bucket, "refine")
        self.assertTrue(leakage["rationale_edit_copy"])
        self.assertEqual(refine, ["rationale_edit_copy"])
        self.assertEqual(hard, [])

    def test_false_rationalization_remains_rejected(self):
        flags = self.clean_flags()
        flags["possible_false_rationalization"] = True
        bucket, hard, refine, _ = select.select_candidate(self.row(), flags)
        self.assertEqual(bucket, "rejected")
        self.assertIn("possible_false_rationalization", hard)
        self.assertEqual(refine, [])


if __name__ == "__main__":
    unittest.main()

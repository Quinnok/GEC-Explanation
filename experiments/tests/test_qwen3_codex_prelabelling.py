import unittest

from experiments.rulefaith import prefill_qwen3_audit_codex as prefill


class Qwen3CodexPrelabellingTest(unittest.TestCase):
    def form_row(self):
        return {
            "candidate_id": "c1",
            "source": "The students goes .",
            "model_prediction": "The students go .",
            "operation": "replace",
            "source_text": "goes",
            "target_text": "go",
            "rule_text": "Plural subjects take base verbs.",
            "evidence_spans_json": "[]",
            "human_alignment_error": "",
            "human_validity_error": "",
            "human_wrong_rule": "",
            "human_inapplicable_rule": "",
            "human_missing_evidence": "",
            "human_wrong_evidence": "",
            "human_generic_explanation": "",
            "human_edit_copy": "",
            "human_semantic_distortion": "",
            "human_unsupported_confidence": "",
            "human_notes": "",
            "human_decision": "",
        }

    def test_missing_evidence_is_refine(self):
        diag = {
            "alignment_error": "False",
            "source_span_match": "True",
            "target_present_in_prediction": "True",
            "validity_error_auto": "False",
            "possible_false_rationalization": "False",
            "semantic_distortion_auto": "False",
            "missing_evidence": "True",
            "wrong_evidence_auto": "False",
            "evidence_text_found_in_prediction_only": "False",
            "generic_explanation": "False",
            "edit_copy": "False",
            "rule_edit_copy": "False",
            "unsupported_confidence": "False",
            "confidence": "0.5",
        }
        row = prefill.prelabel_row(self.form_row(), diag)
        self.assertEqual(row["human_missing_evidence"], "yes")
        self.assertEqual(row["human_decision"], "refine")

    def test_false_rationalization_is_reject(self):
        diag = {
            "alignment_error": "False",
            "source_span_match": "True",
            "target_present_in_prediction": "True",
            "validity_error_auto": "True",
            "possible_false_rationalization": "True",
            "semantic_distortion_auto": "True",
            "missing_evidence": "False",
            "wrong_evidence_auto": "False",
            "evidence_text_found_in_prediction_only": "False",
            "generic_explanation": "False",
            "edit_copy": "False",
            "rule_edit_copy": "False",
            "unsupported_confidence": "True",
            "confidence": "1.0",
            "edit_validity": "valid",
        }
        row = prefill.prelabel_row(self.form_row(), diag)
        self.assertEqual(row["human_validity_error"], "yes")
        self.assertEqual(row["human_wrong_rule"], "yes")
        self.assertEqual(row["human_decision"], "reject")


if __name__ == "__main__":
    unittest.main()

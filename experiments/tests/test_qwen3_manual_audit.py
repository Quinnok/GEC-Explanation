import unittest

from experiments.rulefaith import build_qwen3_manual_audit as audit


class Qwen3ManualAuditTest(unittest.TestCase):
    def test_source_span_match_replace(self):
        source = "The students goes to school ."
        edit = {"operation": "replace", "start": 2, "end": 3, "source_text": "goes", "target_text": "go"}
        self.assertTrue(audit.source_span_match(source, edit))

    def test_evidence_span_must_match_source_indices(self):
        source = "The students goes to school ."
        edit = {"operation": "replace", "start": 2, "end": 3, "source_text": "goes", "target_text": "go"}
        spans = [{"text": "students", "start": 1, "end": 2, "role": "grammatical_subject"}]
        checks = audit.evidence_checks(source, edit, spans)
        self.assertTrue(checks["evidence_span_index_match"])
        self.assertTrue(checks["evidence_contextual"])
        self.assertFalse(checks["missing_evidence"])

    def test_evidence_span_with_wrong_indices_is_flagged(self):
        source = "The students goes to school ."
        edit = {"operation": "replace", "start": 2, "end": 3, "source_text": "goes", "target_text": "go"}
        spans = [{"text": "students", "start": 2, "end": 3, "role": "grammatical_subject"}]
        checks = audit.evidence_checks(source, edit, spans)
        self.assertFalse(checks["evidence_span_index_match"])
        self.assertTrue(checks["wrong_evidence_auto"])

    def test_input_leakage_detects_forbidden_fields(self):
        row = {
            "generator_input_fields": ["source", "model_prediction", "reference"],
            "uses_reference_in_generator": False,
            "uses_behavior_label_in_generator": False,
            "uses_human_label_in_generator": False,
            "uses_gold_edit_in_generator": False,
        }
        self.assertTrue(audit.leakage_input_violation(row))

    def test_false_rationalization_for_wrong_edit_marked_valid(self):
        parsed = {
            "edit_validity": "valid",
            "rule_text": "A third-person subject requires this verb form.",
            "rationale": "This makes the sentence grammatically correct.",
        }
        self.assertTrue(audit.possible_false_rationalization(parsed, "wrong_correction"))

    def test_false_rationalization_not_flagged_when_explanation_caveats_invalid_edit(self):
        parsed = {
            "edit_validity": "invalid",
            "rule_text": "The model changed the verb, but the result is still ungrammatical.",
            "rationale": "This edit is invalid because an auxiliary is still missing.",
        }
        self.assertFalse(audit.possible_false_rationalization(parsed, "wrong_correction"))


if __name__ == "__main__":
    unittest.main()

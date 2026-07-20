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
        checks = audit.evidence_checks(source, "The students go to school .", edit, spans)
        self.assertTrue(checks["evidence_span_index_match"])
        self.assertTrue(checks["evidence_all_spans_source_index_match"])
        self.assertTrue(checks["evidence_contextual"])
        self.assertFalse(checks["missing_evidence"])

    def test_evidence_span_with_wrong_indices_is_flagged(self):
        source = "The students goes to school ."
        edit = {"operation": "replace", "start": 2, "end": 3, "source_text": "goes", "target_text": "go"}
        spans = [{"text": "students", "start": 2, "end": 3, "role": "grammatical_subject"}]
        checks = audit.evidence_checks(source, "The students go to school .", edit, spans)
        self.assertFalse(checks["evidence_span_index_match"])
        self.assertTrue(checks["wrong_evidence_auto"])
        self.assertIn("index_text_mismatch", checks["evidence_error_types"])

    def test_prediction_only_target_is_not_source_evidence(self):
        source = "The students goes to school ."
        prediction = "The students go to school ."
        edit = {"operation": "replace", "start": 2, "end": 3, "source_text": "goes", "target_text": "go"}
        spans = [{"text": "go", "start": 2, "end": 3, "role": "correction"}]
        checks = audit.evidence_checks(source, prediction, edit, spans)
        self.assertTrue(checks["evidence_text_found_in_prediction_only"])
        self.assertTrue(checks["missing_evidence"])
        self.assertTrue(checks["wrong_evidence_auto"])

    def test_spelling_edit_token_can_count_as_contextual_evidence(self):
        source = "Beacuse it rained ."
        prediction = "Because it rained ."
        edit = {
            "operation": "replace",
            "start": 0,
            "end": 1,
            "source_text": "Beacuse",
            "target_text": "Because",
            "error_type": "R:ORTH",
        }
        spans = [{"text": "Beacuse", "start": 0, "end": 1, "role": "misspelled_word"}]
        checks = audit.evidence_checks(source, prediction, edit, spans)
        self.assertTrue(checks["evidence_contextual"])
        self.assertFalse(checks["missing_evidence"])

    def test_punctuation_only_replacement_can_use_modified_token_as_evidence(self):
        source = "Technology will fly above streets and computers will change ."
        prediction = "Technology will fly above streets, and computers will change ."
        edit = {
            "operation": "replace",
            "start": 4,
            "end": 5,
            "source_text": "streets",
            "target_text": "streets,",
            "error_type": "R:NOUN",
        }
        spans = [{"text": "streets", "start": 4, "end": 5, "role": "modified_token"}]
        checks = audit.evidence_checks(source, prediction, edit, spans)
        self.assertTrue(checks["evidence_contextual"])
        self.assertFalse(checks["missing_evidence"])

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

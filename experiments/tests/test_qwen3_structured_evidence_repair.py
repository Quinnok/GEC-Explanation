import unittest

from experiments.rulefaith import build_qwen3_manual_audit as audit
from experiments.rulefaith import repair_qwen3_structured_evidence as repair


class Qwen3StructuredEvidenceRepairTest(unittest.TestCase):
    def candidate(self, source, prediction, edit, error_category=""):
        return {
            "candidate_id": "c1",
            "source": source,
            "model_prediction": prediction,
            "model_edit": edit,
            "error_category": error_category,
            "candidate_type": "evidence_canonicalized",
            "parse_status": "parsed_json",
            "parsed_output": {
                "edit_description": "The model changes the current edit.",
                "edit_validity": "valid",
                "rule_text": "A relevant grammar rule applies.",
                "evidence_spans": [],
                "rationale": "The rule applies in this sentence.",
                "confidence": 0.8,
                "abstain": False,
                "abstain_reason": "",
            },
        }

    def test_sva_adds_subject_context(self):
        row = self.candidate(
            "The students goes to school .",
            "The students go to school .",
            {
                "operation": "replace",
                "start": 2,
                "end": 3,
                "source_text": "goes",
                "target_text": "go",
                "error_type": "R:VERB:SVA",
            },
            "subject_verb_agreement",
        )
        repaired, actions = repair.repair_record(row, window=4)
        spans = repaired["parsed_output"]["evidence_spans"]
        self.assertIn("added_sva_subject", actions)
        self.assertTrue(any(span["text"] == "students" and span["role"] == "grammatical_subject" for span in spans))
        checks = audit.evidence_checks(row["source"], row["model_prediction"], row["model_edit"], spans)
        self.assertTrue(checks["evidence_contextual"])
        self.assertFalse(checks["missing_evidence"])

    def test_determiner_insert_adds_head_noun(self):
        row = self.candidate(
            "I went to school .",
            "I went to the school .",
            {
                "operation": "insert",
                "start": 3,
                "end": 3,
                "source_text": "",
                "target_text": "the",
                "error_type": "M:DET",
            },
        )
        repaired, actions = repair.repair_record(row, window=4)
        spans = repaired["parsed_output"]["evidence_spans"]
        self.assertIn("added_determiner_head_noun", actions)
        self.assertTrue(any(span["text"] == "school" and span["role"] == "head_noun" for span in spans))
        checks = audit.evidence_checks(row["source"], row["model_prediction"], row["model_edit"], spans)
        self.assertTrue(checks["evidence_contextual"])

    def test_preposition_adds_governor_and_complement(self):
        row = self.candidate(
            "She is interested at science .",
            "She is interested in science .",
            {
                "operation": "replace",
                "start": 3,
                "end": 4,
                "source_text": "at",
                "target_text": "in",
                "error_type": "R:PREP",
            },
        )
        repaired, actions = repair.repair_record(row, window=4)
        spans = repaired["parsed_output"]["evidence_spans"]
        self.assertIn("added_preposition_governor", actions)
        self.assertIn("added_preposition_complement", actions)
        self.assertTrue(any(span["text"] == "interested" for span in spans))
        self.assertTrue(any(span["text"] == "science" for span in spans))
        checks = audit.evidence_checks(row["source"], row["model_prediction"], row["model_edit"], spans)
        self.assertTrue(checks["evidence_contextual"])
        self.assertFalse(checks["evidence_text_found_in_prediction_only"])

    def test_specific_source_evidence_excludes_generic_left_right_context(self):
        row = self.candidate(
            "This phrase is odd here .",
            "This phrase is better here .",
            {
                "operation": "replace",
                "start": 3,
                "end": 4,
                "source_text": "odd",
                "target_text": "better",
                "error_type": "R:OTHER",
            },
        )
        repaired, actions = repair.repair_record(row, window=4)
        self.assertIn("added_left_context", actions)
        self.assertTrue(repaired["after_evidence_checks"]["evidence_contextual"])
        self.assertFalse(repair.has_specific_source_evidence(repaired))

    def test_strict_selection_routes_edit_copy_to_refine(self):
        row = self.candidate(
            "The students goes to school .",
            "The students go to school .",
            {
                "operation": "replace",
                "start": 2,
                "end": 3,
                "source_text": "goes",
                "target_text": "go",
                "error_type": "R:VERB:SVA",
            },
            "subject_verb_agreement",
        )
        repaired, _ = repair.repair_record(row, window=4)
        flags = {
            "alignment_error": False,
            "validity_error_auto": False,
            "possible_false_rationalization": False,
            "missing_rule": False,
            "rule_edit_copy": False,
            "missing_evidence": False,
            "wrong_evidence_auto": False,
            "evidence_text_found_in_prediction_only": False,
            "edit_copy": True,
            "unsupported_confidence": False,
            "generic_explanation": False,
        }
        bucket, reasons = repair.selection_for(repaired, flags)
        self.assertEqual(bucket, "refine")
        self.assertEqual(reasons, ["edit_copy"])

    def test_strict_selection_rejects_false_rationalization(self):
        row = self.candidate(
            "She go to school .",
            "She going to school .",
            {
                "operation": "replace",
                "start": 1,
                "end": 2,
                "source_text": "go",
                "target_text": "going",
                "error_type": "R:VERB:FORM",
            },
        )
        repaired, _ = repair.repair_record(row, window=4)
        flags = {
            "alignment_error": False,
            "validity_error_auto": True,
            "possible_false_rationalization": True,
            "missing_rule": False,
            "rule_edit_copy": False,
            "missing_evidence": False,
            "wrong_evidence_auto": False,
            "evidence_text_found_in_prediction_only": False,
            "edit_copy": False,
            "unsupported_confidence": False,
            "generic_explanation": False,
        }
        bucket, reasons = repair.selection_for(repaired, flags)
        self.assertEqual(bucket, "rejected")
        self.assertIn("possible_false_rationalization", reasons)


if __name__ == "__main__":
    unittest.main()

import unittest

from experiments.rulefaith import audit_qwen3_rule_plausibility as plausibility


class Qwen3RulePlausibilityAuditTest(unittest.TestCase):
    def base_row(self):
        return {
            "candidate_id": "c1",
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
            "error_category": "subject_verb_agreement",
            "parsed_output": {
                "rule_text": "Plural subjects require the base present-tense verb form.",
                "rationale": "The plural subject students requires the base verb form.",
                "evidence_spans": [
                    {"text": "students", "start": 1, "end": 2, "role": "grammatical_subject"},
                    {"text": "goes", "start": 2, "end": 3, "role": "finite_verb"},
                ],
                "confidence": 0.75,
            },
        }

    def test_sva_requires_subject_and_verb_evidence(self):
        row = self.base_row()
        label, reasons = plausibility.evidence_sufficiency(row)
        self.assertEqual(label, "sufficient")
        self.assertEqual(reasons, [])

    def test_preposition_requires_governor_and_complement(self):
        row = {
            "candidate_id": "p1",
            "source": "She is interested at science .",
            "model_prediction": "She is interested in science .",
            "model_edit": {
                "operation": "replace",
                "start": 3,
                "end": 4,
                "source_text": "at",
                "target_text": "in",
                "error_type": "R:PREP",
            },
            "error_category": "prepositions",
            "parsed_output": {
                "rule_text": "The preposition should match its governing adjective.",
                "rationale": "Interested takes a preposition before science.",
                "evidence_spans": [{"text": "interested", "start": 2, "end": 3, "role": "preposition_governor"}],
                "confidence": 0.7,
            },
        }
        label, reasons = plausibility.evidence_sufficiency(row)
        self.assertEqual(label, "partial")
        self.assertIn("missing_required_evidence:complement", reasons)

    def test_wrong_rule_category_is_rejected(self):
        row = self.base_row()
        row["source"] = "The government prohibited smoking in public area ."
        row["model_prediction"] = "The government prohibited smoking in public areas ."
        row["model_edit"] = {
            "operation": "replace",
            "start": 6,
            "end": 7,
            "source_text": "area",
            "target_text": "areas",
            "error_type": "R:NOUN:NUM",
        }
        row["error_category"] = "noun_number"
        row["parsed_output"]["rule_text"] = "Subjects and verbs must agree in number."
        row["parsed_output"]["rationale"] = "The noun area should agree with the surrounding phrase."
        row["parsed_output"]["evidence_spans"] = [{"text": "area", "start": 6, "end": 7, "role": "head_noun"}]
        result = plausibility.audit_row(row)
        self.assertEqual(result["decision"], "reject")
        self.assertEqual(result["rule_plausibility_label"], "implausible")


if __name__ == "__main__":
    unittest.main()

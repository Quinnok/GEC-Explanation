import csv
import tempfile
import unittest
from pathlib import Path

from experiments.rulefaith import prepare_qwen3_validation_package as package


class Qwen3ValidationPackageTest(unittest.TestCase):
    def test_blind_form_hides_candidate_identity_and_model(self):
        row = {
            "candidate_id": "rf-edit-1::qwen3_8b::natural",
            "dataset": "EXPECT",
            "model_key": "secret_model",
            "source": "The students goes .",
            "model_prediction": "The students go .",
            "model_edit": {"operation": "replace", "start": 2, "end": 3, "source_text": "goes", "target_text": "go"},
            "parsed_output": {
                "edit_description": "Replace goes with go.",
                "edit_validity": "valid",
                "rule_text": "Plural subjects require the base verb.",
                "evidence_spans": [{"text": "students", "start": 1, "end": 2, "role": "grammatical_subject"}],
                "rationale": "The subject students is plural.",
                "confidence": 0.7,
            },
        }
        blind = package.blind_rows([row])[0]
        self.assertEqual(blind["validation_item_id"], "rfq3-ready-0001")
        self.assertNotIn("candidate_id", blind)
        self.assertNotIn("model_key", blind)

    def test_package_writes_expected_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            form = out / "form.csv"
            rows = [{"validation_item_id": "rfq3-ready-0001"}]
            package.write_csv(form, rows, ["validation_item_id"], overwrite=True)
            with form.open(encoding="utf-8", newline="") as handle:
                loaded = list(csv.DictReader(handle))
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["validation_item_id"], "rfq3-ready-0001")


if __name__ == "__main__":
    unittest.main()

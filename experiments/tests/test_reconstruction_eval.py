import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from evaluate_reconstruction import evaluate_records


class ReconstructionEvalTests(unittest.TestCase):
    def test_unreconstructable_scores_zero(self):
        result = evaluate_records(
            [
                {
                    "sample_id": "x",
                    "edit": {
                        "start": 1,
                        "end": 2,
                        "source_text": "go",
                        "target_text": "goes",
                        "operation": "replace",
                        "error_type": "SVA",
                    },
                    "reconstruction": {"reconstructable": False},
                }
            ]
        )
        self.assertEqual(result["macro_average"]["full_edit_exact"], 0.0)

    def test_exact_reconstruction_scores_one(self):
        edit = {
            "start": 1,
            "end": 2,
            "source_text": "go",
            "target_text": "goes",
            "operation": "replace",
            "error_type": "SVA",
        }
        result = evaluate_records([{"sample_id": "x", "edit": edit, "reconstruction": {"reconstructable": True, **edit}}])
        self.assertEqual(result["macro_average"]["full_edit_exact"], 1.0)


if __name__ == "__main__":
    unittest.main()


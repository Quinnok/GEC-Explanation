import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from evaluate_reconstruction import evaluate_records
from baselines import structured_explicit_edit_baseline


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

    def test_source_span_pattern_without_token_word(self):
        edit = structured_explicit_edit_baseline(
            "She go home .",
            'This edit should replace "go" with "goes" at source span [1,2) for R:VERB:SVA.',
            error_type="R:VERB:SVA",
        )
        self.assertIsNotNone(edit)
        self.assertEqual(edit.start, 1)
        self.assertEqual(edit.end, 2)
        self.assertEqual(edit.target_text, "goes")


if __name__ == "__main__":
    unittest.main()

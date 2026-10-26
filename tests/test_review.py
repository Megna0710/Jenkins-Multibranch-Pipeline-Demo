import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReviewScriptTests(unittest.TestCase):
    def test_review_script_passes(self):
        result = subprocess.run(
            [sys.executable, "scripts/review.py"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Review passed", result.stdout)


if __name__ == "__main__":
    unittest.main()

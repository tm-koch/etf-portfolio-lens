from __future__ import annotations

import json
import subprocess
import unittest

from test_web_runtime import REPOSITORY_ROOT


class DiversificationFrontendTests(unittest.TestCase):
    def run_module(self, script: str) -> dict:
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_effective_number_rating_boundaries_and_dynamic_scale(self) -> None:
        values = self.run_module("""
import { calculateDiversificationScore, classifyDiversificationScore } from './web/diversification.js';

const positions = [{ weight: 100, coveragePct: 100 }];
const equalFour = calculateDiversificationScore([1, 1, 1, 1], positions);
const boundaryRatings = [4.99, 5, 10, 20, 40].map(classifyDiversificationScore);
const fifty = calculateDiversificationScore(Array.from({ length: 50 }, () => 1), positions);
const nearComplete = calculateDiversificationScore([1], [
    { weight: 100, coveragePct: 99.999974 },
]);
const nearlyCompleteButVisible = calculateDiversificationScore([1], [
    { weight: 100, coveragePct: 99.994 },
]);
console.log(JSON.stringify({ equalFour, boundaryRatings, fifty, nearComplete, nearlyCompleteButVisible }));
""")

        self.assertEqual(values["equalFour"]["score"], 4)
        self.assertEqual(values["equalFour"]["rating"], "highlyConcentrated")
        self.assertEqual(
            values["boundaryRatings"],
            [
                "highlyConcentrated",
                "concentrated",
                "moderatelyDiversified",
                "wellDiversified",
                "highlyDiversified",
            ],
        )
        self.assertEqual(values["fifty"]["score"], 50)
        self.assertEqual(values["fifty"]["maximum"], 50)
        self.assertFalse(values["equalFour"]["coverageIncomplete"])
        self.assertFalse(values["nearComplete"]["coverageIncomplete"])
        self.assertTrue(values["nearlyCompleteButVisible"]["coverageIncomplete"])

    def test_partial_coverage_and_unavailable_exposure(self) -> None:
        values = self.run_module("""
import { calculateDiversificationScore } from './web/diversification.js';

const partial = calculateDiversificationScore([2, 1], [
  { weight: 75, coveragePct: 80 },
  { weight: 25, coveragePct: 0 },
  { weight: 0, coveragePct: 100 },
]);
const unavailable = calculateDiversificationScore([], [
  { weight: 100, coveragePct: 0 },
]);
console.log(JSON.stringify({ partial, unavailable }));
""")

        self.assertAlmostEqual(values["partial"]["coveragePct"], 60)
        self.assertAlmostEqual(values["partial"]["score"], 1.8)
        self.assertTrue(values["partial"]["coverageIncomplete"])
        self.assertFalse(values["unavailable"]["available"])
        self.assertIsNone(values["unavailable"]["score"])


if __name__ == "__main__":
    unittest.main()

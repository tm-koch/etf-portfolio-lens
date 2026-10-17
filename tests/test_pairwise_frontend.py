from __future__ import annotations

import json
import subprocess
import unittest

from test_web_runtime import REPOSITORY_ROOT


class PairwiseFrontendTests(unittest.TestCase):
    def run_module(self, script: str) -> dict:
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_pair_index_supports_unordered_pairs_and_legacy_catalogs(self) -> None:
        values = self.run_module("""
import { buildPairwiseOverlapIndex, getPairwiseOverlap } from './web/pairwise-overlap.js';

const index = buildPairwiseOverlapIndex({
  version: 1,
  pairs: [
    { isinA: 'AAA', isinB: 'BBB', overlapPct: 91, available: true },
    { isinA: 'CCC', isinB: 'DDD', overlapPct: null, available: false },
    { isinA: 'BAD', isinB: 'PAIR', overlapPct: 101, available: true },
  ],
});
console.log(JSON.stringify({
  reversed: getPairwiseOverlap(index, 'BBB', 'AAA'),
  unavailable: getPairwiseOverlap(index, 'DDD', 'CCC'),
  bad: getPairwiseOverlap(index, 'BAD', 'PAIR'),
  same: getPairwiseOverlap(index, 'AAA', 'AAA'),
  legacySize: buildPairwiseOverlapIndex(undefined).size,
}));
""")

        self.assertEqual(values["reversed"]["overlapPct"], 91)
        self.assertFalse(values["unavailable"]["available"])
        self.assertIsNone(values["bad"])
        self.assertIsNone(values["same"])
        self.assertEqual(values["legacySize"], 0)

    def test_matrix_uses_selection_order_and_inclusive_threshold(self) -> None:
        values = self.run_module("""
import { buildPairwiseMatrix, buildPairwiseOverlapIndex } from './web/pairwise-overlap.js';

const index = buildPairwiseOverlapIndex({
  version: 1,
  pairs: [{ isinA: 'A', isinB: 'B', overlapPct: 90, coveragePctA: 95, coveragePctB: 92, available: true }],
});
const positions = ['B', 'A', 'C'].map((isin) => ({
  isin,
  entry: { ticker: isin, name: `Fund ${isin}` },
}));
const atThreshold = buildPairwiseMatrix(positions, index, 90);
const aboveThreshold = buildPairwiseMatrix(positions, index, 90.1);
console.log(JSON.stringify({
  order: atThreshold.map((row) => row.product.isin),
  diagonal: atThreshold[0].cells[0].type,
  upper: atThreshold[0].cells[2].type,
  near: atThreshold[1].cells[0].nearIdentical,
  below: aboveThreshold[1].cells[0].nearIdentical,
  missing: atThreshold[2].cells[0].type,
}));
""")

        self.assertEqual(values["order"], ["B", "A", "C"])
        self.assertEqual(values["diagonal"], "diagonal")
        self.assertEqual(values["upper"], "empty")
        self.assertTrue(values["near"])
        self.assertFalse(values["below"])
        self.assertEqual(values["missing"], "unavailable")

    def test_near_identical_pairs_follow_threshold_and_selection(self) -> None:
        values = self.run_module("""
import { buildPairwiseOverlapIndex, findNearIdenticalPairs } from './web/pairwise-overlap.js';

const index = buildPairwiseOverlapIndex({
  version: 1,
  pairs: [
    { isinA: 'A', isinB: 'B', overlapPct: 90, available: true },
    { isinA: 'A', isinB: 'C', overlapPct: 89, available: true },
    { isinA: 'B', isinB: 'C', overlapPct: null, available: false },
  ],
});
const positions = ['A', 'B', 'C'].map((isin) => ({
  isin,
  entry: { ticker: isin, name: `Fund ${isin}` },
}));
console.log(JSON.stringify({
  atDefault: findNearIdenticalPairs(positions, index, 90).map((pair) => pair.overlapPct),
  atLower: findNearIdenticalPairs(positions, index, 89).map((pair) => pair.overlapPct),
  subset: findNearIdenticalPairs(positions.slice(1), index, 90).length,
}));
""")

        self.assertEqual(values["atDefault"], [90])
        self.assertEqual(values["atLower"], [90, 89])
        self.assertEqual(values["subset"], 0)

    def test_catalog_loader_revalidates_the_manifest(self) -> None:
        values = self.run_module("""
import { loadPublishedCatalog } from './web/data.js';

let requestOptions;
globalThis.fetch = async (url, options) => {
  requestOptions = options;
  return { ok: true, json: async () => ({ etfs: [] }) };
};
await loadPublishedCatalog();
console.log(JSON.stringify(requestOptions));
""")

        self.assertEqual(values, {"cache": "no-cache"})


if __name__ == "__main__":
    unittest.main()

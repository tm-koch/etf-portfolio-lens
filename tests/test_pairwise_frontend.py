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

    def test_pairwise_weight_numbers_are_localized_without_percent_suffix(self) -> None:
        values = self.run_module("""
import { formatPercentNumber } from './web/formatting.js';
console.log(JSON.stringify({
  english: formatPercentNumber(5.25, 'en-CH'),
  german: formatPercentNumber(5.25, 'de-CH'),
  polish: formatPercentNumber(5.25, 'pl-PL'),
}));
""")

        self.assertEqual(values["english"], "5.3")
        self.assertEqual(values["german"], "5.3")
        self.assertEqual(values["polish"], "5,3")

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

    def test_holdings_breakdown_matches_company_and_exact_isin_overlap(self) -> None:
        values = self.run_module("""
import { buildPairwiseHoldingsBreakdown } from './web/pairwise-overlap.js';

const holding = (name, weight, isin, companyId, canonicalName = name) => ({
  security: { name, isin, company_id: companyId, canonical_name: canonicalName },
  exposure: { weight_pct: weight },
});
const breakdown = buildPairwiseHoldingsBreakdown(
  [
    holding('Acme Corp', 6, 'SHARED-1', 'acme-corp'),
    holding('Acme Corp', 4, 'CLASS-A', 'acme-corp'),
    holding('Beta Inc', 5, 'BETA', 'beta-inc'),
    holding('Exact Only', 2, 'EXACT', null),
  ],
  [
    holding('Acme Corp', 3, 'SHARED-1', null, 'Acme Corp'),
    holding('Acme Corp', 7, 'CLASS-B', 'acme-corp'),
    holding('Beta Inc', 4, 'BETA', 'beta-inc'),
    holding('Exact Only', 1, 'EXACT', null),
  ],
);
console.log(JSON.stringify(breakdown));
""")

        rows = {row["name"]: row for row in values["companies"]}
        self.assertEqual(rows["Acme Corp"]["contribution"], 10)
        self.assertEqual(rows["Beta Inc"]["contribution"], 4)
        self.assertEqual(rows["Exact Only"]["contribution"], 1)
        self.assertEqual(sum(row["contribution"] for row in values["companies"]), 15)

    def test_holdings_breakdown_sorts_limits_and_summarizes_remaining(self) -> None:
        values = self.run_module("""
import { buildPairwiseHoldingsBreakdown } from './web/pairwise-overlap.js';

const holding = (name, weight, isin) => ({
  security: { name, canonical_name: name, isin },
  exposure: { weight_pct: weight },
});
const left = [holding('Zulu', 6, 'Z'), holding('Alpha', 5, 'A'), holding('Beta', 5, 'B')];
const right = [holding('Zulu', 6, 'Z'), holding('Alpha', 5, 'A'), holding('Beta', 4, 'B')];
const limited = buildPairwiseHoldingsBreakdown(left, right, 2);
const defaulted = buildPairwiseHoldingsBreakdown(left, right, 0);
console.log(JSON.stringify({
  names: limited.displayed.map((company) => company.name),
  remaining: limited.remainingContribution,
  remainingWeights: limited.remainingWeights,
  defaultCount: defaulted.displayed.length,
}));
""")

        self.assertEqual(values["names"], ["Zulu", "Alpha"])
        self.assertEqual(values["remaining"], 4)
        self.assertEqual(values["remainingWeights"], {"weightA": 5, "weightB": 4})
        self.assertEqual(values["defaultCount"], 3)

    def test_pairwise_holdings_maximum_preference_defaults_validates_and_persists(
        self,
    ) -> None:
        values = self.run_module("""
import {
  DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES,
  PAIRWISE_HOLDINGS_MAX_COMPANIES_STORAGE_KEY,
  loadPairwiseHoldingsMaxCompanies,
  savePairwiseHoldingsMaxCompanies,
  validatePairwiseHoldingsMaxCompanies,
} from './web/redundancy.js';

const values = new Map();
const storage = {
  getItem: (key) => values.get(key) ?? null,
  setItem: (key, value) => values.set(key, value),
};
const missing = loadPairwiseHoldingsMaxCompanies(storage);
const saved = savePairwiseHoldingsMaxCompanies(35, storage);
const loaded = loadPairwiseHoldingsMaxCompanies(storage);
values.set(PAIRWISE_HOLDINGS_MAX_COMPANIES_STORAGE_KEY, '"Infinity"');
const malformed = loadPairwiseHoldingsMaxCompanies(storage);
console.log(JSON.stringify({
  defaultValue: DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES,
  missing,
  saved,
  loaded,
  malformed,
  acceptsIntegerString: validatePairwiseHoldingsMaxCompanies('3'),
  rejects: [0, -1, 1.5, ' ', 'NaN'].map(validatePairwiseHoldingsMaxCompanies),
}));
""")

        self.assertEqual(values["defaultValue"], 10)
        self.assertEqual(values["missing"], 10)
        self.assertTrue(values["saved"])
        self.assertEqual(values["loaded"], 35)
        self.assertEqual(values["malformed"], 10)
        self.assertEqual(values["acceptsIntegerString"], 3)
        self.assertEqual(values["rejects"], [None, None, None, None, None])

    def test_pairwise_selection_reconciles_to_current_distinct_portfolio_etfs(
        self,
    ) -> None:
        values = self.run_module("""
import { reconcilePairwiseSelection } from './web/pairwise-overlap.js';

const positions = ['A', 'B', 'C'].map((isin) => ({ isin }));
console.log(JSON.stringify({
  initial: reconcilePairwiseSelection(positions),
  retained: reconcilePairwiseSelection(positions, ['B', 'A']),
  removed: reconcilePairwiseSelection(positions.slice(1), ['A', 'B']),
  insufficient: reconcilePairwiseSelection(positions.slice(0, 1), ['A', 'B']),
}));
""")

        self.assertEqual(values["initial"], ["A", "B"])
        self.assertEqual(values["retained"], ["B", "A"])
        self.assertEqual(values["removed"], ["B", "C"])
        self.assertEqual(values["insufficient"], [])

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

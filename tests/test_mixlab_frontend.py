from __future__ import annotations

import json
import subprocess
import unittest

from test_web_runtime import REPOSITORY_ROOT


class MixLabFrontendTests(unittest.TestCase):
    def run_module(self, script: str) -> dict:
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_exclusive_country_buckets_and_unknown_exposure(self) -> None:
        values = self.run_module("""
import { aggregateCountryExposure, countryBucketFor, normalizeCountryCode } from './web/mixlab.js';

const exposure = aggregateCountryExposure([
  { classification: { country_code: 'CH', country: 'Switzerland' }, exposure: { weight_pct: 55 } },
  { classification: { country_code: 'DE', country: 'Germany' }, exposure: { weight_pct: 25 } },
  { classification: { country_code: 'CZ', country: 'Czech Republic' }, exposure: { weight_pct: 15 } },
  { classification: { country_code: 'ZZ', country: 'Germany' }, exposure: { weight_pct: 5 } },
]);
console.log(JSON.stringify({
  exposure,
  swissBucket: countryBucketFor('CH'),
  developedBucket: countryBucketFor('DE'),
  emergingBucket: countryBucketFor('CZ'),
  koreaBucket: countryBucketFor('KR'),
  unsupportedCode: normalizeCountryCode({ country_code: 'ZZ', country: 'Germany' }),
}));
""")

        self.assertEqual(values["swissBucket"], "switzerland")
        self.assertEqual(values["developedBucket"], "developedEurope")
        self.assertEqual(values["emergingBucket"], "emergingMarkets")
        self.assertEqual(values["koreaBucket"], "emergingMarkets")
        self.assertIsNone(values["unsupportedCode"])
        self.assertEqual(values["exposure"]["buckets"]["switzerland"], 55)
        self.assertEqual(values["exposure"]["buckets"]["developedEurope"], 25)
        self.assertEqual(values["exposure"]["buckets"]["emergingMarkets"], 15)
        self.assertEqual(values["exposure"]["unclassifiedPct"], 5)
        self.assertEqual(values["exposure"]["coveragePct"], 95)

    def test_overlap_normalization_and_coverage_boundary(self) -> None:
        values = self.run_module("""
import { aggregateCountryExposure, calculateProportionalOverlap } from './web/mixlab.js';

const holding = (code, country, weight) => ({
  classification: { country_code: code, country },
  exposure: { weight_pct: weight },
});
const target = aggregateCountryExposure([
  holding('CH', 'Switzerland', 70), holding('US', 'United States', 30),
]);
const identical = aggregateCountryExposure([
  holding('CH', 'Switzerland', 70), holding('US', 'United States', 30),
]);
const different = aggregateCountryExposure([
  holding('CH', 'Switzerland', 50), holding('CA', 'Canada', 50),
]);
const atBoundary = aggregateCountryExposure([
  holding('CH', 'Switzerland', 95), holding(null, 'Unknown', 5),
]);
const belowBoundary = aggregateCountryExposure([
  holding('CH', 'Switzerland', 94), holding(null, 'Unknown', 6),
]);
const unknown = aggregateCountryExposure([
  holding(null, 'European Union', 90),
]);
console.log(JSON.stringify({
  identical: calculateProportionalOverlap(target, identical),
  different: calculateProportionalOverlap(target, different),
  atBoundary: calculateProportionalOverlap(target, atBoundary),
  belowBoundary: calculateProportionalOverlap(target, belowBoundary),
  unknown,
}));
""")

        self.assertEqual(values["identical"]["overlapPct"], 100)
        self.assertEqual(values["different"]["overlapPct"], 80)
        self.assertTrue(values["atBoundary"]["available"])
        self.assertEqual(values["atBoundary"]["candidateCoveragePct"], 95)
        self.assertFalse(values["belowBoundary"]["available"])
        self.assertIsNone(values["belowBoundary"]["overlapPct"])
        self.assertEqual(values["unknown"]["unclassifiedPct"], 100)

    def test_consolidation_search_is_deterministic_and_uses_company_identity(
        self,
    ) -> None:
        values = self.run_module("""
import { prepareMixLabFund, searchConsolidation } from './web/mixlab.js';

const holding = (code, companyId, weight) => ({
  security: { company_id: companyId },
  classification: { country_code: code },
  exposure: { weight_pct: weight },
});
const fund = (isin, terPct, holdings) => prepareMixLabFund({
  isin,
  ticker: isin,
  terPct,
  terSource: 'constructed test data',
  distributionPolicy: 'accumulating',
  investmentUniverse: 'all_country_world',
}, { snapshot: { as_of: '2026-10-20' }, holdings });
const swiss = fund('A', 0.1, [holding('CH', 'swiss-company', 100)]);
const northAmerica = fund('B', 0.2, [holding('US', 'north-american-company', 100)]);
const exactMix = fund('C', 0.15, [
  holding('CH', 'swiss-company', 50),
  holding('US', 'north-american-company', 50),
]);
const missingFee = prepareMixLabFund({
  isin: 'D', ticker: 'D', terPct: null, distributionPolicy: 'accumulating',
  investmentUniverse: 'all_country_world',
}, { holdings: [holding('CH', 'swiss-company', 100)] });
const options = {
  funds: [swiss, northAmerica, exactMix, missingFee],
  target: exactMix.exposure,
  overlapThresholdPct: 100,
  allocationStepPct: 50,
  portfolioValueChf: 10000,
};
const first = searchConsolidation(options);
const second = searchConsolidation(options);
const withoutValue = searchConsolidation({ ...options, portfolioValueChf: null });
console.log(JSON.stringify({ first, second, costWithoutValue: withoutValue.results[0].annualTerCostChf }));
""")

        first = values["first"]
        result = first["results"][0]
        self.assertEqual(first["eligibleFundCount"], 3)
        self.assertEqual(
            result["allocations"], [{"isin": "C", "ticker": "C", "weightPct": 100}]
        )
        self.assertEqual(result["fundCount"], 1)
        self.assertEqual(result["weightedTerPct"], 0.15)
        self.assertEqual(result["effectiveCompanies"], 2)
        self.assertEqual(result["overlapPct"], 100)
        self.assertEqual(result["annualTerCostChf"], 15)
        self.assertEqual(values["second"]["results"][0], result)
        self.assertIsNone(values["costWithoutValue"])

    def test_custom_sleeves_validate_totals_and_keep_lookthrough_separate(self) -> None:
        values = self.run_module("""
import { prepareMixLabFund, searchCustomSleeves } from './web/mixlab.js';

const holding = (code, companyId, weight) => ({
  security: { company_id: companyId },
  classification: { country_code: code },
  exposure: { weight_pct: weight },
});
const fund = (isin, investmentUniverse, holdings) => prepareMixLabFund({
  isin,
  ticker: isin,
  terPct: 0.1,
  terSource: 'constructed test data',
  distributionPolicy: 'accumulating',
  investmentUniverse,
}, { holdings });
const developedWorld = fund('W', 'developed_world', [
  holding('CH', 'swiss-company', 40), holding('US', 'us-company', 60),
]);
const switzerland = fund('S', 'switzerland', [holding('CH', 'swiss-company', 100)]);
const funds = [developedWorld, switzerland];
const valid = searchCustomSleeves({
  funds,
  sleeveAllocations: { developed_world: 70, switzerland: 30 },
});
const invalid = searchCustomSleeves({
  funds,
  sleeveAllocations: { developed_world: 60, switzerland: 30 },
});
const missing = searchCustomSleeves({
  funds,
  sleeveAllocations: { all_country_world: 100 },
});
console.log(JSON.stringify({ valid, invalid, missing }));
""")

        self.assertTrue(values["valid"]["valid"])
        self.assertEqual(
            values["valid"]["results"][0]["sleeveAllocations"],
            {
                "developed_world": 70,
                "switzerland": 30,
            },
        )
        self.assertEqual(
            values["valid"]["results"][0]["exposure"]["buckets"]["switzerland"], 58
        )
        self.assertFalse(values["invalid"]["valid"])
        self.assertIn(
            "sleeve_total_must_equal_100", values["invalid"]["validationErrors"]
        )
        self.assertEqual(values["missing"]["missingSleeves"], ["all_country_world"])

    def test_distribution_and_independent_limits_report_closest_alternatives(
        self,
    ) -> None:
        values = self.run_module("""
import { prepareMixLabFund, searchConsolidation, searchCustomSleeves } from './web/mixlab.js';

const holding = (companyId, weight) => ({
  security: { company_id: companyId },
  classification: { country_code: 'CH' },
  exposure: { weight_pct: weight },
});
const fund = (isin, terPct, distributionPolicy, holdings) => prepareMixLabFund({
  isin,
  ticker: isin,
  terPct,
  terSource: 'constructed test data',
  distributionPolicy,
  investmentUniverse: 'all_country_world',
}, { holdings });
const accumulating = fund('A', 0.1, 'accumulating', [holding('one-company', 100)]);
const distributing = fund('B', 0.2, 'distributing', [
  holding('company-one', 25), holding('company-two', 25),
  holding('company-three', 25), holding('company-four', 25),
]);
const funds = [accumulating, distributing];
const options = { funds, target: accumulating.exposure, overlapThresholdPct: 100 };
const filtered = searchConsolidation({ ...options, distributionPolicyFilter: 'accumulating' });
const terBound = searchConsolidation({
  ...options, maximumTerEnabled: true, maximumTerPct: 0.15,
});
const breadthBound = searchConsolidation({
  ...options, minimumEffectiveCompaniesEnabled: true, minimumEffectiveCompanies: 2,
});
const noneQualify = searchConsolidation({
  ...options,
  maximumTerEnabled: true,
  maximumTerPct: 0.05,
  minimumEffectiveCompaniesEnabled: true,
  minimumEffectiveCompanies: 5,
});
const customFiltered = searchCustomSleeves({
  funds,
  sleeveAllocations: { all_country_world: 100 },
  distributionPolicyFilter: 'distributing',
});
const customLimited = searchCustomSleeves({
  funds,
  sleeveAllocations: { all_country_world: 100 },
  minimumEffectiveCompaniesEnabled: true,
  minimumEffectiveCompanies: 5,
});
console.log(JSON.stringify({ filtered, terBound, breadthBound, noneQualify, customFiltered, customLimited }));
""")

        self.assertEqual(values["filtered"]["filteredByDistributionCount"], 1)
        self.assertEqual(
            values["filtered"]["results"][0]["allocations"][0]["ticker"], "A"
        )
        self.assertEqual(
            values["terBound"]["results"][0]["allocations"][0]["ticker"], "A"
        )
        breadth_result = values["breadthBound"]["results"][0]
        self.assertGreaterEqual(breadth_result["effectiveCompanies"], 2)
        self.assertTrue(breadth_result["constraintStatus"]["minimumEffectiveCompanies"])
        self.assertEqual(values["noneQualify"]["results"], [])
        self.assertTrue(values["noneQualify"]["closestAlternatives"])
        alternatives = values["noneQualify"]["closestAlternatives"]
        self.assertIn("maximumTer", alternatives[0]["failedConstraints"])
        self.assertTrue(
            any(
                "minimumEffectiveCompanies" in alternative["failedConstraints"]
                for alternative in alternatives
            )
        )
        self.assertEqual(
            values["customFiltered"]["results"][0]["allocations"][0]["ticker"],
            "B",
        )
        self.assertEqual(values["customLimited"]["results"], [])
        self.assertTrue(values["customLimited"]["closestAlternatives"])
        self.assertIn(
            "minimumEffectiveCompanies",
            values["customLimited"]["closestAlternatives"][0]["failedConstraints"],
        )

    def test_consolidation_search_adapts_to_candidate_count_budget(self) -> None:
        values = self.run_module("""
import { prepareMixLabFund, searchConsolidation } from './web/mixlab.js';

const funds = Array.from({ length: 10 }, (_, index) => prepareMixLabFund({
  isin: `I${index}`,
  ticker: `T${index}`,
  terPct: 0.1,
  terSource: 'constructed test data',
  distributionPolicy: 'accumulating',
  investmentUniverse: 'all_country_world',
}, {
  holdings: [{
    security: { company_id: 'shared-company' },
    classification: { country_code: 'CH' },
    exposure: { weight_pct: 100 },
  }],
}));
const result = searchConsolidation({ funds, target: funds[0].exposure });
console.log(JSON.stringify({
  allocationStepPct: result.allocationStepPct,
  evaluatedMixCount: result.evaluatedMixCount,
}));
""")

        self.assertEqual(values["allocationStepPct"], 10)
        self.assertLessEqual(values["evaluatedMixCount"], 500_000)


if __name__ == "__main__":
    unittest.main()

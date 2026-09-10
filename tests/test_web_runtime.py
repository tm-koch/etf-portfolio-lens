import json
import subprocess
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class WebRuntimeTests(unittest.TestCase):
    def test_share_links_preserve_compatibility_and_private_payload_boundaries(
        self,
    ) -> None:
        script = """
import { decodePortfolioShare, encodePortfolioShare, encodePrivatePortfolioShare } from './web/share.js';

const encodePayload = (payload) => Buffer.from(JSON.stringify(payload)).toString('base64url');
const legacy = decodePortfolioShare(encodePayload({
  version: 1,
  portfolio: [{ isin: 'ch0237935652', shares: 2 }],
}));
const current = decodePortfolioShare(encodePortfolioShare([{
  isin: 'IE00B44Z5B48',
  shares: 1,
  valuationMode: 'latest',
  price: 265.35,
  currency: 'CHF',
  value: 265.35,
  valueChf: 265.35,
}]));
const privateToken = encodePrivatePortfolioShare(
  [{ isin: 'CH0237935652', shares: 2 }, { isin: 'IE00B44Z5B48', shares: 1 }],
  (positions) => positions.reduce((sum, position) => sum + position.shares, 0),
  (position, total) => (position.shares / total) * 100,
);
const privatePayload = JSON.parse(Buffer.from(privateToken, 'base64url').toString('utf8'));
console.log(JSON.stringify({ legacy, current, privatePayload, decodedPrivate: decodePortfolioShare(privateToken) }));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(
            values["legacy"],
            {
                "status": "valid",
                "mode": "full",
                "portfolio": [{"isin": "CH0237935652", "shares": 2}],
            },
        )
        self.assertEqual(values["current"]["status"], "valid")
        self.assertEqual(values["current"]["portfolio"][0]["valuationMode"], "latest")
        self.assertEqual(values["privatePayload"]["version"], 2)
        self.assertEqual(values["privatePayload"]["mode"], "percentage")
        self.assertEqual(
            set(values["privatePayload"]["portfolio"][0]),
            {"isin", "shares"},
        )
        private_shares = [
            position["shares"] for position in values["decodedPrivate"]["portfolio"]
        ]
        self.assertAlmostEqual(private_shares[0], 200 / 3)
        self.assertAlmostEqual(private_shares[1], 100 / 3)

    def test_effective_valuation_covers_live_fallback_and_unavailable_states(
        self,
    ) -> None:
        script = """
import { getEffectiveValuation } from './web/valuation.js';

const livePrices = {
  schema_version: 1,
  generated_at: '2026-08-29T21:00:00Z',
  quotes: {
    CHF_ETF: { price: 101.25, currency: 'CHF', status: 'available', quoted_at: '2026-08-29T17:00:00Z' },
    EUR_ETF: { price: 50, currency: 'EUR', status: 'available', quoted_at: '2026-08-29T17:00:00Z' },
  },
  fx: { 'EUR/CHF': { rate: 0.96, status: 'available', quoted_at: '2026-08-29' } },
};

const cases = [
  getEffectiveValuation({ isin: 'CHF_ETF', shares: 2 }, livePrices),
  getEffectiveValuation({ isin: 'EUR_ETF', shares: 3 }, livePrices),
  getEffectiveValuation({ isin: 'CHF_ETF', shares: 2, price: 90, valueChf: 180, valuationMode: 'imported' }, livePrices),
  getEffectiveValuation({ isin: 'EUR_ETF', shares: 3, valueChf: 140 }, { ...livePrices, fx: {} }),
  getEffectiveValuation({ isin: 'MISSING', shares: 1 }, livePrices),
];
console.log(JSON.stringify(cases));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)
        self.assertEqual(
            [value["status"] for value in values],
            ["live", "live", "fallback", "fallback", "unavailable"],
        )
        self.assertAlmostEqual(values[0]["valueChf"], 202.5)
        self.assertAlmostEqual(values[1]["valueChf"], 144)
        self.assertEqual(values[2]["valueChf"], 180)
        self.assertEqual(values[3]["valueChf"], 140)


if __name__ == "__main__":
    unittest.main()

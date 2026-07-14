from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from etf_ingestion_backend.pipeline import IngestionPipeline
from etf_ingestion_backend.normalization import normalize_row
from etf_ingestion_backend.parsing import parse_xlsx_bytes
from etf_ingestion_backend.registry import load_registry
from etf_ingestion_backend.security_master import SecurityMaster, SecurityRecord

ROOT = Path(__file__).resolve().parents[1]


class IngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT / "data" / "etf_registry.json")
        cls.security_master = SecurityMaster.from_csv(ROOT / "data" / "tickers.csv")

    def test_registry_has_five_supported_sources(self) -> None:
        self.assertEqual(5, len(self.registry.entries))

    def test_fixtures_generate_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry, self.security_master, Path(temp_dir)
            )
            results = pipeline.run(self.registry.entries, use_fixtures=True)

            self.assertEqual(5, len(results))
            for result in results:
                self.assertTrue(result.snapshot_path.exists())
                snapshot = json.loads(result.snapshot_path.read_text(encoding="utf-8"))
                self.assertEqual(result.etf.isin, snapshot["etf"]["isin"])
                self.assertEqual(
                    str(result.raw_download_path),
                    snapshot["snapshot"]["resolved_download_url"],
                )
                self.assertIn("holdings", snapshot)
                self.assertIn("aggregates", snapshot)
                self.assertTrue((result.output_dir / "downloads").exists())

    def test_match_diagnostics_and_ticker_isin_fallback_are_in_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry, self.security_master, Path(temp_dir)
            )
            selected = self.registry.select_by_isins(["CH0237935652"])
            results = pipeline.run(selected, use_fixtures=True)

            snapshot = json.loads(results[0].snapshot_path.read_text(encoding="utf-8"))
            novn = next(
                holding
                for holding in snapshot["holdings"]
                if holding["security"]["ticker"] == "NOVN"
            )

            self.assertEqual("CH0012005267", novn["security"]["isin"])
            self.assertEqual("NOVARTIS AG", novn["security"]["name"])
            self.assertEqual("matched", novn["provenance"]["match"]["status"])
            self.assertEqual("ticker", novn["provenance"]["match"]["matched_by"])
            self.assertIn("isin", novn["provenance"]["match"]["missing_elements"])
            self.assertEqual(
                ["ticker+exchange", "ticker"], novn["provenance"]["match"]["attempted"]
            )

            sector_weights = snapshot["aggregates"]["sector_weights"]
            currency_weights = snapshot["aggregates"]["currency_weights"]
            self.assertGreater(max(item["weight_pct"] for item in sector_weights), 0.0)
            self.assertGreater(
                max(item["weight_pct"] for item in currency_weights), 0.0
            )

    def test_unresolved_holdings_keep_source_name_in_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry, self.security_master, Path(temp_dir)
            )
            selected = self.registry.select_by_isins(["CH0130595124"])
            results = pipeline.run(selected, use_fixtures=True)

            snapshot = json.loads(results[0].snapshot_path.read_text(encoding="utf-8"))
            smg = next(
                holding
                for holding in snapshot["holdings"]
                if holding["security"]["isin"] == "CH1484953687"
            )

            self.assertEqual(
                smg["provenance"]["source_fields"]["Securities"],
                smg["security"]["name"],
            )
            self.assertEqual("unmatched", smg["provenance"]["match"]["status"])
            forbidden_labels = {
                "This overview shows the portfolio positions. The actual positions of the ETF may deviate from this.",
                "Source: UBS AG, 07.07.2026",
            }
            self.assertFalse(
                any(
                    holding["provenance"]["source_fields"]["Securities"]
                    in forbidden_labels
                    for holding in snapshot["holdings"]
                )
            )

    def test_xlsx_parser_stops_at_first_empty_row(self) -> None:
        data = Path("data/example/UBSFunds_Constituents_1783782798132.xls").read_bytes()

        parsed = parse_xlsx_bytes(data, stop_at_empty_row=True)

        self.assertEqual("Securities", parsed.headers[0])
        self.assertEqual("SMG SWISS MARKETPLACE GROUP", parsed.rows[-1]["Securities"])
        self.assertEqual("CH1484953687", parsed.rows[-1]["ISIN"])
        self.assertFalse(
            any(
                row.get("Securities")
                == "This overview shows the portfolio positions. The actual positions of the ETF may deviate from this."
                for row in parsed.rows
            )
        )

    def test_ambiguous_ticker_only_match_warns_and_stays_unresolved(self) -> None:
        master = SecurityMaster(
            records=[
                SecurityRecord(
                    ticker="DUP",
                    name="Duplicate One",
                    exchange="EX1",
                    sector="Financials",
                    asset_type="Stock",
                    country="Country A",
                    country_code="AA",
                    isin="AA1111111111",
                    aliases=[],
                ),
                SecurityRecord(
                    ticker="DUP",
                    name="Duplicate Two",
                    exchange="EX2",
                    sector="Financials",
                    asset_type="Stock",
                    country="Country B",
                    country_code="BB",
                    isin="BB2222222222",
                    aliases=[],
                ),
            ],
            version="test",
            warnings=[],
        )
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer):
            holding = normalize_row(
                {"Ticker": "DUP", "Name": "Duplicate Holding"},
                master,
                "test",
                "ssga_xlsx_v1",
            )

        self.assertIsNone(holding.isin)
        self.assertEqual("ambiguous", holding.match.status)
        self.assertEqual("ticker", holding.match.matched_by)
        self.assertIn("isin", holding.match.missing_elements)
        self.assertIn("ambiguous ticker match", buffer.getvalue())

    def test_normalize_row_preserves_percent_based_parser_weight(self) -> None:
        holding = normalize_row(
            {
                "ISIN code": "US0378331005",
                "Name": "Apple Inc.",
                "Asset class": "EQUITY",
                "Currency": "USD",
                "Weight (%)": "4.591172",
                "Sector": "Information Technology",
                "Country": "United States",
            },
            self.security_master,
            "test",
            "ssga_xlsx_v1",
        )

        self.assertAlmostEqual(4.591172, holding.weight_pct or 0.0, places=6)

    def test_normalize_row_converts_fractional_weight_to_percent(self) -> None:
        holding = normalize_row(
            {
                "ISIN code": "NL0010273215",
                "Name": "ASML HOLDING NV",
                "Asset class": "EQUITY",
                "Currency": "EUR",
                "Weight": "0.2517",
                "Sector": "Information Technology",
                "Country": "Netherlands",
            },
            self.security_master,
            "test",
            "amundi_landing_xlsx_v1",
        )

        self.assertAlmostEqual(25.17, holding.weight_pct or 0.0, places=2)

    def test_aggregate_holdings_rejects_totals_over_100_percent(self) -> None:
        holding = normalize_row(
            {
                "ISIN code": "NL0010273215",
                "Name": "ASML HOLDING NV",
                "Asset class": "EQUITY",
                "Currency": "EUR",
                "Weight": "0.2517",
                "Sector": "Information Technology",
                "Country": "Netherlands",
            },
            self.security_master,
            "test",
            "amundi_landing_xlsx_v1",
        )
        holding.weight_pct = 101.0

        with self.assertRaisesRegex(ValueError, "holding weights sum"):
            from etf_ingestion_backend.aggregation import aggregate_holdings

            aggregate_holdings([holding])


if __name__ == "__main__":
    unittest.main()

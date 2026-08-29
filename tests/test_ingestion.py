from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError
from email.message import Message
from unittest.mock import patch

from etf_ingestion_backend.fetching import (
    AmundiHoldingsError,
    DownloadError,
    DownloadedSource,
    fetch_amundi_full_holdings,
    fetch_url,
)
from etf_ingestion_backend.pipeline import IngestionPipeline
from etf_ingestion_backend.normalization import normalize_row, parse_weight_float
from etf_ingestion_backend.parsing import parse_xlsx_bytes, parse_xlsx_file
from etf_ingestion_backend.registry import load_registry
from etf_ingestion_backend.sector_taxonomy import normalize_sector_label
from etf_ingestion_backend.security_master import SecurityMaster, SecurityRecord
from etf_ingestion_backend.overrides import OverrideRegistry

ROOT = Path(__file__).resolve().parents[1]


class FakeHttpResponse:
    def __init__(self, payload: bytes, content_type: str = "application/json") -> None:
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        self.payload = payload

    def __enter__(self) -> "FakeHttpResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


class IngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT / "data" / "etf_registry.json")
        cls.security_master_fixture = tempfile.TemporaryDirectory()
        fixture_path = Path(cls.security_master_fixture.name) / "tickers.csv"
        fixture_path.write_text(
            "\n".join(
                [
                    "ticker,name,exchange,stock_sector,asset_type,country,country_code,isin,aliases",
                    "NOVN,NOVARTIS AG,Other Exchange,Health Care,Stock,Switzerland,CH,CH0012005267,",
                    "SMG,SMG AG,SIX Swiss Exchange,Communication Services,Stock,Switzerland,CH,US8101861065,",
                    "KPN,KONINKLIJKE KPN NV,Euronext Amsterdam,Communication Services,Stock,Netherlands,NL,NL0000000001,",
                ]
            ),
            encoding="utf-8",
        )
        cls.security_master_source_url = fixture_path.as_uri()
        cls.security_master = SecurityMaster.from_csv(fixture_path)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.security_master_fixture.cleanup()

    def test_registry_has_five_supported_sources(self) -> None:
        self.assertEqual(7, len(self.registry.entries))

    def test_registry_contains_ubs_spi_extra_metadata(self) -> None:
        entry = self.registry.select_by_isins(["CH1553162921"])[0]

        self.assertEqual("SPIEXT", entry.ticker)
        self.assertEqual("UBS SPI® Extra ETF", entry.name)
        self.assertEqual("UBS", entry.provider)
        self.assertEqual(
            "https://www.ubs.com/ch/en/assetmanagement/funds/etf/"
            "ch1553162921-ubs-spi-extra-etf-pd001.html",
            entry.source_url,
        )
        self.assertEqual("xls", entry.expected_format)
        self.assertEqual("ubs_xml_xls_v1", entry.parser_id)
        self.assertEqual(
            "data/example/UBSFunds_Constituents_1786975364611.xls",
            entry.fixture_path,
        )

    def test_ubs_spi_extra_fixture_preserves_complete_holdings(self) -> None:
        path = ROOT / "data" / "example" / "UBSFunds_Constituents_1786975364611.xls"

        parsed = parse_xlsx_bytes(path.read_bytes(), stop_at_empty_row=True)
        weights = [float(row["Weight %"]) for row in parsed.rows]

        self.assertEqual(179, len(parsed.rows))
        self.assertEqual("Securities", parsed.headers[0])
        self.assertEqual("VILLARS HOLDING AG-REG", parsed.rows[-1]["Securities"])
        self.assertEqual("0", parsed.rows[-1]["Weight %"])
        self.assertAlmostEqual(99.21987, sum(weights), places=5)
        self.assertFalse(
            any("Quelle: UBS AG" in row.get("Securities", "") for row in parsed.rows)
        )

    def test_ubs_spi_extra_snapshot_uses_registry_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry,
                Path(temp_dir),
                self.security_master_source_url,
            )
            selected = self.registry.select_by_isins(["CH1553162921"])
            results = pipeline.run(selected, use_fixtures=True)

            snapshot = json.loads(results[0].snapshot_path.read_text(encoding="utf-8"))

            self.assertEqual("CH1553162921", snapshot["etf"]["isin"])
            self.assertEqual("SPIEXT", snapshot["etf"]["ticker"])
            self.assertEqual("UBS SPI® Extra ETF", snapshot["etf"]["name"])
            self.assertEqual("ubs_xml_xls_v1", snapshot["snapshot"]["parser_id"])
            self.assertEqual(179, snapshot["aggregates"]["counts"]["holdings"])
            self.assertFalse(
                any(
                    "Quelle: UBS AG" in holding["security"].get("name", "")
                    for holding in snapshot["holdings"]
                )
            )

    def test_fixtures_generate_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry,
                Path(temp_dir),
                self.security_master_source_url,
            )
            results = pipeline.run(self.registry.entries, use_fixtures=True)

            self.assertEqual(7, len(results))
            for result in results:
                self.assertTrue(result.snapshot_path.exists())
                snapshot = json.loads(result.snapshot_path.read_text(encoding="utf-8"))
                self.assertEqual(result.etf.isin, snapshot["etf"]["isin"])
                self.assertEqual(
                    str(result.raw_download_path),
                    snapshot["snapshot"]["resolved_download_url"],
                )
                self.assertEqual(
                    self.security_master_source_url,
                    snapshot["provenance"]["security_master_source_url"],
                )
                self.assertTrue(
                    Path(
                        snapshot["provenance"]["security_master_download_path"]
                    ).exists()
                )
                self.assertIn("holdings", snapshot)
                self.assertIn("aggregates", snapshot)
                self.assertTrue((result.output_dir / "downloads").exists())

    def test_match_diagnostics_and_ticker_isin_fallback_are_in_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry,
                Path(temp_dir),
                self.security_master_source_url,
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
                self.registry,
                Path(temp_dir),
                self.security_master_source_url,
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

    def test_eumd_registry_entry_ingests_successfully(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry,
                Path(temp_dir),
                self.security_master_source_url,
            )
            selected = self.registry.select_by_isins(["IE00BF20LF40"])
            results = pipeline.run(selected, use_fixtures=True)

            self.assertEqual(1, len(results))
            snapshot = json.loads(results[0].snapshot_path.read_text(encoding="utf-8"))
            self.assertEqual("IE00BF20LF40", snapshot["etf"]["isin"])
            self.assertEqual("EUMD", snapshot["etf"]["ticker"])
            self.assertGreater(len(snapshot["holdings"]), 10)

    def test_eumd_registry_uses_direct_full_holdings_csv(self) -> None:
        entry = self.registry.select_by_isins(["IE00BF20LF40"])[0]

        self.assertIn("/fund/1495092304805.ajax", entry.source_url)
        self.assertIn("fileType=csv", entry.source_url)
        self.assertIn("fileName=EUMD_holdings", entry.source_url)
        self.assertIn("dataType=fund", entry.source_url)

    def test_fetch_url_resolves_query_parameter_csv_link(self) -> None:
        html = (
            b'<a href="/fund/1495092304805.ajax?fileType=csv&'
            b'fileName=EUMD_holdings&dataType=fund">Holdings</a>'
        )
        csv_data = b"Fund Holdings as of,19/Aug/2026\nTicker,Name\nABC,Example\n"
        responses = [
            FakeHttpResponse(html, "text/html"),
            FakeHttpResponse(csv_data, "text/csv"),
        ]

        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "etf_ingestion_backend.fetching.urllib.request.urlopen",
            side_effect=responses,
        ) as urlopen:
            downloaded = fetch_url(
                "https://www.ishares.com/ch/products/287746/holdings",
                Path(temp_dir),
            )

        self.assertEqual(".csv", downloaded.download_path.suffix)
        self.assertEqual(2, urlopen.call_count)
        self.assertIn("fileType=csv", urlopen.call_args.args[0].full_url)

    def test_fetch_url_rejects_html_without_download_link(self) -> None:
        response = FakeHttpResponse(b"<html>product page</html>", "text/html")

        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "etf_ingestion_backend.fetching.urllib.request.urlopen",
            return_value=response,
        ):
            with self.assertRaisesRegex(DownloadError, "returned HTML"):
                fetch_url("https://example.test/product", Path(temp_dir))

    def test_eumd_rejects_top_ten_response_before_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "EUMD_holdings.csv"
            rows = ["Ticker,Name,Weight (%)"] + [
                f"TICK{i},Holding {i},1" for i in range(10)
            ]
            source_path.write_text("\n".join(rows), encoding="utf-8")
            security_master_download = Path(self.security_master_source_url[8:])
            downloaded = DownloadedSource(
                source_path=source_path,
                download_path=source_path,
                content_type="text/csv",
            )
            security_master_source = DownloadedSource(
                source_path=security_master_download,
                download_path=security_master_download,
                content_type="text/csv",
            )
            pipeline = IngestionPipeline(
                self.registry,
                Path(temp_dir) / "output",
                self.security_master_source_url,
            )

            with patch(
                "etf_ingestion_backend.pipeline.fetch_url",
                side_effect=[security_master_source, downloaded],
            ):
                with self.assertRaisesRegex(ValueError, "Incomplete EUMD holdings"):
                    pipeline.run(self.registry.select_by_isins(["IE00BF20LF40"]))

            self.assertFalse(
                (
                    Path(temp_dir)
                    / "output"
                    / "2026-08-19"
                    / "snapshots"
                    / "IE00BF20LF40.json"
                ).exists()
            )

    def test_latest_amundi_fixture_has_complete_fractional_holdings(self) -> None:
        path = (
            ROOT
            / "data"
            / "example"
            / (
                "Fund Holdings_Amundi Core Stoxx Europe 600 UCITS ETF Acc_"
                "LU0908500753_12_08_2026.xlsx"
            )
        )
        parsed = parse_xlsx_file(path)
        weights = [
            parse_weight_float(row.get("Weight"), "amundi_landing_xlsx_v1")
            for row in parsed.rows
        ]
        values = [weight for weight in weights if weight is not None]

        self.assertEqual(619, len(parsed.rows))
        self.assertAlmostEqual(100.0, sum(values), places=4)
        self.assertLess(max(values), 10.0)

    def test_amundi_fetcher_maps_complete_composition(self) -> None:
        payload = {
            "products": [
                {
                    "productId": "LU0908500753",
                    "composition": {
                        "totalNumberOfInstruments": 11,
                        "compositionData": [
                            {
                                "compositionCharacteristics": {
                                    "isin": f"ISIN{i:010d}",
                                    "name": f"Holding {i}",
                                    "type": "EQUITY_ORDINARY",
                                    "currency": "EUR",
                                    "weight": 1 / 11,
                                    "sector": "Financials",
                                    "countryOfRisk": "France",
                                }
                            }
                            for i in range(11)
                        ],
                    },
                }
            ]
        }
        response = FakeHttpResponse(json.dumps(payload).encode("utf-8"))
        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "etf_ingestion_backend.fetching.urllib.request.urlopen",
            return_value=response,
        ) as urlopen:
            downloaded, rows = fetch_amundi_full_holdings(
                "LU0908500753", Path(temp_dir)
            )
            self.assertTrue(downloaded.download_path.exists())

        request = urlopen.call_args.args[0]
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual("POST", request.method)
        self.assertEqual(["LU0908500753"], body["productIds"])
        self.assertEqual("CHE", body["context"]["countryCode"])
        self.assertEqual(11, len(rows))
        self.assertEqual("ISIN0000000000", rows[0]["ISIN code"])
        self.assertEqual("json-api", downloaded.source_format)

    def test_amundi_fetcher_rejects_top_ten_composition(self) -> None:
        payload = {
            "products": [
                {
                    "productId": "LU0908500753",
                    "composition": {
                        "totalNumberOfInstruments": 10,
                        "compositionData": [],
                    },
                }
            ]
        }
        response = FakeHttpResponse(json.dumps(payload).encode("utf-8"))
        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "etf_ingestion_backend.fetching.urllib.request.urlopen",
            return_value=response,
        ):
            with self.assertRaisesRegex(AmundiHoldingsError, "incomplete"):
                fetch_amundi_full_holdings("LU0908500753", Path(temp_dir))

    def test_amundi_fetcher_rejects_html_response(self) -> None:
        response = FakeHttpResponse(b"<html>product page</html>", "text/html")
        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "etf_ingestion_backend.fetching.urllib.request.urlopen",
            return_value=response,
        ):
            with self.assertRaisesRegex(AmundiHoldingsError, "not JSON"):
                fetch_amundi_full_holdings("LU0908500753", Path(temp_dir))

    def test_amundi_fetcher_rejects_missing_composition_fields(self) -> None:
        payload = {"products": [{"productId": "LU0908500753"}]}
        response = FakeHttpResponse(json.dumps(payload).encode("utf-8"))
        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "etf_ingestion_backend.fetching.urllib.request.urlopen",
            return_value=response,
        ):
            with self.assertRaisesRegex(AmundiHoldingsError, "no complete composition"):
                fetch_amundi_full_holdings("LU0908500753", Path(temp_dir))

    def test_sector_normalization_maps_communication_and_preserves_raw_source(
        self,
    ) -> None:
        master = SecurityMaster(
            records=[
                SecurityRecord(
                    ticker="KPN",
                    name="KONINKLIJKE KPN NV",
                    exchange="Euronext Amsterdam",
                    sector="Communication Services",
                    asset_type="Stock",
                    country="Netherlands",
                    country_code="NL",
                    isin="NL0000000001",
                    aliases=[],
                )
            ],
            version="test",
            warnings=[],
        )

        holding = normalize_row(
            {
                "Ticker": "KPN",
                "Name": "KONINKLIJKE KPN NV",
                "Sektor": "Communication",
                "Exchange": "Euronext Amsterdam",
                "Location": "Netherlands",
            },
            master,
            "test",
            "ishares_csv_v1",
        )

        self.assertEqual("Communication Services", holding.sector)
        self.assertEqual("Communication", holding.source_fields["Sektor"])
        self.assertEqual(
            "Communication Services",
            normalize_sector_label("communication services"),
        )

    def test_exchange_alias_and_override_resolve_roche(self) -> None:
        master = SecurityMaster(
            records=[
                SecurityRecord(
                    ticker="RO",
                    name="Roche Holding AG",
                    exchange="SIX",
                    sector="Health Care",
                    asset_type="Stock",
                    country="Switzerland",
                    country_code="CH",
                    isin="CH0012032113",
                    aliases=[],
                )
            ],
            version="test",
            warnings=[],
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            override_path = Path(temp_dir) / "overrides.json"
            override_path.write_text(
                json.dumps(
                    {
                        "overrides": [
                            {
                                "match": {
                                    "ticker": "ROP",
                                    "exchange": "SIX",
                                    "holding_name": "ROCHE PS PAR AG",
                                },
                                "set": {
                                    "isin": "CH0012032113",
                                    "company_id": "roche-holding",
                                    "canonical_name": "Roche Holding AG",
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            holding = normalize_row(
                {
                    "Ticker": "ROP",
                    "Name": "ROCHE PS PAR AG",
                    "Exchange": "SIX Swiss Exchange",
                    "Location": "Switzerland",
                },
                master,
                "test",
                "ishares_csv_v1",
                overrides=OverrideRegistry.from_json(override_path),
            )

        self.assertEqual("SIX", holding.exchange_code)
        self.assertEqual("CH0012032113", holding.isin)
        self.assertEqual("roche-holding", holding.company_id)
        self.assertEqual("Roche Holding AG", holding.name)
        self.assertEqual("overridden", holding.match.status)

    def test_strict_mode_rejects_unresolved_holdings_without_partial_snapshot(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry,
                Path(temp_dir),
                self.security_master_source_url,
            )
            with self.assertRaisesRegex(
                ValueError, "Strict identity validation failed"
            ):
                pipeline.run(
                    self.registry.select_by_isins(["IE00B44Z5B48"]),
                    use_fixtures=True,
                    strict=True,
                )
            snapshots = list(Path(temp_dir).rglob("snapshots/*.json"))
            self.assertEqual([], snapshots)

    def test_sector_normalization_maps_cash_style_aliases_to_unknown(self) -> None:
        master = SecurityMaster(
            records=[
                SecurityRecord(
                    ticker="CASH",
                    name="Cash Position",
                    exchange="Test Exchange",
                    sector="Financials",
                    asset_type="Stock",
                    country="United States",
                    country_code="US",
                    isin="US0000000001",
                    aliases=[],
                )
            ],
            version="test",
            warnings=[],
        )

        holding = normalize_row(
            {
                "Ticker": "CASH",
                "Name": "Cash Position",
                "Sector": "Cash and/or Derivatives",
                "Exchange": "Test Exchange",
                "Location": "United States",
            },
            master,
            "test",
            "ishares_csv_v1",
        )

        self.assertEqual("Unknown", holding.sector)
        self.assertEqual("Cash and/or Derivatives", holding.source_fields["Sector"])

    def test_security_master_download_failure_stops_ingestion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = IngestionPipeline(
                self.registry,
                Path(temp_dir),
                "https://127.0.0.1:9/does-not-exist.csv",
            )

            with self.assertRaises(URLError):
                pipeline.run(
                    self.registry.select_by_isins(["CH0237935652"]), use_fixtures=True
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

    def test_same_ticker_uses_exchange_to_keep_companies_distinct(self) -> None:
        master = SecurityMaster(
            records=[
                SecurityRecord(
                    "DUP",
                    "Company One",
                    "EX1",
                    "Financials",
                    "Stock",
                    "Country A",
                    "AA",
                    "AA1111111111",
                    [],
                ),
                SecurityRecord(
                    "DUP",
                    "Company Two",
                    "EX2",
                    "Financials",
                    "Stock",
                    "Country B",
                    "BB",
                    "BB2222222222",
                    [],
                ),
            ],
            version="test",
            warnings=[],
        )

        first = normalize_row(
            {"Ticker": "DUP", "Exchange": "EX1", "Name": "Company One"},
            master,
            "test",
            "ishares_csv_v1",
        )
        second = normalize_row(
            {"Ticker": "DUP", "Exchange": "EX2", "Name": "Company Two"},
            master,
            "test",
            "ishares_csv_v1",
        )

        self.assertEqual("AA1111111111", first.isin)
        self.assertEqual("BB2222222222", second.isin)
        self.assertNotEqual(first.company_id, second.company_id)

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

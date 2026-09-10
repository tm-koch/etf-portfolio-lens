from __future__ import annotations

import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from etf_ingestion_backend.live_adapters import (
    LiveFetchError,
    parse_frankfurter_rate,
    parse_swiss_trade_csv,
    parse_yahoo_chart,
)
from etf_ingestion_backend.live_cli import fetch_live_prices


class LiveAdapterTests(unittest.TestCase):
    def test_yahoo_chart_parses_eur_market_quote(self) -> None:
        payload = b'{"chart":{"result":[{"meta":{"currency":"EUR","regularMarketPrice":10.342,"regularMarketTime":1789054501}}],"error":null}}'

        quote = parse_yahoo_chart(payload, "IE00BF20LF40", "EUR", ticker="EUMD.L")

        self.assertEqual(10.342, quote.price)
        self.assertEqual("EUR", quote.currency)
        self.assertEqual("EUMD.L", quote.ticker)
        self.assertEqual("2026-09-10T15:35:01Z", quote.quoted_at)

    def test_yahoo_chart_rejects_invalid_responses(self) -> None:
        invalid_payloads = (
            '{"chart":{"error":{"description":"not found"},"result":null}}',
            '{"chart":{"error":null,"result":[{}]}}',
            '{"chart":{"error":null,"result":[{"meta":{"currency":"USD","regularMarketPrice":1,"regularMarketTime":1}}]}}',
            '{"chart":{"error":null,"result":[{"meta":{"currency":"EUR","regularMarketPrice":-1,"regularMarketTime":1}}]}}',
            '{"chart":{"error":null,"result":[{"meta":{"currency":"EUR","regularMarketPrice":1,"regularMarketTime":0}}]}}',
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(Exception):
                    parse_yahoo_chart(payload, "IE00BF20LF40", "EUR", ticker="EUMD.L")

    def test_swiss_csv_selects_latest_valid_row(self) -> None:
        payload = """Trading date;2026-09-10\nTime;Price;Volume\n09:01;101,20;10\ninvalid;bad;\n15:30:01;103.40;5\n12:00;102.00;2\n"""
        quote = parse_swiss_trade_csv(payload, "CH0008899764", "CHF")
        self.assertEqual(103.4, quote.price)
        self.assertEqual("2026-09-10T15:30:01Z", quote.quoted_at)

    def test_swiss_csv_accepts_fractional_seconds(self) -> None:
        payload = "10.09.2026\nTime;Price;Volume\n17:36:51.00;142.44;257\n"
        quote = parse_swiss_trade_csv(payload, "CH0008899764", "CHF")
        self.assertEqual(142.44, quote.price)
        self.assertEqual("2026-09-10T17:36:51Z", quote.quoted_at)

    def test_swiss_csv_rejects_empty_valid_rows(self) -> None:
        with self.assertRaises(Exception):
            parse_swiss_trade_csv(
                "Time;Price;Volume\ninvalid;bad;",
                "CH0008899764",
                "CHF",
                date(2026, 9, 10),
            )

    def test_frankfurter_preserves_reference_date(self) -> None:
        rate = parse_frankfurter_rate(
            '{"amount":1,"base":"EUR","date":"2026-09-09","rates":{"CHF":0.934}}',
            "EUR/CHF",
        )
        self.assertEqual(0.934, rate.rate)
        self.assertEqual("2026-09-09T00:00:00Z", rate.quoted_at)

    def test_fetch_failure_preserves_previous_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config = root / "config.json"
            output = root / "live_prices.json"
            config.write_text(
                '{"schema_version":1,"quotes":[{"isin":"CH0008899764","adapter_id":"swiss_csv_v1","currency":"CHF","secret_name":"QUOTE_URL"}]}',
                encoding="utf-8",
            )
            output.write_text('{"schema_version":1,"status":"old"}\n', encoding="utf-8")

            def failing_fetcher(url: str) -> bytes:
                raise OSError("secret-value-must-not-leak")

            with patch.dict(os.environ, {"QUOTE_URL": "https://secret.example/{isin}"}):
                with self.assertRaises(LiveFetchError):
                    fetch_live_prices(config, output, fetcher=failing_fetcher)
            self.assertEqual(
                '{"schema_version":1,"status":"old"}\n',
                output.read_text(encoding="utf-8"),
            )

    def test_invalid_quote_template_fails_before_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config = root / "config.json"
            output = root / "live_prices.json"
            config.write_text(
                '{"schema_version":1,"quotes":[{"isin":"CH0008899764","adapter_id":"swiss_csv_v1","currency":"CHF"}]}',
                encoding="utf-8",
            )
            output.write_text('{"schema_version":1,"status":"old"}\n', encoding="utf-8")

            with self.assertRaisesRegex(
                LiveFetchError, r"absolute HTTP\(S\).*\{isin\}"
            ):
                fetch_live_prices(config, output, quote_url_template="secret")
            self.assertEqual(
                '{"schema_version":1,"status":"old"}\n',
                output.read_text(encoding="utf-8"),
            )

    def test_each_quote_uses_its_configured_secret(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config = root / "config.json"
            output = root / "live_prices.json"
            config.write_text(
                '{"schema_version":1,"quotes":['
                '{"isin":"CH0008899764","adapter_id":"swiss_csv_v1","currency":"CHF",'
                '"quote_url_template_secret":"PROVIDER_ONE_URL"},'
                '{"isin":"CH0019852802","adapter_id":"swiss_csv_v1","currency":"CHF",'
                '"quote_url_template_secret":"PROVIDER_TWO_URL"}]}',
                encoding="utf-8",
            )
            requests: list[str] = []

            def fetcher(url: str) -> bytes:
                requests.append(url)
                if "one.example" in url:
                    return b"10.09.2026\nTime;Price;Volume\n15:30;101.20;1\n"
                if "two.example" in url:
                    return b"10.09.2026\nTime;Price;Volume\n15:31;202.40;1\n"
                if "EUR" in url:
                    return b'{"amount":1,"base":"EUR","date":"2026-09-10","rates":{"CHF":0.93}}'
                return b'{"amount":1,"base":"USD","date":"2026-09-10","rates":{"CHF":0.79}}'

            environment = {
                "PROVIDER_ONE_URL": "https://one.example/{isin}",
                "PROVIDER_TWO_URL": "https://two.example/{isin}",
            }
            with patch.dict(os.environ, environment, clear=False):
                artifact = fetch_live_prices(
                    config,
                    output,
                    fetcher=fetcher,
                    trading_date=date(2026, 9, 10),
                )

            self.assertEqual(101.2, artifact.quotes["CH0008899764"].price)
            self.assertEqual(202.4, artifact.quotes["CH0019852802"].price)
            self.assertIn("https://one.example/CH0008899764", requests)
            self.assertIn("https://two.example/CH0019852802", requests)

    def test_ticker_quote_uses_ticker_url_and_preserves_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config = root / "config.json"
            output = root / "live_prices.json"
            config.write_text(
                '{"schema_version":1,"quotes":[{"isin":"IE00BF20LF40",'
                '"ticker":"EUMD.L","adapter_id":"yahoo_chart_v1",'
                '"currency":"EUR","quote_url_template_secret":"YAHOO_URL"}]}',
                encoding="utf-8",
            )
            requests: list[str] = []

            def fetcher(url: str) -> bytes:
                requests.append(url)
                if "yahoo.example" in url:
                    return b'{"chart":{"result":[{"meta":{"currency":"EUR","regularMarketPrice":10.342,"regularMarketTime":1789054501}}],"error":null}}'
                if "from=USD" in url:
                    return b'{"amount":1,"base":"USD","date":"2026-09-10","rates":{"CHF":0.81}}'
                return b'{"amount":1,"base":"EUR","date":"2026-09-10","rates":{"CHF":0.93}}'

            with patch.dict(
                os.environ, {"YAHOO_URL": "https://yahoo.example/{ticker}"}
            ):
                artifact = fetch_live_prices(config, output, fetcher=fetcher)

            self.assertIn("https://yahoo.example/EUMD.L", requests)
            self.assertEqual("EUMD.L", artifact.quotes["IE00BF20LF40"].ticker)
            self.assertEqual(
                "EUMD.L", artifact.to_dict()["quotes"]["IE00BF20LF40"]["ticker"]
            )


if __name__ == "__main__":
    unittest.main()

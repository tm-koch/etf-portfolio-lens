from __future__ import annotations

import json
import unittest
from pathlib import Path

from etf_ingestion_backend.live_market_data import (
    FXRate,
    LiveMarketDataError,
    LivePricesArtifact,
    Quote,
    QuoteConfig,
    load_quote_config,
)


class LiveMarketDataTests(unittest.TestCase):
    timestamp = "2026-09-10T21:00:00Z"

    def test_round_trip_artifact(self) -> None:
        artifact = LivePricesArtifact(
            generated_at=self.timestamp,
            quotes={
                "CH0008899764": Quote(
                    "CH0008899764", 123.45, "CHF", self.timestamp, "available"
                )
            },
            fx={"EUR/CHF": FXRate("EUR/CHF", 0.94, self.timestamp, "available")},
        )

        restored = LivePricesArtifact.from_dict(artifact.to_dict())

        self.assertEqual(artifact.to_dict(), restored.to_dict())

    def test_rejects_unsupported_currency_and_missing_timestamp(self) -> None:
        with self.assertRaises(LiveMarketDataError):
            Quote("CH0008899764", 1, "GBP", self.timestamp, "available")
        with self.assertRaises(LiveMarketDataError):
            Quote("CH0008899764", 1, "CHF", None, "available")

    def test_rejects_public_source_fields(self) -> None:
        document = {
            "schema_version": 1,
            "generated_at": self.timestamp,
            "quotes": {
                "CH0008899764": {
                    "price": 1,
                    "currency": "CHF",
                    "quoted_at": self.timestamp,
                    "status": "available",
                    "source_url": "https://secret.example/quote",
                }
            },
            "fx": {},
        }
        with self.assertRaisesRegex(LiveMarketDataError, "source fields"):
            LivePricesArtifact.from_dict(document)

    def test_missing_data_is_allowed_only_as_unavailable(self) -> None:
        artifact = LivePricesArtifact(
            generated_at=self.timestamp,
            quotes={
                "CH0008899764": Quote("CH0008899764", None, "CHF", None, "unavailable")
            },
        )
        self.assertEqual(
            "unavailable", artifact.to_dict()["quotes"]["CH0008899764"]["status"]
        )

    def test_public_quote_configuration_has_no_urls(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config_path = root / "data" / "live_price_config.json"
        config = load_quote_config(config_path)
        self.assertEqual(
            [
                "CH0008899764",
                "CH0019852802",
                "CH0237935652",
                "CH0130595124",
                "CH1553162921",
                "CH0111762537",
                "CH1447931341",
                "IE00B44Z5B48",
                "IE00BF20LF40",
                "LU0908500753",
                "IE00BCLWRD08",
            ],
            [entry.isin for entry in config],
        )
        self.assertEqual(
            {"SWISS_QUOTE_URL_TEMPLATE", "YAHOO_QUOTE_URL_TEMPLATE"},
            {entry.secret_name for entry in config},
        )
        public_config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("quote_url_template_secret", public_config)
        self.assertEqual(
            {"SWISS_QUOTE_URL_TEMPLATE", "YAHOO_QUOTE_URL_TEMPLATE"},
            {entry["quote_url_template_secret"] for entry in public_config["quotes"]},
        )
        self.assertEqual(
            {
                "IE00BF20LF40": "EUMD.L",
                "LU0908500753": "LYP6.DE",
                "IE00BCLWRD08": "IS3H.DE",
            },
            {entry.isin: entry.ticker for entry in config if entry.ticker is not None},
        )
        self.assertNotIn("source_url", public_config)
        self.assertNotIn("url_template", public_config)

    def test_quote_config_validates_opaque_secret_reference(self) -> None:
        config = QuoteConfig(
            "CH0008899764", "swiss_csv_v1", "CHF", "QUOTE_URL_CH0008899764"
        )
        self.assertEqual("swiss_csv_v1", config.to_dict()["adapter_id"])
        with self.assertRaises(LiveMarketDataError):
            QuoteConfig("CH0008899764", "https-provider", "CHF", "QUOTE_URL")
        with self.assertRaises(LiveMarketDataError):
            QuoteConfig("CH0008899764", "yahoo_chart_v1", "EUR", "QUOTE_URL")


if __name__ == "__main__":
    unittest.main()

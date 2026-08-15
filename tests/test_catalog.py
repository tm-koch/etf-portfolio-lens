from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from etf_ingestion_backend.catalog import build_catalog, write_catalog
from etf_ingestion_backend.cli import build_parser
from etf_ingestion_backend.models import ETFSourceEntry, IngestionResult


def make_entry(isin: str, ticker: str) -> ETFSourceEntry:
    return ETFSourceEntry(
        isin=isin,
        ticker=ticker,
        name=f"Fund {ticker}",
        provider="Test",
        source_url="https://example.test/fund",
        expected_format="xlsx",
        parser_id="test_parser",
    )


def make_result(entry: ETFSourceEntry, output_dir: Path) -> IngestionResult:
    return IngestionResult(
        etf=entry,
        output_dir=output_dir,
        snapshot_path=output_dir / "snapshots" / f"{entry.isin}.json",
        raw_download_path=None,
        snapshot=None,
    )


class CatalogTests(unittest.TestCase):
    def test_build_catalog_preserves_entry_order_and_snapshot_date(self) -> None:
        first = make_entry("FIRST", "ONE")
        second = make_entry("SECOND", "TWO")
        output_dir = Path("data/raw/2026-08-16")

        catalog = build_catalog(
            [first, second],
            [make_result(first, output_dir), make_result(second, output_dir)],
        )

        self.assertEqual("2026-08-16", catalog["generatedAt"])
        self.assertEqual("share_weighted", catalog["basis"])
        self.assertEqual(
            ["FIRST", "SECOND"], [item["isin"] for item in catalog["etfs"]]
        )
        self.assertEqual(
            "/data/raw/2026-08-16/snapshots/SECOND.json",
            catalog["etfs"][1]["snapshotPath"],
        )

    def test_build_catalog_includes_only_successful_selected_results(self) -> None:
        first = make_entry("FIRST", "ONE")
        second = make_entry("SECOND", "TWO")

        catalog = build_catalog(
            [first, second],
            [make_result(second, Path("data/raw/2026-08-16"))],
        )

        self.assertEqual(["SECOND"], [item["isin"] for item in catalog["etfs"]])

    def test_write_catalog_replaces_atomically_and_preserves_previous_on_serialization_error(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "catalog.json"
            target.write_text('{"generatedAt":"old"}\n', encoding="utf-8")

            write_catalog({"generatedAt": "new"}, target)
            self.assertEqual("new", json.loads(target.read_text())["generatedAt"])

            with self.assertRaises(TypeError):
                write_catalog({"invalid": object()}, target)
            self.assertEqual("new", json.loads(target.read_text())["generatedAt"])

    def test_catalog_update_is_explicit_cli_option(self) -> None:
        args = build_parser().parse_args(["--all", "--fixtures", "--update-catalog"])
        self.assertTrue(args.update_catalog)

        args_without_update = build_parser().parse_args(["--all", "--fixtures"])
        self.assertFalse(args_without_update.update_catalog)


if __name__ == "__main__":
    unittest.main()

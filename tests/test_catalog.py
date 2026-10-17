from __future__ import annotations

import json
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path

from etf_ingestion_backend.catalog import build_catalog, write_catalog
from etf_ingestion_backend.cli import build_parser
from etf_ingestion_backend.models import (
    ETFSourceEntry,
    IngestionResult,
    NormalizedHolding,
)


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


def make_result(
    entry: ETFSourceEntry,
    output_dir: Path,
    holdings: list[NormalizedHolding] | None = None,
) -> IngestionResult:
    return IngestionResult(
        etf=entry,
        output_dir=output_dir,
        snapshot_path=output_dir / "snapshots" / f"{entry.isin}.json",
        raw_download_path=None,
        snapshot=SimpleNamespace(holdings=holdings) if holdings is not None else None,
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
        self.assertEqual(1, catalog["pairwiseOverlap"]["version"])
        self.assertEqual(
            [("FIRST", "SECOND")],
            [
                (pair["isinA"], pair["isinB"])
                for pair in catalog["pairwiseOverlap"]["pairs"]
            ],
        )
        self.assertFalse(catalog["pairwiseOverlap"]["pairs"][0]["available"])

    def test_build_catalog_includes_only_successful_selected_results(self) -> None:
        first = make_entry("FIRST", "ONE")
        second = make_entry("SECOND", "TWO")

        catalog = build_catalog(
            [first, second],
            [make_result(second, Path("data/raw/2026-08-16"))],
        )

        self.assertEqual(["SECOND"], [item["isin"] for item in catalog["etfs"]])
        self.assertEqual([], catalog["pairwiseOverlap"]["pairs"])

    def test_build_catalog_calculates_ordered_pairs_from_snapshot_holdings(
        self,
    ) -> None:
        first = make_entry("FIRST", "ONE")
        second = make_entry("SECOND", "TWO")
        third = make_entry("THIRD", "THREE")
        run_date = Path("data/raw/2026-08-16")
        results = [
            make_result(
                first,
                run_date,
                [NormalizedHolding(None, None, isin="SHARED", weight_pct=6)],
            ),
            make_result(
                second,
                run_date,
                [NormalizedHolding(None, None, isin="SHARED", weight_pct=4)],
            ),
            make_result(
                third,
                run_date,
                [NormalizedHolding(None, None, isin="OTHER", weight_pct=8)],
            ),
        ]

        catalog = build_catalog([first, second, third], results)

        pairs = catalog["pairwiseOverlap"]["pairs"]
        self.assertEqual(
            [("FIRST", "SECOND"), ("FIRST", "THIRD"), ("SECOND", "THIRD")],
            [(pair["isinA"], pair["isinB"]) for pair in pairs],
        )
        self.assertEqual(4, pairs[0]["overlapPct"])
        self.assertTrue(all(pair["available"] for pair in pairs))

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

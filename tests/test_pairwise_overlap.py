from __future__ import annotations

import json
import unittest
from pathlib import Path

from etf_ingestion_backend.models import NormalizedHolding
from etf_ingestion_backend.pairwise_overlap import calculate_pairwise_overlap


def holding(
    weight: float,
    *,
    isin: str | None = None,
    company_id: str | None = None,
    canonical_name: str | None = None,
) -> NormalizedHolding:
    return NormalizedHolding(
        ticker=None,
        name=canonical_name,
        isin=isin,
        company_id=company_id,
        canonical_name=canonical_name,
        weight_pct=weight,
    )


class PairwiseOverlapTests(unittest.TestCase):
    def test_smi_and_cssmi_snapshots_overlap_by_company_across_roche_isins(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]

        def load_holdings(isin: str) -> list[NormalizedHolding]:
            snapshot_path = (
                repository_root
                / "data"
                / "raw"
                / "2026-10-17"
                / "snapshots"
                / f"{isin}.json"
            )
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            return [
                NormalizedHolding(
                    ticker=holding["security"].get("ticker"),
                    name=holding["security"].get("name"),
                    isin=holding["security"].get("isin"),
                    company_id=holding["security"].get("company_id"),
                    canonical_name=holding["security"].get("canonical_name"),
                    weight_pct=holding["exposure"].get("weight_pct"),
                )
                for holding in snapshot["holdings"]
            ]

        result = calculate_pairwise_overlap(
            load_holdings("CH0008899764"),
            load_holdings("CH1447931341"),
        )

        self.assertEqual(98.732, result["overlap_pct"])

    def test_uses_smaller_weight_for_shared_isin(self) -> None:
        result = calculate_pairwise_overlap(
            [holding(6, isin="CH0000000001")],
            [holding(4, isin="ch0000000001")],
        )

        self.assertEqual(4, result["overlap_pct"])
        self.assertTrue(result["available"])

    def test_falls_back_to_company_identity_when_isin_is_missing(self) -> None:
        result = calculate_pairwise_overlap(
            [holding(6, company_id="acme-corp")],
            [holding(4, canonical_name="Acme Corp")],
        )

        self.assertEqual(4, result["overlap_pct"])

    def test_falls_back_to_company_identity_when_only_one_holding_has_isin(self) -> None:
        result = calculate_pairwise_overlap(
            [holding(6, isin="CH0000000001", company_id="acme-corp")],
            [holding(4, canonical_name="Acme Corp")],
        )

        self.assertEqual(4, result["overlap_pct"])

    def test_matches_different_isins_by_company_without_double_counting(self) -> None:
        result = calculate_pairwise_overlap(
            [
                holding(6, isin="CH0000000001", company_id="same-company"),
                holding(4, isin="CH0000000002", company_id="same-company"),
            ],
            [
                holding(3, isin="CH0000000001", company_id="same-company"),
                holding(7, isin="CH0000000003", company_id="same-company"),
            ],
        )

        self.assertEqual(10, result["overlap_pct"])

    def test_does_not_fall_back_when_both_holdings_have_different_isins(self) -> None:
        result = calculate_pairwise_overlap(
            [holding(6, isin="CH0000000001", company_id="acme-corp")],
            [holding(4, isin="CH0000000002", canonical_name="Other Corp")],
        )

        self.assertEqual(0, result["overlap_pct"])

    def test_does_not_normalize_incomplete_holdings(self) -> None:
        result = calculate_pairwise_overlap(
            [holding(20, isin="SHARED"), holding(30, isin="ONLY-A")],
            [holding(10, isin="SHARED"), holding(20, isin="ONLY-B")],
        )

        self.assertEqual(10, result["overlap_pct"])
        self.assertEqual(50, result["coverage_pct_a"])
        self.assertEqual(30, result["coverage_pct_b"])

    def test_reports_unavailable_without_stable_holdings(self) -> None:
        result = calculate_pairwise_overlap(
            [holding(20)],
            [holding(15, isin="KNOWN")],
        )

        self.assertIsNone(result["overlap_pct"])
        self.assertFalse(result["available"])

    def test_zero_overlap_is_available_when_both_holdings_are_identifiable(self) -> None:
        result = calculate_pairwise_overlap(
            [holding(20, isin="ONLY-A")],
            [holding(15, isin="ONLY-B")],
        )

        self.assertEqual(0, result["overlap_pct"])
        self.assertTrue(result["available"])


if __name__ == "__main__":
    unittest.main()
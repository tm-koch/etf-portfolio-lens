from __future__ import annotations

import math
import re
from collections import defaultdict
from collections.abc import Iterable

from .models import NormalizedHolding


def _holding_company_identity(holding: NormalizedHolding) -> str | None:
    company = holding.company_id or holding.canonical_name
    if company and company.strip():
        normalized = re.sub(r"[^a-z0-9]+", "-", company.casefold()).strip("-")
        if normalized:
            return normalized
    return None


def _summarize_holdings(
    holdings: Iterable[NormalizedHolding],
) -> tuple[float, dict[str, float], dict[str, float], dict[str, dict[str, float]]]:
    coverage = 0.0
    isin_weights: dict[str, float] = defaultdict(float)
    company_weights: dict[str, float] = defaultdict(float)
    company_isin_weights: dict[str, dict[str, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    for holding in holdings:
        weight = holding.weight_pct
        if weight is None or not math.isfinite(weight) or weight < 0:
            continue
        coverage += weight
        isin = holding.isin.strip().casefold() if holding.isin and holding.isin.strip() else None
        company = _holding_company_identity(holding)
        if isin:
            isin_weights[isin] += weight
        if company:
            company_weights[company] += weight
            if isin:
                company_isin_weights[company][isin] += weight
    return (
        coverage,
        dict(isin_weights),
        dict(company_weights),
        {company: dict(weights) for company, weights in company_isin_weights.items()},
    )


def calculate_pairwise_overlap(
    holdings_a: Iterable[NormalizedHolding],
    holdings_b: Iterable[NormalizedHolding],
) -> dict[str, float | bool | None]:
    coverage_a, isins_a, companies_a, company_isins_a = _summarize_holdings(holdings_a)
    coverage_b, isins_b, companies_b, company_isins_b = _summarize_holdings(holdings_b)
    if not (isins_a or companies_a) or not (isins_b or companies_b):
        return {
            "overlap_pct": None,
            "coverage_pct_a": round(coverage_a, 4),
            "coverage_pct_b": round(coverage_b, 4),
            "available": False,
        }

    overlap = sum(min(weight, isins_b[isin]) for isin, weight in isins_a.items() if isin in isins_b)
    for company in companies_a.keys() & companies_b.keys():
        exact_company_overlap = sum(
            min(weight, company_isins_b.get(company, {}).get(isin, 0.0))
            for isin, weight in company_isins_a.get(company, {}).items()
        )
        company_overlap = min(companies_a[company], companies_b[company])
        overlap += max(0.0, company_overlap - exact_company_overlap)
    return {
        "overlap_pct": round(overlap, 4),
        "coverage_pct_a": round(coverage_a, 4),
        "coverage_pct_b": round(coverage_b, 4),
        "available": True,
    }
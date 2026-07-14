from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import NormalizedHolding

WEIGHT_TOTAL_TOLERANCE = 0.5


def _validate_total(name: str, total: float) -> None:
    if total > 100.0 + WEIGHT_TOTAL_TOLERANCE:
        raise ValueError(
            f"{name} weights sum to {total:.4f}, which exceeds 100 percent plus tolerance"
        )


def aggregate_holdings(holdings: Iterable[NormalizedHolding]) -> dict:
    sector_weights: dict[str, float] = defaultdict(float)
    region_weights: dict[str, float] = defaultdict(float)
    currency_weights: dict[str, float] = defaultdict(float)

    holdings_list = list(holdings)
    holdings_total = 0.0
    for holding in holdings_list:
        weight = holding.weight_pct or 0.0
        holdings_total += weight
        sector_weights[holding.sector or "Unknown"] += weight
        region_weights[holding.region or "Unknown"] += weight
        currency_weights[holding.market_currency or "Unknown"] += weight

    _validate_total("holding", holdings_total)
    _validate_total("sector", sum(sector_weights.values()))
    _validate_total("region", sum(region_weights.values()))
    _validate_total("currency", sum(currency_weights.values()))

    top_holdings = sorted(
        holdings_list, key=lambda item: item.weight_pct or 0.0, reverse=True
    )[:10]

    return {
        "sector_weights": [
            {"name": name, "weight_pct": round(weight, 4)}
            for name, weight in sorted(
                sector_weights.items(), key=lambda item: item[1], reverse=True
            )
        ],
        "region_weights": [
            {"name": name, "weight_pct": round(weight, 4)}
            for name, weight in sorted(
                region_weights.items(), key=lambda item: item[1], reverse=True
            )
        ],
        "currency_weights": [
            {"name": name, "weight_pct": round(weight, 4)}
            for name, weight in sorted(
                currency_weights.items(), key=lambda item: item[1], reverse=True
            )
        ],
        "top_holdings": [
            {
                "ticker": item.ticker,
                "name": item.name,
                "weight_pct": round(item.weight_pct or 0.0, 4),
            }
            for item in top_holdings
        ],
        "counts": {
            "holdings": len(holdings_list),
        },
    }

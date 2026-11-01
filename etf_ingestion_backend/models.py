from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DISTRIBUTION_POLICIES = {"accumulating", "distributing"}
INVESTMENT_UNIVERSES = {
    "developed_world",
    "all_country_world",
    "emerging_markets",
    "developed_europe",
    "switzerland",
}


@dataclass(slots=True)
class MatchDiagnostics:
    status: str
    matched_by: str | None = None
    attempted: list[str] = field(default_factory=list)
    missing_elements: list[str] = field(default_factory=list)
    warning: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "matched_by": self.matched_by,
            "attempted": self.attempted,
            "missing_elements": self.missing_elements,
            "warning": self.warning,
        }


@dataclass(slots=True)
class ETFSourceEntry:
    isin: str
    ticker: str
    name: str
    provider: str
    source_url: str
    expected_format: str
    parser_id: str
    fixture_path: str | None = None
    fetcher_id: str | None = None
    fetcher_context: dict[str, str] = field(default_factory=dict)
    share_class_currency: str | None = None
    exchange: str | None = None
    listing_ticker: str | None = None
    listing_currency: str | None = None
    fixture_only: bool = False
    ter_pct: float | None = None
    ter_source: str | None = None
    distribution_policy: str | None = None
    investment_universe: str | None = None

    def __post_init__(self) -> None:
        if self.ter_pct is not None:
            try:
                ter_pct = float(self.ter_pct)
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid TER for {self.isin}") from error
            if not math.isfinite(ter_pct) or ter_pct < 0:
                raise ValueError(f"Invalid TER for {self.isin}")
            self.ter_pct = ter_pct
            if self.ter_source is None:
                raise ValueError(f"Missing TER source for {self.isin}")
        if self.ter_source is not None and (
            not isinstance(self.ter_source, str) or not self.ter_source.strip()
        ):
            raise ValueError(f"Invalid TER source for {self.isin}")
        if self.distribution_policy is not None and (
            not isinstance(self.distribution_policy, str)
            or self.distribution_policy not in DISTRIBUTION_POLICIES
        ):
            raise ValueError(f"Invalid distribution policy for {self.isin}")
        if self.investment_universe is not None and (
            not isinstance(self.investment_universe, str)
            or self.investment_universe not in INVESTMENT_UNIVERSES
        ):
            raise ValueError(f"Invalid investment universe for {self.isin}")

    @property
    def optimizer_metadata_issues(self) -> list[str]:
        fields = {
            "ter_pct": self.ter_pct,
            "ter_source": self.ter_source,
            "distribution_policy": self.distribution_policy,
            "investment_universe": self.investment_universe,
        }
        return [name for name, value in fields.items() if value is None]

    @property
    def mixlab_eligible(self) -> bool:
        return not self.optimizer_metadata_issues


@dataclass(slots=True)
class NormalizedHolding:
    ticker: str | None
    name: str | None
    isin: str | None = None
    company_id: str | None = None
    canonical_name: str | None = None
    sector: str | None = None
    asset_class: str | None = None
    region: str | None = None
    country: str | None = None
    country_code: str | None = None
    exchange: str | None = None
    exchange_code: str | None = None
    market_currency: str | None = None
    weight_pct: float | None = None
    market_value: float | None = None
    notional_value: float | None = None
    shares: float | None = None
    price: float | None = None
    source_fields: dict[str, Any] = field(default_factory=dict)
    enrichment_source: str | None = None
    venue_discrepancy: str | None = None
    match: MatchDiagnostics | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "security": {
                "isin": self.isin,
                "ticker": self.ticker,
                "name": self.name,
                "company_id": self.company_id,
                "canonical_name": self.canonical_name,
            },
            "classification": {
                "asset_class": self.asset_class,
                "sector": self.sector,
                "region": self.region,
                "country": self.country,
                "country_code": self.country_code,
                "exchange": self.exchange,
                "market_currency": self.market_currency,
            },
            "exposure": {
                "weight_pct": self.weight_pct,
                "market_value": self.market_value,
                "shares": self.shares,
                "price": self.price,
                "notional_value": self.notional_value,
                "currency_exposure": self.market_currency,
            },
            "provenance": {
                "source_fields": self.source_fields,
                "enrichment_source": self.enrichment_source,
                "exchange_code": self.exchange_code,
                "venue_discrepancy": self.venue_discrepancy,
                "match": self.match.to_dict() if self.match else None,
            },
        }


@dataclass(slots=True)
class ETFSnapshot:
    etf: ETFSourceEntry
    as_of: str
    generated_at: str
    source_url: str
    resolved_download_url: str | None
    source_format: str
    parser_id: str
    holdings: list[NormalizedHolding]
    aggregates: dict[str, Any]
    provenance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        etf = {
            "isin": self.etf.isin,
            "ticker": self.etf.ticker,
            "name": self.etf.name,
            "provider": self.etf.provider,
            "domicile": self.provenance.get("domicile"),
            "base_currency": self.provenance.get("base_currency"),
        }
        for field_name in (
            "share_class_currency",
            "exchange",
            "listing_ticker",
            "listing_currency",
        ):
            value = getattr(self.etf, field_name)
            if value is not None:
                etf[field_name] = value
        return {
            "schema_version": "1.0",
            "etf": etf,
            "snapshot": {
                "as_of": self.as_of,
                "generated_at": self.generated_at,
                "source_url": self.source_url,
                "resolved_download_url": self.resolved_download_url,
                "source_format": self.source_format,
                "parser_id": self.parser_id,
            },
            "holdings": [holding.to_dict() for holding in self.holdings],
            "aggregates": self.aggregates,
            "provenance": self.provenance,
        }


@dataclass(slots=True)
class IngestionResult:
    etf: ETFSourceEntry
    output_dir: Path
    snapshot_path: Path
    raw_download_path: Path | None
    snapshot: ETFSnapshot

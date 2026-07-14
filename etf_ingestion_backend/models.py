from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


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


@dataclass(slots=True)
class NormalizedHolding:
    ticker: str | None
    name: str | None
    isin: str | None = None
    sector: str | None = None
    asset_class: str | None = None
    region: str | None = None
    country: str | None = None
    exchange: str | None = None
    market_currency: str | None = None
    weight_pct: float | None = None
    market_value: float | None = None
    notional_value: float | None = None
    shares: float | None = None
    price: float | None = None
    source_fields: dict[str, Any] = field(default_factory=dict)
    enrichment_source: str | None = None
    match: MatchDiagnostics | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "security": {
                "isin": self.isin,
                "ticker": self.ticker,
                "name": self.name,
            },
            "classification": {
                "asset_class": self.asset_class,
                "sector": self.sector,
                "region": self.region,
                "country": self.country,
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
        return {
            "schema_version": "1.0",
            "etf": {
                "isin": self.etf.isin,
                "ticker": self.etf.ticker,
                "name": self.etf.name,
                "provider": self.etf.provider,
                "domicile": self.provenance.get("domicile"),
                "base_currency": self.provenance.get("base_currency"),
            },
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

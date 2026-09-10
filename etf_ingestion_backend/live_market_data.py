from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SUPPORTED_CURRENCIES = frozenset({"CHF", "EUR", "USD"})
SUPPORTED_FX_PAIRS = frozenset({"EUR/CHF", "USD/CHF"})
ARTIFACT_SCHEMA_VERSION = 1
ISIN_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$")
ISO_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})$"
)
PUBLIC_SOURCE_FIELDS = {"source_url", "resolved_url", "provider", "raw_response"}


class LiveMarketDataError(ValueError):
    """Raised when live market data is malformed or unsafe to publish."""


def _validate_timestamp(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not ISO_TIMESTAMP_PATTERN.fullmatch(value):
        raise LiveMarketDataError(f"{field_name} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise LiveMarketDataError(f"{field_name} must be a valid timestamp") from error
    if parsed.tzinfo is None:
        raise LiveMarketDataError(f"{field_name} must include a timezone")
    return value


def _validate_currency(value: str, field_name: str = "currency") -> str:
    if value not in SUPPORTED_CURRENCIES:
        raise LiveMarketDataError(
            f"{field_name} must be one of {sorted(SUPPORTED_CURRENCIES)}"
        )
    return value


def _validate_isin(value: str) -> str:
    if not isinstance(value, str) or not ISIN_PATTERN.fullmatch(value):
        raise LiveMarketDataError(f"invalid ISIN: {value!r}")
    return value


def _reject_public_source_fields(value: Mapping[str, Any], field_name: str) -> None:
    leaked = PUBLIC_SOURCE_FIELDS.intersection(value)
    if leaked:
        raise LiveMarketDataError(
            f"{field_name} contains prohibited source fields: {sorted(leaked)}"
        )


@dataclass(frozen=True, slots=True)
class QuoteConfig:
    isin: str
    adapter_id: str
    currency: str
    secret_name: str = "SWISS_QUOTE_URL_TEMPLATE"

    def __post_init__(self) -> None:
        _validate_isin(self.isin)
        _validate_currency(self.currency)
        if not self.adapter_id or not re.fullmatch(r"[a-z0-9_]+", self.adapter_id):
            raise LiveMarketDataError(
                "adapter_id must be a non-empty opaque identifier"
            )
        if not self.secret_name or not re.fullmatch(r"[A-Z0-9_]+", self.secret_name):
            raise LiveMarketDataError("secret_name must be an environment-style name")

    def to_dict(self) -> dict[str, str]:
        return {
            "isin": self.isin,
            "adapter_id": self.adapter_id,
            "currency": self.currency,
            "secret_name": self.secret_name,
        }


@dataclass(frozen=True, slots=True)
class Quote:
    isin: str
    price: float | None
    currency: str
    quoted_at: str | None
    status: str

    def __post_init__(self) -> None:
        _validate_isin(self.isin)
        _validate_currency(self.currency)
        if self.price is not None and (
            self.price < 0 or not isinstance(self.price, (int, float))
        ):
            raise LiveMarketDataError("quote price must be a non-negative number")
        if self.quoted_at is not None:
            _validate_timestamp(self.quoted_at, "quoted_at")
        if self.status not in {"available", "unavailable"}:
            raise LiveMarketDataError("quote status must be available or unavailable")
        if self.status == "available" and (
            self.price is None or self.quoted_at is None
        ):
            raise LiveMarketDataError("available quotes require price and quoted_at")

    def to_dict(self) -> dict[str, Any]:
        return {
            "price": self.price,
            "currency": self.currency,
            "quoted_at": self.quoted_at,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class FXRate:
    pair: str
    rate: float | None
    quoted_at: str | None
    status: str

    def __post_init__(self) -> None:
        if self.pair not in SUPPORTED_FX_PAIRS:
            raise LiveMarketDataError(f"unsupported FX pair: {self.pair}")
        if self.rate is not None and (
            self.rate <= 0 or not isinstance(self.rate, (int, float))
        ):
            raise LiveMarketDataError("FX rate must be a positive number")
        if self.quoted_at is not None:
            _validate_timestamp(self.quoted_at, "quoted_at")
        if self.status not in {"available", "unavailable"}:
            raise LiveMarketDataError("FX status must be available or unavailable")
        if self.status == "available" and (self.rate is None or self.quoted_at is None):
            raise LiveMarketDataError("available FX rates require rate and quoted_at")

    def to_dict(self) -> dict[str, Any]:
        return {
            "rate": self.rate,
            "quoted_at": self.quoted_at,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class LivePricesArtifact:
    generated_at: str
    quotes: dict[str, Quote] = field(default_factory=dict)
    fx: dict[str, FXRate] = field(default_factory=dict)
    status: str = "complete"

    def __post_init__(self) -> None:
        _validate_timestamp(self.generated_at, "generated_at")
        if self.status not in {"complete", "degraded", "unavailable"}:
            raise LiveMarketDataError("artifact status is invalid")
        if not self.quotes and not self.fx:
            raise LiveMarketDataError("artifact must contain quotes or FX rates")
        for isin, quote in self.quotes.items():
            if isin != quote.isin:
                raise LiveMarketDataError("quote map key must match quote ISIN")
        for pair, rate in self.fx.items():
            if pair != rate.pair:
                raise LiveMarketDataError("FX map key must match FX pair")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ARTIFACT_SCHEMA_VERSION,
            "generated_at": self.generated_at,
            "status": self.status,
            "quotes": {isin: quote.to_dict() for isin, quote in self.quotes.items()},
            "fx": {pair: rate.to_dict() for pair, rate in self.fx.items()},
        }

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")

    @classmethod
    def from_dict(cls, document: Mapping[str, Any]) -> "LivePricesArtifact":
        if document.get("schema_version") != ARTIFACT_SCHEMA_VERSION:
            raise LiveMarketDataError("unsupported live-price schema version")
        _reject_public_source_fields(document, "artifact")
        quotes: dict[str, Quote] = {}
        for isin, raw_quote in _mapping(document, "quotes").items():
            if not isinstance(raw_quote, Mapping):
                raise LiveMarketDataError(f"quote {isin} must be an object")
            _reject_public_source_fields(raw_quote, f"quote {isin}")
            quotes[isin] = Quote(isin=isin, **raw_quote)
        fx: dict[str, FXRate] = {}
        for pair, raw_rate in _mapping(document, "fx").items():
            if not isinstance(raw_rate, Mapping):
                raise LiveMarketDataError(f"FX rate {pair} must be an object")
            _reject_public_source_fields(raw_rate, f"FX rate {pair}")
            fx[pair] = FXRate(pair=pair, **raw_rate)
        return cls(
            generated_at=document.get("generated_at", ""),
            quotes=quotes,
            fx=fx,
            status=document.get("status", "complete"),
        )


def _mapping(document: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = document.get(key, {})
    if not isinstance(value, Mapping):
        raise LiveMarketDataError(f"{key} must be an object")
    return value


def load_quote_config(path: Path) -> list[QuoteConfig]:
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("quotes")
    if not isinstance(entries, list):
        raise LiveMarketDataError("quote configuration must contain a quotes list")
    shared_secret_name = document.get(
        "quote_url_template_secret", "SWISS_QUOTE_URL_TEMPLATE"
    )
    configs = []
    for entry in entries:
        normalized_entry = dict(entry)
        entry_secret_name = normalized_entry.pop("quote_url_template_secret", None)
        if entry_secret_name is None:
            entry_secret_name = normalized_entry.pop("secret_name", shared_secret_name)
        configs.append(QuoteConfig(**normalized_entry, secret_name=entry_secret_name))
    if len({entry.isin for entry in configs}) != len(configs):
        raise LiveMarketDataError("quote configuration contains duplicate ISINs")
    return configs


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

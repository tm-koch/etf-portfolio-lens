from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .models import NormalizedHolding


def _normalize(value: str | None) -> str:
    return (value or "").strip().casefold()


def _split_aliases(value: str | None) -> list[str]:
    if not value:
        return []
    return [alias.strip() for alias in value.split("|") if alias.strip()]


@dataclass(slots=True)
class SecurityRecord:
    ticker: str
    name: str
    exchange: str
    sector: str | None
    asset_type: str | None
    country: str | None
    country_code: str | None
    isin: str | None
    aliases: list[str]


@dataclass(slots=True)
class SecurityMatch:
    record: SecurityRecord | None
    status: str
    matched_by: str | None
    attempted: list[str]
    missing_elements: list[str]
    warning: str | None = None

    @property
    def matched(self) -> bool:
        return self.record is not None and self.status == "matched"

    def to_diagnostics(self) -> dict[str, object]:
        return {
            "status": self.status,
            "matched_by": self.matched_by,
            "attempted": self.attempted,
            "missing_elements": self.missing_elements,
            "warning": self.warning,
        }


@dataclass(slots=True)
class SecurityMaster:
    records: list[SecurityRecord]
    version: str
    warnings: list[str]

    @classmethod
    def from_csv(cls, path: Path) -> "SecurityMaster":
        records: list[SecurityRecord] = []
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                records.append(
                    SecurityRecord(
                        ticker=(row.get("ticker") or "").strip(),
                        name=(row.get("name") or "").strip(),
                        exchange=(row.get("exchange") or "").strip(),
                        sector=(row.get("stock_sector") or None),
                        asset_type=(row.get("asset_type") or None),
                        country=(row.get("country") or None),
                        country_code=(row.get("country_code") or None),
                        isin=(row.get("isin") or None),
                        aliases=_split_aliases(row.get("aliases")),
                    )
                )
        return cls(records=records, version=path.name, warnings=[])

    def _records_by_ticker(self, ticker: str) -> list[SecurityRecord]:
        normalized_ticker = _normalize(ticker)
        return [
            record
            for record in self.records
            if _normalize(record.ticker) == normalized_ticker
        ]

    def _records_by_alias(self, value: str) -> list[SecurityRecord]:
        normalized_value = _normalize(value)
        if not normalized_value:
            return []
        matches: list[SecurityRecord] = []
        for record in self.records:
            if normalized_value in {_normalize(alias) for alias in record.aliases}:
                matches.append(record)
        return matches

    def match(self, holding: NormalizedHolding) -> SecurityMatch:
        attempted: list[str] = []
        missing_elements: list[str] = []

        if holding.isin:
            attempted.append("isin")
            normalized_isin = _normalize(holding.isin)
            for record in self.records:
                if _normalize(record.isin) == normalized_isin:
                    return SecurityMatch(
                        record, "matched", "isin", attempted, missing_elements
                    )
        else:
            missing_elements.append("isin")

        ticker = _normalize(holding.ticker)
        exchange = _normalize(holding.exchange)
        if ticker and exchange:
            attempted.append("ticker+exchange")
            for record in self.records:
                if (
                    _normalize(record.ticker) == ticker
                    and _normalize(record.exchange) == exchange
                ):
                    return SecurityMatch(
                        record,
                        "matched",
                        "ticker+exchange",
                        attempted,
                        missing_elements,
                    )
        else:
            if not ticker:
                missing_elements.append("ticker")
            if not exchange:
                missing_elements.append("exchange")

        if ticker:
            attempted.append("ticker")
            ticker_matches = self._records_by_ticker(ticker)
            if len(ticker_matches) == 1:
                return SecurityMatch(
                    ticker_matches[0],
                    "matched",
                    "ticker",
                    attempted,
                    missing_elements,
                )
            if len(ticker_matches) > 1:
                warning = f"ambiguous ticker match for {holding.ticker}: {len(ticker_matches)} candidates"
                return SecurityMatch(
                    None,
                    "ambiguous",
                    "ticker",
                    attempted,
                    missing_elements,
                    warning,
                )

        alias_candidates = [value for value in (holding.ticker, holding.name) if value]
        if alias_candidates:
            attempted.append("alias")
            alias_matches: list[SecurityRecord] = []
            for candidate in alias_candidates:
                alias_matches.extend(self._records_by_alias(candidate))
            unique_matches: list[SecurityRecord] = []
            seen: set[str] = set()
            for record in alias_matches:
                key = f"{record.ticker}|{record.exchange}|{record.isin}"
                if key not in seen:
                    seen.add(key)
                    unique_matches.append(record)
            if len(unique_matches) == 1:
                return SecurityMatch(
                    unique_matches[0],
                    "matched",
                    "alias",
                    attempted,
                    missing_elements,
                )
            if len(unique_matches) > 1:
                warning = f"ambiguous alias match for {holding.ticker or holding.name}: {len(unique_matches)} candidates"
                return SecurityMatch(
                    None,
                    "ambiguous",
                    "alias",
                    attempted,
                    missing_elements,
                    warning,
                )

        warning = f"could not fully match holding {holding.ticker or holding.name or '<unknown>'}; missing={missing_elements or ['unknown']}"
        return SecurityMatch(
            None, "unmatched", None, attempted, missing_elements, warning
        )

    def lookup(self, holding: NormalizedHolding) -> SecurityRecord | None:
        return self.match(holding).record

    def lookup_etf_metadata(self) -> dict[str, str | None]:
        return {"domicile": None, "base_currency": None}

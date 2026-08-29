from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .exchange import normalize_exchange
from .models import NormalizedHolding
from .sector_taxonomy import normalize_sector_label


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
                        sector=normalize_sector_label(row.get("stock_sector")),
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

    def _records_by_name(self, value: str) -> list[SecurityRecord]:
        normalized_value = _normalize(value)
        return [
            record
            for record in self.records
            if _normalize(record.name) == normalized_value
        ]

    def match(self, holding: NormalizedHolding) -> SecurityMatch:
        attempted: list[str] = []
        missing_elements: list[str] = []
        ambiguous_ticker_warning: str | None = None

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
        country = _normalize(holding.country)
        has_context = bool(exchange or country)
        if ticker and exchange:
            attempted.append("ticker+exchange")
            for record in self.records:
                if _normalize(record.ticker) == ticker and _normalize(
                    normalize_exchange(record.exchange)
                ) == _normalize(holding.exchange_code):
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
            exchange_matches = [
                record
                for record in ticker_matches
                if not exchange
                or _normalize(normalize_exchange(record.exchange)) == exchange
            ]
            contextual_matches = [
                record
                for record in exchange_matches
                if not country or _normalize(record.country) == country
            ]
            if exchange and not contextual_matches and country:
                contextual_matches = [
                    record
                    for record in ticker_matches
                    if _normalize(record.country) == country
                ]
            if len(contextual_matches) == 1:
                return SecurityMatch(
                    contextual_matches[0],
                    "matched",
                    "ticker",
                    attempted,
                    missing_elements,
                )
            if len(contextual_matches) > 1:
                if has_context:
                    ambiguous_ticker_warning = f"ambiguous contextual ticker match for {holding.ticker}: {len(contextual_matches)} candidates"
                else:
                    ambiguous_ticker_warning = f"ambiguous ticker match for {holding.ticker}: {len(contextual_matches)} candidates"
            elif has_context and ticker_matches:
                ambiguous_ticker_warning = (
                    f"ticker match for {holding.ticker} conflicts with holding context "
                    f"exchange={holding.exchange or '<missing>'}, country={holding.country or '<missing>'}"
                )
            elif len(ticker_matches) > 1:
                ambiguous_ticker_warning = f"ambiguous ticker match for {holding.ticker}: {len(ticker_matches)} candidates"

        name_matches = self._records_by_name(holding.name or "")
        if len(name_matches) == 1:
            return SecurityMatch(
                name_matches[0],
                "matched",
                "name",
                attempted + ["name"],
                missing_elements,
            )
        if len(name_matches) > 1:
            return SecurityMatch(
                None,
                "ambiguous",
                "name",
                attempted + ["name"],
                missing_elements,
                f"ambiguous name match for {holding.name}: {len(name_matches)} candidates",
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

        if ambiguous_ticker_warning:
            return SecurityMatch(
                None,
                "ambiguous",
                "ticker",
                attempted,
                missing_elements,
                ambiguous_ticker_warning,
            )

        warning = f"could not fully match holding {holding.ticker or holding.name or '<unknown>'}; missing={missing_elements or ['unknown']}"
        return SecurityMatch(
            None, "unmatched", None, attempted, missing_elements, warning
        )

    def lookup(self, holding: NormalizedHolding) -> SecurityRecord | None:
        return self.match(holding).record

    def lookup_etf_metadata(self) -> dict[str, str | None]:
        return {"domicile": None, "base_currency": None}

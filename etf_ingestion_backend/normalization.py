from __future__ import annotations

import re
import sys
from typing import Any

from .exchange import normalize_exchange
from .models import MatchDiagnostics, NormalizedHolding
from .overrides import OverrideRegistry
from .sector_taxonomy import normalize_sector_label
from .security_master import SecurityMaster, SecurityRecord

PERCENT_WEIGHT_PARSERS = {
    "ishares_csv_v1",
    "ssga_xlsx_v1",
    "ubs_xml_xls_v1",
}

FRACTION_WEIGHT_PARSERS = {
    "amundi_landing_xlsx_v1",
}

REGION_BY_COUNTRY = {
    "austria": "Europe",
    "belgium": "Europe",
    "czech republic": "Europe",
    "denmark": "Europe",
    "finland": "Europe",
    "france": "Europe",
    "germany": "Europe",
    "hong kong": "Asia",
    "ireland": "Europe",
    "italy": "Europe",
    "luxembourg": "Europe",
    "netherlands": "Europe",
    "norway": "Europe",
    "portugal": "Europe",
    "spain": "Europe",
    "switzerland": "Europe",
    "united kingdom": "Europe",
    "united states": "North America",
    "usa": "North America",
    "canada": "North America",
    "japan": "Asia",
    "taiwan": "Asia",
    "china": "Asia",
    "south korea": "Asia",
}


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.replace("’", "").replace("'", "").replace(",", ".")
    text = re.sub(r"[^0-9.\-]", "", text)
    if not text or text in {"-", "."}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_percent_float(value: Any) -> float | None:
    parsed = parse_float(value)
    if parsed is None:
        return None
    return parsed * 100


def parse_weight_float(value: Any, parser_id: str) -> float | None:
    if parser_id in PERCENT_WEIGHT_PARSERS:
        return parse_float(value)
    if parser_id in FRACTION_WEIGHT_PARSERS:
        return parse_percent_float(value)
    return parse_float(value)


def _normalize_key(value: str | None) -> str:
    return (value or "").strip().casefold()


def _infer_region(country: str | None) -> str | None:
    if not country:
        return None
    return REGION_BY_COUNTRY.get(_normalize_key(country))


def _company_id(name: str | None, isin: str | None) -> str | None:
    value = re.sub(r"[^a-z0-9]+", "-", (name or "").casefold()).strip("-")
    return value or (f"instrument-{isin.casefold()}" if isin else None)


def normalize_row(
    raw_row: dict[str, Any],
    security_master: SecurityMaster,
    source_name: str,
    parser_id: str,
    overrides: OverrideRegistry | None = None,
) -> NormalizedHolding:
    isin = (
        raw_row.get("ISIN")
        or raw_row.get("ISIN code")
        or raw_row.get("Security ISIN")
        or raw_row.get("isin")
        or raw_row.get("isin_code")
        or raw_row.get("ISIN-Code")
        or ""
    ).strip() or None
    ticker = (
        raw_row.get("Ticker")
        or raw_row.get("ticker")
        or raw_row.get("Symbol")
        or raw_row.get("symbol")
        or raw_row.get("Emittententicker")
        or ""
    ).strip() or None
    name = (raw_row.get("Name") or raw_row.get("name") or "").strip() or None
    name = (
        name
        or (raw_row.get("Security Name") or raw_row.get("security name") or "").strip()
        or (
            raw_row.get("Fondsname") or raw_row.get("Fonds Position Name") or ""
        ).strip()
        or None
    )
    sector = normalize_sector_label(
        raw_row.get("Sector")
        or raw_row.get("sector")
        or raw_row.get("Sector Classification")
        or raw_row.get("sector classification")
        or raw_row.get("Sektor")
        or ""
    )
    asset_class = (
        raw_row.get("Asset Class")
        or raw_row.get("asset_class")
        or raw_row.get("AssetClass")
        or raw_row.get("Asset class")
        or raw_row.get("Anlageklasse")
        or ""
    ).strip() or None
    country = (
        raw_row.get("Location")
        or raw_row.get("country")
        or raw_row.get("Country")
        or raw_row.get("Trade Country Name")
        or raw_row.get("Standort")
        or ""
    ).strip() or None
    exchange = (
        raw_row.get("Exchange") or raw_row.get("exchange") or raw_row.get("Börse") or ""
    ).strip() or None
    market_currency = (
        raw_row.get("Market Currency")
        or raw_row.get("market_currency")
        or raw_row.get("Currency")
        or raw_row.get("Marktwährung")
        or ""
    ).strip() or None

    holding = NormalizedHolding(
        ticker=ticker,
        name=name,
        isin=isin,
        sector=sector,
        asset_class=asset_class,
        region=_infer_region(country),
        country=country,
        exchange=exchange,
        exchange_code=normalize_exchange(exchange),
        market_currency=market_currency,
        weight_pct=parse_weight_float(
            raw_row.get("Weight %")
            or raw_row.get("Weight (%)")
            or raw_row.get("weight_pct")
            or raw_row.get("Weight")
            or raw_row.get("Percent of Fund")
            or raw_row.get("Percent of fund"),
            parser_id,
        ),
        market_value=parse_float(
            raw_row.get("Market Value")
            or raw_row.get("Base Market Value")
            or raw_row.get("market_value")
        ),
        notional_value=parse_float(
            raw_row.get("Notional Value") or raw_row.get("notional_value")
        ),
        shares=parse_float(
            raw_row.get("Shares")
            or raw_row.get("Number of Shares")
            or raw_row.get("shares")
        ),
        price=parse_float(
            raw_row.get("Price") or raw_row.get("Local Price") or raw_row.get("price")
        ),
        source_fields=dict(raw_row),
        enrichment_source=source_name,
    )

    override = (overrides or OverrideRegistry.empty()).find(holding)
    if override:
        for field, value in override.set_values.items():
            if hasattr(holding, field) and value not in (None, ""):
                setattr(holding, field, value)
        if holding.exchange:
            holding.exchange_code = normalize_exchange(holding.exchange)

    match = security_master.match(holding)
    holding.match = MatchDiagnostics(
        status=match.status,
        matched_by=match.matched_by,
        attempted=match.attempted,
        missing_elements=match.missing_elements,
        warning=match.warning,
    )
    if match.record:
        enrich_holding(holding, match.record)
        holding.enrichment_source = "security_master"
    else:
        if not holding.name:
            source_label = (
                raw_row.get("Securities")
                or raw_row.get("Security Name")
                or raw_row.get("Name")
                or raw_row.get("name")
                or ""
            ).strip()
            if source_label:
                holding.name = source_label
        fallback_identifier = holding.ticker or holding.name or "<unknown>"
        warning = match.warning or "could not fully match holding {} from {}".format(
            fallback_identifier,
            source_name,
        )
        print(f"WARNING: {warning}", file=sys.stderr)

    if not holding.region:
        holding.region = _infer_region(holding.country)

    if override:
        holding.enrichment_source = (
            "override+security_master" if match.record else "override"
        )
        holding.match.status = "overridden"
        holding.match.matched_by = "override"
    if holding.canonical_name:
        holding.name = holding.canonical_name
    elif match.record:
        holding.canonical_name = match.record.name
        holding.name = holding.canonical_name
    if holding.name and not holding.company_id:
        holding.company_id = _company_id(holding.name, holding.isin)

    return holding


def enrich_holding(holding: NormalizedHolding, record: SecurityRecord) -> None:
    if not holding.isin:
        holding.isin = record.isin
    if not holding.ticker:
        holding.ticker = record.ticker
    if not holding.name:
        holding.name = record.name
    if not holding.sector:
        holding.sector = normalize_sector_label(record.sector)
    if not holding.asset_class:
        holding.asset_class = record.asset_type or "Stock"
    if not holding.country:
        holding.country = record.country
    if not holding.exchange:
        holding.exchange = record.exchange
    if not holding.exchange_code:
        holding.exchange_code = normalize_exchange(record.exchange)
    if not holding.market_currency:
        holding.market_currency = record.country_code or None
    if not holding.region:
        holding.region = _infer_region(record.country)

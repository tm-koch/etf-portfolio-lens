from __future__ import annotations

import csv
import io
import json
import re
from datetime import date, datetime, timezone
from typing import Callable, Mapping

from .live_market_data import FXRate, LiveMarketDataError, Quote, _validate_currency


class LiveFetchError(RuntimeError):
    """Raised when a live source cannot be fetched or parsed."""


def _timestamp(trading_date: date, time_text: str) -> str:
    match = re.fullmatch(r"(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?", time_text.strip())
    if not match:
        raise LiveMarketDataError(f"invalid trade time: {time_text!r}")
    hour = int(match.group(1))
    minute = int(match.group(2))
    second = int(match.group(3) or 0)
    microsecond = int((match.group(4) or "").ljust(6, "0")[:6])
    parsed = datetime(
        trading_date.year,
        trading_date.month,
        trading_date.day,
        hour,
        minute,
        second,
        microsecond,
        tzinfo=timezone.utc,
    )
    return parsed.isoformat().replace("+00:00", "Z")


def _number(value: str, *, positive: bool = False) -> float:
    normalized = value.strip().replace("'", "").replace(" ", "").replace(",", ".")
    try:
        parsed = float(normalized)
    except ValueError as error:
        raise LiveMarketDataError(f"invalid numeric value: {value!r}") from error
    if parsed < 0 or (positive and parsed <= 0):
        raise LiveMarketDataError(f"invalid numeric value: {value!r}")
    return parsed


def _parse_date(value: str) -> date:
    for format_string in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value.strip(), format_string).date()
        except ValueError:
            continue
    raise LiveMarketDataError(f"invalid trading date: {value!r}")


def parse_swiss_trade_csv(
    payload: bytes | str,
    isin: str,
    currency: str,
    trading_date: date | None = None,
) -> Quote:
    _validate_currency(currency)
    text = (
        payload.decode("utf-8-sig", errors="replace")
        if isinstance(payload, bytes)
        else payload
    )
    rows = list(csv.reader(io.StringIO(text), delimiter=";"))
    header_index = next(
        (
            index
            for index, row in enumerate(rows)
            if [cell.strip() for cell in row[:3]] == ["Time", "Price", "Volume"]
        ),
        None,
    )
    if header_index is None:
        raise LiveMarketDataError("Swiss trade CSV is missing Time;Price;Volume header")
    resolved_date = trading_date
    if resolved_date is None:
        for row in rows[:header_index]:
            for cell in row:
                if re.fullmatch(
                    r"(?:\d{4}-\d{2}-\d{2}|\d{2}[./]\d{2}[./]\d{4})", cell.strip()
                ):
                    resolved_date = _parse_date(cell)
                    break
            if resolved_date:
                break
    if resolved_date is None:
        raise LiveMarketDataError("Swiss trade CSV has no trading date")

    latest_timestamp: str | None = None
    latest_price: float | None = None
    for row in rows[header_index + 1 :]:
        if len(row) < 2 or not row[0].strip() or not row[1].strip():
            continue
        try:
            timestamp = _timestamp(resolved_date, row[0])
            price = _number(row[1])
        except LiveMarketDataError:
            continue
        if latest_timestamp is None or timestamp > latest_timestamp:
            latest_timestamp = timestamp
            latest_price = price
    if latest_timestamp is None or latest_price is None:
        raise LiveMarketDataError("Swiss trade CSV contains no valid trade rows")
    return Quote(isin, latest_price, currency, latest_timestamp, "available")


def parse_frankfurter_rate(payload: bytes | str, pair: str) -> FXRate:
    text = payload.decode("utf-8") if isinstance(payload, bytes) else payload
    try:
        document = json.loads(text)
    except json.JSONDecodeError as error:
        raise LiveMarketDataError("Frankfurter response is not valid JSON") from error
    if not isinstance(document, Mapping):
        raise LiveMarketDataError("Frankfurter response must be an object")
    base, quote_currency = pair.split("/")
    if (
        document.get("base") != base
        or document.get("rates", {}).get(quote_currency) is None
    ):
        raise LiveMarketDataError(f"Frankfurter response does not contain {pair}")
    try:
        rate = _number(str(document["rates"][quote_currency]), positive=True)
        observed_date = _parse_date(str(document["date"]))
    except (KeyError, LiveMarketDataError) as error:
        raise LiveMarketDataError(
            f"Frankfurter response is missing {pair} data"
        ) from error
    quoted_at = datetime.combine(
        observed_date, datetime.min.time(), tzinfo=timezone.utc
    )
    return FXRate(pair, rate, quoted_at.isoformat().replace("+00:00", "Z"), "available")


def fetch_and_parse(
    url: str,
    parser: Callable[[bytes], Quote | FXRate],
    fetcher: Callable[[str], bytes],
) -> Quote | FXRate:
    try:
        return parser(fetcher(url))
    except Exception as error:
        if isinstance(error, LiveMarketDataError):
            raise LiveFetchError(str(error)) from error
        raise LiveFetchError("live source request failed") from error

from __future__ import annotations

import argparse
import json
import os
import tempfile
import urllib.request
from datetime import date
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit

from .live_adapters import (
    LiveFetchError,
    fetch_and_parse,
    parse_frankfurter_rate,
    parse_swiss_trade_csv,
    parse_yahoo_chart,
)
from .live_market_data import (
    FXRate,
    LiveMarketDataError,
    LivePricesArtifact,
    Quote,
    load_quote_config,
    utc_now,
)

FRANKFURTER_URLS = {
    "EUR/CHF": "https://api.frankfurter.app/latest?from=EUR&to=CHF",
    "USD/CHF": "https://api.frankfurter.app/latest?from=USD&to=CHF",
}

QUOTE_ADAPTERS = {
    "swiss_csv_v1": parse_swiss_trade_csv,
    "yahoo_chart_v1": parse_yahoo_chart,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch and stage live ETF prices and FX rates."
    )
    parser.add_argument("--config", default="data/live_price_config.json")
    parser.add_argument("--output", default="data/live_prices.json")
    parser.add_argument("--trading-date", type=date.fromisoformat, default=None)
    parser.add_argument(
        "--quote-url-template",
        help="Quote URL template for local runs and tests; {isin} or {ticker} is substituted.",
    )
    return parser


def _fetch_url(url: str) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "ETF-Portfolio-Lens/1.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _format_secret_url(template: str, isin: str, ticker: str | None) -> str:
    identifier = ticker if ticker is not None else isin
    placeholder = "{ticker}" if ticker is not None else "{isin}"
    return template.replace(placeholder, identifier)


def _validate_quote_url_template(template: str, ticker: str | None) -> None:
    placeholder = "{ticker}" if ticker is not None else "{isin}"
    parsed = urlsplit(template.replace(placeholder, "TESTIDENTIFIER"))
    if (
        placeholder not in template
        or parsed.scheme not in {"http", "https"}
        or not parsed.netloc
    ):
        raise LiveFetchError(
            f"configured quote URL template must be an absolute HTTP(S) URL containing {placeholder}"
        )


def _atomic_write(document: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=output.parent, delete=False
    ) as staged:
        json.dump(document, staged, indent=2)
        staged.write("\n")
        staged_path = Path(staged.name)
    try:
        staged_path.replace(output)
    finally:
        staged_path.unlink(missing_ok=True)


def fetch_live_prices(
    config_path: Path,
    output_path: Path,
    fetcher: Callable[[str], bytes] = _fetch_url,
    trading_date: date | None = None,
    quote_url_template: str | None = None,
) -> LivePricesArtifact:
    configs = load_quote_config(config_path)
    quotes: dict[str, Quote] = {}
    fx: dict[str, FXRate] = {}
    try:
        for config in configs:
            template = quote_url_template or os.environ.get(config.secret_name)
            if not template:
                raise LiveFetchError(
                    f"missing configured source secret {config.secret_name}"
                )
            parser = QUOTE_ADAPTERS.get(config.adapter_id)
            if parser is None:
                raise LiveFetchError(f"unsupported quote adapter {config.adapter_id}")
            _validate_quote_url_template(template, config.ticker)
            url = _format_secret_url(template, config.isin, config.ticker)
            result = fetch_and_parse(
                url,
                lambda payload, config=config, parser=parser: parser(
                    payload,
                    config.isin,
                    config.currency,
                    trading_date,
                    config.ticker,
                ),
                fetcher,
            )
            assert isinstance(result, Quote)
            quotes[config.isin] = result
        for pair, url in FRANKFURTER_URLS.items():
            result = fetch_and_parse(
                url,
                lambda payload, pair=pair: parse_frankfurter_rate(payload, pair),
                fetcher,
            )
            assert isinstance(result, FXRate)
            fx[pair] = result
        artifact = LivePricesArtifact(utc_now(), quotes=quotes, fx=fx)
        _atomic_write(artifact.to_dict(), output_path)
        return artifact
    except (OSError, ValueError) as error:
        raise LiveFetchError("live market data update failed") from error


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        artifact = fetch_live_prices(
            Path(args.config),
            Path(args.output),
            trading_date=args.trading_date,
            quote_url_template=args.quote_url_template,
        )
    except (
        LiveFetchError,
        LiveMarketDataError,
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
    ) as error:
        print(f"Live market data update failed: {error}")
        return 1
    print(
        f"Staged live market data: {len(artifact.quotes)} quotes, {len(artifact.fx)} FX rates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import logging
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
logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch and stage live ETF prices and FX rates."
    )
    parser.add_argument("--config", default="data/live_price_config.json")
    parser.add_argument("--output", default="data/live_prices.json")
    parser.add_argument("--trading-date", type=date.fromisoformat, default=None)
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Log per-ETF quote progress without source details.",
    )
    parser.add_argument(
        "--quote-url-template",
        help="Quote URL template for local runs and tests; {isin}, {ticker}, and {currency} are substituted.",
    )
    return parser


def _fetch_url(url: str) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "ETF-Portfolio-Lens/1.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _format_secret_url(
    template: str, isin: str, ticker: str | None, currency: str
) -> str:
    identifier = ticker if ticker is not None else isin
    placeholder = "{ticker}" if ticker is not None else "{isin}"
    return template.replace(placeholder, identifier).replace("{currency}", currency)


def _validate_quote_url_template(
    template: str, ticker: str | None, currency: str
) -> None:
    placeholder = "{ticker}" if ticker is not None else "{isin}"
    formatted_template = template.replace(placeholder, "TESTIDENTIFIER").replace(
        "{currency}", currency
    )
    parsed = urlsplit(formatted_template)
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
    debug: bool = False,
) -> LivePricesArtifact:
    configs = load_quote_config(config_path)
    quotes: dict[str, Quote] = {}
    fx: dict[str, FXRate] = {}
    try:
        for config in configs:
            stage = "configuration"
            if debug:
                logger.debug(
                    "Starting quote for ISIN %s using adapter %s",
                    config.isin,
                    config.adapter_id,
                )
            try:
                template = quote_url_template or os.environ.get(config.secret_name)
                if not template:
                    raise LiveFetchError(
                        f"missing configured source secret {config.secret_name}"
                    )
                parser = QUOTE_ADAPTERS.get(config.adapter_id)
                if parser is None:
                    raise LiveFetchError(
                        f"unsupported quote adapter {config.adapter_id}"
                    )
                _validate_quote_url_template(template, config.ticker, config.currency)
                url = _format_secret_url(
                    template, config.isin, config.ticker, config.currency
                )
                stage = "fetch/parse"
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
            except (LiveFetchError, LiveMarketDataError, OSError, ValueError):
                if debug:
                    logger.debug(
                        "Quote failed for ISIN %s using adapter %s at stage %s",
                        config.isin,
                        config.adapter_id,
                        stage,
                    )
                raise LiveFetchError(
                    f"quote {stage} failed for ISIN {config.isin} "
                    f"using adapter {config.adapter_id}"
                ) from None
            assert isinstance(result, Quote)
            quotes[config.isin] = result
            if debug:
                logger.debug(
                    "Quote succeeded for ISIN %s using adapter %s",
                    config.isin,
                    config.adapter_id,
                )
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
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    try:
        artifact = fetch_live_prices(
            Path(args.config),
            Path(args.output),
            trading_date=args.trading_date,
            quote_url_template=args.quote_url_template,
            debug=args.debug,
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

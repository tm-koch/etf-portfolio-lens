from __future__ import annotations

import argparse
import json
from pathlib import Path

from .live_market_data import LivePricesArtifact


def _format_price(price: float) -> str:
    return f"{price:g}"


def render_live_market_data_summary(artifact: LivePricesArtifact) -> str:
    lines = [
        "## Live market data",
        "",
        f"Generated at: `{artifact.generated_at}`",
        "",
        "### ETF quotes",
        "",
        "| ISIN | Price |",
        "| --- | ---: |",
    ]
    for isin, quote in sorted(artifact.quotes.items()):
        price = (
            f"{quote.currency} {_format_price(quote.price)}"
            if quote.status == "available" and quote.price is not None
            else "Unavailable"
        )
        lines.append(f"| {isin} | {price} |")

    lines.extend(
        [
            "",
            "### Exchange rates",
            "",
            "| Pair | Rate |",
            "| --- | ---: |",
        ]
    )
    for pair, fx_rate in sorted(artifact.fx.items()):
        rate = (
            f"{fx_rate.rate:g}"
            if fx_rate.status == "available" and fx_rate.rate is not None
            else "Unavailable"
        )
        lines.append(f"| {pair} | {rate} |")

    return "\n".join(lines) + "\n"


def render_live_market_data_file(input_path: Path) -> str:
    document = json.loads(input_path.read_text(encoding="utf-8"))
    artifact = LivePricesArtifact.from_dict(document)
    return render_live_market_data_summary(artifact)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render live market data as Markdown")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = render_live_market_data_file(args.input)
    if args.output is None:
        print(summary, end="")
    else:
        args.output.write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()

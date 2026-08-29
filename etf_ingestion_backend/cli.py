from __future__ import annotations

import argparse
from pathlib import Path

from .catalog import build_catalog, write_catalog
from .pipeline import IngestionPipeline
from .registry import load_registry

SECURITY_MASTER_SOURCE_URL = "https://raw.githubusercontent.com/adanos-software/free-ticker-database/main/data/tickers.csv"
DEFAULT_OVERRIDE_PATH = "data/security_overrides.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest ETF holdings into normalized JSON snapshots."
    )
    parser.add_argument(
        "--registry",
        default="data/etf_registry.json",
        help="Path to the ETF registry JSON file.",
    )
    parser.add_argument(
        "--security-master-url",
        default=SECURITY_MASTER_SOURCE_URL,
        help="URL for the ticker security master CSV.",
    )
    parser.add_argument(
        "--output-base",
        default="data/raw",
        help="Base directory for date-stamped outputs.",
    )
    parser.add_argument(
        "--overrides",
        default=DEFAULT_OVERRIDE_PATH,
        help="Path to the holding identity override JSON file.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when any holding cannot be resolved to a canonical identity.",
    )
    parser.add_argument(
        "--isin",
        action="append",
        dest="isins",
        help="Limit ingestion to one or more ETF ISINs.",
    )
    parser.add_argument(
        "--all", action="store_true", help="Ingest every registry entry."
    )
    parser.add_argument(
        "--fixtures",
        action="store_true",
        help="Use local fixture files when registry entries provide fixture paths.",
    )
    parser.add_argument(
        "--update-catalog",
        action="store_true",
        help="Update web/data/catalog.json from the successful ingestion results.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    registry = load_registry(Path(args.registry))
    pipeline = IngestionPipeline(
        registry=registry,
        output_base=Path(args.output_base),
        security_master_source_url=args.security_master_url,
        override_path=Path(args.overrides),
    )

    if args.all or not args.isins:
        selected = registry.entries
    else:
        selected = registry.select_by_isins(args.isins)

    results = pipeline.run(selected, use_fixtures=args.fixtures, strict=args.strict)
    if args.update_catalog:
        catalog = build_catalog(selected, results)
        write_catalog(catalog, Path("web/data/catalog.json"))
    for result in results:
        print(f"{result.etf.isin}: {result.snapshot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import IngestionPipeline
from .registry import load_registry
from .security_master import SecurityMaster


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
        "--security-master",
        default="data/tickers.csv",
        help="Path to the ticker security master CSV.",
    )
    parser.add_argument(
        "--output-base",
        default="data/raw",
        help="Base directory for date-stamped outputs.",
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    registry = load_registry(Path(args.registry))
    security_master = SecurityMaster.from_csv(Path(args.security_master))
    pipeline = IngestionPipeline(
        registry=registry,
        security_master=security_master,
        output_base=Path(args.output_base),
    )

    if args.all or not args.isins:
        selected = registry.entries
    else:
        selected = registry.select_by_isins(args.isins)

    results = pipeline.run(selected, use_fixtures=args.fixtures)
    for result in results:
        print(f"{result.etf.isin}: {result.snapshot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

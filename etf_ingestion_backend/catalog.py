from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Iterable

from .models import ETFSourceEntry, IngestionResult


def build_catalog(
    entries: Iterable[ETFSourceEntry], results: Iterable[IngestionResult]
) -> dict[str, object]:
    result_by_isin = {result.etf.isin: result for result in results}
    selected_entries = [entry for entry in entries if entry.isin in result_by_isin]
    if not selected_entries:
        raise ValueError("Cannot generate a catalog without successful snapshots")

    run_dates = {
        result_by_isin[entry.isin].output_dir.name for entry in selected_entries
    }
    if len(run_dates) != 1:
        raise ValueError("Catalog results must belong to one run date")
    run_date = next(iter(run_dates))

    return {
        "generatedAt": run_date,
        "basis": "share_weighted",
        "etfs": [_catalog_entry(entry, run_date) for entry in selected_entries],
    }


def _catalog_entry(entry: ETFSourceEntry, run_date: str) -> dict[str, object]:
    result: dict[str, object] = {
        "isin": entry.isin,
        "ticker": entry.ticker,
        "name": entry.name,
        "provider": entry.provider,
        "snapshotPath": f"/data/raw/{run_date}/snapshots/{entry.isin}.json",
    }
    for field_name in (
        "share_class_currency",
        "exchange",
        "listing_ticker",
        "listing_currency",
    ):
        value = getattr(entry, field_name)
        if value is not None:
            result[field_name] = value
    return result


def write_catalog(catalog: dict[str, object], target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=target_path.parent,
            prefix=f".{target_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_file.write(payload)
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, target_path)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()

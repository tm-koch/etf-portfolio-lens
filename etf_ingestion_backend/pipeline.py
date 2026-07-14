from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

from .aggregation import aggregate_holdings
from .fetching import copy_fixture, fetch_url
from .models import ETFSnapshot, ETFSourceEntry, IngestionResult
from .normalization import normalize_row
from .parsing import parse_table
from .registry import ETFRegistry
from .security_master import SecurityMaster


@dataclass(slots=True)
class IngestionPipeline:
    registry: ETFRegistry
    security_master: SecurityMaster
    output_base: Path

    def run(
        self, entries: Iterable[ETFSourceEntry], use_fixtures: bool = False
    ) -> list[IngestionResult]:
        run_date = date.today().isoformat()
        output_dir = self.output_base / run_date
        downloads_dir = output_dir / "downloads"
        snapshots_dir = output_dir / "snapshots"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        snapshots_dir.mkdir(parents=True, exist_ok=True)

        results: list[IngestionResult] = []
        for entry in entries:
            if use_fixtures and entry.fixture_path:
                downloaded = copy_fixture(
                    Path(entry.fixture_path), downloads_dir, preferred_name=entry.isin
                )
            else:
                downloaded = fetch_url(
                    entry.source_url, downloads_dir, preferred_name=entry.isin
                )

            parsed = parse_table(
                downloaded.download_path,
                stop_at_empty_row=entry.parser_id == "ubs_xml_xls_v1",
            )
            holdings = [
                normalize_row(
                    row,
                    self.security_master,
                    source_name=entry.provider,
                    parser_id=entry.parser_id,
                )
                for row in parsed.rows
            ]
            aggregates = aggregate_holdings(holdings)
            generated_at = datetime.now(timezone.utc).isoformat()
            snapshot = ETFSnapshot(
                etf=entry,
                as_of=run_date,
                generated_at=generated_at,
                source_url=entry.source_url,
                resolved_download_url=str(downloaded.download_path),
                source_format=entry.expected_format,
                parser_id=entry.parser_id,
                holdings=holdings,
                aggregates=aggregates,
                provenance={
                    "security_master_version": self.security_master.version,
                    "warnings": self.security_master.warnings,
                    "raw_download_path": str(downloaded.download_path),
                    "domicile": self.security_master.lookup_etf_metadata().get(
                        "domicile"
                    ),
                    "base_currency": self.security_master.lookup_etf_metadata().get(
                        "base_currency"
                    ),
                },
            )

            snapshot_path = snapshots_dir / f"{entry.isin}.json"
            snapshot_path.write_text(
                json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            results.append(
                IngestionResult(
                    etf=entry,
                    output_dir=output_dir,
                    snapshot_path=snapshot_path,
                    raw_download_path=downloaded.download_path,
                    snapshot=snapshot,
                )
            )
        return results

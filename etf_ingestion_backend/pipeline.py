from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

from .aggregation import aggregate_holdings
from .fetching import (
    DownloadedSource,
    copy_fixture,
    fetch_amundi_full_holdings,
    fetch_url,
)
from .models import ETFSnapshot, ETFSourceEntry, IngestionResult, NormalizedHolding
from .normalization import normalize_row
from .overrides import OverrideRegistry
from .parsing import parse_table
from .registry import ETFRegistry
from .security_master import SecurityMaster

STRICT_IDENTITY_EXEMPTIONS = {
    "EUR CASH",
    "CHF CASH",
    "CASH COLLATERAL CHF F-GSI",
    "GBP CASH",
    "SWISS MKT IX SEP 26",
}

SPMCHA_CLASSIFICATION_ISINS = {
    "CH0466642201",
    "CH0102484968",
    "CH0025751329",
    "CH0360826991",
    "CH0038388911",
    "CH0025536027",
    "CH0024590272",
    "CH0371153492",
    "CH0468525222",
    "CH0406705126",
    "CH1484953687",
}


def _is_strict_identity_exempt(holding: NormalizedHolding) -> bool:
    return (holding.name or "").strip().upper() in STRICT_IDENTITY_EXEMPTIONS or (
        holding.match and holding.match.status == "excluded"
    )


@dataclass(slots=True)
class IngestionPipeline:
    registry: ETFRegistry
    output_base: Path
    security_master_source_url: str
    override_path: Path | None = None

    def _download_security_master(
        self, downloads_dir: Path
    ) -> tuple[SecurityMaster, DownloadedSource]:
        downloaded = fetch_url(
            self.security_master_source_url,
            downloads_dir,
            preferred_name="tickers",
        )
        return SecurityMaster.from_csv(downloaded.download_path), downloaded

    def run(
        self,
        entries: Iterable[ETFSourceEntry],
        use_fixtures: bool = False,
        strict: bool = False,
    ) -> list[IngestionResult]:
        run_date = date.today().isoformat()
        output_dir = self.output_base / run_date
        downloads_dir = output_dir / "downloads"
        snapshots_dir = output_dir / "snapshots"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        snapshots_dir.mkdir(parents=True, exist_ok=True)

        security_master, security_master_download = self._download_security_master(
            downloads_dir
        )
        overrides = (
            OverrideRegistry.from_json(self.override_path)
            if self.override_path and self.override_path.exists()
            else OverrideRegistry.empty()
        )

        results: list[IngestionResult] = []
        pending: list[tuple[ETFSourceEntry, DownloadedSource, ETFSnapshot]] = []
        failures: list[str] = []
        for entry in entries:
            parsed_rows = None
            if use_fixtures and entry.fixture_path:
                downloaded = copy_fixture(
                    Path(entry.fixture_path), downloads_dir, preferred_name=entry.isin
                )
            elif entry.fetcher_id == "amundi_product_page_v1":
                downloaded, parsed_rows = fetch_amundi_full_holdings(
                    entry.isin,
                    downloads_dir,
                    context=entry.fetcher_context,
                )
            else:
                downloaded = fetch_url(
                    entry.source_url, downloads_dir, preferred_name=entry.isin
                )

            parsed = (
                None
                if parsed_rows is not None
                else self._parse_downloaded_table(entry, downloaded)
            )
            rows = parsed_rows if parsed_rows is not None else parsed.rows
            if entry.isin == "IE00BF20LF40" and len(rows) <= 10:
                raise ValueError(
                    "Incomplete EUMD holdings: expected more than ten rows"
                )
            holdings = [
                normalize_row(
                    row,
                    security_master,
                    source_name=entry.provider,
                    parser_id=entry.parser_id,
                    overrides=overrides,
                )
                for row in rows
            ]
            if strict:
                for index, holding in enumerate(holdings, start=1):
                    if not _is_strict_identity_exempt(holding) and (
                        not holding.company_id
                        or not holding.canonical_name
                        or not holding.match
                        or holding.match.status in {"unmatched", "ambiguous"}
                    ):
                        failures.append(
                            f"{entry.ticker} row {index}: unresolved identity "
                            f"status={holding.match.status if holding.match else 'missing'} "
                            f"name={holding.name or '<unknown>'}"
                        )
                    if holding.isin in SPMCHA_CLASSIFICATION_ISINS and any(
                        not getattr(holding, field)
                        for field in (
                            "company_id",
                            "canonical_name",
                            "sector",
                            "asset_class",
                            "country",
                            "exchange",
                        )
                    ):
                        failures.append(
                            f"{entry.ticker} row {index}: incomplete SPMCHA classification "
                            f"isin={holding.isin}"
                        )
            aggregates = aggregate_holdings(holdings)
            generated_at = datetime.now(timezone.utc).isoformat()
            snapshot = ETFSnapshot(
                etf=entry,
                as_of=run_date,
                generated_at=generated_at,
                source_url=entry.source_url,
                resolved_download_url=str(downloaded.download_path),
                source_format=downloaded.source_format or entry.expected_format,
                parser_id=entry.parser_id,
                holdings=holdings,
                aggregates=aggregates,
                provenance={
                    "security_master_version": security_master.version,
                    "security_master_source_url": self.security_master_source_url,
                    "security_master_download_path": str(
                        security_master_download.download_path
                    ),
                    "warnings": security_master.warnings,
                    "raw_download_path": str(downloaded.download_path),
                    "domicile": security_master.lookup_etf_metadata().get("domicile"),
                    "base_currency": security_master.lookup_etf_metadata().get(
                        "base_currency"
                    ),
                },
            )

            pending.append((entry, downloaded, snapshot))

        if failures:
            raise ValueError(
                "Strict identity validation failed:\n" + "\n".join(failures)
            )

        for entry, downloaded, snapshot in pending:
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

    @staticmethod
    def _parse_downloaded_table(entry: ETFSourceEntry, downloaded: DownloadedSource):
        actual_format = downloaded.download_path.suffix.lower().lstrip(".")
        if actual_format != entry.expected_format.lower():
            raise ValueError(
                f"Download format mismatch for {entry.isin}: "
                f"expected {entry.expected_format}, received {actual_format or 'unknown'}"
            )
        return parse_table(
            downloaded.download_path,
            stop_at_empty_row=entry.parser_id == "ubs_xml_xls_v1",
        )

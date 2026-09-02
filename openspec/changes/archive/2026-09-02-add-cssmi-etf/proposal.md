## Why

ETF Portfolio Lens already supports several iShares funds, but it does not include iShares SMI® ETF (CH), a natural Swiss-market companion to the existing SPI holding. The supplied iShares holdings export and fixture are compatible with the current ingestion path, so adding CSSMI now provides useful Swiss large-cap coverage with a small, well-bounded integration.

## What Changes

- Add CSSMI (`CH0008899764`) to the ETF source registry using the supplied iShares CSV holdings endpoint and existing `ishares_csv_v1` parsing flow.
- Preserve the supplied CSSMI holdings file as an offline fixture and generate its normalized snapshot and web catalog entry.
- Add focused registry, fixture, normalization, snapshot, and catalog coverage for CSSMI.
- Extend controlled identity handling for CSSMI's `LOGN` provider-name variant.
- Ensure cash and derivative rows, including `USD CASH`, are not interpreted as company securities during enrichment or strict validation.

## Capabilities

### New Capabilities

- `cssmi-etf`: Register, ingest, normalize, aggregate, and publish iShares SMI® ETF (CH) holdings.

### Modified Capabilities

- `etf-holdings-ingestion`: Refine strict identity and cash/derivative handling so CSSMI's non-company rows remain excluded from company identity requirements and cannot resolve to unrelated ticker records.

## Impact

- `data/etf_registry.json`, `data/example/CSSMI_holdings.csv`, and `data/security_overrides.json`.
- Python ingestion, normalization, aggregation, and catalog-generation workflows.
- Ingestion and catalog tests plus a new dated CSSMI snapshot under `data/raw/`.
- `web/data/catalog.json` and the frontend's available ETF selection data.

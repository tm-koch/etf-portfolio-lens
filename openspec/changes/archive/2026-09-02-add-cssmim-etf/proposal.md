## Why

The ETF registry currently lacks the iShares SMIM® ETF (CH), preventing the ingestion backend and web catalog from representing this Swiss mid-cap portfolio. The supplied holdings export is compatible with the existing iShares CSV parser and has been verified to pass strict identity validation, so the fund can be added using the established registry-driven workflow.

## What Changes

- Register iShares SMIM® ETF (CH) with ISIN `CH0019852802`, ticker `CSSMIM`, its verified iShares holdings CSV endpoint, and the supplied fixture.
- Add regression coverage for fixture structure, holdings completeness, weight totals, strict identity enrichment, snapshot provenance, and catalog publication.
- Generate the dated normalized snapshot and update the web catalog after successful fixture ingestion.

## Capabilities

### New Capabilities

- `cssmim-etf`: Register and ingest the complete iShares SMIM® ETF (CH) holdings export and publish its normalized snapshot/catalog identity.

### Modified Capabilities

<!-- No existing requirement changes are needed; the current iShares parser and identity-exclusion contract already support this ETF. -->

## Impact

- Backend registry data in `data/etf_registry.json`.
- Offline fixture data in `data/example/CSSMIM_holdings.csv`.
- Python ingestion and regression tests.
- Dated raw/snapshot outputs under `data/raw/` and `web/data/catalog.json`.
- No new parser, fetcher, dependency, or public API is required.

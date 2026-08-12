## Why

The registry currently stops short of this iShares ETF, so the backend cannot ingest its holdings and the web app cannot offer it in the portfolio selector. Adding it now keeps the supported ETF catalog aligned with the desired portfolio choices without changing the existing product model.

## What Changes

- Add a new ETF registry entry for the iShares EUMD holdings source using the existing CSV ingestion path.
- Add backend fixture coverage and snapshot generation for the new ETF so it can be downloaded and normalized like the existing iShares CSV sources.
- Regenerate the published catalog data so the web front-end can surface the new ETF in the portfolio add flow.
- Keep the existing ETF entries unchanged.

## Capabilities

### New Capabilities
- `portfolio-etf-selection`: supported ETFs that are present in the registry and have generated snapshots SHALL appear in the published catalog and be selectable in the portfolio builder.

### Modified Capabilities

## Impact

- `data/etf_registry.json` will gain a new source entry.
- `data/example/` may need a new fixture file for offline ingestion tests.
- `etf_ingestion_backend/` should be exercised through the existing iShares CSV parser and snapshot pipeline.
- `web/data/catalog.json` and the portfolio selection UI will need refreshed catalog data so the ETF is visible to users.

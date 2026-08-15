## Why

The registry and web catalog currently identify ISIN `LU0908500753` with an outdated Amundi share-class name and legacy product URL. Correcting the metadata keeps the ingestion registry, generated snapshots, and user-facing ETF catalog aligned with the current Amundi product page.

## What Changes

- Update the registry name for `LU0908500753` to `Amundi Core Stoxx Europe 600 UCITS ETF Acc`.
- Replace the legacy Amundi URL with the current canonical product page URL.
- Update the matching entry in `web/data/catalog.json` so the user-facing catalog uses the same current name.
- Preserve the existing ticker, ISIN, provider, expected `xlsx` format, parser ID, fixture path, and historical snapshot files.
- Keep resolving the current holdings download endpoint out of scope for this metadata-only change.

## Capabilities

### New Capabilities

- `etf-registry-metadata`: Canonical ETF identity metadata shared by ingestion configuration and the web catalog.

### Modified Capabilities

## Impact

- `data/etf_registry.json`: Correct the Amundi name and canonical product URL.
- `web/data/catalog.json`: Synchronize the displayed Amundi fund name.
- Existing snapshots remain historical records and are not rewritten.
- No parser, download resolver, API, or dependency changes are included.

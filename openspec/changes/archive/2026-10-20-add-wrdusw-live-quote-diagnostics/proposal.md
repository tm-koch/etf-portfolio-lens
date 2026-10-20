# Proposal

## Why

The live refresh currently omits the UBS Core MSCI World ETF (`IE00BD4TXV59`), even though its SIX listing is CHF-denominated. When any configured quote source fails, the workflow also reports the parsing or fetch error without identifying which ISIN failed, making provider issues difficult to isolate.

## What Changes

- Configure a CHF live quote for `IE00BD4TXV59` using the existing Swiss CSV adapter and secret-backed Swiss URL template, without changing its fixture-only holdings-ingestion status.
- Include the failing ETF ISIN and adapter in sanitized quote-fetch failures, and add opt-in debug progress that the GitHub workflow enables.
- Keep quote URLs, credentials, and raw provider responses out of logs and artifacts; preserve all-or-nothing publication.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `live-market-data`: Add the CHF quote for `IE00BD4TXV59`, revise the fixture-only quote exclusion, and specify privacy-safe per-ISIN failure diagnostics.

## Impact

- `data/live_price_config.json` and live-market-data configuration tests.
- `etf_ingestion_backend/live_cli.py` and quote-fetch error/logging behavior in the live market-data backend.
- `.github/workflows/live-market-data.yml` to enable debug progress during scheduled and manual refreshes.
- The live-market-data OpenSpec capability and its change delta.

## Why

ETF Portfolio Lens currently relies on prices and values imported from a broker PDF, uses a fixed EUR-to-CHF conversion assumption, and has no scheduled market-data refresh. This prevents the portfolio view from valuing positions with current prices and leaves the published PWA without a reliable, timestamped live-data snapshot.

## What Changes

- Add a provider-agnostic live ETF quote pipeline with source-specific URL templates, parsers, and normalized quote output.
- Support the initial Swiss CSV trade-data provider, selecting the latest valid price by timestamp and retaining quote provenance without publishing provider identity or secret URLs.
- Add latest daily FX reference-rate retrieval for EUR/CHF and USD/CHF through Frankfurter using `https://api.frankfurter.app/latest?from=EUR&to=CHF` and `https://api.frankfurter.app/latest?from=USD&to=CHF`.
- Add a daily GitHub Actions workflow scheduled for 22:00 fixed CET (UTC+1 year-round), with manual dispatch support and per-ETF secret-backed URL templates.
- Make quote and FX publication atomic: any required fetch, parse, validation, or FX failure leaves the previous published data unchanged.
- Publish `data/live_prices.json` together with the GitHub Pages site and expose quote/FX timestamps and freshness state to the PWA.
- Add hybrid portfolio valuation: use live prices when available and fall back to imported broker values when unavailable, with visible provenance and fallback status.
- Replace the fixed EUR-to-CHF import conversion with the selected live FX rate when current valuation is used, while preserving imported values for fallback and historical context.
- Extend supported displayed currencies and valuation calculations to USD/CHF.
- Preserve compatibility with existing portfolio persistence, full/private sharing, offline caching, and dated holdings snapshots.

## Capabilities

### New Capabilities

- `live-market-data`: Define normalized ETF quotes, FX rates, source configuration, parser behavior, validation, timestamps, failure policy, and hybrid valuation inputs.
- `scheduled-market-data-publication`: Define the scheduled/manual GitHub Actions workflow, secret handling, atomic output, dated commits, and GitHub Pages publication behavior.

### Modified Capabilities

- `saxo-pdf-portfolio-import`: Imported broker values remain available as hybrid fallbacks, while live FX may be used for current valuation instead of the fixed conversion.
- `portfolio-currency-display`: Support USD values and distinguish imported, live, and fallback valuation states.
- `home-tab`: Calculate the portfolio total from effective hybrid valuations and expose data availability/fallback state.
- `portfolio-sharing`: Preserve valuation mode and compatibility of full/private share payloads without leaking private absolute values.
- `offline-web-runtime`: Cache the published live-price artifact with network-first behavior and offline fallback.
- `build-provenance`: Include live-data generation and effective data status without exposing provider identities or secrets.
- `pwa-publishing`: Copy and validate the live-price artifact as part of the published Pages tree.

## Impact

Affected areas include a new Python live-data fetch/parser module and CLI entry point, public ETF quote configuration, Frankfurter FX retrieval, GitHub Actions workflow and repository secrets, `data/live_prices.json`, the GitHub Pages publisher, service-worker runtime caching, frontend data loading and portfolio valuation state, import review behavior, sharing payload versioning, documentation, and Python/JavaScript/workflow tests. Existing holdings ingestion and dated ETF snapshots remain separate from live quote data.

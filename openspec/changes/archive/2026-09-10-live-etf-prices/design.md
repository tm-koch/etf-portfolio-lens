## Context

The repository has a Python holdings-ingestion backend with provider-specific download/parser identifiers, dated JSON snapshots under `data/raw`, a catalog consumed by the browser, a PowerShell GitHub Pages publisher, and a PWA service worker with network-first runtime data caching. Portfolio import currently parses Saxo PDFs in the browser and persists imported price/value fields in local storage. EUR-to-CHF conversion is currently fixed at `1`, and no live quote or FX artifact exists.

Live quotes are a separate data domain from ETF constituent holdings. The first quote source returns a semicolon-delimited Swiss trade CSV whose header is `Time;Price;Volume`; the latest valid combined date/time is the valuation price. Each ETF configuration entry names its own secret-backed URL template, while public configuration identifies only opaque adapters, currencies, and secret names. The workflow must run daily at 22:00 CET/local Swiss time, support manual dispatch, and publish no partial update.

## Goals / Non-Goals

**Goals:**

- Define a normalized, versioned live-price and FX artifact consumed by both the publisher and browser.
- Support multiple ETF quote providers through adapter-specific URL formatting and parsers.
- Implement the initial Swiss CSV trade parser and EUR/CHF plus USD/CHF latest daily reference-rate retrieval through Frankfurter.
- Make scheduled and manual GitHub Actions runs reproducible, secret-safe, and atomic.
- Provide hybrid portfolio valuation using live values first and imported broker values as explicit fallbacks.
- Preserve offline PWA operation, existing holdings snapshots, local PDF import privacy, and share-link privacy.

**Non-Goals:**

- Direct browser requests to quote providers.
- Publishing provider names, source URLs, credentials, or raw quote responses.
- True network anonymity from the quote provider; hiding configuration from the public repository is the supported privacy boundary.
- Intraday streaming, websockets, order-book data, or portfolio broker synchronization.
- Rejecting FX data solely because it is old; timestamps are retained for transparency.
- Replacing the existing ETF holdings ingestion pipeline.

## Decisions

1. **Use a separate live-data pipeline and artifact.** Holdings snapshots remain dated constituent data. Live quotes and FX rates are written to `data/live_prices.json` with schema version, generation timestamp, quote timestamps, currencies, and status fields. This avoids coupling high-frequency quote refreshes to holdings ingestion.

2. **Use adapter IDs with per-ETF secret-backed URL templates.** Public configuration maps each ISIN to an opaque parser/source adapter, currency, and `quote_url_template_secret` environment name. The runtime reads the corresponding template from the environment, formats `{isin}`, dispatches to the configured adapter, and never logs or serializes the resolved URL. A legacy top-level secret name remains a fallback for existing configurations, but new entries are explicit so different providers can coexist.

3. **Select the latest valid quote by timestamp.** The Swiss CSV parser combines the file trading date with each `Time` value, validates numeric price and timestamp fields, and selects the greatest timestamp. Volume is diagnostic only. Rows with invalid values are ignored; no valid row is a provider failure.

4. **Treat FX as a first-class normalized input.** The Frankfurter adapter returns the latest daily reference rates for EUR/CHF and USD/CHF with timestamps. The valuation layer converts an ETF quote currency to CHF using the corresponding pair and leaves CHF unchanged. Unsupported currencies remain unvalued and visible.

5. **Make the workflow all-or-nothing.** The fetch command stages quotes and FX in a temporary directory, validates the complete document, then atomically replaces the working-tree artifact. The workflow commits and publishes only after validation succeeds. Any required source or FX failure exits non-zero and leaves the previous artifact and Pages deployment untouched.

6. **Use hybrid valuation with explicit provenance.** Each persisted position retains imported fields and a valuation mode. Effective valuation uses a valid live quote plus FX when available; otherwise it uses the imported value and marks the position as fallback. Missing both sources produces an unavailable value rather than an invented number.

7. **Schedule against a declared timezone policy.** The workflow interprets 22:00 CET as fixed UTC+1 year-round and schedules the corresponding 21:00 UTC GitHub Actions cron. It does not shift for CEST. Manual dispatch bypasses the schedule gate.

8. **Publish live data as same-origin runtime data.** The publisher copies `data/live_prices.json` to the Pages root data tree, build metadata records its generation timestamp and aggregate status, and the service worker caches it using the existing network-first runtime path. The browser displays the artifact timestamp and fallback state when offline.

9. **Version share payloads conservatively.** Existing full and private payloads remain readable. New full payloads may include valuation mode and imported fields, while private payloads contain only ISIN and relative units. Live quotes are resolved from the recipient’s latest published artifact and are never embedded in private links.

## Risks / Trade-offs

- **[Provider format or access changes]** -> Keep parsers isolated by adapter ID, retain fixture-based tests, validate schema and timestamps, and fail atomically rather than publishing suspect data.
- **[Secret URL exposure through logs]** -> Disable verbose request logging, redact URL/error details, and test workflow output handling.
- **[“Anonymous” provider usage is misunderstood]** -> Document that secrets hide configuration from the public site but do not hide the GitHub runner from the provider; use a proxy only as a separate future capability.
- **[Fixed CET differs from Swiss summer local time]** -> Document that the workflow remains at 22:00 UTC+1 year-round and is 23:00 Europe/Zurich during CEST.
- **[Stale weekend quote]** -> Preserve quote timestamps and status in the artifact and UI; do not reject solely for age because the requirement permits old FX/market data.
- **[Offline cache serves old quotes]** -> Display the live-data generation time and distinguish cached/offline fallback from current online data.
- **[Existing local portfolios lack new fields]** -> Treat absent valuation mode as legacy imported mode and migrate in memory without invalidating stored portfolios or links.

## Migration Plan

1. Add quote/FX configuration, adapters, normalized models, CLI command, fixtures, and tests without changing existing holdings ingestion.
2. Generate an initial valid `data/live_prices.json` fixture and update the publisher, build metadata, and service-worker runtime handling.
3. Add frontend hybrid valuation and import review selection with backward-compatible local-storage normalization and share payload version handling.
4. Add the workflow with manual dispatch first; verify secret redaction, atomic failure behavior, artifact validation, and Pages publication in a controlled run.
5. Enable the daily schedule after source secrets are configured; the fixed CET timezone policy is already defined.
6. Roll back by disabling the workflow and reverting the live artifact/frontend deployment; existing imported-value portfolios remain usable because live valuation is additive and fallback-aware.

## Open Questions

- Confirm the Swiss quote URL template's exact endpoint shape and required `{isin}` substitution before production use.
- Confirm Frankfurter usage and its licensing/redistribution terms before production publication.
- Unchanged quote content will skip a commit by default; confirm only if a separate Pages publication check is required on no-change days.

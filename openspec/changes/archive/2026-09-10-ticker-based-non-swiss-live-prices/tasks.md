## 1. Quote Model and Adapter Support

- [x] 1.1 Extend quote configuration and normalized quote models with optional provider ticker data while keeping ISIN as the canonical identity and artifact key.
- [x] 1.2 Add adapter-aware identifier validation and URL-template formatting for ISIN-based and ticker-based adapters.
- [x] 1.3 Implement the `yahoo_chart_v1` parser for EUR regular market price and Unix timestamp data, including provider-error, structure, currency, price, and timestamp validation.
- [x] 1.4 Register the Yahoo adapter and wire ticker-based failures through the existing atomic pipeline error handling.

## 2. Configuration and Secrets

- [x] 2.1 Add `IE00BF20LF40` with ticker `EUMD.L`, `LU0908500753` with ticker `LYP6.DE`, and `IE00BCLWRD08` with ticker `IS3H.DE` to live-price configuration using EUR and `YAHOO_QUOTE_URL_TEMPLATE`.
- [x] 2.2 Add configuration validation that every registry ETF intended for live pricing has the required adapter identifier, currency, secret name, and provider-specific ticker.
- [x] 2.3 Document the `YAHOO_QUOTE_URL_TEMPLATE` local/CI variable convention without committing a concrete secret value or provider URL.

## 3. Workflow and Publication

- [x] 3.1 Map `YAHOO_QUOTE_URL_TEMPLATE` from GitHub repository secrets into the live market-data workflow without exposing its value.
- [x] 3.2 Add a `main` push trigger for relevant source, configuration, workflow, backend, parser, and publication paths while excluding `data/live_prices.json` to prevent self-triggering.
- [x] 3.3 Preserve manual dispatch, daily scheduling, required permissions, atomic artifact commits, and Pages publication for both Swiss and ticker-based quotes.

## 4. Tests and Artifact Verification

- [x] 4.1 Add valid and malformed Yahoo chart fixtures covering provider errors, missing metadata, non-EUR currency, invalid prices, and invalid timestamps.
- [x] 4.2 Add unit tests for ticker-aware URL formatting, ticker provenance, configuration validation, and the three registry/config mappings while preserving Swiss adapter coverage.
- [x] 4.3 Add workflow contract tests for the push path filter, Yahoo secret mapping, and artifact recursion guard.
- [x] 4.4 Run the focused live-data and workflow tests, the full test suite, and the live-price fetch validation; regenerate the ISIN-keyed artifact only after all sources and FX data succeed.

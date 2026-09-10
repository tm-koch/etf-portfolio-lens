## 1. Live-data domain and configuration

- [x] 1.1 Define the versioned live-price artifact schema and validation model for ETF quotes, quote timestamps, currencies, statuses, and generation metadata.
- [x] 1.2 Add public ETF quote configuration mapping supported ISINs to opaque adapter IDs, currencies, and per-ETF secret references with no embedded provider URLs.
- [x] 1.3 Add normalized FX model and Frankfurter adapter configuration for latest daily EUR/CHF and USD/CHF reference rates.
- [x] 1.4 Add tests for schema validation, supported currencies, timestamp parsing, prohibited secret/source fields, and legacy/missing-data behavior.

## 2. Provider adapters and fetch command

- [x] 2.1 Implement provider adapter interfaces for URL formatting, response fetching, parsing, and normalized quote output.
- [x] 2.2 Implement the Swiss semicolon-delimited CSV adapter using the trading date and latest valid `Time;Price;Volume` row.
- [x] 2.3 Implement the Frankfurter FX adapter for EUR/CHF and USD/CHF with timestamp preservation.
- [x] 2.4 Add a CLI command that loads configuration, reads each ETF's secret-backed URL template or explicit test parameter, dispatches the configured adapter, fetches all required quotes and FX rates, validates the complete result, and stages the artifact in a temporary location.
- [x] 2.5 Ensure fetch errors redact resolved URLs and response secrets from logs and return a non-zero exit code.
- [x] 2.6 Add fixture-based tests for the attached Swiss CSV, malformed rows, empty responses, latest-timestamp selection, FX responses, and all-or-nothing failure behavior.

## 3. Atomic data update and publishing integration

- [x] 3.1 Implement atomic replacement of `data/live_prices.json` only after complete quote and FX validation succeeds.
- [x] 3.2 Extend the GitHub Pages publisher to copy and validate `data/live_prices.json` and include its generation/status metadata in `build-info.json`.
- [x] 3.3 Extend publish/deployment validation and web contract tests for the live artifact path, schema, and secret-free contents.
- [x] 3.4 Update PWA runtime-data caching and cache-generation tests so quote changes use runtime caching while shell changes remain cache-coherent.

## 4. Portfolio valuation and import behavior

- [x] 4.1 Add browser loading and validation for `data/live_prices.json`, including online failure and cached/unavailable states.
- [x] 4.2 Add backward-compatible portfolio normalization for imported fields and effective live/fallback value.
- [x] 4.3 Implement hybrid effective valuation using live quote plus EUR/CHF or USD/CHF conversion, imported CHF fallback, and explicit unavailable status.
- [x] 4.4 Update Saxo import review to retain imported values and allow imported versus latest valuation selection without changing the existing portfolio until confirmation.
- [x] 4.5 Update Portfolio, Home, Compare, and Explore calculations and displays to use effective hybrid values and show live/fallback/unavailable status.
- [x] 4.6 Add USD formatting and ensure EUR/CHF/USD values retain the existing two-decimal and apostrophe-separated presentation.
- [x] 4.7 Add frontend tests for live valuation, imported fallback, missing FX, mixed totals, weekend timestamps, legacy local storage, and import cancellation.

## 5. Sharing and provenance

- [x] 5.1 Version full share payloads to preserve valuation mode and imported fallback fields while accepting legacy full payloads.
- [x] 5.2 Keep private share payloads limited to ISIN and relative units and add tests rejecting absolute market/FX data.
- [x] 5.3 Extend build-details UI and provenance loading to show live-data generation/status without exposing source identity or URLs.
- [x] 5.4 Add compatibility tests for existing full/private share links and current selection feedback behavior.

## 6. GitHub Actions workflow

- [x] 6.1 Add a manually dispatchable and scheduled workflow at 21:00 UTC for fixed 22:00 CET year-round, with concurrency control and minimal write permissions.
- [x] 6.2 Configure the documented per-provider quote-template repository secrets, including `SWISS_QUOTE_URL_TEMPLATE`, ensuring workflow logs redact their values.
- [x] 6.3 Run the fetch command, verify staged output, commit successful updates with the date, and invoke GitHub Pages publication only after validation succeeds.
- [x] 6.4 Ensure failed runs preserve the previous live artifact and Pages deployment and do not create partial commits.
- [x] 6.5 Add workflow/documentation checks for manual execution, schedule policy, failure behavior, and no provider identity in public output.

## 7. Documentation and end-to-end verification

- [x] 7.1 Document live-data configuration, supported adapters, secret setup, FX assumptions, hybrid valuation, fallback behavior, and the anonymity boundary.
- [x] 7.2 Document the fixed CET schedule and its difference from Europe/Zurich local time during daylight-saving months.
- [x] 7.3 Run the full Python, JavaScript, publisher, and deployment validation suites with an offline fixture workflow.
- [ ] 7.4 Perform a controlled manual workflow run and verify the published artifact, build metadata, PWA cache behavior, and portfolio valuation end to end.

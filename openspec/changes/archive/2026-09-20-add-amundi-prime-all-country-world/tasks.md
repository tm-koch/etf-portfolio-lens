## 1. Confirm Source Metadata

- [x] 1.1 Confirm the exact Amundi product URL, canonical display name, and registry ticker for `IE0009HF1MK9`.
- [x] 1.2 Confirm the Swiss quote provider endpoint/template and lookup identifier for the `WEBGCHF SW` CHF listing.
- [x] 1.3 Decide and document the registry field names for share-class currency, exchange, listing ticker, and listing currency, preserving compatibility for existing entries.

## 2. Implement Amundi Holdings Support

- [x] 2.1 Add `IE0009HF1MK9` to `data/etf_registry.json` using `amundi_product_page_v1`, `amundi_landing_xlsx_v1`, and the supplied workbook fixture.
- [x] 2.2 Update Amundi parsing or validation to exclude rows without a valid holding ISIN and numeric weight while retaining fractional holdings.
- [x] 2.3 Add fixture tests for headers, valid holding count, weight tolerance, footer exclusion, and preservation of the final valid holding.
- [x] 2.4 Add an ingestion test proving the new registry entry produces a snapshot with the correct registry identity and complete holdings.
- [x] 2.5 Run offline ingestion for the new ISIN and verify no partial snapshot is published when completeness validation fails.

## 3. Add Registry and Catalog Metadata

- [x] 3.1 Add explicit share-class/fund currency and intended listing metadata for the new ETF without requiring legacy entries to supply the new fields.
- [x] 3.2 Update catalog generation or catalog payloads if listing metadata must be exposed to the web application.
- [x] 3.3 Generate and verify the new `web/data/catalog.json` entry without modifying historical snapshots.

## 4. Add Live Market Data

- [x] 4.1 Add the new CHF Swiss quote configuration for `IE0009HF1MK9`, using the verified provider secret reference and lookup identifier.
- [x] 4.2 Add live configuration tests for the new ISIN, CHF adapter/currency, opaque secret handling, and preserved existing quote entries.
- [x] 4.3 Add or update live fixture assertions for a CHF quote and confirm CHF valuation does not consume USD/CHF.
- [x] 4.4 Confirm the existing live CLI continues to publish both EUR/CHF and USD/CHF for configurations requiring them.

## 5. Fix Saxo Currency Parsing and Valuation Coverage

- [x] 5.1 Extend Saxo section-level and row-level currency matching to include USD.
- [x] 5.2 Add Saxo fixtures for USD section/row parsing and the CHF `WEBGCHF SW` row, asserting shares, price, value, and source currency.
- [x] 5.3 Verify imported USD positions use USD/CHF while imported CHF positions remain unconverted.
- [x] 5.4 Verify missing USD/CHF leaves USD valuation unavailable rather than treating the source as CHF.

## 6. Validate and Publish

- [x] 6.1 Run focused ingestion, live-market-data, portfolio-import, and web contract tests.
- [x] 6.2 Run the full Python and Node-backed test suite and resolve only regressions caused by this change.
- [x] 6.3 Refresh derived live/catalog artifacts through the existing repository workflows and inspect the resulting public schemas for URLs or secrets.
- [x] 6.4 Run PWA/deployment validation and document the final generated snapshot and quote timestamps.

# Tasks

## 1. Register and ingest holdings

- [x] 1.1 Add the three ETF entries to `data/etf_registry.json` with supplied fixture paths, existing parser IDs, and separate share-class/listing metadata; mark UBS Core MSCI World fixture-only, then verify registry validation and complete supported downloads for both iShares URLs.
- [x] 1.2 Run fixture ingestion for all three ISINs and verify snapshot row counts of 3,094 for EIMI, 398 for IMEA, and 1,181 for UBS Core MSCI World, including retention of valid non-equity rows.
- [x] 1.3 Review identity-enrichment diagnostics from the new snapshots; add only independently verified overrides if required and verify them with focused ingestion tests.
- [x] 1.4 Generate the web catalog and verify each ETF is selectable with registry-matching ISIN, name, ticker, and provider; confirm no existing historical snapshot changed.

## 2. Configure live quotes

- [x] 2.1 Extend Swiss URL-template formatting and validation to support `{currency}` while retaining `{isin}` and `{ticker}` behavior; add focused tests for CHF, USD, and existing templates without a currency placeholder.
- [x] 2.2 Add quote configuration for EIMI USD and IMEA CHF; verify config validation, normalized records for both ISINs, and absence of a quote entry for fixture-only UBS Core MSCI World.
- [ ] 2.3 Update the external `SWISS_QUOTE_URL_TEMPLATE` value to interpolate the configured currency and verify existing CHF entries and the new EIMI USD entry resolve and parse successfully.

## 3. Integration verification

- [x] 3.1 Run focused ingestion, catalog, and live-market-data test suites; verify all new requirements pass and existing quote entries remain present.
- [x] 3.2 Run `openspec validate add-three-global-etfs-and-live-quotes --strict` and resolve any artifact or scenario validation errors.
## Why

The portfolio database cannot currently represent Amundi Prime All Country World UCITS ETF Dist (`IE0009HF1MK9`), even though the existing Amundi full-holdings importer can retrieve its composition. The product has a USD share-class currency and separate SIX listings in CHF (`WEBGCHF SW`) and USD (`WEBG SW`), so adding it also requires the application to preserve the currency supplied by the selected source rather than inferring it from the fund currency.

## What Changes

- Add `IE0009HF1MK9` to the ETF registry with its canonical Amundi identity, supplied holdings fixture, and reusable `amundi_product_page_v1` fetch strategy.
- Validate and ingest the supplied full-fund holdings workbook without retaining Amundi footer and disclaimer rows as holdings.
- Add live quote configuration for the intended SIX CHF listing, preserving CHF as the quote currency in normalized live data.
- Retain the existing USD/CHF FX path for any USD source or USD listing without converting CHF source data a second time.
- Extend Saxo PDF parsing so USD-denominated sections and rows are recognized while imported source currency remains authoritative.
- Add explicit product/listing metadata where needed to distinguish fund currency, trading venue, listing ticker, and quote currency.
- Regenerate the catalog and live-price fixtures only as part of implementation; do not rewrite historical snapshots.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `etf-holdings-ingestion`: require the new Amundi product to use the full composition importer and ensure the supplied workbook produces only valid holdings rows with completeness validation.
- `etf-registry-metadata`: require canonical metadata and explicit listing/source currency metadata for the new Amundi ETF.
- `live-market-data`: add the new SIX quote configuration and preserve the quote currency returned by the configured source while continuing to publish USD/CHF when USD valuation requires it.
- `portfolio-currency-display`: ensure imported and live source currencies remain authoritative for displayed prices and CHF conversion, including USD Saxo rows and CHF live quotes for a USD share class.

## Impact

- Registry and fixture data: `data/etf_registry.json`, `data/live_price_config.json`, and the supplied Amundi workbook.
- Python ingestion and live-data models/configuration, including registry metadata validation and quote configuration tests.
- JavaScript Saxo import parsing and focused import/valuation tests.
- Generated `web/data/catalog.json` and, when live data is refreshed, `data/live_prices.json`.
- OpenSpec requirements and implementation tasks; no new external dependency is expected.

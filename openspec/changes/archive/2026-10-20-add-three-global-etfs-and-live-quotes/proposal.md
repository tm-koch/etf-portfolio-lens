# Proposal

## Why

The catalog does not yet include three requested broad-market ETFs, so portfolios holding them cannot use their supplied holdings for exposure analysis. Adding the ETFs with independent share-class and quote currencies will also make their holdings and live prices available without conflating fund currency with listing currency.

## What Changes

- Register iShares Core MSCI Europe UCITS ETF EUR (Acc) (`IE00B4K48X80`), iShares Core MSCI EM IMI UCITS ETF (`IE00BKM4GZ66`), and UBS Core MSCI World UCITS ETF USD acc (`IE00BD4TXV59`) with their supplied holdings fixtures and existing parser families.
- Include the ETFs in generated snapshots and the selectable web catalog while preserving existing historical snapshots.
- Configure live quotes for the intended iShares listings: IMEA in CHF and EIMI in USD; retain each fund's share-class currency separately. Register UBS Core MSCI World from its supplied fixture only, without a live quote or automated source refresh.
- Extend Swiss quote URL-template formatting and validation to accept `{currency}` so one configured template can form the currency-specific quote path. USD quote parsing is already supported.
- Keep the existing holdings and quote artifact contracts, and add focused validation for the new registry entries, fixtures, catalog metadata, and quote currencies.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `etf-holdings-ingestion`: Require complete ingestion of the three supplied holdings sets using existing parser behavior and fixture mode.
- `etf-registry-metadata`: Require canonical registry and generated catalog entries for the three ETFs, including distinct share-class and listing quote currencies where applicable.
- `live-market-data`: Require currency-aware formatting for Swiss quote templates and normalized live quote entries for the three configured ISINs.

## Impact

Affected areas include `data/etf_registry.json`, `data/live_price_config.json`, `ETFSourceEntry` fixture-only handling, the live quote URL formatter and its validation, fixture-based ingestion and catalog generation, and focused tests. Existing parser implementations should be reused; source URL checks for the two iShares entries and fixture completeness checks will confirm whether any parser deviation is needed.
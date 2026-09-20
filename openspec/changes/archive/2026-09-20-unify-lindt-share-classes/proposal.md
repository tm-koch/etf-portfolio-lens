## Why

The two listed Lindt share classes, `CH0010570759` (`LISN`) and `CH0010570767` (`LISP`), currently inherit different canonical names from the security master. That produces different automatically derived `company_id` values, so portfolio company aggregation treats them as separate companies even though both represent Chocoladefabriken Lindt & Spruengli AG.

## What Changes

- Add exact-ISIN identity overrides for both Lindt share classes.
- Assign both share classes the stable company ID `chocoladefabriken-lindt-spruengli-ag`.
- Display both share classes as `Chocoladefabriken Lindt & Spruengli AG` while retaining their original tickers and ISINs.
- Preserve raw provider names and security-master provenance for auditability.
- Add regression coverage for unified identity and unrelated-ISIN isolation.
- Regenerate current `2026-09-20` snapshots containing either share class; leave historical snapshots unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `etf-holdings-ingestion`: Exact-ISIN overrides SHALL be able to assign multiple distinct share-class instruments to one canonical company identity and display name for aggregation.

## Impact

- `data/security_overrides.json` gains entries for `CH0010570759` and `CH0010570767`.
- Current generated snapshots and their company aggregation keys are updated; the web catalog and frontend aggregation logic require no code changes.
- Ingestion tests and generated snapshot validation are affected. Existing source fields, share-class instruments, prices, weights, and valuation behavior remain unchanged.

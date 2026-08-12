## Why

Sector labels currently pass through the backend with provider-specific wording and localized translations, which makes portfolio rollups and snapshots inconsistent with a standardized GIC-style sector taxonomy. Normalizing the full sector vocabulary now reduces ambiguity in comparisons and keeps the backend outputs aligned across ETF providers.

## What Changes

- Normalize sector labels in the ingestion backend to a standard GIC-style taxonomy before they are written into snapshots and aggregates.
- Translate known source labels, localized sector names, and abbreviations to canonical GIC sector names, including `Communication` → `Communication Services`.
- Cover the full observed sector vocabulary rather than a single one-off replacement so source files from different providers converge on the same canonical buckets.
- Preserve raw source sector text in provenance so the original source data remains inspectable.
- Keep region and currency aggregation behavior unchanged.

## Capabilities

### New Capabilities
- `gic-sector-normalization`: sector labels from ETF source files and security master enrichment SHALL be normalized to a consistent GIC-style sector taxonomy before snapshot aggregation and rendering, covering all known sector aliases in the current data set.

### Modified Capabilities
- `etf-holdings-ingestion`: sector fields in normalized holdings and sector aggregates change from source-specific labels to normalized GIC-style labels.

## Impact

- `etf_ingestion_backend/normalization.py` will need a sector normalization step.
- `etf_ingestion_backend/security_master.py` may need to expose or map standardized sector names consistently.
- Snapshot JSON, aggregate sector weights, and any UI display that reads sector labels will reflect the normalized taxonomy.
- Regression tests should cover the specific `Communication` → `Communication Services` translation, a localized sector label, and at least one additional alias from the current source vocabulary.
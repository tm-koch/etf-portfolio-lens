## Why

The current aggregate weights are not consistently derived from the final normalized holdings state after missing fields are enriched. That makes sector, region, and currency summaries vulnerable to stale or incomplete source data instead of reflecting the actual holdings output.

## What Changes

- Recompute `sector_weights`, `region_weights`, and `currency_weights` from the final holding records after enrichment and fallback field filling.
- Ensure aggregate totals reflect the normalized holdings that are written to the snapshot, not the partially parsed source rows.
- Keep the existing snapshot format intact while making the aggregate values more accurate and deterministic.

## Capabilities

### New Capabilities
- `derived-portfolio-aggregates`: derive portfolio aggregate weights from the final holdings output so summaries stay aligned with enriched holding data.

### Modified Capabilities


## Impact

Affects the ingestion pipeline, aggregate calculation logic, snapshot generation, and regression tests that validate portfolio summary output.

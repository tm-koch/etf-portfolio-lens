## Why

The ingestion backend currently writes `weight_pct` values as fractions such as `0.2517`, even though the field name and downstream UI contract imply percentage values. That makes snapshot data hard to read directly and can cause 100x display errors in consumers that format the values as percentages.

## What Changes

- Update the backend snapshot generation path so `weight_pct` values in holdings, `sector_weights`, `region_weights`, and `currency_weights` are emitted as percentage numbers in the 0-100 range.
- Keep the `weight_pct` field name, but change its unit semantics from fraction to percentage to match the name and consumer expectations.
- Regenerate or validate affected snapshots so sample data reflects the new unit contract.
- **BREAKING**: Existing JSON consumers that expect `weight_pct` to be a 0-1 fraction will need to adjust.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `etf-holdings-ingestion`: the canonical snapshot contract changes so holding and aggregate `weight_pct` values, including `sector_weights`, `region_weights`, and `currency_weights`, are written as percentages instead of fractions.

## Impact

- Affects the Python ingestion pipeline under `etf_ingestion_backend/`, especially normalization and aggregate generation.
- Affects snapshot JSON output written to `data/raw/.../snapshots/*.json`.
- Affects any UI or downstream tooling that reads `weight_pct` values from the published snapshots.

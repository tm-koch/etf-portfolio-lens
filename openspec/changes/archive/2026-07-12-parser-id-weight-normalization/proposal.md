## Why

Some ETF sources already publish `Weight %` values as percentages, while others publish fractional weights that must be scaled. A blanket conversion in the backend produces 100x errors for percent-based sources and makes the published snapshot contract inconsistent.

## What Changes

- Normalize holding weights based on the parser ID that produced the source file.
- Keep percent-based sources unchanged and scale fraction-based sources to percentage numbers.
- Add a backend validation check that the sum of weights for each topic stays at or below 100 percent, within a small rounding tolerance.
- Keep snapshot field names unchanged while correcting unit handling in the backend.

## Capabilities

### New Capabilities
- `parser-id-weight-normalization`: ETF ingestion selects the correct weight unit conversion per parser and validates topic totals.

### Modified Capabilities
- `etf-holdings-ingestion`: the ingestion contract changes so `weight_pct` values are normalized per parser source semantics and validated against percent totals.

## Impact

- Affects parser-aware normalization in `etf_ingestion_backend/normalization.py`.
- Affects aggregate generation and validation in `etf_ingestion_backend/aggregation.py` or related backend helpers.
- Affects generated snapshot JSON for affected ETFs.
- May require snapshot regeneration for percent-based and fraction-based sources to ensure the published data matches the corrected contract.

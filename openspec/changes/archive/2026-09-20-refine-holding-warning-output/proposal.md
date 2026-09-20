## Why

The web warning summary currently includes `isin_only` holdings even though an exact ISIN is known and the holding is usable for exposure analysis. This inflates the visible warning counts and makes genuinely unmatched holdings harder to identify. Backend warnings also lack the ETF ticker, making multi-ETF ingestion output difficult to trace back to its source.

## What Changes

- Exclude `isin_only` holdings from the web warning summary while retaining `ambiguous` and `unmatched` diagnostics.
- Prefix backend holding warnings with the ETF ticker that produced the warning.
- Preserve the existing holding status, snapshot data, and diagnostic details; this change only refines warning visibility and labeling.

## Capabilities

### New Capabilities

### Modified Capabilities

- `etf-holdings-ingestion`: refine incomplete-match warning visibility and include the ETF ticker in backend warning output.

## Impact

- `web/app.js` warning filtering and display text.
- `etf_ingestion_backend/normalization.py` and/or `etf_ingestion_backend/pipeline.py` warning context.
- Ingestion and web contract tests covering warning status selection and ticker-prefixed output.
- No snapshot schema or identity-resolution behavior changes.

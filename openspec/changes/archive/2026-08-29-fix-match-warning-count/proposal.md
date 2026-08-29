## Why

The website reports successful identity overrides as "unmatched or partially matched" because it treats every status other than `matched` as a warning. This makes a healthy CHSPI snapshot appear to have dozens of unresolved holdings and obscures the small set of genuinely incomplete cash or derivative rows.

## What Changes

- Count only genuinely incomplete holding statuses (`ambiguous` and `unmatched`) in the website warning summary.
- Treat `overridden` holdings as successfully resolved for warning purposes while preserving their provenance.
- Keep the existing company exposure, sector, region, and currency visualization behavior unchanged.
- Add regression coverage for warning counts containing successful overrides and intentional incomplete rows.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `etf-holdings-ingestion`: Clarify that successful override resolution is not reported as an unresolved holding in the visualization diagnostics.

## Impact

- Frontend warning aggregation in `web/app.js`.
- Frontend or contract tests covering CHSPI snapshot diagnostics.
- The serialized snapshot schema and ingestion behavior remain unchanged.

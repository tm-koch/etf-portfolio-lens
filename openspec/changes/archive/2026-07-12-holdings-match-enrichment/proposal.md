## Why

Some holdings cannot currently be fully matched, but the output only shows a generic warning. That makes it hard to tell whether the missing element was an ISIN, ticker, exchange, or another field, and it also leaves avoidable gaps in enrichment when the security master can resolve the ISIN from the ticker alone.

## What Changes

- Add explicit match diagnostics to holdings output so each unmatched record shows which fields were missing and which fallback steps were attempted.
- Enrich holdings with a missing ISIN from `data/tickers.csv` when the ticker can be matched uniquely.
- Keep partial matches and unmatched records in the output, but make the unresolved elements visible for review.
- Preserve existing fallback behavior for ISIN, ticker-plus-exchange, and alias matching while improving diagnostics.

## Capabilities

### New Capabilities
- `holdings-match-diagnostics`: Expose match-failure details in normalized holdings output and support ticker-based ISIN fallback when the security master can resolve it.

### Modified Capabilities
- None.

## Impact

- Updates to the Python enrichment and normalization flow that decides how holdings are matched and how unresolved fields are reported.
- Changes to the JSON snapshot provenance so unmatched holdings can show missing elements and match attempts.
- Improved use of `data/tickers.csv` as the fallback enrichment source for missing ISIN values.

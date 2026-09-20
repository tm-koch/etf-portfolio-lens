## Context

The frontend builds the current-selection warning list in `web/app.js` from each holding's serialized match status. Its incomplete-status set currently includes `ambiguous`, `isin_only`, and `unmatched`, so holdings with an exact ISIN but no complete security-master enrichment inflate the warning count.

The backend emits row-level warnings from `normalize_row()` while the pipeline is processing an ETF. The normalization function receives the provider name and row data, but not the ETF registry entry, while `pipeline.py` has the ETF ticker available as `entry.ticker`.

## Goals / Non-Goals

**Goals:**

- Exclude `isin_only` holdings from the web warning count while retaining `ambiguous` and `unmatched` warnings.
- Prefix backend warning lines with the ETF ticker that produced the holding.
- Keep holding serialization, match statuses, snapshot diagnostics, and exposure calculations unchanged.
- Add focused regression coverage for both warning paths.

**Non-Goals:**

- Do not change how holdings are matched or normalized.
- Do not remove `isin_only` holdings from snapshots or visualizations.
- Do not suppress ambiguous or unmatched diagnostics from snapshot provenance.
- Do not redesign the warning UI.

## Decisions

### Use an explicit ETF ticker context for backend warnings

Pass the ETF ticker from the pipeline into the normalization warning path, or move the final warning print into the pipeline where `entry.ticker` is already available. Prefer the smallest interface change that preserves direct `normalize_row()` callers and keeps the warning text generated from the match diagnostic.

A provider name is not sufficient because it identifies the data source, not the specific ETF. Deriving the ticker from a holding row is also incorrect because that is the constituent ticker, not the ETF ticker.

### Restrict web warning aggregation to genuinely unresolved statuses

Change the frontend warning filter to include only `ambiguous` and `unmatched`. `isin_only` remains a valid serialized match status and continues contributing to all existing exposure visualizations; it is simply omitted from the warning count.

### Keep the existing warning wording structure

Retain one warning row per ETF and the existing count-based summary, changing only the status scope and wording as needed to avoid describing excluded `isin_only` holdings as partially matched.

## Risks / Trade-offs

- [Risk] Direct unit tests that call `normalize_row()` may not provide an ETF ticker. -> Preserve an optional context path or test warning formatting at the pipeline boundary so existing normalization callers remain valid.
- [Risk] Warning text becomes an externally observed CLI contract. -> Add an exact regression assertion for the ticker-prefixed format.
- [Risk] The frontend and backend could drift in which statuses are considered warnings. -> Define both behaviors explicitly in the ingestion capability spec and test them independently.

## Migration Plan

No data migration is required. Update the warning logic and tests, regenerate frontend artifacts only if the project build requires it, run the focused and full test suites, and deploy normally. Rollback consists of reverting the code and test changes; existing snapshots remain compatible.

## Open Questions

None. The intended warning statuses are `ambiguous` and `unmatched`, and the backend prefix is the ETF registry ticker.

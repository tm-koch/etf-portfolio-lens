## 1. Backend Warning Context

- [x] 1.1 Pass the ETF registry ticker into the backend warning-emission path without changing direct normalization callers that do not need warning context.
- [x] 1.2 Prefix emitted unresolved holding warnings with the ETF ticker while preserving the existing diagnostic detail.
- [x] 1.3 Add or update ingestion tests covering ETF-ticker prefixes and constituent tickers that differ from the ETF ticker.

## 2. Web Warning Filtering

- [x] 2.1 Remove `isin_only` from the web incomplete-match warning filter and update warning wording to reflect the remaining statuses.
- [x] 2.2 Add or update web contract tests proving `isin_only` holdings are excluded while `ambiguous` and `unmatched` holdings remain visible.
- [x] 2.3 Verify excluded `isin_only` holdings remain available to all existing exposure visualizations.

## 3. Validation

- [x] 3.1 Run focused backend and web tests for warning behavior.
- [x] 3.2 Run the full test suite and inspect the generated diff for unintended snapshot or schema changes.

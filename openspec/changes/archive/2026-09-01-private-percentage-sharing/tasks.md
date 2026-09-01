## 1. Portfolio Mode and Persistence

- [x] 1.1 Add explicit private percentage mode state and persist it alongside the existing portfolio while preserving legacy array-based local storage.
- [x] 1.2 Add migration and startup handling so existing local portfolios and version 1 full share links remain normal share-count portfolios.

## 2. Private Share Payloads

- [x] 2.1 Add private share payload encoding that derives each selected ETF's current weight, stores it as synthetic `shares` units with sufficient precision, and strips all absolute valuation fields.
- [x] 2.2 Add private payload decoding and validation for the mode marker, supported version, valid duplicate-free ISINs, and finite non-negative relative units.
- [x] 2.3 Add a private share action and feedback path while preserving the existing fallback URL and clipboard behavior.
- [x] 2.4 Ensure private links load before local storage, select the Portfolio tab, persist private mode, and preserve unknown-position handling.

## 3. Weighting and Presentation

- [x] 3.1 Update the central portfolio weighting helper to use synthetic relative units in private mode and ignore any absolute valuation basis.
- [x] 3.2 Ensure edited private Shares values are persisted and normalized consistently by the position table, summary calculations, charts, and look-through exposure views.
- [x] 3.3 Keep the existing no-price portfolio GUI for private mode and add concise explanatory feedback that Shares represent relative weighting units.
- [x] 3.4 Retain absolute summary cards while rendering private-mode share-count totals as `0` and monetary totals as `Not available` or the established unavailable representation.
- [x] 3.5 Prevent private mode from importing or restoring PDF valuation fields and ensure private re-sharing remains redacted.

## 4. Verification

- [x] 4.1 Add web contract tests for private payload creation, field redaction, validation, and version 1 compatibility.
- [x] 4.2 Add tests for private startup precedence, persistence, unknown ETFs, and malformed-payload fallback.
- [x] 4.3 Add tests proving edited relative units drive the same table weights, portfolio rollups, charts, and company aggregation.
- [x] 4.4 Add tests proving private summary cards do not expose source share counts or monetary values while normal summaries remain unchanged.
- [x] 4.5 Run the focused web and portfolio test suites and inspect the final rendered behavior at desktop and mobile widths.

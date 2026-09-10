## 1. Portfolio State and Valuation Contract

- [x] 1.1 Add a normalized portfolio-level `valuationMode` with `latest` as the default for legacy full portfolios.
- [x] 1.2 Extend the effective valuation boundary to accept the selected mode and distinguish live, imported, imported fallback, and unavailable results.
- [x] 1.3 Preserve imported price, currency, value, and CHF-normalized fields while switching modes.

## 2. Portfolio Controls and Rendering

- [x] 2.1 Add a full-portfolio valuation mode control near the selected positions and keep it unavailable for percentage-only portfolios.
- [x] 2.2 Wire mode changes to persistence and rerender position prices, CHF values, source labels, weights, totals, and dependent views immediately.
- [x] 2.3 Initialize the portfolio-level mode from the import review selection when confirming a valid PDF import.
- [x] 2.4 Ensure existing local portfolios and full-portfolio share links remain compatible, with explicit mode preserved where the share contract supports it.

## 3. Tests and Browser Verification

- [x] 3.1 Add valuation tests covering latest live valuation, imported mode bypass, latest fallback, missing FX, and unavailable values.
- [x] 3.2 Add frontend tests covering legacy state normalization, mode persistence, import initialization, and percentage portfolio behavior.
- [x] 3.3 Add contract tests for the new control, source labels, and cache/version updates.
- [x] 3.4 Run the focused and full test suites, then browser-verify switching modes before and after reload with CHF and EUR positions.

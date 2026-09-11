## 1. Private Portfolio Rendering

- [x] 1.1 Update private position-row rendering to include the normalized relative Weight cell while retaining relative Shares and Remove controls.
- [x] 1.2 Keep private row rendering valuation-independent so Price, Value CHF, and absolute valuation resolution remain absent.
- [x] 1.3 Update private empty-state column spans, table headers, and desktop/mobile layout rules for the visible Weight column.

## 2. Valuation Status Visibility

- [x] 2.1 Ensure the portfolio-level valuation-status box is hidden whenever the active portfolio mode is percentage-only.
- [x] 2.2 Verify the hidden state is reapplied after shared-link startup, asynchronous data loading, position edits, additions, removals, and other portfolio rerenders.
- [x] 2.3 Preserve the existing Live/Imported status box and flashing-dot behavior for full portfolios.

## 3. Regression Coverage

- [x] 3.1 Update web contract tests for private Weight headers/cells and the hidden valuation-status box.
- [x] 3.2 Add runtime coverage for valid private share loading and rerender persistence of the hidden status box.
- [x] 3.3 Add or update full-portfolio coverage proving Live shows the animated dot and Imported hides the dot while keeping the status box visible.
- [x] 3.4 Run focused web tests and the complete test suite, then verify the OpenSpec scenarios.

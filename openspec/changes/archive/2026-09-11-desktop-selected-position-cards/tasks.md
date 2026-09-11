## 1. Position Markup

- [x] 1.1 Add or refine stable markup hooks for the selected-position identity and wide metrics presentation without removing existing data labels or accessibility attributes.
- [x] 1.2 Preserve the existing full-portfolio and percentage-only cell differences while ensuring both modes support the wide position-box layout.

## 2. Wide Position-Box Styling

- [x] 2.1 Style wide selected-position rows as rounded enclosed boxes with stable spacing, borders, and minimum-width behavior.
- [x] 2.2 Place ticker and ETF name on the first line and labeled Shares, pricing/value, and Weight metrics on the second line.
- [x] 2.3 Right-align the Remove control in a dedicated column and vertically center it across the complete wide box.
- [x] 2.4 Keep the existing mobile reflow rules, control sizing, and narrow-viewport behavior unchanged.

## 3. Regression Coverage

- [x] 3.1 Extend web contract tests for wide rounded boxes, two-line identity/metrics hooks, labeled metrics, and Remove alignment.
- [x] 3.2 Verify full and percentage-only position rendering, accessible names, editing, valuation display, and removal behavior remain covered.
- [x] 3.3 Run focused web tests and the complete test suite, then validate the OpenSpec change.

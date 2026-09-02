## Why

Larger CHF and EUR amounts in the Portfolio workflow are harder to scan when thousands are not visually grouped. Consistent apostrophe-separated currency displays improve readability across the portfolio summary, selected positions, and PDF import review without changing any underlying values or calculations.

## What Changes

- Centralize presentation formatting for supported CHF and EUR monetary values with two decimal places and apostrophe-separated thousands, such as `CHF 12'345.67` and `EUR 1'234.56`.
- Apply the format to Portfolio summary totals, selected ETF prices, and selected ETF CHF values.
- Apply the format to PDF import review source-currency values and CHF-normalized values, including totals recalculated after review edits.
- Preserve raw numeric inputs, persisted numeric fields, parsing, conversion, share counts, and calculations.
- Preserve unavailable-value presentation for private portfolios that do not contain absolute valuation data.

## Capabilities

### New Capabilities

- `portfolio-currency-display`: Define consistent apostrophe-separated CHF and EUR formatting for monetary values shown in the Portfolio workflow.

### Modified Capabilities

- `home-tab`: Require apostrophe-separated thousands for displayed finite CHF summary totals while retaining the existing zero-value behavior.
- `saxo-pdf-portfolio-import`: Require apostrophe-separated thousands for displayed source-currency and CHF-normalized review values and totals.

## Impact

The primary impact is limited to the vanilla JavaScript display-formatting paths in `web/app.js` and their web contract tests in `tests/test_web_contract.py`. No API, storage schema, import parser, currency conversion rule, or persisted portfolio representation changes are expected.

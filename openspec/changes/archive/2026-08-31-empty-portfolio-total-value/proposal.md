## Why

When the portfolio is empty, the Home tab displays `Unavailable` for Total value while the other summary cards display numeric zero. This makes a normal empty state look like missing data and creates an inconsistent summary experience.

## What Changes

- Display the empty-portfolio Total value as `CHF 0.00`, using the same currency formatting as populated Total value cards.
- Preserve the existing calculated value for portfolios with imported valuation data.
- Add a regression contract covering the empty-portfolio Total value presentation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `home-tab`: Extend the empty portfolio summary requirement to include Total value as an explicit zero currency value.

## Impact

- Affected frontend logic: `web/app.js`, specifically the Home summary calculation in `updateSummary()`.
- Affected frontend contract tests: `tests/test_web_contract.py`.
- No API, data model, import behavior, or external dependency changes are expected.

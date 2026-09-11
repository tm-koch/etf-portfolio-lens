## Why

The wide Portfolio view currently presents selected ETFs as a dense table row, making long ETF names compete horizontally with prices, weights, and controls. A rounded position box with a clear identity line and a labeled metrics line will improve scanning while making the Remove action easier to locate.

## What Changes

- Render selected ETF positions as rounded boxes in the wide, side-by-side catalog and portfolio layout.
- Place the ticker and ETF name on the first line of each box.
- Place labeled Shares, pricing/value, and Weight information on the second line.
- Right-align the Remove control and center it vertically against the full position box.
- Preserve existing position editing, valuation, weight calculation, removal behavior, accessible names, and mobile card reflow.
- Use the labeled metrics presentation: `Shares [input]`, `Price ...` or `Value CHF ...`, and `Weight ...`.

## Capabilities

### New Capabilities

### Modified Capabilities

- `mobile-positions-layout`: Change larger viewport selected positions from a plain four-column table presentation to rounded two-line position boxes while retaining the existing mobile behavior and controls.

## Impact

- Affects selected-position markup generated in `web/app.js` and wide-layout styling in `web/styles.css`.
- Updates the selected-position web contract tests and adds coverage for wide card structure, metric ordering, Remove alignment hooks, and mobile compatibility.
- Does not change portfolio state, JSON data, valuation calculations, sharing, or backend APIs.

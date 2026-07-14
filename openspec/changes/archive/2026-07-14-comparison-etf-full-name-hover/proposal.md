## Why

The comparison tab currently shows only ETF tickers in the selector pills, which makes it harder to identify funds quickly when multiple ETFs are selected. Surfacing the full ETF name on hover improves readability without adding visual clutter to the toolbar.

## What Changes

- Add a hover tip to the comparison tab ETF selector pills.
- Show the full ETF name when the user hovers over a comparison checkbox/pill.
- Keep the existing ticker label and selection behavior unchanged.

## Capabilities

### New Capabilities
- `comparison-etf-full-name-hover`: comparison selector pills show the full ETF name in a hover tip while preserving the existing checkbox UI.

### Modified Capabilities
- None.

## Impact

- Affects the comparison toolbar rendering in `web/app.js`.
- May require small supporting text or tooltip styling in `web/styles.css`.
- Does not change chart data, selection state, or comparison logic.

## Why

Private percentage-only links intentionally contain no absolute valuation data, but the Portfolio table currently resolves live catalog data and renders Price and Value CHF for those positions. This exposes misleading absolute values and conflicts with the privacy contract, so the presentation must make percentage-only portfolios valuation-free.

## What Changes

- Hide the Valuation basis label and selector whenever a percentage-only private portfolio is active.
- Omit the Price, Value CHF, and Weight headers and cells for percentage-only portfolio rows, while retaining the Remove control.
- Avoid resolving position valuations for percentage-only rows; calculate weights from relative allocation units only.
- Add clear mobile separation between the valuation/header area and the first ETF position row.
- Show one portfolio-level valuation source note beside the valuation selector instead of appending source labels to each total value cell.
- Keep the valuation source note horizontally aligned with the valuation selector on wider layouts.
- Right-align the valuation source note and align it with the selector control rather than its label.
- Align the top of the valuation source note with the top of the valuation select box.
- Preserve the existing six-column valuation presentation and valuation calculations for full portfolios.
- Preserve the existing mobile percentage-portfolio layout and private sharing payload format.

## Capabilities

### New Capabilities

### Modified Capabilities

- `private-percentage-sharing`: Require percentage-only portfolios to use a no-valuation table presentation instead of rendering unavailable or rehydrated valuation fields.
- `portfolio-valuation-mode`: Clarify that percentage-only portfolios do not render valuation columns or invoke valuation resolution, while full portfolios remain unchanged.

## Impact

- Affects the Portfolio positions rendering and empty-state column span in `web/app.js` and the corresponding table contract in `web/index.html`.
- May require focused desktop and mobile web regression coverage in `tests/test_web_contract.py` and runtime tests for valuation non-resolution.
- No share payload, catalog, backend, or public API format changes are required.
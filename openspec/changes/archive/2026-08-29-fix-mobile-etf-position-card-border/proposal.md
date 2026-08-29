## Why

At mobile widths, the individual ETF entries in Selected positions can appear to lose part of their lower surrounding border. The mobile table-to-card reflow currently suppresses the row's table bottom border, so the card edge is not explicitly guaranteed at the bottom where the row becomes the visible card surface.

## What Changes

- Ensure every mobile selected-position entry has a complete, continuous surrounding border, including its lower edge.
- Preserve the existing mobile layout: ETF identity above the Shares, Weight, and Remove control row.
- Preserve desktop and tablet table presentation and existing spacing, controls, accessibility, and interaction behavior.
- Add a focused browser or DOM/CSS regression check for the mobile card boundary and a contract assertion for the required border styling.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `mobile-positions-layout`: Require each reflowed mobile selected-position entry to render as a fully enclosed card without a missing lower border.

## Impact

- `web/styles.css` mobile `.position-row` styling is the primary implementation surface.
- `tests/test_web_contract.py` and/or browser-based validation will cover the mobile card boundary.
- No data model, API, or dependency changes are expected.
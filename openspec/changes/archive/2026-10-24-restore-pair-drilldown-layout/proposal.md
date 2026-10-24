# Proposal

## Why

The pair drill-down card has regressed visually: its title no longer aligns with neighboring card headings on widescreen, and its ETF selectors become too narrow on mobile. This change restores the intended card hierarchy and usable side-by-side selection layout.

## What Changes

- Align the drill-down title with the other aggregation card headings while keeping its information control positioned consistently in the header.
- Keep both ETF selectors side by side at narrow viewport widths, with each selector using its available column width.
- Add focused responsive layout regression coverage for the drill-down header and selectors.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `pairwise-product-overlap`: Specify consistent drill-down header alignment and usable, equal-width side-by-side selectors on mobile.

## Impact

- Affected UI: `web/styles.css` and, if needed, the pair drill-down header markup in `web/index.html`.
- Tests: focused web contract/runtime checks for the header and mobile selector layout.
- No API, data, or dependency changes.
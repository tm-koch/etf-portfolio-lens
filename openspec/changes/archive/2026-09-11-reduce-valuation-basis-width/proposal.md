## Why

The portfolio-level valuation basis control is wider than necessary, leaving the selected positions header unnecessarily spread out. Reducing it by 30% will make the control more compact while preserving readable options and the adjacent Live/Imported status.

## What Changes

- Reduce both the portfolio-level and portfolio-import valuation basis control widths from 320px to 224px.
- Apply the width at the shared valuation-control rule so both workflows stay consistent.
- Preserve responsive behavior, including the existing mobile stacking and status alignment.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `outer-layout-density`: Adjust the portfolio valuation basis control's presentation width without changing its behavior.

## Impact

- Affected stylesheet: `web/styles.css`.
- Affected visual contract coverage, if needed, for the portfolio valuation control width.
- No changes to valuation behavior, portfolio data, APIs, or import-dialog behavior beyond presentation width.

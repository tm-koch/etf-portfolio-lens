## Why

The mobile Selected positions layout currently expands the Shares input to fill its grid column, while the wide layout keeps the input at a fixed width. This makes the same control look disproportionately wide on mobile and weakens the visual consistency of the position cards.

## What Changes

- Keep the Selected positions Shares input at the existing fixed wide-mode width on mobile.
- Preserve the mobile card's responsive outer layout, identity row, Weight display, and Remove control.
- Add contract coverage confirming the fixed Shares input width applies across mobile and wide layouts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `mobile-positions-layout`: Require the Shares input to retain a fixed width across supported viewport layouts.

## Impact

- Updates the responsive Selected positions CSS in `web/styles.css`.
- Extends the web contract tests in `tests/test_web_contract.py`.
- Does not change position data, state updates, accessibility attributes, or application APIs.
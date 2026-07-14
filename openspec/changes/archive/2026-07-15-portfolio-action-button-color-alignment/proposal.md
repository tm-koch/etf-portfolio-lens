## Why

The portfolio tab uses gradient-filled action buttons that visually clash with the active tab state, which already uses the project’s solid accent color. Aligning the action buttons with the active tab color makes the UI feel more cohesive and reduces unnecessary visual noise.

## What Changes

- Change the portfolio tab action buttons to use the same solid accent color as the active tabs.
- Remove the gradient treatment from the add and remove buttons in the portfolio area.
- Preserve the existing button sizing, shape, and interaction states.

## Capabilities

### New Capabilities
- `portfolio-action-button-color-alignment`: portfolio action buttons use the same solid accent color as active tabs instead of gradient styling.

### Modified Capabilities
- None.

## Impact

- Affects the button styling rules in `web/styles.css`.
- Does not change portfolio data, rendering logic, or browser behavior.

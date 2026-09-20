## Why

The ETF catalog currently renders both actionable `Add` buttons and completed `Added` buttons with the same filled blue treatment. This makes the completed state look like an action instead of a status, so the distinction should be made visually explicit.

## What Changes

- Mark catalog buttons for ETFs already in the portfolio with a dedicated added-state marker.
- Style the added state with a blue border, white background, and blue text.
- Preserve the existing disabled behavior so an ETF cannot be added twice.
- Cover the state marker and styling contract with focused web tests.

## Capabilities

### New Capabilities

- `added-etf-button-state`: Distinguishes completed ETF additions from available catalog actions through an explicit button status style.

### Modified Capabilities

- None.

## Impact

- Affected frontend rendering in `web/app.js` and catalog button styles in `web/styles.css`.
- Affected static web contract coverage in `tests/test_web_contract.py`.
- No backend, persistence, API, dependency, or portfolio data-model changes.

## Why

Private shared portfolios correctly enter percentage-only mode in JavaScript, but the valuation control and Live/Imported status box remain visible because their CSS `display` declarations override the HTML `hidden` state. This makes a private portfolio appear to have absolute valuation context and is visible immediately after loading a shared portfolio.

## What Changes

- Ensure the portfolio valuation basis control is not displayed when it has the `hidden` attribute.
- Ensure the portfolio valuation status box is not displayed when it has the `hidden` attribute.
- Preserve the existing visible valuation control and Live/Imported status behavior for full portfolios.
- Add focused contract coverage proving the CSS visibility contract for both elements.

## Capabilities

### New Capabilities

### Modified Capabilities

- `private-percentage-sharing`: Private percentage-only portfolios must not display valuation controls or valuation provenance.
- `portfolio-valuation-mode`: Hidden valuation UI must remain visually hidden when private mode sets the `hidden` state.

## Impact

- Affects the portfolio valuation styles in `web/styles.css`.
- Adds or updates focused web contract tests under `tests/`.
- Does not change share payloads, portfolio state, valuation calculations, or backend behavior.

## Why

The compact Explore company search currently relies on browser-native search decorations, so its clear cross is inconsistent or absent in Firefox mobile and desktop. The ranked holding cell can also wrap the rank and company name onto separate lines, reducing scanability; this change makes both interactions consistent and predictable.

## What Changes

- Add an application-owned clear button to the compact Explore company search field.
- Show the clear button only when the search contains text and restore the unfiltered first batch when activated.
- Preserve search focus and provide an accessible name for the clear action across desktop and mobile browsers.
- Keep each compact Explore holding rank and company name on a single line while preserving responsive clipping and hover disclosure.
- Add automated and browser-facing coverage for clear-button visibility, reset behavior, focus, and nowrap rendering.

## Capabilities

### New Capabilities

### Modified Capabilities

- `compact-explore-preview`: Make company search clearing consistent across browsers and keep ranked holding labels on one line.

## Impact

- `web/index.html`: search control markup and accessible clear action.
- `web/app.js`: clear-button visibility, reset behavior, and focus handling.
- `web/styles.css`: search control positioning, touch target, and rank/name nowrap layout.
- `tests/test_web_contract.py`: frontend contract assertions.
- Browser verification for Chromium and Firefox-sized mobile layouts; no new runtime dependencies.

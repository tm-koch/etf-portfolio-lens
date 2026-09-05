## Why

On Chrome Mobile, tapping a navigation button in Bright mode briefly shows a light-blue flash before the selected tab appears active. The app updates its active state synchronously, so the flash is caused by Chrome's native tap highlight being visible through the transparent mobile navigation styling. This makes navigation feel delayed or unstable even though the correct tab is selected.

## What Changes

- Define an explicit mobile navigation pressed-state treatment that does not expose Chrome's default tap highlight.
- Preserve clear active-tab styling, keyboard focus visibility, touch usability, and the existing tab-selection behavior.
- Add regression coverage for the navigation interaction CSS and active-state contract.

## Capabilities

### New Capabilities

- `mobile-navigation-feedback`: Provides stable, browser-consistent pressed, active, and focus feedback for the mobile navigation buttons.

### Modified Capabilities

<!-- No existing spec-level behavior changes are required. -->

## Impact

- Affects the mobile navigation rules in `web/styles.css` and, only if needed to preserve interaction semantics, the navigation event handling in `web/app.js`.
- Extends web contract tests and may add a browser-level verification step for Chrome Mobile-sized viewports.
- No navigation destinations, URL behavior, portfolio state, PWA installability, or desktop navigation behavior should change.

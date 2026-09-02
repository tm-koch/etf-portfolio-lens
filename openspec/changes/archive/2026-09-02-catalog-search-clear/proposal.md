## Why

The ETF catalog search currently depends on browser-native search cancellation, while the Explore search has a consistent application-owned clear button. Adding the same explicit affordance to the catalog makes clearing discoverable and consistent across browsers, including the existing behavior for whitespace-only input.

## What Changes

- Add an application-owned clear button to the ETF catalog search field.
- Show the button whenever the catalog search input contains any raw value, including whitespace, matching the Explore search behavior.
- Clear the catalog search, restore the unfiltered catalog, and return focus to the catalog input when activated.
- Preserve the existing trimmed, case-insensitive catalog filtering behavior.

## Capabilities

### New Capabilities

- `catalog-search-clear`: Provides an accessible, application-owned clear control for the ETF catalog search.

### Modified Capabilities

<!-- None. The existing Explore search capability is used as the behavioral reference but its requirements do not change. -->

## Impact

- Affects the Portfolio tab catalog-search markup, client-side event handling, and shared search-control styling in `web/index.html`, `web/app.js`, and `web/styles.css`.
- Extends web contract coverage for the catalog clear control and its whitespace behavior.
- No backend, data, API, or dependency changes are expected.
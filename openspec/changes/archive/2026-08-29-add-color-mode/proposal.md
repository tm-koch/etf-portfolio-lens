## Why

ETF Portfolio Lens currently presents only a bright visual scheme, which can be uncomfortable in low-light environments and ignores the user's browser or operating-system appearance preference. A persistent color-mode choice will make the site more comfortable to use while preserving the bright scheme as an explicit option.

## What Changes

- Add three color modes: `Bright`, `Automatic`, and `Dark`.
- Make `Automatic` the default and resolve it from the browser or operating system `prefers-color-scheme` preference.
- Add a compact three-state color-mode control using the existing icon language, with sun, monitor, and moon states similar to the Docusaurus color-mode control.
- Persist the selected mode in browser `localStorage` and restore it on subsequent visits.
- Apply dark styling consistently to the page, navigation, panels, dialogs, forms, tables, badges, warnings, empty states, focus states, and responsive layouts.
- Keep charts and chart legends legible in every color mode and refresh theme-sensitive chart rendering when the effective mode changes.
- Respect reduced-motion preferences for any color-mode control transitions.

## Capabilities

### New Capabilities

- `color-mode`: User-selectable bright, automatic, and dark website appearance with browser persistence and system preference integration.

### Modified Capabilities

<!-- No existing capability requirements change. -->

## Impact

- Frontend markup in `web/index.html` for the color-mode control and its accessible menu or selector.
- Frontend state, persistence, system-preference detection, and event handling in `web/app.js`.
- Theme tokens, component states, responsive navigation, and dark-mode overrides in `web/styles.css`.
- Theme-sensitive Chart.js colors and redraw behavior in `web/charts.js`.
- Web contract tests covering persistence, default resolution, control markup, and theme coverage.
- No backend, catalog schema, ingestion, or external dependency changes are expected.

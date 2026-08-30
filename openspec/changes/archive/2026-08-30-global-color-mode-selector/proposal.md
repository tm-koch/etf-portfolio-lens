## Why

The color-mode selector is currently hidden inside the About this build dialog, making a global visual preference difficult to discover. A persistent top-right utility control will make Bright, Automatic, and Dark modes easier to find while preserving the existing local persistence and system-preference behavior.

## What Changes

- Add a globally reachable color-mode selector in the app's top-right utility area without introducing a separate utility frame.
- Keep Bright, Automatic, and Dark as the available choices.
- Preserve the selected preference across reloads and continue resolving Automatic from the system color scheme.
- Provide an appropriately compact and accessible presentation at mobile widths.
- Align the selector with the active panel's primary title row, including the Home hero's `ETF Portfolio Lens` title and the `Portfolio entry` title.
- Remove the color-mode control from the developer/build-details area once the global control is available.

## Capabilities

### New Capabilities

- `global-color-mode-selector`: Persistent, accessible global control for selecting the application's color mode.

### Modified Capabilities

- `home-tab`: Move color-mode access out of build details while retaining the Home tab's build-information action.
- `bottom-navigation`: Add a global utility placement that remains discoverable alongside the responsive primary navigation.

## Impact

- Affects `web/index.html`, `web/app.js`, and `web/styles.css`.
- Updates web contract tests for selector placement, accessibility, responsive layout, and persistence behavior.
- No backend, catalog, data, or external API changes are expected.

## Why

The app currently presents its product introduction and portfolio summary outside the navigation, so users do not have a dedicated starting point for understanding the current portfolio. A Home destination will make that overview explicit and give the application a clear first destination as the product grows.

## What Changes

- Add a Home destination with a house icon at the beginning of the primary navigation.
- Move the existing ETF Portfolio Lens introduction and four portfolio summary boxes into the Home panel.
- Make Home the default destination when no valid destination is stored.
- Preserve the existing Portfolio, Compare, and Explore workflows and their current calculations.
- Keep the build-information dialog available from the Home information area.
- Preserve local destination persistence, without adding URL routing or browser history changes.

## Capabilities

### New Capabilities

- `home-tab`: A dedicated Home destination containing the product overview and live portfolio summary metrics.

### Modified Capabilities

- `bottom-navigation`: Expand the primary destination registry from Portfolio, Compare, and Explore to Home, Portfolio, Compare, and Explore, with Home first and selected by default for new users.

## Impact

- `web/index.html`: Reorganize the introduction, summary metrics, and destination panels.
- `web/app.js`: Add the Home destination and panel state while reusing existing summary rendering and persistence behavior.
- `web/styles.css`: Preserve responsive navigation behavior and style the relocated overview content.
- `openspec/specs/bottom-navigation/`: Update the navigation contract and add the Home capability specification.
- No backend, catalog, snapshot, API, or portfolio-storage migration is required.

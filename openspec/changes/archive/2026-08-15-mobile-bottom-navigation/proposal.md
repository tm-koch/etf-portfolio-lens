## Why

The web app currently presents Portfolio, Comparison, and Aggregated as a conventional tab bar, while the app's three topics are better understood as primary destinations. A responsive bottom navigation will make those destinations easier to discover and use on mobile while preserving the existing summary and content model.

## What Changes

- Replace the existing tab bar with an extensible primary navigation containing Portfolio, Compare, and Explore.
- Display a suitable icon above each destination label, using a consistent icon style.
- Keep the navigation in normal document flow on desktop and fix it to the viewport bottom on mobile.
- Add solid navigation styling and mobile safe-area spacing so the fixed navigation does not obscure content or conflict with device gesture areas.
- Preserve the summary cards above every destination.
- Keep Compare and Explore available when no portfolio positions exist, using their existing empty states.
- Persist the selected destination across page reloads without changing the browser URL or history.
- Keep the existing internal `aggregated` state name while presenting that destination as Explore.
- Structure the navigation so future destinations and optional badges can be added later without redesigning the core contract.

## Capabilities

### New Capabilities

- `bottom-navigation`: Responsive primary navigation for the app's Portfolio, Compare, and Explore destinations, including selection, persistence, accessibility, responsive positioning, and extensibility behavior.

### Modified Capabilities

## Impact

- `web/index.html`: Replace the current tab navigation markup with the primary navigation and icon-bearing destination items.
- `web/app.js`: Preserve destination switching, persist and restore the selected destination, and map the visible Explore label to the existing `aggregated` state.
- `web/styles.css`: Add desktop flow and mobile fixed-navigation layouts, solid background treatment, active-state styling, safe-area spacing, and content clearance.
- Frontend icon dependency: add a consistent icon solution, preferably Lucide, compatible with the current dependency-light browser application.
- No server API, URL routing, browser history, or portfolio data contracts change.

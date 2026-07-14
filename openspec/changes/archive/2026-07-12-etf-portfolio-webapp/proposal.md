## Why

The backend already produces normalized ETF snapshot JSON under `data/raw/<date>/snapshots`, so the missing piece is a responsive frontend that turns that data into a usable portfolio analysis tool. This change creates the product surface for entering ETF positions, comparing ETF composition, and viewing aggregated look-through exposure without adding a live backend dependency.

## What Changes

- Add a responsive web frontend that works on desktop and smartphones.
- Add a developer webserver for local testing on a desktop PC.
- Add a portfolio entry tab where users can add ETFs and enter share counts.
- Add a comparison tab that visualizes ETF sector, region, and currency composition with Chart.js doughnut charts, including concentric multi-ring views where useful.
- Add an aggregated portfolio tab that ranks company exposure across the whole portfolio and highlights holdings that appear in multiple ETFs.
- Aggregate sector, region, and currency exposure across the full portfolio using weighted ETF positions.
- Store the user portfolio locally in the browser.
- Defer CSV portfolio import to V2.

## Capabilities

### New Capabilities
- `portfolio-dashboard`: responsive ETF portfolio web app with portfolio entry, ETF comparison charts, and aggregated look-through exposure views.

### Modified Capabilities
- None.

## Impact

- New frontend application and local development server.
- Chart.js as the primary visualization dependency.
- Static snapshot JSON becomes the frontend data source.
- Browser local storage for persisted portfolio state.
- Potential follow-on data work if ETF share prices or NAV values are needed for share-based portfolio valuation.

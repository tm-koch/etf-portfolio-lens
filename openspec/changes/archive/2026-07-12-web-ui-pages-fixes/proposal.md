## Why

The current frontend is too visually heavy, the comparison charts are not rendering reliably, and the local development server is only reachable on localhost. The project also needs a clear GitHub Pages publish structure so the static frontend and snapshot data can be deployed consistently.

## What Changes

- Switch the UI to a lighter white visual style.
- Stack the sector, region, and currency sections vertically instead of showing them side by side.
- Fix the chart layout so the Chart.js doughnuts render correctly in their containers.
- Make the local development server reachable from a browser beyond the local machine when needed.
- Add GitHub Pages deployment documentation that lists the files and folder structure to upload.

## Capabilities

### New Capabilities
- `web-ui-pages-experience`: lightweight white frontend layout, reliable doughnut chart rendering, browser-accessible local server, and GitHub Pages publish guidance for the static app and data files.

### Modified Capabilities
- None.

## Impact

- Frontend layout, styling, and chart containers.
- Local web server defaults and browser access behavior.
- Static asset and data publish structure for GitHub Pages.
- Documentation for deployment and file placement.

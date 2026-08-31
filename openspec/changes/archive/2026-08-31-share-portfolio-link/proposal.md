## Why

Portfolio configurations are currently persisted only in the sender's browser, so a user cannot show somebody else the same ETF positions and share weights. A shareable link would make portfolio details easy to communicate while preserving the application's static GitHub Pages deployment.

## What Changes

- Add a share action to the Portfolio tab that creates a URL containing the current ETF selections and share counts.
- Load and validate a portfolio encoded in an opened link before falling back to the recipient's locally stored portfolio.
- Initialize the recipient's portfolio from the link and persist the loaded selection locally for subsequent visits.
- Keep shared links based on the latest catalog and ETF snapshot data available in the deployed application.
- Provide user-visible feedback for successful sharing, invalid links, and positions that are no longer present in the catalog.
- Do not add a server-side share database or historical snapshot pinning.

## Capabilities

### New Capabilities

- `portfolio-sharing`: Create, encode, open, validate, and apply shareable portfolio links.

### Modified Capabilities

<!-- No existing capability requirements are changed. -->

## Impact

- `web/index.html`, `web/app.js`, and `web/styles.css` for the Portfolio tab control, link handling, and feedback states.
- The static browser URL and `localStorage` portfolio initialization behavior.
- Web contract tests for payload validation, precedence over local state, and share-control accessibility.
- No new runtime services, backend APIs, or external dependencies are required.
## Why

The GitHub Pages deployment omits the frontend `portfolio-import.js` module even though `web/app.js` imports it. This causes a 404 and prevents application bootstrap, leaving navigation and color-mode controls unusable in the published site.

## What Changes

- Include `web/portfolio-import.js` in the GitHub Pages publish file list.
- Add regression coverage that verifies required frontend modules are copied into the deployment.
- Republish the site and verify navigation, color-mode selection, and portfolio import loading on the deployed page.

## Capabilities

### New Capabilities

- `portfolio-deployment-integrity`: Ensures all frontend modules required by the published application are deployed and load successfully.

### Modified Capabilities



## Impact

- Affects `scripts/publish-gh-pages.ps1` and deployment-focused tests.
- Requires a GitHub Pages republish after implementation.
- No portfolio data schema, backend API, or import parsing behavior changes.

## Why

The product currently uses "ETF Lens" across the web app, docs, and server messaging, but the new name "ETF Portfolio Lens" better describes the app's purpose and makes the brand more explicit. Renaming now keeps the user-facing identity consistent before the branding spreads further.

## What Changes

- Rename the product name from ETF Lens to ETF Portfolio Lens across user-facing text.
- Update the browser title, hero label, error copy, server description, and documentation to use the new name.
- Keep technical identifiers such as file paths, snapshot IDs, and data keys unchanged.
- **BREAKING**: Any downstream text snapshots, documentation references, or screenshots that assert the old product name will need to be updated.

## Capabilities

### New Capabilities
- `product-branding`: repo-wide product name and branding consistency across the app, docs, and local server messaging.

### Modified Capabilities
- None.

## Impact

- Affects the static web app in `web/`.
- Affects repository documentation in `README.md`, `web/README.md`, and `doc/product_idea.md`.
- Affects server and error strings in `web/server.py` and `web/app.js`.
- May affect screenshots, demo material, and any copy-based assertions in tests or docs.

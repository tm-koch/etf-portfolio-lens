## Why

A shared private portfolio is intended to expose relative allocation information without implying that live or imported absolute valuation data is active. The Portfolio view can still show the valuation-status box with `Live` in this scenario, which is misleading and can reveal the wrong valuation context.

## What Changes

- Display each private portfolio position's normalized relative `Weight` alongside its relative `Shares` value.
- Hide the portfolio-level valuation-status box whenever a valid private percentage-only share portfolio is active.
- Keep the box hidden after startup, asynchronous catalog/snapshot loading, edits, and other portfolio rerenders.
- Preserve the existing `Live` and `Imported` status presentation for full portfolios.
- Add regression coverage for a valid private share link and for full-portfolio status behavior.
- Clarify the private-sharing and valuation-mode requirements so private mode does not render valuation provenance.

## Capabilities

### New Capabilities

### Modified Capabilities

- `private-percentage-sharing`: Require relative Weight cells to remain visible and the valuation-status box to be absent for an active private percentage-only portfolio.
- `portfolio-valuation-mode`: Clarify that valuation provenance is available only for full portfolios and is hidden for private percentage-only portfolios.

## Impact

- Affects the web Portfolio view state/rendering path in `web/app.js` and its existing valuation-status markup in `web/index.html`.
- Adds focused contract and runtime/browser regression coverage under `tests/`.
- Changes no share payload format, catalog data, backend behavior, or public API.

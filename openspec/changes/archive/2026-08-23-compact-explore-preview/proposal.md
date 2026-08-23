## Why

The current Explore tab presents each aggregated holding as a large visual row, which makes it harder to scan many holdings and compare how ETFs contribute to the same company. A compact matrix view provides a denser, results-table-style comparison while allowing the existing view to remain the stable default during preview.

## What Changes

- Add a developer-mode switch for a compact Explore preview, defaulting to off.
- Persist the preview switch in browser storage so the selected mode survives page reloads.
- Add a compact holdings matrix with one row per aggregated holding, sorted by total portfolio exposure descending.
- Display the holding name, total portfolio contribution, and one contribution column for every selected ETF.
- Reuse the existing aggregated holding and contributor values; do not introduce a second calculation or data contract.
- Keep the current Explore presentation unchanged when the preview switch is disabled.
- Support horizontal scrolling when the ETF columns exceed the available viewport width.

## Capabilities

### New Capabilities

- `compact-explore-preview`: Developer-controlled, persisted compact Explore matrix for comparing aggregated holdings and ETF contributions.

### Modified Capabilities

None.

## Impact

- `web/app.js`: preview preference state, developer-mode control wiring, compact matrix rendering, and mode selection.
- `web/index.html`: developer-mode switch and compact Explore markup.
- `web/styles.css`: dense matrix styling, responsive overflow, and preview-mode presentation.
- Existing aggregation behavior remains the source of truth; no backend, snapshot, catalog, or external dependency changes are expected.

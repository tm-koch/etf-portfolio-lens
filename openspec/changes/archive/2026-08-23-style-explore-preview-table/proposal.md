## Why

The compact Explore preview is information-dense, but its current transparent row treatment makes the header, holding names, and ETF contribution values harder to scan. A restrained light table palette will improve row separation and make the preview easier to read on desktop and mobile.

## What Changes

- Give the compact Explore table header a fixed `rgb(232, 236, 244)` background.
- Alternate compact Explore body rows between `rgb(244, 246, 251)` and white.
- Apply the same alternating backgrounds to the sticky holding-name cells so horizontal scrolling does not create a mismatched first column.
- Preserve the existing hover feedback, sticky behavior, borders, typography, overflow behavior, and table data.

## Capabilities

### New Capabilities

- `explore-preview-table-styling`: Consistent header, alternating-row, and sticky-column colors for the compact Explore holdings matrix.

### Modified Capabilities

- `compact-explore-preview`: Add visual requirements for the table header and alternating body row treatment without changing the matrix data or interaction model.

## Impact

- `web/styles.css`: Update compact Explore table background selectors.
- `openspec/specs/compact-explore-preview/`: Add the styling contract for the existing preview table.
- No JavaScript, backend, catalog, snapshot, API, or data-model changes are required.

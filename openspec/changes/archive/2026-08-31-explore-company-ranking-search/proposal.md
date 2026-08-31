## Why

The compact Explore preview shows company exposure efficiently, but users cannot tell each company's position in the overall ranking or quickly isolate a company by name. Adding persistent portfolio ranks and a live company-name filter will make the preview useful for both scanning and targeted inspection.

## What Changes

- Display a rank number for every company in the compact Explore preview.
- Add a company search field to the compact Explore preview.
- Filter companies live while the user types, using case-insensitive substring matching against company names only.
- Display all matching companies when a search term is present; display no company rows when there are no matches.
- Preserve each company's original full-list portfolio rank while filtering.
- Preserve the existing first-20-plus-infinite-scroll behavior when the search field is empty.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `compact-explore-preview`: Add visible ranking numbers and live company-name filtering to the compact holdings matrix.

## Impact

- `web/index.html`: compact Explore company search field and accessible labeling.
- `web/app.js`: company search state, live filtering, rank rendering, and filtered-list pagination behavior.
- `web/styles.css`: search-field and rank presentation within the compact matrix.
- `tests/test_web_contract.py`: frontend contract coverage for ranking and filtering hooks.
- No backend, aggregation, API, catalog, or dependency changes.

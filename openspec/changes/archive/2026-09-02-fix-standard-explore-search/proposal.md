## Why

The Explore company search field is available in both presentation modes, but entering a search term only affects the compact preview. In the standard Explore presentation, the company list remains unfiltered, making the existing search control misleading and slowing targeted portfolio inspection.

## What Changes

- Apply the existing company-name search term to the standard Explore company list.
- Update the standard list immediately on every search input and when the existing clear button is activated.
- Display all standard-mode companies matching the trimmed, case-insensitive company-name substring search.
- Display no company rows for a non-matching search term and restore the existing lazy first-20 behavior when the search is empty or whitespace-only.
- Preserve the complete exposure ranking and each matched company's original rank while filtering.
- Keep the existing search field markup, visibility, clear-button interaction, aggregation calculations, and compact-preview behavior unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `compact-explore-preview`: Extend live company-name filtering and filtered-list behavior to the standard Explore presentation as well as compact preview mode.

## Impact

- `web/app.js`: standard Explore rendering and company-search event handling.
- `tests/test_web_contract.py`: contract coverage for standard-mode filtering, pagination restoration, and rank preservation.
- `openspec/specs/compact-explore-preview/spec.md`: clarify the shared search behavior across both Explore presentations.
- No backend, data, API, dependency, or catalog changes.

# Proposal

## Why

The Explore holdings list currently grows to the full ranked list, which makes it harder to inspect a predictable top-N slice during development. In compact preview, the wide table header also needs to remain visible during normal page scrolling so ETF columns can be identified without losing context.

## What Changes

- Add a persisted developer-mode numeric maximum for displayed top holdings in both standard and compact Explore presentations. A value of `0` means unlimited and is the default.
- Apply the maximum to the unfiltered ranked list while allowing search to find and display matches anywhere in the full ranking.
- Keep the compact Explore table header sticky during page scrolling, bounded by the table's start and end, while preserving horizontal table scrolling and the sticky holding-name column.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `compact-explore-preview`: Specify the developer-configurable maximum for both Explore presentations and preserve full-ranking search behavior.
- `explore-preview-table-styling`: Specify page-scroll sticky header behavior bounded by the compact table while retaining horizontal scrolling and the sticky holding-name column.

## Impact

Affected areas include the Explore rendering and developer settings in `web/app.js` and `web/index.html`, compact table structure and styles in `web/styles.css`, localized developer-setting labels, and focused frontend tests. No backend APIs or new dependencies are expected.

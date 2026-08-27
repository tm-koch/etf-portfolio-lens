## Why

The compact Explore holdings matrix keeps the first column visible while the ETF columns scroll horizontally, but its opaque background completely hides the cells moving underneath it. A lightly transparent sticky body column would make the scroll relationship visible while retaining the fixed holding labels.

## What Changes

- Apply a slightly translucent treatment to the sticky holding-name body cells in the compact Explore table.
- Preserve an opaque sticky header so the `Holding` label remains clear.
- Preserve alternating row colors, hover feedback, text fading, table dimensions, and horizontal scrolling behavior.
- Add focused verification for the transparent sticky-column behavior on desktop and mobile-sized layouts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `compact-explore-preview`: The responsive compact holdings matrix SHALL allow horizontally scrolling ETF cells to remain faintly visible beneath the sticky holding column without compromising readability.

## Impact

- `web/styles.css`: compact Explore table sticky-column styling and related visual states.
- `openspec/specs/compact-explore-preview/spec.md`: responsive table behavior contract.
- Browser-level or focused UI verification for horizontal scrolling, row states, and mobile presentation.
- No API, data model, dependency, or generated catalog changes.

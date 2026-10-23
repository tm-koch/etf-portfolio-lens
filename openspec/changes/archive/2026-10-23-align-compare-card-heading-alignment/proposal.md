# Proposal

## Why

Titles inside Compare metric cards, the Rollups section, and the Portfolio Selected positions box do not share the Redundancy score title's top inset across viewports. Matching that reference will make the card layouts feel consistent without changing chart content or inner rollup cards.

## What Changes

- Align Compare metric-card titles, the Rollups section heading, and the Selected positions heading with the Redundancy score title in Explore at every viewport width.
- Preserve existing subtitles, chart and legend spacing, card padding, inner rollup card layout, and responsive structure.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `comparison-donut-spacing`: Require consistent top alignment for Compare card titles and the Explore Rollups heading across viewport widths, using the Redundancy score title as the reference.
- `mobile-positions-layout`: Require the Portfolio Selected positions heading to use the same top inset as the Redundancy score title across viewport widths.

## Impact

- `web/styles.css`: align Compare, Rollups, and Selected positions headings without changing card padding.
- Responsive regression coverage for heading offsets across Portfolio, Compare, and Explore.
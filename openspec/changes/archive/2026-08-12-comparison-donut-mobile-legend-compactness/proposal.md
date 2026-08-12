## Why

The smartphone legend for the comparison donuts is still too tall because each item is forced onto its own row. That wastes vertical space and makes the chart section feel less compact than the desktop version, even though the legend can fit more efficiently.

## What Changes

- Allow the comparison legend on smartphone-sized viewports to display multiple entries per row instead of forcing one item per line.
- Keep the legend compact in the same general flow style used on larger screens, while still preserving readability.
- Preserve the existing comparison donut data, ordering, labels, and tooltips.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `comparison-donut-layout`: smartphone viewports SHALL render the comparison legend in a compact multi-entry row flow instead of a forced single-column stack, while keeping the donut and legend visually separated.

## Impact

- Frontend comparison legend layout in `web/styles.css`.
- No backend, registry, or snapshot data changes are expected.

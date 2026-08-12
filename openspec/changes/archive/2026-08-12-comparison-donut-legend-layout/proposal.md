## Why

The comparison view currently renders the sector, region, and currency doughnuts in a fixed chart box, but the visible ring size is not consistent and the legend can be clipped or compressed by the available canvas area. This makes the charts harder to compare at a glance and hides part of the labeling for the densest chart.

## What Changes

- Make the comparison doughnuts visually wider so the ring reads more clearly.
- Ensure the sector, region, and currency comparison charts use the same effective donut size.
- Make the legend fully visible for all three comparison charts.
- Preserve the existing multi-ring comparison behavior and dataset ordering.

## Capabilities

### New Capabilities
- `comparison-donut-layout`: comparison donut charts SHALL present consistent ring sizing across sector, region, and currency metrics and keep the legend fully visible.

### Modified Capabilities
- None

## Impact

- Frontend chart rendering in `web/charts.js`.
- Comparison layout sizing in `web/app.js` and `web/styles.css`.
- No backend, ingestion, registry, or snapshot data changes are expected.

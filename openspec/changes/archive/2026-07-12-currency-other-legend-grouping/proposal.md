## Why

The comparison donut charts already show currency exposure, but very small currency slices and Unknown values make the legend noisy and harder to scan. Grouping those small entries into a single `Other` bucket will make the chart easier to read while keeping the legend aligned with the plot.

## What Changes

- Group currency slices smaller than 1% into `Other` before rendering comparison charts.
- Group any currency entry labeled `Unknown` into `Other` as well.
- Show `Other` in both the donut plot and the legend so the user can see the aggregation explicitly.
- Keep the 12 o'clock chart alignment and the larger ring styling unchanged except where needed for the new currency grouping.

## Capabilities

### New Capabilities
- `currency-other-legend-grouping`: currency comparison charts render a consolidated `Other` bucket for sub-1% and Unknown entries, and the legend reflects that grouping.

### Modified Capabilities
- None.

## Impact

- Affects comparison chart label preparation in `web/app.js`.
- May require minor chart data shaping in `web/charts.js` if the legend needs to inherit the merged bucket label directly from the chart data.
- Does not change the underlying snapshot data or currency exposure calculations.

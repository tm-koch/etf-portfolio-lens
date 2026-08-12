## Why

The comparison donuts on smartphones currently leave more vertical white space than they need to, which makes the charts feel smaller and less focused. The layout already separates the legend from the canvas, so this is a good time to tighten the chart framing for small screens without changing the comparison behavior.

## What Changes

- Reduce the vertical whitespace around the comparison donuts on smartphone-sized viewports.
- Make the donut presentation responsive to screen size so phone layouts use a tighter frame than desktop layouts.
- Keep the comparison legends fully visible outside the donut canvas.
- Preserve the existing comparison data, ordering, labels, and tooltips.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `comparison-donut-layout`: smartphone viewports SHALL use a tighter comparison donut layout with less empty vertical space while preserving the existing legend separation and comparison behavior.

## Impact

- Frontend comparison chart sizing and padding logic in `web/app.js`, `web/charts.js`, and `web/styles.css`.
- Mobile presentation of the comparison tab in the static web app.
- No backend, registry, or snapshot data changes are expected.

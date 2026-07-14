## Why

The comparison donuts currently reuse a short palette and dark slice borders, which makes the chart look repetitive once the category count grows. A more distinct palette with a white separator will improve readability and make the chart feel more intentional without changing the underlying exposure data.

## What Changes

- Replace the current short donut palette with a longer set of unique, harmonic colors.
- Bias the palette toward a cool blue anchor while keeping enough variation for distinct slices.
- Increase saturation slightly so adjacent categories are easier to distinguish.
- Replace the current dark donut slice border with a white separator.
- Keep the existing chart data, labels, and percentage values unchanged.

## Capabilities

### New Capabilities
- `comparison-donut-styling`: comparison donut charts use a distinct, harmonic categorical palette and white slice separators for sectors, regions, and currencies.

### Modified Capabilities
- None.

## Impact

- Affects the donut rendering path in `web/charts.js`.
- May require small visual tuning in `web/styles.css` if the surrounding chart cards need balance after the new palette.
- Does not change snapshot generation, exposure calculations, or chart semantics.

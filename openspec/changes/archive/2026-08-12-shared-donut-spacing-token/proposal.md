## Why

The comparison donuts currently rely on separate spacing systems for the chart canvas, the surrounding card layout, and the legend blocks. That makes the mobile presentation feel uneven: the left/right donut breathing room does not match the vertical spacing to the title and legend.

## What Changes

- Introduce one shared spacing token for comparison donut layouts on mobile-sized viewports.
- Use that token to keep the donut's left/right inset, the title-to-donut gap, and the donut-to-legend gap visually aligned.
- Preserve the existing compact mobile legend behavior while making the overall chart stack feel more balanced.
- Keep the current comparison donut sizing behavior intact; this change is about spacing consistency, not ring geometry.

## Capabilities

### New Capabilities
- `comparison-donut-spacing`: consistent mobile spacing rules for the comparison donut stack, including the donut, title, and legend.

### Modified Capabilities
- `comparison-donut-layout`: the smartphone comparison layout gains a stricter spacing requirement so the donut's surrounding whitespace is symmetric and consistent across the stack.

## Impact

- `web/styles.css`: mobile chart and legend spacing will be driven from a shared token instead of separate hard-coded margins.
- `web/charts.js`: Chart.js layout padding will be aligned with the shared spacing token.
- `web/app.js`: responsive chart frame sizing may need to reference the same spacing value if the frame height is tuned alongside the new gutter.
- `openspec/specs/comparison-donut-layout/spec.md`: the existing layout spec will need a delta update for the mobile spacing requirement.

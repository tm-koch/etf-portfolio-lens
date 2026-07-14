## Why

The aggregated top-company bars do not adapt when the window is resized, so the visual length can drift away from the available space and become misleading. This needs to be fixed now because the aggregated view is explicitly presented as a responsive summary of look-through exposure, and the current behavior breaks that promise on resize.

## What Changes

- Make the top-company bars in the aggregated view respond to container or window size changes.
- Keep each bar fully contained within the visible frame as the layout narrows or expands.
- Preserve the existing stacked-segment composition and ranking order.
- Keep the exposure labels and contributor chips available so width remains readable and not ambiguous.

## Capabilities

### New Capabilities
- `aggregated-company-bar-scaling`: aggregated company rows keep their stacked bars scaled to the available container width during dynamic resize events.

### Modified Capabilities
- None.

## Impact

- Affects the aggregated company list rendering in `web/app.js`.
- May require layout or sizing adjustments in `web/styles.css`.
- Does not change portfolio ingestion, aggregation, or ranking data.

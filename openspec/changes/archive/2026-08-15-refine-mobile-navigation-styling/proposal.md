## Why

The current smartphone navigation is visually heavier than the content because it is inset, rounded, shadowed, and uses a filled blue active tile. A quieter edge-to-edge navigation bar will feel more native to a mobile app while keeping the active destination clear through blue icon and label text.

## What Changes

- Make the smartphone navigation span the full viewport width.
- Remove smartphone navigation corner rounding so the bar is rectangular.
- Remove the heavy mobile navigation shadow and retain only subtle separation from page content.
- Keep the mobile navigation background solid.
- Replace the blue active-item background with a transparent active state.
- Render both the active icon and active label in the accent blue.
- Keep inactive icons and labels muted.
- Preserve the mobile safe-area inset and content clearance behavior.
- Leave desktop navigation positioning and styling unchanged.

## Capabilities

### New Capabilities

### Modified Capabilities

- `bottom-navigation`: Refine smartphone navigation geometry, visual emphasis, and active-state colors without changing destination behavior or accessibility semantics.

## Impact

- `web/styles.css`: Update mobile-only navigation dimensions, border radius, shadow, and active-state rules.
- No changes to navigation state, URL behavior, destination labels, icons, browser storage, APIs, or desktop layout.
- No new dependencies.

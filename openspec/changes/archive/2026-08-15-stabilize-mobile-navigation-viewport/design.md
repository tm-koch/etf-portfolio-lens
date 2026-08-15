## Context

The mobile navigation is fixed to the viewport bottom and already uses `env(safe-area-inset-bottom)`. On Firefox for Android, the browser's dynamic toolbar changes the visual viewport during scrolling. The current navigation has intrinsic height from button minimums and padding, so the fixed element can appear to jump and show changing whitespace below its icons. Firefox desktop responsive mode does not reproduce the real browser toolbar, so it is not a sufficient validation environment for this issue.

## Goals / Non-Goals

**Goals:**

- Make the mobile navigation's total height stable while Firefox Android changes the visual viewport during scroll.
- Give the icon-and-label row and Firefox Android navigation footprint explicit heights independent of dynamic environment values.
- Preserve safe-area expansion on platforms where the safe-area environment value is stable.
- Keep page bottom clearance aligned with the stable navigation footprint.
- Preserve fixed positioning, edge-to-edge styling, active colors, destination behavior, accessibility, and desktop presentation.
- Verify the result on real Firefox Android scrolling with browser chrome expanded and collapsed.

**Non-Goals:**

- Add JavaScript listeners for `visualViewport.resize` or browser-toolbar state.
- Change navigation destinations, persistence, URL behavior, or panel rendering.
- Replace fixed positioning with sticky positioning in this change.
- Change desktop responsive emulation behavior or desktop navigation styling.

## Decisions

### Use explicit mobile geometry

Define a mobile navigation row height and set the navigation height to the row height plus `env(safe-area-inset-bottom)`. The navigation's top and horizontal padding remain fixed, while safe-area padding is reserved only at the bottom. Set each destination button to the same row height rather than relying on `min-height` and content-driven sizing.

This makes the icon-to-bottom spacing deterministic. Leaving the navigation intrinsically sized allows browser safe-area and fixed-element calculations to change the visible whitespace.

### Keep the fixed navigation on the basic paint path

The mobile navigation must remain fixed and opaque, with `backdrop-filter`, containment, `isolation`, transform promotion, and `will-change` left disabled. Firefox Android can show subpixel layer jitter when a fixed element is moved into a special compositing or paint-containment path while the visual viewport changes.

This targets Firefox Android's fixed-element repaint behavior without adding scroll listeners or abandoning the always-visible navigation contract. Do not read viewport values from JavaScript or update CSS variables on `visualViewport.resize`; those events occur during toolbar animation and could create additional layout movement.

### Preserve fixed positioning

Keep `position: fixed` and `bottom: 0` because the navigation is intended to remain available while scrolling. A sticky alternative could avoid some fixed-element repaint behavior, but it would change the interaction model and is not needed unless Firefox-specific testing shows the browser still moves a stable-height bar.

### Validate on real Firefox Android

Use desktop responsive mode only for basic layout checks. The acceptance test must run on Firefox Android and include scrolling upward and downward with the browser toolbar changing state. Record the navigation rectangle, computed height, bottom padding, and visual viewport height when investigating regressions.

## Risks / Trade-offs

- [Firefox may still repaint a fixed element when its visual viewport changes] -> Keep the element on the basic opaque paint path; evaluate sticky positioning separately only if the basic fixed element still moves.
- [A taller explicit navigation can reduce usable content space] -> Keep the row height equal to the current intended navigation footprint and preserve only the required safe-area inset.
- [Firefox Android devices with display cutouts may need bottom inset compensation] -> Prefer stable geometry for the reported Firefox toolbar issue and validate any affected cutout device separately; reintroduce a bounded inset only if required.
- [Body clearance and navigation height can drift] -> Define both from the same row-height custom property and verify the last content remains reachable.

## Migration Plan

1. Add the mobile navigation row-height custom property and explicit navigation dimensions.
2. Set destination buttons and their container to the stable row height.
3. Align mobile body bottom clearance with the same navigation footprint.
4. Verify Firefox Android scroll behavior and desktop styling.
5. Roll back by reverting the CSS-only geometry changes if the mobile result is worse.

## Open Questions

No product questions remain. Firefox Android should use a fixed 79px navigation footprint; WebKit mobile may add its stable safe-area inset.

## Context

The mobile navigation is an edge-to-edge, fixed white bar with a 1px top border. Its height, safe-area handling, and basic paint path were recently tuned to reduce Firefox Android scroll movement. The remaining visual issue is that the top boundary does not clearly separate the navigation from the page content.

## Goals / Non-Goals

**Goals:**

- Add a small upward-facing shadow above the mobile navigation.
- Preserve the existing fixed geometry, safe-area behavior, and scroll-stability choices.
- Keep the visual treatment quiet and static.
- Leave desktop navigation unchanged.

**Non-Goals:**

- Change navigation height, padding, position, or safe-area calculations.
- Add animation, transitions, or scroll-dependent styling.
- Restore the former heavy global card shadow.
- Modify JavaScript or navigation behavior.

## Decisions

### Use a mobile-only static box shadow

Set the mobile navigation shadow to `0 -2px 8px rgba(22, 34, 58, 0.10)`. The negative vertical offset projects the shadow above the bar, while the short blur and low opacity provide separation without making the dock dominant.

The existing desktop shadow remains unaffected because the declaration belongs inside the mobile media query. A pseudo-element was considered, but it would add another positioned layer without improving the simple boundary effect.

### Keep the border and shadow together

Retain the existing 1px top border and add the shadow beneath it. The border provides a crisp edge and the shadow supplies a gradual transition into page content. Removing the border would make the boundary less defined on light backgrounds.

### Avoid motion and geometry changes

Do not add transitions, animations, `filter`, transform promotion, containment, or scroll listeners. A static `box-shadow` does not alter layout dimensions and avoids reintroducing the special fixed-layer behavior addressed by the previous change.

## Risks / Trade-offs

- [The shadow could make the navigation too prominent] -> Keep opacity at 0.10 and blur at 8px; do not reuse the stronger global shadow.
- [Firefox may repaint the shadow during toolbar changes] -> Keep it static and avoid animation or compositor hints; validate on the real device when available.
- [The shadow may be barely visible on some screens] -> Retain the 1px border as the guaranteed separation cue.

## Migration Plan

1. Replace the mobile `box-shadow: none` declaration with the restrained static top shadow.
2. Verify mobile visual separation and unchanged computed geometry.
3. Verify desktop navigation remains unchanged.
4. Roll back by restoring `box-shadow: none` if device testing shows unwanted repaint or prominence.

## Open Questions

No product questions remain. The proposed shadow is mobile-only, static, and uses `0 -2px 8px rgba(22, 34, 58, 0.10)`.

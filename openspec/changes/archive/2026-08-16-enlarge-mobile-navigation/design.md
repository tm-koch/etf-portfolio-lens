## Context

The mobile navigation currently uses a 57.6px icon-and-label row after the compact-navigation refinement, with 18px icons and 0.75rem labels. The fixed bar, safe-area handling, content clearance, active/inactive styling, and desktop layout are already established and should remain stable while the mobile presentation becomes slightly more readable.

## Goals / Non-Goals

**Goals:**

- Increase the mobile row to 64px, approximately 10% larger than 57.6px.
- Increase mobile labels to 0.8rem for modestly improved legibility.
- Preserve 18px icons, current spacing, active/inactive colors and weights, and minimum touch-target sizing.
- Keep body clearance coupled to the shared mobile row variable.

**Non-Goals:**

- Change desktop navigation styling, placement, or typography.
- Change icon size, labels, destination state, persistence, URL behavior, or JavaScript.
- Change the active transparent background, mobile shadow, full-width placement, or safe-area behavior.
- Increase the row beyond the point where the mobile navigation becomes visually dominant or labels wrap.

## Decisions

### Keep the change mobile-only

Update the existing rules inside the `max-width: 760px` media query. This preserves the desktop navigation contract and limits the visual adjustment to the mode requested. A global sizing change was rejected because desktop currently has independent 20px icons and 16px button text.

### Use a 64px row and 0.8rem labels

Set `--mobile-nav-row-height` to 64px and the mobile button label size to 0.8rem. The 64px target is a practical rounded CSS value that is approximately 10% above 57.6px while remaining comfortably above the 44px touch-target minimum. The 0.8rem label is a small increase over 0.75rem without changing the existing icon-label arrangement.

An exact fractional 63.36px row was rejected because the rounded 64px value is easier to maintain and inspect while remaining within the requested approximate increase. A larger type jump was rejected because it could cause wrapping at narrow widths.

### Preserve shared clearance and state rules

Continue deriving the navigation total height and body bottom padding from `--mobile-nav-row-height`, including any safe-area inset. Leave the existing active/inactive selectors, spacing, colors, and font weights unchanged. No JavaScript changes are needed because navigation state is already exposed through the existing classes and `aria-current` attribute.

## Risks / Trade-offs

- [The larger row may reduce available content height] -> Keep the increase limited to 64px and derive clearance from the shared variable so content remains reachable.
- [The larger label may wrap on narrow screens] -> Retain the existing short labels and verify at 320px, 375px, 430px, and 760px widths.
- [A larger active label may feel visually heavier] -> Preserve the existing 0.8rem size for both states and keep active emphasis limited to bold blue styling.
- [Safe-area devices may increase the total footprint further] -> Preserve safe-area padding separately from the fixed 64px icon-and-label row.

## Migration Plan

1. Update only the mobile row variable and mobile label font size in `web/styles.css`.
2. Verify mobile geometry, label fit, touch target height, clearance, active/inactive state styling, and keyboard behavior.
3. Confirm desktop computed styles remain unchanged.
4. Roll back by restoring the 57.6px row and 0.75rem label values if the enlarged presentation causes wrapping or excessive visual weight.

## Open Questions

None. The target is 64px for the mobile row and 0.8rem for mobile navigation labels.

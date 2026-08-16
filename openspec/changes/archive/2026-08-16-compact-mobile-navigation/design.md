## Context

The mobile navigation is fixed at the bottom of the viewport at widths up to 760px. Its current icon-and-label row is 78px high, uses 20px icons, and applies a 700 font weight to every destination. The existing navigation contract requires stable geometry, safe-area content clearance, muted inactive destinations, and an accent-blue active destination.

## Goals / Non-Goals

**Goals:**

- Reduce the mobile navigation footprint without compromising destination discoverability or touch access.
- Use a 64px icon-and-label row with 18px icons, a 0.75rem label size, and reduced internal gaps.
- Make inactive labels regular weight and muted; make only the active label and icon bold and accent blue.
- Keep the row height explicit so viewport changes do not cause layout shifts.
- Preserve the existing fixed placement, full-width opaque surface, safe-area handling, content clearance, focus behavior, and destination switching.

**Non-Goals:**

- Change desktop navigation dimensions, colors, or placement.
- Change navigation labels, icons, state persistence, URL behavior, or JavaScript rendering.
- Remove visible labels or reduce button hit areas below 44px.
- Change the existing active transparent background or mobile shadow treatment.

## Decisions

### Scope all sizing changes to the mobile media query

The compact rules will live under the existing `max-width: 760px` media query. This keeps desktop behavior unchanged and makes the new presentation explicitly responsive. A global `.tab-button` change was rejected because it would alter desktop typography and geometry.

### Use fixed compact dimensions

Set the mobile row and button height to 64px, the icon to 18px square, the label to 0.75rem, the icon-label gap to 3px, and the navigation item gap to 2px. The button remains a full-height flex control, so its 64px height remains above the 44px minimum touch target while preserving predictable geometry.

A smaller but content-driven height was rejected because it could make the fixed navigation footprint unstable and reduce touch access on narrow devices.

### Separate inactive and active emphasis with CSS state

Set the base mobile button weight to 400 and retain `var(--muted)` for inactive content. Set the active button weight to 700 and `var(--accent)` for both its label and Lucide icon. The active background remains transparent. JavaScript already toggles `.active` and `aria-current`, so no state or rendering changes are needed.

### Keep content clearance coupled to the row variable

Continue deriving body bottom padding and navigation total height from `--mobile-nav-row-height`, including the safe-area inset. Changing the shared row variable to 64px keeps the page clearance synchronized with the compact bar.

## Risks / Trade-offs

- [Smaller labels may be harder to read on narrow screens] -> Keep labels visible, use the existing high-contrast typeface and muted/accent tokens, and verify at 320px and 375px widths.
- [A compact row could reduce touch comfort] -> Keep each button 64px tall, above the 44px minimum target.
- [Reduced spacing could make destinations feel crowded] -> Keep equal flex allocation, a 2px item gap, and a 3px icon-label gap; verify all three labels fit without wrapping.
- [Changing the shared row variable could affect content clearance] -> Verify the body bottom padding and navigation total height continue to include the safe-area inset.

## Migration Plan

1. Update only the mobile navigation sizing and typography overrides in `web/styles.css`.
2. Validate mobile geometry, colors, typography, focus visibility, and content clearance at representative widths.
3. Confirm desktop computed navigation styles remain unchanged.
4. Roll back by removing the compact mobile overrides and restoring the 78px row variable if visual or accessibility checks fail.

## Open Questions

None. The compact target dimensions are 64px row height, 18px icons, 0.75rem labels, 3px icon-label spacing, and 2px item spacing.

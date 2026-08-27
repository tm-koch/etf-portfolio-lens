## Context

The web app uses a centered `.content-column` with a `24px` page padding and an `.app-shell` with an `18px` top-level gap. The desktop primary navigation also uses a `48px` total horizontal inset and `10px` internal bar padding. These outer values constrain the active area available to the main portfolio and analysis panels. Mobile overrides already make destination content full width and reserve space for the fixed bottom navigation.

The request concerns perceived active area, so the change must distinguish shell spacing from internal component rhythm. Existing card padding, table cell padding, chart spacing, and control hit areas are not targets.

## Goals / Non-Goals

**Goals:**

- Reduce the desktop/tablet content-column padding and top-level shell gap by approximately one third.
- Reduce the desktop primary-navigation outer horizontal inset in the same proportion where it is coupled to the page shell.
- Preserve the centered `1440px` content maximum and the navigation's independent app-bar behavior.
- Preserve mobile full-width content, bottom-navigation clearance, component readability, and usable hit targets.
- Validate that more content is visible without overlap or clipping.

**Non-Goals:**

- No changes to inner card or panel padding, table spacing, chart dimensions, typography, or data presentation.
- No changes to the mobile navigation row height, safe-area handling, or fixed navigation behavior.
- No changes to application logic, APIs, persistence, or dependencies.

## Decisions

1. **Reduce shell values directly in CSS.** Adjust the owning layout declarations for `.app-shell`, `.content-column`, and the desktop primary navigation rather than applying transforms or negative margins. Direct values keep layout flow, hit testing, and sticky positioning predictable.

   Alternatives considered: scaling the whole page would also shrink typography and controls; negative margins would reclaim space but risk clipping and make responsive behavior harder to reason about.

2. **Use one-third reductions rounded to practical pixels.** Use `12px` for the `18px` shell gap, `16px` for the `24px` content padding, and a matching reduced desktop navigation width inset. These values are easy to audit and preserve the existing spacing rhythm while providing a measurable density improvement.

   Alternatives considered: a much denser token reset could make the interface cramped; fractional or viewport-relative values would make the target reduction less predictable.

3. **Keep mobile overrides authoritative.** The existing `max-width: 760px` content-column padding of `0` and fixed navigation clearance remain unchanged. Desktop/tablet density changes must not leak into mobile bottom navigation geometry.

   Alternatives considered: applying the reduction globally would have no useful effect on the already full-width content but could unintentionally alter mobile navigation spacing.

4. **Validate by measuring layout geometry and visual interaction.** Browser checks should compare the shell's computed spacing and visible content area at desktop/tablet/mobile widths, while checking for overflow, overlap, stable navigation hit areas, and unchanged internal component spacing.

## Risks / Trade-offs

- [Panels feel too close to the viewport edge] → Keep the reduced `16px` content gutter on desktop/tablet and inspect representative wide and medium viewports.
- [Navigation and content gutters become visually inconsistent] → Reduce the coupled desktop navigation inset together with content-column padding and verify alignment.
- [Mobile layout regression] → Preserve the mobile overrides verbatim and test the fixed bottom navigation at a phone-sized viewport.
- [More dense layout increases visual competition] → Leave internal component spacing and typography unchanged.

## Migration Plan

Update the shell spacing declarations, then run browser geometry and responsive interaction checks plus the existing repository tests. Rollback is a CSS-only restoration of the prior shell values; no data migration is required.

## Open Questions

None. The target is a roughly one-third reduction of outer shell spacing, with internal and mobile-specific spacing preserved.

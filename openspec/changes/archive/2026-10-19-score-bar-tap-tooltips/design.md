# Design

## Context

The score bars are DOM elements with colored band spans, while the comparison donuts are Chart.js canvases with localized tooltips. Each score band already has a translation key for its hover title, and the bars expose an accessible summary of the current score. See proposal.md for motivation and the spec delta for the touch behavior.

## Goals / Non-Goals

**Goals:**
- Show the tapped band's localized label directly below the touch point on both score bars.
- Preserve existing hover tooltips, current score badges, and score-bar accessibility summaries.
- Keep the tooltip visible within the score card and avoid shifting surrounding layout.

**Non-Goals:**
- Change score calculations, rating boundaries, donut chart behavior, or persistent score badges.
- Replace the DOM score bars with canvas charts or add a dependency.

## Decisions

- Use a small HTML tooltip for score-band taps rather than routing the bars through Chart.js. The bars are already DOM-based, and their existing translation keys can provide the localized tooltip text.
- Resolve the band from the touch's horizontal position on the track, not from the event target alone. The score marker overlays the bands and must not cause a tap to report the marker's current rating instead of the band under the finger.
- Position the tooltip immediately below the touch point, clamp it within the score card, and render it as an overlay so the card layout does not move. A tap on another band replaces the current label; an outside tap or Escape dismisses it. Do not prevent normal page scrolling.
- Keep desktop hover behavior intact and style the touch tooltip with the existing chart tooltip surface, text, border, and theme colors.

## Risks / Trade-offs

- **The tapped band is narrow near small viewports or score boundaries** → Resolve the band from the actual track coordinate and verify both bars at narrow phone widths.
- **A tooltip near the card edge could be clipped or cover endpoint values** → Clamp its horizontal position within the score card and visually verify endpoint readability at both ends of each bar.

## Migration Plan

No data migration is needed. Implement the shared interaction, add focused regression coverage, and verify touch placement and existing hover behavior. Rollback consists of removing the touch tooltip behavior while retaining the current hover titles.

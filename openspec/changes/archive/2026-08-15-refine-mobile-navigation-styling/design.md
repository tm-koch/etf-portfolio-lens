## Context

The existing bottom-navigation capability is implemented in the dependency-light static web app. On smartphone widths, the navigation is fixed with a 14px horizontal inset, rounded top corners, a prominent shadow, and a blue filled background for the active destination. The requested refinement is limited to smartphone presentation; desktop navigation remains unchanged.

## Goals / Non-Goals

**Goals:**

- Make the mobile navigation edge-to-edge and rectangular.
- Reduce visual prominence by removing the heavy shadow.
- Keep the navigation solid and visually separated with a subtle top border.
- Show the active mobile icon and label in the accent blue without a filled active background.
- Preserve safe-area spacing, content clearance, focus visibility, and existing destination behavior.

**Non-Goals:**

- Change desktop navigation styling or placement.
- Change destination labels, icons, state persistence, URL behavior, or accessibility semantics.
- Change the navigation height or content layout beyond the spacing required by the edge-to-edge bar.
- Add dependencies or modify JavaScript.

## Decisions

### Scope style changes to the mobile media query

Keep the existing desktop rules and place all visual overrides in the `max-width: 760px` media query. This prevents the mobile refinement from changing the established desktop navigation.

An unconditional change to `.primary-navigation` would be shorter but would violate the desktop-unchanged requirement.

### Use an edge-to-edge opaque rectangle

Set the mobile navigation's left and right offsets to zero and remove its border radius. Keep the solid white background and preserve bottom safe-area padding. The page's mobile content clearance remains tied to the navigation's footprint so the edge-to-edge bar does not cover content.

Keeping the existing 14px inset would preserve the current card-like appearance, which is the visual problem this change addresses.

### Use color-only active styling

Override the mobile active button to retain a transparent background and set both its text color and nested icon color to `var(--accent)`. Inactive items retain the muted color. A subtle top border replaces the heavy shadow as the visual boundary.

The existing `aria-current` state and keyboard focus behavior remain unchanged; CSS provides the visual treatment without adding JavaScript state.

## Risks / Trade-offs

- [Edge-to-edge navigation can feel visually attached to the viewport rather than the app shell] -> Keep the solid surface and subtle top border while removing only the heavy shadow and rounded card treatment.
- [Blue text and icon may have insufficient contrast against the solid background if the accent changes] -> Use the existing accent token and verify contrast and legibility at mobile width.
- [Removing the shadow can reduce separation from content] -> Retain a one-pixel top border and solid background.
- [Safe-area padding can make the bar taller on some devices] -> Preserve the existing safe-area expression and verify labels remain vertically centered.

## Migration Plan

1. Update only mobile navigation CSS rules.
2. Verify desktop computed styles remain unchanged.
3. Verify mobile edge-to-edge geometry, active colors, safe-area spacing, and content clearance.
4. Roll back by reverting the mobile CSS overrides if the visual result is not acceptable.

## Open Questions

No product questions remain. The active icon and label are both blue, the mobile bar is edge-to-edge and rectangular, and the heavy shadow is removed.

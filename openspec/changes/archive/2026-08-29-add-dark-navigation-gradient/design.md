## Context

The static frontend defines the primary navigation in `web/styles.css` as a sticky frame around the tab buttons. Bright mode already gains visual separation from the surrounding page through light surface treatment, but the dark-mode override currently replaces that separation with the flat `--card-strong` color. The change is limited to presentation and must preserve the existing navigation structure, sticky behavior, active state, and mobile layout.

## Goals / Non-Goals

**Goals:**

- Give dark-mode primary navigation a subtle top-to-bottom gradient that separates it from the dark page frame.
- Keep the gradient theme-aware, readable, and visually consistent with the existing bright navigation treatment.
- Validate the result at desktop and mobile breakpoints without changing navigation behavior.

**Non-Goals:**

- Changing navigation labels, icons, tab routing, or active-tab colors.
- Adding animation, new dependencies, or a new navigation component.
- Changing the page-wide dark background or other dark surfaces.

## Decisions

### Define the dark navigation edge as a theme token

Keep `--navigation-background` as the flat theme surface and add a `--navigation-edge-gradient` token with a restrained dark gradient. Apply the edge token to a non-interactive pseudo-element anchored at the navigation separator, rather than painting the navigation bar itself.

A token is preferred over a dark-only selector with an inline gradient because it keeps theme ownership explicit and makes future theme adjustments local. Reusing the page background is rejected because it would reduce separation from the frame; applying a gradient to the full navigation surface is rejected because it tints the controls instead of beginning at the separator.

### Preserve the existing navigation cascade

Keep the current sticky positioning, shadow, border radius, spacing, and active-tab gradient unchanged. Use the flat navigation surface token and position the edge layer below the desktop separator and above the mobile separator.

This avoids visual regressions in responsive navigation and ensures the active tab remains the strongest visual state.

### Verify through contract and browser checks

Add a focused web contract assertion for the dark navigation token and its application. Manually check desktop and mobile-sized viewports in Dark mode, confirming the gradient is visible, text remains readable, and the navigation remains correctly positioned.

## Risks / Trade-offs

- [Gradient contrast is too weak against the dark frame] -> Use two nearby but distinct dark surface colors and verify the boundary visually.
- [Gradient competes with active navigation state] -> Keep the gradient low contrast and leave the existing active-tab gradient unchanged.
- [Token is accidentally overridden at a responsive breakpoint] -> Check the desktop and mobile cascade and keep the token application on the base navigation rule.

## Migration Plan

No data migration is required. Deploy the stylesheet and contract-test change together. Rollback consists of restoring the flat dark navigation background declaration.

## Open Questions

None.

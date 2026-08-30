## Context

The application already supports Bright, Automatic, and Dark color modes in `web/app.js`. The preference is stored under `etf-lens.color-mode.v1`, Automatic follows `prefers-color-scheme`, and the current control is rendered inside the About this build dialog on the Home panel. This makes a global preference dependent on opening a developer-oriented dialog and unavailable when users are viewing another destination.

The primary navigation is responsive: it is a persistent top app bar on desktop and a fixed bottom bar on mobile. The new selector must remain globally discoverable without competing with the four destination buttons or changing their mobile geometry.

## Goals / Non-Goals

**Goals:**

- Expose one global color-mode control in a top-right utility area.
- Preserve the existing three choices, persistence key, Automatic resolution, and live chart theme updates.
- Keep the control keyboard accessible and usable at desktop and mobile widths.
- Keep About this build focused on provenance and developer details.
- Ensure the selector does not alter primary navigation order, active-tab behavior, or mobile bottom-navigation geometry.

**Non-Goals:**

- Do not add new color modes or change theme tokens.
- Do not change the meaning of Automatic or its system-preference listener.
- Do not make the selector Home-specific or duplicate it in multiple dialogs.
- Do not redesign the primary destination navigation.

## Decisions

1. **Use a global utility placement without a separate frame.** The preference affects every destination and persists globally, so its control belongs in app-level chrome. The control is positioned at the top right on the same visual level as the active panel's primary title row, including the Home hero's `ETF Portfolio Lens` title, without adding a standalone utility row or card. On mobile it occupies that same title level above the content while the destination navigation remains at the bottom.

2. **Keep a menu button with the existing three options.** A button labelled with the current mode and its icon makes the current state visible and supports Bright, Automatic, and Dark without introducing a second interaction model. A simple sun/moon toggle would hide the Automatic option and make the current preference ambiguous.

3. **Reuse the existing rendering and state functions.** Move the DOM anchor for the control, not the color-mode state machine. `renderColorModeControl`, `setColorMode`, storage, media-query handling, and chart refresh behavior should remain the single implementation path.

4. **Preserve dialog ownership for build details.** Remove only the color-mode row from the developer settings section. Keep the About this build action and dialog so source, deployment, warnings, and compact Explore settings remain available through their existing workflow.

5. **Test behavior and responsive placement through the web contract.** Add assertions for the global anchor, absence from the build dialog, menu semantics, all three options, and preservation of the existing storage and Automatic behavior. Verify that the mobile selector is outside the fixed bottom navigation footprint.

## Risks / Trade-offs

- [Risk] A compact top-right control may be less obvious than a full text label on narrow screens. -> Mitigation: retain an accessible name, current-mode state, tooltip/title, and a visible icon; use the full label where space allows.
- [Risk] Moving the DOM anchor could break event wiring or icon initialization. -> Mitigation: keep the existing IDs and event delegation, and add contract coverage for the new location.
- [Risk] Aligning the utility control with the Home hero can make its position feel disconnected on other destinations. -> Mitigation: keep it in app-level chrome with stable viewport-relative placement and use the same top-right alignment on every destination.
- [Risk] A mobile top-right control could be mistaken for Home content. -> Mitigation: place it in app-level chrome with consistent positioning across all destinations.

## Migration Plan

1. Add the global utility control markup and move the existing color-mode control out of the build dialog.
2. Update JavaScript element lookup and rendering only as needed; preserve IDs and behavior.
3. Add responsive styles and contract tests for desktop and mobile placement.
4. Run focused web tests and the full suite.
5. Roll back by restoring the control markup to the build dialog and removing the utility styles; stored preferences remain compatible throughout.

## Open Questions

- Should the desktop utility display the current mode text at all widths, or become icon-only below a compact breakpoint?
- Should the top-right utility area include only color mode now, or reserve space for future global settings?

## Context

The mobile navigation renders four `<button>` elements inside the fixed bottom navigation bar. In Bright mode, the navigation background is white and inactive buttons use a transparent background. The app assigns `.active` in the synchronous `click` handler, but Chrome Mobile also paints its native tap highlight during the touch-to-click sequence. That browser paint is visible as a light-blue flash because the button does not define a mobile pressed state or tap-highlight color.

## Goals / Non-Goals

**Goals:**

- Remove the browser-specific flash from mobile navigation taps.
- Keep a deliberate pressed-state indication while the pointer or touch is down.
- Preserve the persistent active-tab appearance and keyboard focus visibility.
- Limit the styling change to the primary navigation and retain desktop behavior.
- Verify that selecting a tab still updates the same panel and active class synchronously.

**Non-Goals:**

- Changing tab destinations, URL routing, local-storage behavior, or panel rendering.
- Removing all touch feedback from the application.
- Altering the color-mode model or the PWA install flow.
- Adding a JavaScript pointer-state implementation unless CSS cannot provide the required behavior.

## Decisions

### Control the mobile tap highlight in CSS

The primary navigation buttons SHALL set `-webkit-tap-highlight-color: transparent` and define an explicit `:active` background that uses the application accent at low opacity. This targets Chrome's native overlay while preserving visible feedback during the touch gesture.

Alternatives considered: leaving the browser default preserves platform behavior but causes the reported flash; handling `pointerdown` and `pointerup` in JavaScript adds state-management complexity and risks stuck pressed states; removing all active feedback would hide the symptom at the cost of touch usability.

### Add an explicit keyboard focus treatment

The navigation buttons SHALL use `:focus-visible` with the existing focus-ring token and an offset that remains legible against the navigation bar. This ensures suppressing the tap highlight does not reduce keyboard or assistive-technology focus visibility.

Alternatives considered: relying on the browser outline is inconsistent with the app's other controls; using `:focus` would leave a persistent ring after touch activation on some browsers.

### Scope the fix to mobile navigation

The pressed-state and tap-highlight rules SHALL be scoped to `.primary-navigation .tab-button`, with the mobile-specific visual treatment placed beside the existing mobile navigation rules. The `.active` class remains the source of truth for the selected tab, and the existing `setTab()` event path remains unchanged.

Alternatives considered: a global button reset could affect dialogs, import controls, and sharing actions; changing `setTab()` would not remove a browser paint that occurs before the click handler.

## Risks / Trade-offs

- [Risk] Transparent tap highlight may differ from platform conventions on browsers other than Chrome. -> Mitigation: provide an explicit CSS `:active` background and retain `:focus-visible` feedback.
- [Risk] A low-opacity pressed background could be too subtle in one color mode. -> Mitigation: test Bright and Dark modes at a mobile viewport and verify contrast against each navigation background.
- [Risk] Browser screenshot automation may not reproduce native touch painting exactly. -> Mitigation: assert the CSS contract in web tests and manually verify Chrome Mobile behavior after deployment.

## Migration Plan

1. Add the scoped CSS tap-highlight, pressed-state, and focus-visible rules.
2. Extend web contract tests for those rules and verify tab selection still works.
3. Test Bright and Dark modes at a mobile viewport, then publish normally; no data or service-worker migration is required.
4. Roll back by reverting the CSS and test changes if a target browser shows a worse interaction state.

## Open Questions

- Confirm the final pressed-state opacity after testing on a physical Chrome Mobile device; the implementation can tune the value without changing the interaction contract.

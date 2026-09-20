## Context

The Portfolio catalog renders each ETF from `web/app.js`. An ETF already present in `state.portfolio` is rendered with the label `Added` and the native `disabled` attribute. The shared catalog button rule in `web/styles.css` currently gives both actionable and completed buttons the same filled accent appearance.

The change is limited to the static web client. Existing portfolio state, local persistence, imports, share links, and duplicate-add protection remain the source of truth for whether an ETF is added.

## Goals / Non-Goals

**Goals:**

- Make the completed `Added` state visually distinct from the actionable `Add` state.
- Preserve the existing disabled semantics and state-driven rerender behavior.
- Keep the styling compatible with bright and dark color modes.
- Make the state contract easy to verify with focused static web tests.

**Non-Goals:**

- Change portfolio state shape, persistence, import behavior, or share-link behavior.
- Add a new interaction for removing or toggling an ETF from the catalog.
- Change the styling of unrelated disabled buttons.

## Decisions

### Use an explicit added-state marker

The catalog button will receive a dedicated state marker when `selected` is true, alongside its existing `disabled` attribute and `Added` label. The style will target that marker rather than all disabled buttons.

This is preferred over a disabled-only selector because disabled is a general interaction state and may be used by unrelated controls later. A dedicated marker expresses the product meaning and prevents accidental styling bleed.

### Reuse the existing accent token

The added-state border and text will use `var(--accent)`, while the background will be white as requested. This keeps the blue consistent with the current application identity without introducing a new color token.

The added-state rule must override the existing filled catalog button declarations, including their `!important` declarations, and must restore full opacity so the status does not look unavailable.

### Keep the native disabled state

The button remains disabled after an ETF is added. The existing `addPosition()` guard remains in place as a defensive state check, while the disabled control communicates that the action is complete.

## Risks / Trade-offs

- [Risk] White added-state buttons may feel brighter in dark mode. → Mitigation: retain the requested white background and use the existing accent blue for sufficient contrast; verify both color modes during implementation.
- [Risk] The current catalog rule uses `!important`, which can make an override ineffective. → Mitigation: place the explicit added-state rule after the base rule and use matching specificity/importance only for the state properties that need overriding.
- [Risk] Static contract tests could verify markup without catching a browser rendering regression. → Mitigation: keep the selector and state marker explicit so a focused browser check can be added later if the web test harness expands.
## Context

The portfolio tab currently uses gradient-styled action buttons for add and remove actions, while the active tab state already establishes the project’s primary accent color. The UI would be more coherent if these action buttons shared the same solid color treatment as the active tab.

This change is isolated to front-end styling in the web app. It does not affect portfolio data, tab behavior, or button semantics.

## Goals / Non-Goals

**Goals:**
- Make portfolio add and remove buttons use the same solid accent color as active tabs.
- Preserve the existing button shape, spacing, and interaction affordances.
- Keep the button text readable and the actions clearly differentiated from neutral content.

**Non-Goals:**
- No changes to portfolio data handling or tab logic.
- No redesign of the portfolio layout.
- No new color system or theme tokens.

## Decisions

1. Reuse the existing active-tab accent color for portfolio action buttons.
   - Rationale: it keeps the visual language consistent and avoids adding another button treatment.
   - Alternatives considered: keep the gradients; rejected because they visually compete with the active tab state.
   - Alternatives considered: introduce a separate button color; rejected because it creates unnecessary visual variants for the same interaction tier.

2. Keep the current button geometry and typography unchanged.
   - Rationale: the issue is color consistency, not button layout.
   - Alternatives considered: adjust padding or radius at the same time; rejected to keep the change scoped and low-risk.

3. Preserve a single style rule for both add and remove buttons where practical.
   - Rationale: these controls belong to the same action family and should read consistently.
   - Alternatives considered: style them separately; rejected because the user asked for the same treatment on both buttons.

## Risks / Trade-offs

- [Solid color buttons may feel heavier than the previous gradients] → Mitigation: keep the existing shape, contrast, and spacing so the visual weight remains familiar.
- [Button text contrast could regress on the solid accent] → Mitigation: verify legibility in the browser and adjust foreground color only if needed.

## Migration Plan

No migration is required.

1. Update the portfolio action button styles to use the active-tab color.
2. Confirm both add and remove buttons match the active tabs visually.
3. Verify the portfolio tab still reads clearly on the current light theme.
4. Roll back only the style rule if any contrast issue appears.

## Context

The comparison toolbar already renders a checkbox pill for each selected ETF, but it only shows the ticker. The underlying ETF name is already available in the existing comparison selection data, so the change is limited to presentation and hover affordance.

This is a front-end UX refinement. It does not alter comparison behavior, chart logic, or portfolio state.

## Goals / Non-Goals

**Goals:**
- Show the full ETF name in the comparison selector hover tip.
- Preserve the existing checkbox selection behavior and visible ticker label.
- Keep the interaction lightweight and non-intrusive.

**Non-Goals:**
- No changes to comparison chart calculations.
- No changes to portfolio data or ETF metadata loading.
- No redesign of the comparison toolbar layout.

## Decisions

1. Attach the hover tip to the comparison pill label rather than introducing a custom tooltip component.
   - Rationale: the label already wraps the checkbox and visible ticker, so it is the smallest reliable hover target.
   - Alternatives considered: attach the tooltip only to the checkbox; rejected because the hover area is smaller and less discoverable.
   - Alternatives considered: build a custom tooltip UI; rejected because it adds unnecessary complexity for a single piece of text.

2. Use the existing ETF full name from the selection data.
   - Rationale: the data is already present and avoids duplicating any lookup logic.
   - Alternatives considered: fetch or derive a separate tooltip string; rejected because there is no new data requirement.

3. Keep the visible label as the ticker.
   - Rationale: the ticker remains the compact, familiar selector label while the hover tip supplies extra context.
   - Alternatives considered: replacing the visible label with the full name; rejected because it would make the toolbar much wider and harder to scan.

## Risks / Trade-offs

- [Native tooltip behavior can vary slightly by browser] → Mitigation: use the standard `title`/hover semantics on the label so the behavior remains simple and compatible.
- [Long ETF names may be truncated in some browser tooltip implementations] → Mitigation: keep the visible ticker label unchanged so the UI still works even when the hover tip presentation differs.

## Migration Plan

No migration is required.

1. Update the comparison toolbar label markup to include the ETF full name in a hover tip.
2. Verify the ticker remains visible and clickable.
3. Confirm the hover tip appears when pointing at the selector pill.
4. Roll back only the label attribute change if any browser-specific tooltip issue appears.

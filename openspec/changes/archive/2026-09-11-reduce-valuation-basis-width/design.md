## Context

The selected-positions header renders the portfolio-level valuation basis control and the adjacent Live/Imported status in `.portfolio-valuation-row`. The shared `.portfolio-valuation-control` rule currently caps both the portfolio control and the import-dialog control at 320px. Both controls now need the same 30% reduction.

## Goals / Non-Goals

**Goals:**

- Set both valuation basis control widths to 224px, exactly 70% of the current 320px cap.
- Preserve the existing status alignment, mobile stacking, and control height/hit area.
- Preserve the import-dialog layout and behavior apart from the requested width reduction.

**Non-Goals:**

- Changing valuation options, labels, state behavior, or portfolio calculations.
- Changing the Live/Imported status placement or animation.
- Changing outer page spacing or unrelated form controls.

## Decisions

Change the shared `.portfolio-valuation-control` width from `min(100%, 320px)` to `min(100%, 224px)`. Remove the redundant portfolio-row width override while retaining its margin rule, so both controls receive the same cap without duplicated width declarations.

Use `width: min(100%, 224px)` so the control is exactly 224px when space permits but can shrink within narrow containers. Keep the existing mobile row rules; the control remains full-width only up to its 224px cap and the status continues to stack below it on small screens.

A CSS contract assertion should verify the shared 224px rule and the absence of the old 320px cap, preventing either control from reverting to the wider presentation.

## Risks / Trade-offs

- [Long option text may feel tighter] The imported valuation label is the longest option. -> Preserve the existing select padding and verify both controls remain readable at 224px.
- [Narrow containers may constrain the control] A fixed width could overflow a small viewport. -> Use `min(100%, 224px)` and retain the mobile layout boundary.

## Migration Plan

1. Change the shared valuation-control width to 224px and remove the redundant portfolio-only width override.
2. Extend the relevant web contract test if needed.
3. Run the focused web contract/runtime tests and inspect the control at desktop and mobile widths.
4. Roll back by removing the scoped override; no data or migration changes are required.

## Open Questions

None.

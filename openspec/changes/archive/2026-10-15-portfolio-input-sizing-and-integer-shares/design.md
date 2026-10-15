# Design

## Context

See `proposal.md` for motivation. The selected-position input is rendered by the shared position table, with its entry step selected by portfolio mode. The current CSS sets the input to 84px both in the base rule and in the narrow-screen override. The change handler persists finite non-negative values for both modes but does not distinguish integer Shares from decimal Allocation values.

## Goals / Non-Goals

**Goals:**
- Make the shared numeric field approximately 97px wide across desktop and mobile layouts.
- Validate a Shares edit before changing portfolio state or persistence, while retaining decimal Allocation edits.
- Restore the previous committed Shares value after an invalid fractional edit.

**Non-Goals:**
- Migrate or normalize existing saved or imported position values.
- Change allocation precision, portfolio weight calculations, or panel-column sizing.
- Add a backend validation path or dependency.

## Decisions

- Keep the existing shared numeric input and set its width to approximately 97px in both the base `.position-input` rule and the narrow-screen override. This changes the field itself, not the selected-positions panel, and leaves the existing responsive grid intact.
- Enforce Shares-mode integer validation in the existing input change path before calling the persistence update. Require a finite value, value >= 0, and `Number.isInteger(value)`. For invalid edits, do not save or mutate the portfolio; rerender from the last committed state so the previous value returns. Keep Allocation mode on its current decimal behavior.
- Retain the existing mode-specific input steps (`1` for Shares and `0.1` for Allocation) as user guidance, but do not rely on native step validity as the only enforcement because the current handler saves without checking it.
- Apply the rule only to manual edits. Loaded and imported values remain as stored until a user edits that position, avoiding an implicit data migration or rounding policy.

## Risks / Trade-offs

- [Invalid entry is not self-explanatory if only restored] -> Keep native whole-number step guidance and ensure the field returns to its previously committed value without silently rounding.
- [Mobile layout could become crowded] -> Apply the width in the mobile override too and verify that the selected-position layout does not introduce horizontal overflow.

## Migration Plan

No data migration is required. Rollback consists of reverting the CSS width and manual edit validation; persisted portfolio formats remain unchanged.

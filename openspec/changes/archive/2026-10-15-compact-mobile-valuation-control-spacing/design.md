# Design

## Context

See `proposal.md` for the user impact. The valuation row is a flex container. At widths up to 480px it changes to a column, while its `.portfolio-valuation-details` child retains `flex: 1 1 360px`. Browser inspection at 390px confirmed a 360px-high details box beneath an 18px Entry mode control, matching the visible blank region in the supplied smartphone screenshot.

## Goals / Non-Goals

**Goals:**
- Let valuation details take their natural content height on smartphone widths.
- Keep the selector and status on one row within the available panel width, with the status vertically centered against the select box.
- Preserve the desktop flex basis and current valuation visibility and status behavior.

**Non-Goals:**
- Change the desktop alignment, valuation control behavior, or portfolio state.
- Rework the selected-position card or the overall mobile navigation/layout.

## Decisions

- In the existing `max-width: 480px` rule, override `.portfolio-valuation-details` with `flex: 0 1 auto`, `width: 100%`, and no wrapping. Keep the provenance status at its intrinsic width and let the valuation control shrink with `min-width: 0`; set the select to fill that control. The parent is a column at this breakpoint, so removing the 360px flex basis prevents a reserved height while the no-wrap row keeps status beside the select.
- Keep the base `flex: 1 1 360px` rule for wider layouts, where the parent is a row and the basis acts as the intended horizontal sizing behavior.
- Align the status to the selector's lower edge so the status pill is centered against the select surface; keep this adjustment phone-only.

## Risks / Trade-offs

- [The selected option text may be truncated when the selector shrinks on narrow phones] -> Keep the field label and native select intact, and verify the control remains operable at 320px.
- [A cached stylesheet could obscure the change during manual verification] -> Update the stylesheet cache-busting URL and verify the loaded style at a smartphone viewport.

## Migration Plan

No data migration is needed. Reverting the phone-only override and stylesheet URL change restores the current layout.

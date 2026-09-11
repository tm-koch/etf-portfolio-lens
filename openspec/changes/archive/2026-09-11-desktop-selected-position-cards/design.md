## Context

The Portfolio view currently renders selected ETFs as rows in `.positions-table`. Each row already contains the ETF identity, editable shares, live/imported price, CHF value, weight, and Remove button. At wide viewports the catalog and selected positions are shown side by side; at mobile widths an existing grid card reflow already places identity above Shares, Weight, and Remove.

The requested change is visual and ergonomic: wide selected positions should read as rounded boxes with a two-line hierarchy. Existing state updates, valuation calculations, event selectors, accessibility attributes, and the mobile layout are constraints.

## Goals / Non-Goals

**Goals:**

- Present each wide selected position as an enclosed rounded box.
- Put ticker and ETF name on the first line.
- Put labeled Shares, Price/Value, and Weight metrics on the second line.
- Keep Remove in a dedicated right-side area, right-aligned and vertically centered across the box.
- Preserve the current mobile reflow and all position interactions.

**Non-Goals:**

- Changing portfolio state, calculations, valuation modes, or persisted data.
- Changing the catalog column or the breakpoint at which the columns stack.
- Adding a new component framework or dependency.
- Redesigning the mobile position card.

## Decisions

- Keep the existing table and `data-label` attributes as the source structure, but apply a wide-screen-only grid presentation to the position body and rows. This keeps the existing event and accessibility hooks while allowing the row to behave visually as a two-line box. Replacing the table with unrelated div markup would require rebuilding semantics and mobile behavior.
- Hide the table header only in the wide card presentation and expose metric labels through the existing `data-label` values in the metric cells. The identity cell spans the first visual line; metric cells occupy the second; Remove spans both lines in the final column.
- Use the existing border, radius, text, muted-color, and input tokens. Add only position-card-specific spacing and alignment rules. The Remove button remains the existing icon-plus-label control on wide screens and the existing icon-only control on mobile.
- Scope the new rules to viewports above the mobile breakpoint, leaving the established `@media (max-width: 760px)` grid areas unchanged. Tablet layouts remain stacked by the existing `max-width: 1100px` portfolio rule but use the same non-mobile card treatment unless implementation testing shows the available width is insufficient.
- Keep metric content compact but labeled: Shares with its input, Price and Value CHF when applicable, and Weight. Private percentage portfolios continue to omit absolute valuation cells while retaining Shares, Weight, and Remove.

## Risks / Trade-offs

- [Risk] CSS grid styling on table elements can vary across browsers. -> Mitigation: test Chromium at wide, tablet, and mobile widths and retain the current mobile fallback rules; use explicit display rules for `tbody` and `tr` only in the card presentation.
- [Risk] Long ETF names can make a card too tall or push metrics out of view. -> Mitigation: allow the identity text to wrap, constrain the metric row with minimum-width zero, and keep the Remove column fixed and compact.
- [Risk] Hiding the table header may reduce context for screen readers. -> Mitigation: preserve `data-label`, accessible input labels, Remove names, and table semantics in the DOM; verify keyboard and screen-reader-relevant attributes remain present in contract tests.
- [Risk] Percentage-only rows have fewer metric cells than full rows. -> Mitigation: use grid placement that tolerates absent price/value cells and test both portfolio modes.

## Migration Plan

Update the position row markup only if needed to provide stable styling hooks, add wide-screen card CSS, and extend web contract coverage. No data migration is required. Rollback consists of removing the card-specific rules and markup hooks, restoring the current tabular desktop presentation.

## Open Questions

None. The labeled metrics presentation selected during exploration is the intended design.

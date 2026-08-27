## Context

The mobile Selected positions layout uses a grid row containing a full-width Shares input, a Weight cell containing only the percentage, and a compact Remove icon button. The input and icon establish a roughly 40px control row, but the Weight text is currently aligned to the cell's top edge. The desktop layout remains a native four-column table.

## Goals / Non-Goals

**Goals:**

- Vertically center the mobile Weight percentage within the lower control row.
- Align it visually with the Shares input and Remove icon.
- Keep the change limited to the mobile breakpoint.
- Preserve accessible Weight semantics and all existing control behavior.

**Non-Goals:**

- Changing portfolio calculations, displayed percentages, or warning content.
- Altering the desktop or tablet table layout.
- Changing the mobile row structure, control sizes, or spacing beyond the needed alignment.

## Decisions

The mobile Weight cell will become a flex container with centered cross-axis alignment within the existing grid row. This directly centers the text against the neighboring controls and remains stable if the input or icon dimensions change.

A margin or line-height adjustment is rejected because it depends on current font metrics and control heights. Applying `vertical-align` is rejected because the mobile position row is reflowed with CSS grid rather than remaining a table layout. The alignment rule will live inside the existing mobile media query so larger viewports retain their current table-cell behavior.

## Risks / Trade-offs

- [Risk] A future multi-line Weight value could alter the visual balance. -> Mitigation: preserve the existing concise percentage output and verify the row at narrow mobile widths.
- [Risk] The rule could accidentally affect desktop if placed outside the breakpoint. -> Mitigation: keep it scoped to the mobile position selector inside the established `max-width: 760px` block.

## Migration Plan

No migration is required. Add the mobile-only alignment rule, run the focused web tests, and verify mobile and desktop geometry in the browser. Rollback consists of removing that CSS rule.

## Open Questions

None.

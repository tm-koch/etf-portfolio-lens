## Context

The comparison view already uses a separate legend block below each donut chart, which keeps the chart canvas clean. On smartphone-sized viewports, the legend is still using a forced full-width stack, so each entry consumes an entire row and pushes the donut section taller than necessary.

This change is limited to the static web frontend and specifically to the comparison legend layout on mobile. The chart data, ordering, and donut geometry are not being changed.

## Goals / Non-Goals

**Goals:**
- Make the smartphone comparison legend more compact by allowing multiple entries per line when space permits.
- Preserve readability and the existing color/label mapping.
- Keep the legend visually separated from the donut canvas.
- Avoid changing comparison data, tooltips, or donut sizing.

**Non-Goals:**
- No changes to the underlying chart data or aggregation rules.
- No changes to the donut frame height or chart padding logic.
- No changes to desktop legend behavior beyond preserving the current wrapping style.

## Decisions

- Keep the legend as a wrapping flex row on mobile instead of a forced single-column stack.
  - Rationale: the existing legend markup already supports wrapping, so the simplest and most predictable fix is to remove the mobile-only full-width override and let labels flow naturally.
  - Alternative considered: convert mobile legend to a grid. Rejected because the current flex behavior already matches desktop more closely and avoids introducing a second layout model.

- Preserve compact pills rather than expanding legend entries to full width on phones.
  - Rationale: the user goal is to reduce vertical whitespace and make the smartphone layout more compact, not to maximize tappable area.
  - Alternative considered: keep one-item rows for clarity. Rejected because it directly conflicts with the desired density.

- Keep breakpoint logic local to the legend styles.
  - Rationale: this is a presentation-only tweak and should not affect chart rendering code.
  - Alternative considered: add chart-side legend generation logic. Rejected because the structure already exists in CSS and is easier to reason about there.

## Risks / Trade-offs

- [Long labels may wrap awkwardly if too many items share a row] → Mitigation: rely on the existing pill styling and allow row wrapping rather than forcing a fixed column count.
- [Legend rows can become uneven across different metrics] → Mitigation: keep the same compact wrapping rule across sector, region, and currency legends.
- [Compactness can reduce touch comfort] → Mitigation: preserve the existing padding inside each legend item so they remain readable and tappable.

## Migration Plan

1. Update the mobile legend CSS so legend items can share rows instead of being forced to full width.
2. Verify at a common phone viewport that the legend becomes more compact while still wrapping cleanly.
3. Confirm the donut canvas and legend separation remain unchanged.
4. If the row density is too high, tune the gap and padding without changing the overall wrapping behavior.

Rollback is straightforward: restore the mobile `width: 100%` legend-item rule.

## Open Questions

- Should the mobile legend use a two-column rhythm, or is free wrapping sufficient once the full-width override is removed?
- Should the smallest phones get slightly larger gaps for readability, or should the same compact rule apply across all smartphone widths?

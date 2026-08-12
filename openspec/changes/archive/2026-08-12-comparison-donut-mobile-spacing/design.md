## Context

The comparison tab already renders the legend outside the donut canvas, which solved the prior issue where legend height shrank the chart area. The remaining problem is that smartphone-sized viewports still leave too much empty vertical space around the donut, making the chart feel undersized even though the data itself is unchanged.

This change is limited to the static web frontend. The backend, registry, and snapshot data are unaffected.

## Goals / Non-Goals

**Goals:**
- Reduce unused vertical whitespace around the comparison donuts on smartphone-sized screens.
- Make the chart frame and donut padding responsive to viewport width.
- Keep the legend fully visible and visually separated from the donut canvas.
- Preserve the current chart data, ordering, and tooltip behavior.

**Non-Goals:**
- No change to the underlying comparison metrics or aggregation rules.
- No change to the legend content or ordering.
- No introduction of a new charting library or custom canvas renderer.

## Decisions

- Use viewport-based breakpoints for chart framing and padding.
  - Rationale: phone, tablet, and desktop layouts have different available vertical space, so a single fixed height produces either too much whitespace on phones or too little breathing room on larger screens.
  - Alternative considered: one fixed mobile height. Rejected because it does not adapt across common smartphone sizes and orientations.

- Tighten the donut canvas padding on smaller screens.
  - Rationale: the extra white space is primarily inside Chart.js layout padding, so reducing that padding on phones directly increases the visible donut area without affecting the legend block.
  - Alternative considered: only increase the frame height. Rejected because it can still leave a floaty donut if chart padding stays large.

- Keep the legend outside the chart canvas and do not compress it into the donut area.
  - Rationale: the legend should remain readable and fully visible; shrinking it to reclaim space would reintroduce the original clipping problem.
  - Alternative considered: moving the legend into an overlay. Rejected because it risks hiding data and complicates touch interaction.

## Risks / Trade-offs

- [Too little padding on small screens can make the chart feel cramped] → Mitigation: keep a small but non-zero phone padding value and verify visually at common phone widths.
- [Landscape phones may have different space trade-offs than portrait phones] → Mitigation: use width-based breakpoints rather than device-specific assumptions.
- [Increasing the chart’s apparent size can push content further down the page] → Mitigation: limit the tighter spacing change to the comparison chart cards only.

## Migration Plan

1. Update the comparison chart sizing logic to choose phone/tablet/desktop frame heights by viewport width.
2. Reduce Chart.js layout padding on small screens so the donut fills more of the available canvas.
3. Verify at common smartphone widths that the donut gains usable space while the legend remains separate and readable.
4. If the result feels too dense, tune the phone breakpoint values before broadening the change.

Rollback is straightforward: restore the previous frame-height and chart-padding constants.

## Open Questions

- Should the smallest-phone layout be tuned separately from larger phones, or is one mobile breakpoint enough?
- Should portrait and landscape phones share the same sizing rule, or should landscape use a slightly smaller frame because the available height is lower?

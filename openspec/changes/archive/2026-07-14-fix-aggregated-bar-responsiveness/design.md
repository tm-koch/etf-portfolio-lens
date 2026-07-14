## Context

The aggregated top-company view already computes a ranked list of company exposure and renders each company as a stacked bar with ETF-colored segments. The current problem is that the bar length is derived from a one-time width measurement, so the visualization does not stay in sync with the available layout width when the window is resized.

The requirement is purely visual and affects the front-end rendering path. It should not alter portfolio aggregation, ranking, or contributor composition.

## Goals / Non-Goals

**Goals:**
- Keep each company bar contained within the available frame during window and container resize.
- Preserve the existing stacked-segment composition inside each bar.
- Keep the ranked ordering and textual exposure labels unchanged.
- Avoid introducing a resize-specific rendering bug or dependency on brittle DOM measurements.

**Non-Goals:**
- No change to aggregation formulas or data normalization.
- No new charting library or layout system.
- No backend or persistence changes.
- No redesign of the aggregated page beyond the bar sizing behavior.

## Decisions

1. Express the company bar width relative to its container instead of using a cached pixel measurement.
   - Rationale: container-relative sizing automatically tracks layout changes and removes the stale measurement problem.
   - Alternatives considered: keep inline pixel widths and recalculate on resize; rejected because it still depends on measurement timing and adds lifecycle complexity.
   - Alternatives considered: hard-code minimum/maximum widths; rejected because it would not solve the resize issue and would distort ranking semantics.

2. Keep the stacked ETF segments inside the same bar track.
   - Rationale: the current composition already communicates which ETFs contribute to the company exposure, and the change should only fix responsive sizing.
   - Alternatives considered: split the row into separate bars or replace the stacked track with a different visualization; rejected because it changes the established reading model.

3. Preserve the existing labels and contributor chips as the exact-value source of truth.
   - Rationale: relative bar width is only a summary signal, so textual percentages remain necessary for precise interpretation.
   - Alternatives considered: rely on width alone; rejected because responsive sizing makes width relative, not absolute.

## Risks / Trade-offs

- [Very narrow containers may compress small companies too aggressively] → Mitigation: keep the company percentage label and contributor chips visible so exact values remain readable.
- [A purely relative width can make the top row appear to change more subtly than expected] → Mitigation: preserve the current ranking and scaling rule so the visual stays aligned with the exposure ordering.
- [Changing sizing strategy can expose layout assumptions elsewhere in the row] → Mitigation: verify the aggregated panel at multiple viewport widths and keep the bar track constrained to its parent container.

## Migration Plan

No data migration is required.

1. Update the aggregated company row rendering to use container-relative bar sizing.
2. Verify that the stacked segments remain intact across narrow and wide viewports.
3. Check the aggregated panel during live window resizing to confirm the bar stays within the frame.
4. Roll back only the front-end rendering change if any unexpected layout regression appears.

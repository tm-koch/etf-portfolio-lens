## Context

ETF Lens already renders comparison doughnut charts and aggregated company bars, but the current presentation makes the comparison rings feel small and the aggregated rows look visually flatter than the underlying exposure distribution. The change is limited to the static web UI and does not alter the data model or backend pipeline.

## Goals / Non-Goals

**Goals:**
- Make comparison doughnut charts read as larger, more legible visual elements.
- Reduce the apparent thickness of the comparison ring so the chart is easier to scan.
- Improve hover text so the user immediately sees the ETF and metric category for the hovered segment.
- Normalize aggregated company bar widths so the largest holding anchors the visual scale.
- Preserve the existing stacked ETF contribution segments inside each company bar.

**Non-Goals:**
- No backend schema changes.
- No new chart library or UI framework.
- No change to the underlying exposure calculations beyond presentation scaling.
- No redesign of the overall page layout beyond what is needed for the targeted chart and bar behavior.

## Decisions

1. Keep the comparison charts in Chart.js and tune their configuration rather than replacing the chart implementation.
   - Rationale: the current comparison view already uses Chart.js successfully; the requested changes are presentation-level and fit cleanly into chart options and wrapper sizing.
   - Alternatives considered: custom SVG rendering or a different visualization library. Rejected because they add complexity without improving the requirement fit.

2. Use a larger chart frame and a larger inner cutout to make the doughnut feel bigger while making the ring thinner.
   - Rationale: the user wants both more overall presence and less ring thickness; these are separate controls and can be adjusted independently.
   - Alternatives considered: only scaling the canvas or only adjusting border widths. Rejected because neither alone addresses both aspects of the request.

3. Update tooltip text to explicitly name the ETF and the active metric category.
   - Rationale: the current hover label is too generic. The chart already has the needed label context, so the change should be localized to the tooltip formatter.
   - Alternatives considered: adding a legend-only explanation or a separate details panel. Rejected because hover is the most direct interaction for this view.

4. Normalize aggregated company bar widths against the maximum company exposure, then keep contributor segments proportional within each bar.
   - Rationale: this makes the biggest holding a visual baseline while preserving the existing information about how each ETF contributes to that holding.
   - Alternatives considered: fixed-width bars or absolute-value bars. Rejected because fixed widths hide relative importance and absolute widths are less informative without a market-value baseline.

## Risks / Trade-offs

- [Chart frames become too tall on smaller screens] -> Mitigation: keep responsive breakpoints and verify the comparison section still fits a mobile viewport.
- [Thinner rings reduce perceived slice separation] -> Mitigation: preserve segment borders and ensure tooltip detail remains available on hover.
- [Bar normalization may make smaller holdings feel visually compressed] -> Mitigation: retain contributor chips and numeric labels so exact values remain visible.
- [Users may misread scaled row width as absolute value rather than normalized exposure] -> Mitigation: keep labels and headings explicit about total exposure and compare relative size consistently across rows.

## Migration Plan

No data migration is required. The change can ship as a UI-only update.

1. Update chart sizing and tooltip behavior in the comparison renderer.
2. Update aggregated bar width calculations and styling.
3. Validate the browser rendering on desktop and mobile layouts.
4. If necessary, revert only the presentation changes; no backend rollback is needed.

## Open Questions

- Should the aggregated bar scale be linear against the maximum holding, or should it use a capped minimum width for very small holdings?
- Should the comparison tooltip show one combined line or separate lines for ETF, metric category, and percentage?

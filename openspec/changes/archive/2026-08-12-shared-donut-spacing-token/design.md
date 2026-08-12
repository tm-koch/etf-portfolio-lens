## Context

The comparison view already renders the donut chart, title block, and legend as separate DOM siblings. The donut itself is sized through Chart.js layout padding, while the surrounding card spacing and legend spacing are controlled in CSS. On mobile-sized viewports, that split makes the visual gaps feel uneven because the horizontal inset around the donut does not match the vertical spacing to the heading and legend.

## Goals / Non-Goals

**Goals:**
- Make the smartphone comparison chart stack feel evenly spaced on all sides of the donut.
- Use one shared spacing value so the donut's left/right gutter and the top/bottom spacing around the surrounding text blocks remain visually consistent.
- Preserve the existing compact legend wrapping behavior and the current donut ring sizing.

**Non-Goals:**
- Do not change the meaning of the chart data or the legend ordering.
- Do not rework the comparison page into a different layout structure unless it is required to apply the shared spacing cleanly.
- Do not change the desktop spacing model unless it is needed to keep the mobile behavior isolated.

## Decisions

1. **Use a shared spacing token instead of separate per-layer constants.**
   - The mobile chart spacing should be driven from one source of truth so the CSS gap, frame padding, and Chart.js layout padding stay aligned.
   - Alternative considered: fine-tune each gap independently. Rejected because it would keep the current visual asymmetry and make future adjustments harder to reason about.

2. **Keep the current DOM structure.**
   - The title, canvas, and legend already have clear separation and are easy to style independently.
   - Alternative considered: wrapping all three in a single container and recomputing layout from that wrapper. Rejected because it would be a larger structural change with little benefit for this spacing fix.

3. **Scope the stricter spacing primarily to smartphone-sized viewports.**
   - The issue is most visible on narrow screens, and the desktop layout already has enough room to breathe.
   - Alternative considered: apply the same spacing token everywhere. Rejected because desktop charts already have a more generous composition and do not need the same tight alignment constraints.

4. **Treat the token as a layout value, not a chart-data concern.**
   - The token should feed CSS and chart layout configuration only.
   - Alternative considered: baking the spacing into the chart generation logic itself. Rejected because spacing is presentation state, not a data transformation.

## Risks / Trade-offs

- [Risk] A single token could make the layout feel too rigid on some phone widths → Mitigation: keep the token viewport-aware and allow a small range rather than a fixed one-size-fits-all value.
- [Risk] Matching the legend and donut gutters may slightly reduce the space available for the canvas → Mitigation: preserve the current compact legend wrapping and validate on small phone viewports.
- [Risk] Desktop behavior might be unintentionally affected if the token is applied too broadly → Mitigation: constrain the token to mobile breakpoints first and only expand it if needed.

## Migration Plan

1. Introduce the shared spacing value in the frontend styling and chart configuration.
2. Update the comparison layout to consume that value for the donut inset and the title/legend spacing.
3. Validate on a smartphone viewport that the gaps on all four sides feel visually balanced.
4. If the change regresses desktop balance, narrow the token scope or adjust the breakpoint thresholds.

## Open Questions

- Should the shared spacing token be expressed as a CSS custom property, a JavaScript constant, or both?
- Do we want the same token to drive the region and currency charts as well, or only the comparison donut stack currently under review?

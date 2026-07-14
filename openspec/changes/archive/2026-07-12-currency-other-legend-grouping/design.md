## Context

ETF Lens already renders currency exposure in the comparison view using Chart.js donut charts. The current data path passes currency labels directly from the snapshot aggregates into the chart, which keeps the implementation simple but makes the legend noisy when many tiny currencies are present. This change keeps the chart structure intact and adds a lightweight grouping step before render.

## Goals / Non-Goals

**Goals:**
- Merge currency entries below 1% into `Other`.
- Merge any `Unknown` currency entry into `Other`.
- Keep `Other` visible in both the plot and the legend.
- Preserve the existing chart styling and 12 o'clock alignment.

**Non-Goals:**
- No change to the underlying snapshot schema.
- No change to sector or region charts.
- No redesign of the chart UI beyond the currency grouping behavior.
- No additional chart library or heavy data-processing layer.

## Decisions

1. Perform the grouping in the comparison data-preparation layer before Chart.js receives labels and values.
   - Rationale: the legend is derived from the chart labels, so the cleanest way to keep plot and legend in sync is to normalize the dataset once before rendering.
   - Alternatives considered: post-processing the legend only. Rejected because the plot and legend would diverge.

2. Treat `Unknown` as a grouping signal in the same pass as the sub-1% threshold.
   - Rationale: the user wants one clear `Other` bucket, not two separate edge-case categories.
   - Alternatives considered: keeping `Unknown` separate and only merging tiny currencies. Rejected because that preserves the same legend noise problem.

3. Leave the donut rotation and size settings unchanged for this change.
   - Rationale: the visual geometry has already been tuned separately; this change is specifically about legend and currency grouping semantics.
   - Alternatives considered: reworking chart size and ring thickness at the same time. Rejected because it broadens the scope and risks masking whether the currency grouping is correct.

## Risks / Trade-offs

- [Grouping small currencies can hide detail] → Mitigation: expose the grouped total as `Other` and keep the existing percentage labels in the chart tooltip.
- [Thresholding may move values between the visible slice list and Other as portfolios change] → Mitigation: keep the threshold explicit at 1% and document the behavior in the spec.
- [Legend ordering may shift after consolidation] → Mitigation: preserve the chart's existing sort/order semantics where possible and only merge the grouped items into a single bucket.

## Migration Plan

No migration is required.

1. Add the currency grouping step in the comparison data-preparation path.
2. Verify the currency donut and legend both show `Other` when grouping occurs.
3. Validate that sector and region charts remain unchanged.
4. If necessary, revert only the comparison data-preparation change; no data rollback is required.

## Open Questions

- Should `Other` always appear when `Unknown` exists, even if the total is exactly 0%? The current intent is yes, to keep legend behavior consistent.
- Should the `Other` bucket be capped at one combined slice only, or should extremely large `Unknown` values still be merged even when they exceed 1%? The current requirement says yes, merge all `Unknown` values.

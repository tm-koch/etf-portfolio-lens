## Context

The comparison tab renders sector, region, and currency exposure as multi-ring doughnut charts using a shared Chart.js configuration. Today the chart canvas and the legend share the same fixed-height frame, so the available donut area changes with legend length. That is most visible in the sector chart, where the legend consumes more space and the donut appears smaller or more cramped than the other metrics.

The current user-facing requirement is that the three comparison charts should read as the same visual system: wider rings, consistent donut size across metrics, and a legend that remains fully visible.

## Goals / Non-Goals

**Goals:**
- Make sector, region, and currency comparison donuts look consistent in size.
- Increase the perceived ring width so the comparison charts read more clearly.
- Keep the legend fully visible for all comparison charts.
- Preserve the existing comparison behavior, including multi-ring dataset ordering and labels.

**Non-Goals:**
- No backend or snapshot-data changes.
- No changes to the meaning of the aggregated numbers.
- No redesign of the overall comparison tab beyond the chart and legend layout.

## Decisions

- Use a shared donut sizing model for all comparison charts.
  - Rationale: the three charts are conceptually the same visualization with different data domains. They should use the same ring thickness and overall footprint so users can compare them visually without compensating for layout differences.
  - Alternative considered: tweak each chart individually based on its legend length. Rejected because it creates inconsistent visuals and makes maintenance harder.

- Decouple the legend from the chart drawing area.
  - Rationale: Chart.js legend layout currently subtracts from the available chart area, which makes donut size vary with label count. A separate legend block keeps the chart geometry stable and makes the legend fully visible.
  - Alternative considered: make the chart frame taller or reduce legend font size. Rejected because it only masks the symptom and still ties donut size to label count.

- Keep the comparison charts responsive with shared frame sizing constants.
  - Rationale: a single source of truth for desktop and mobile chart dimensions preserves consistency across the three metric panels and avoids per-chart tuning.
  - Alternative considered: rely on auto-sizing alone. Rejected because the comparison tab needs predictable chart proportions on both desktop and mobile.

## Risks / Trade-offs

- [More vertical space required] → Mitigate by reserving a dedicated legend area and rebalancing the chart frame height so the donut remains readable.
- [Very dense legends may still feel long on mobile] → Mitigate with wrapping, spacing, or an internal scroll region for the legend while keeping all entries visible.
- [Legend extraction could affect tooltip/legend behavior parity with Chart.js defaults] → Mitigate by keeping dataset labels, tooltip content, and legend item ordering aligned with the existing chart configuration.

## Migration Plan

1. Update the shared comparison chart rendering to use a stable donut viewport and thicker ring settings.
2. Move legend presentation into a layout area that does not reduce the donut drawing space.
3. Verify sector, region, and currency charts render with matching ring size and that the legend remains fully visible at desktop and mobile widths.
4. If needed, adjust the comparison tab frame heights slightly to preserve balance after the legend is separated.

Rollback is straightforward: revert the chart/layout changes and restore the current Chart.js legend-in-frame behavior.

## Open Questions

- Should the legend wrap into multiple rows or become a scrollable region on narrow screens if it exceeds the available width?
- Should the chart viewport be tuned for the sector chart first and then applied identically to region/currency, or should all three use a slightly more compact default to leave extra room for legends?

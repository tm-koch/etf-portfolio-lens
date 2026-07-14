## Context

The aggregated holdings view already computes company exposure totals and ranking order. The remaining problem is visual semantics: the bar should communicate a company's total exposure, not a per-ETF breakdown at the top level. The internal stacked segments already provide the ETF composition, so the design change is focused on making the whole row width represent the same exposure value used for ranking.

## Goals / Non-Goals

**Goals:**
- Render one stacked bar per company row.
- Make the bar length proportional to the company's total exposure used in ranking.
- Keep the ETF-colored stacked segments inside the bar.
- Keep the exact company exposure visible in text so the normalized width cannot be misread.

**Non-Goals:**
- No change to the exposure aggregation or ranking formula.
- No new charting or visualization library.
- No backend data model changes.
- No redesign of the comparison charts.

## Decisions

1. Use the existing aggregated exposure value as the bar-width source.
   - Rationale: the list already ranks companies by total exposure, so the display should reuse that same signal instead of introducing a second normalization axis.
   - Alternatives considered: normalizing by ETF contributor count or by portfolio share buckets. Rejected because they distort the ranking semantics.

2. Keep one stacked bar per company and represent ETF contributions as segments inside that bar.
   - Rationale: the current data already groups contributions by company, and the bar can show composition without fragmenting the row into multiple bars.
   - Alternatives considered: separate bars per ETF or a mini chart per company. Rejected because they make the row harder to compare at a glance.

3. Preserve the textual company exposure label next to the bar.
   - Rationale: the visual width is relative; the exact percentage remains necessary to prevent ambiguity.
   - Alternatives considered: relying on bar width alone. Rejected because normalized bars can be misread as absolute values.

## Risks / Trade-offs

- [Smaller companies may look visually compressed] -> Mitigation: keep the exact company percentage and ETF chips visible next to each bar.
- [Users may confuse relative bar width with absolute position size] -> Mitigation: label the company exposure explicitly and keep the rows sorted by the same value.
- [Very small ETF segments may become hard to see] -> Mitigation: preserve tooltips and chips for the exact contributor percentages.

## Migration Plan

No migration is required. The change is a UI-only refinement.

1. Update the aggregated company rendering to bind bar width to company exposure.
2. Verify that stacked segments still render within the resized bar.
3. Validate the layout in the browser.
4. Roll back only the UI rendering changes if needed; no data rollback is necessary.

## Open Questions

- Should the smallest company bars have a minimum visual width to preserve legibility, or should the width remain strictly proportional?
- Should the exact company percentage appear in the row header or only in the bar tooltip/aria label?

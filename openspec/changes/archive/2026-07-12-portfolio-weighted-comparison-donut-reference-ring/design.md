## Context

The comparison tab already renders sector, region, and currency donuts as concentric rings, with one ring per selected ETF. Users now want an additional reference ring that summarizes the entire portfolio, weighted by the share counts that already drive portfolio composition elsewhere in the app.

The key constraint is that this should stay within the current Chart.js comparison path. The new behavior should not alter the underlying snapshot data, only the data prepared for rendering.

## Goals / Non-Goals

**Goals:**
- Render a portfolio-weighted outer reference ring for sector, region, and currency comparison donuts.
- Use portfolio share counts across the entire portfolio as the weighting basis for the reference ring.
- Preserve the existing per-ETF rings and the current comparison tab layout.
- Keep the change local to the frontend comparison rendering path.

**Non-Goals:**
- Changing the backend snapshot format or aggregation pipeline.
- Introducing a new chart library or a new chart layout.
- Changing how individual ETF rings are computed.
- Reworking the portfolio weighting model itself.

## Decisions

1. Build the reference ring as a synthetic dataset derived from the selected portfolio.
   - Rationale: the current comparison chart already accepts multiple datasets, so a computed outer series fits the existing concentric doughnut model without new primitives.
   - Alternatives considered: drawing a separate annotation layer or a second chart. Rejected because both would complicate the current UI and make the reference less directly comparable to the ETF rings.

2. Weight the reference by portfolio share counts across the entire portfolio.
   - Rationale: share counts are the portfolio weighting proxy already used elsewhere in the app, so the reference ring should follow the same whole-portfolio weighting semantics rather than the comparison selection.
   - Alternatives considered: equal-weighting selected ETFs or weighting only the comparison toggles. Rejected because both would misrepresent the current portfolio mix.

3. Render the reference as the outermost ring.
   - Rationale: keeping the portfolio summary outside the per-ETF rings makes it read as a frame of reference rather than another ETF in the comparison set.
   - Alternatives considered: inserting the reference between ETF rings or making it the innermost ring. Rejected because both options make it harder to interpret the portfolio summary as the top-level comparison.

4. Reuse the existing label normalization and currency grouping logic before aggregation.
   - Rationale: the reference should stay aligned with the same sector, region, and currency buckets already used for the ETF rings, so the chart remains comparable at the category level.
   - Alternatives considered: introducing separate category handling for the reference ring. Rejected because that would create label mismatches and increase maintenance cost.

## Risks / Trade-offs

- [The outer ring may look like another ETF ring] → Mitigation: label it explicitly as a portfolio reference in the legend and tooltip.
- [Weighted reference values can be misread as a simple average] → Mitigation: make the weighting basis explicit in the ring label and supporting text.
- [Many categories can make the outer ring visually dense] → Mitigation: preserve the current label normalization and existing palette behavior so the ring remains readable.
- [If the portfolio changes, the reference ring must refresh in sync] → Mitigation: derive the reference from the full portfolio state while keeping the comparison selection separate.

## Migration Plan

No data migration is required.

1. Extend the comparison data-preparation path to compute one weighted reference series per metric.
2. Pass the reference series into the existing doughnut renderer as the outermost dataset.
3. Update chart labels or legend text so the reference ring is clearly identified.
4. Validate the comparison tab with multiple selected ETFs and confirm the outer ring updates with portfolio share changes.
5. If needed, revert only the frontend comparison-rendering changes; no backend rollback is required.

## Open Questions

- Should the reference ring use the exact portfolio share weighting already used in the rest of the app, or should it be normalized independently within the comparison tab?
- Should the outer ring appear in the legend as a single named reference series, or should it be visually emphasized only through its position and tooltip text?

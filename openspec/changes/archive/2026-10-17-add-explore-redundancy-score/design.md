# Design

## Context

The Explore view already aggregates security exposure using each position's current normalized portfolio weight and keeps per-ETF contribution weights for every security. The contribution values therefore provide the inputs for the proposed look-through calculation without a new data source. Portfolio weights may come from share-count valuation or relative allocation mode.

See [proposal.md](proposal.md) for motivation and [specs/portfolio-redundancy-score/spec.md](specs/portfolio-redundancy-score/spec.md) for observable behavior.

## Goals / Non-Goals

**Goals:**
- Derive the score from current selected positions and the existing aggregated holdings data.
- Keep computation, scale, classifications, and UI synchronized with portfolio and developer-setting changes.
- Preserve useful behavior when the portfolio has one ETF or incomplete holdings data.

**Non-Goals:**
- Detect or explain near-identical ETF pairs.
- Change security identity matching or holdings ingestion.

## Decisions

- **Reuse the existing look-through aggregation.** For each security, compute its overlap as the total aggregated portfolio contribution minus the largest single-ETF contributor, then sum the overlaps. This keeps the score aligned with the company exposure view and avoids introducing a second weighting implementation. An alternative would be a separate pass over raw snapshots, but it would duplicate identity grouping and portfolio-weight logic.
- **Require complete holdings for every positive-weight position.** Determine positive weights with the existing portfolio weighting rules. If any such position lacks usable holdings, render the score as unavailable rather than presenting a partial result as portfolio-wide. Ignore zero-weight positions in both the calculation and ETF count. This prevents missing snapshots from reducing the score or changing its scale silently.
- **Scale the bar by the positive-weight ETF count.** For `n` usable, positive-weight ETFs, use `100 * (1 - 1/n)` as the maximum. A single ETF has a 0% maximum and a 0% score. This is a count-based upper bound; unequal ETF allocations can mean the portfolio does not reach the endpoint.
- **Keep thresholds in absolute percentage points.** Use 10% and 25% defaults for band classification regardless of the current scale. Map score and thresholds onto the visible bar relative to its maximum; thresholds beyond that maximum remain valid classifications but do not extend the bar. Reject invalid threshold pairs and retain the last valid settings or defaults.
- **Persist settings locally and place the score between the rollups and companies sections.** Store the two developer thresholds in browser local storage using the existing developer-preference pattern. Add a dedicated score box after Rollups and before Top companies, independent of either section. Align the band labels with the threshold-defined bar segments. Use the existing font, responsive CSS conventions, and localized interface strings. No pair-warning content is rendered.

## Risks / Trade-offs

- **[Security identities may be incomplete or ambiguous]** → Reuse the existing canonical security key and do not attempt new matching in this change; current selection warnings remain available in the existing data details surface.
- **[Unequal allocations may not reach the count-based scale endpoint]** → Treat the endpoint as the theoretical maximum for equal ETF allocations and preserve the requested count-dependent scale.
- **[A configured threshold can exceed the current endpoint]** → Keep classification in absolute percentage points and clamp only its visual position to the bar; do not silently rewrite the user's setting.
- **[The single-ETF bar has no positive width]** → Render a clear 0% value and Low classification without suggesting a nonzero overlap range.

## Migration Plan

No portfolio data migration is needed. Missing or invalid stored threshold preferences use the 10% and 25% defaults. The feature can be rolled back by removing the score UI and its local preference handling; existing portfolio storage remains unchanged.

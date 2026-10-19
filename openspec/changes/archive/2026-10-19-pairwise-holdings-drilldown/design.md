# Design

## Context

The pairwise catalog contains the overlap total and coverage for each ETF pair, while published ETF snapshots contain the per-holding weights needed for a company-level view. The existing heatmap is filtered to portfolio-selected ETFs. Developer numeric preferences already use validation, browser storage, application state, and inline feedback. See proposal.md for motivation and the spec delta for user-visible behavior.

## Goals / Non-Goals

**Goals:**
- Keep the drill-down pair aligned with the current portfolio selection and the existing pairwise result.
- Reuse established company identity and weight aggregation semantics so detail rows explain, rather than redefine, the pair score.
- Let a persisted developer setting control the displayed row maximum while preserving a default of 20.
- Keep the comparison readable on narrow screens and usable by keyboard and assistive technology.

**Non-Goals:**
- Comparing ETFs that are not currently selected in the portfolio.
- Changing pairwise metric generation, heatmap behavior, or portfolio selection.
- Showing every shared holding as an individual row when the configured maximum is lower; undisplayed rows are summarized.

## Decisions

- Place the drill-down in its own card adjacent to, but outside, the product-overlap heatmap card. Keep the heatmap focused on the portfolio-wide matrix. Reuse the selected pair's precomputed record for the drill-down headline total and coverage, and construct company detail from the corresponding published snapshots, aggregating holdings by the same stable company identity used for pairwise overlap and contributing the smaller aggregate weight.
- Use two accessible selectors following the existing color-mode selector interaction pattern. Keep them on one row, populate them from the selected portfolio ETFs, initialize to the first two in portfolio order, and keep them distinct. When a portfolio change invalidates a chosen ETF, reset to the first valid pair; with fewer than two ETFs, do not render a pair result.
- Add a persisted developer preference for the maximum displayed companies. Default it to 20, accept finite positive integers, and follow the existing developer-setting lifecycle for loading, saving, validation feedback, and state updates. Invalid stored data falls back to 20; invalid input leaves the last valid value active.
- Render up to the configured maximum in descending smaller-weight contribution order, then descending combined weight, then company name for deterministic ties. Show each company name above mirrored horizontal bars: the first ETF extends left from a shared center line and the second extends right. Use a common scale for both directions, print exact weights directly beside the outer bar endpoints, and show a compact legend keyed by ETF ticker and theme-aware color. Show a remaining-holdings contribution when additional shared companies exist; derive it from the pair total minus displayed contributions to keep the summary aligned with the published score, with precision handled before formatting.
- Format bar weights as localized numbers without a percent sign and place a localized percentage-unit note beside any remaining overlap contribution in a compact, left-aligned footer line with no added layout gap, allowing a wrap only when the viewport is too narrow. Do not show separate per-ETF totals for undisplayed shared holdings; retain only their combined overlap contribution. Use content-sized number-label columns and proportional grid tracks so the longest bar fills the available side width after its label and gap are reserved. Separate the opposing bar colors with a narrow transparent center gap and no axis line.
- Give the heatmap and drill-down independent information icons and dialogs in their respective card headers. Each dialog has localized copy and restores focus to its opener when closed.
- Keep pairwise content available on narrow viewports; do not hide the heatmap, selectors, drill-down rows, or summary behind hover-only behavior.
- Keep the pair label and overlap total prominent in the standalone card header, with a concise title that does not name the chart style. Define distinct light- and dark-theme colors for the two bars. Extend the existing localized information dialog rather than adding another help control; explain that each butterfly row shows disclosed weights and the smaller weight contributes to overlap.
- Add the setting label and validation feedback alongside existing developer controls, and keep all new labels, unavailable/empty states, selector names, and explanatory content in the existing locale files. Use semantic labels and preserve keyboard focus and expanded state in the selector menus.

## Risks / Trade-offs

- **Snapshot aggregation differs from published pair calculation** -> Reuse the same company identity and weight aggregation rules, and add a check that displayed contributions plus the remainder reconcile to the precomputed pair total within rounding precision.
- **A saved maximum is invalid or malformed** -> Validate both loaded and newly entered values; fall back to 20 on load and retain the last valid value during input errors.
- **A fixed bar scale obscures small weights** -> Use one common scale for both butterfly directions and print exact percentages at the outer bar endpoints.
- **Portfolio changes invalidate a selected pair** -> Reconcile selector values immediately when the selected ETF list changes and cover the fewer-than-two state.
- **A very large maximum requests more rows than exist** -> Display no more than the available shared companies.
- **Additional labels increase mobile density** -> Keep company names and percentages visible, use compact paired bars, and validate narrow viewport layouts.
- **The remainder could be confused with pair total** -> Keep the undisplayed overlap contribution clearly labeled and separate from the precomputed pair total.
- **A stale local server can omit the new card** -> Verify the current served app version and use the active development server when checking smartphone layouts.

## Migration Plan

No data migration is required. Existing installations without a saved maximum use 20, and published snapshots and pairwise catalog records supply the drill-down input. Rollback consists of removing the drill-down UI and its preference handling; the heatmap and catalog format remain unchanged.

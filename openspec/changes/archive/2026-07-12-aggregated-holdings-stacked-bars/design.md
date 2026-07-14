## Context

The current application already computes company-level look-through exposure across the portfolio, but the output is a ranked list of companies with percentage badges. That makes the ranking visible, yet it hides which ETFs are actually driving each company’s exposure.

This change is purely presentational and analytical at the frontend layer. The underlying exposure math remains the same; only the aggregated holdings view changes from a simple ranked list to a stacked horizontal bar representation.

## Goals / Non-Goals

**Goals:**
- Show each aggregated company exposure as a horizontal stacked bar.
- Make the ETF contribution to each company visually explicit.
- Keep the existing ranking by total company exposure.
- Preserve whole-portfolio percentage semantics.
- Keep the layout readable on smaller screens.

**Non-Goals:**
- Changing the portfolio aggregation math.
- Adding live data fetching or new backend sources.
- Replacing the rest of the comparison or portfolio tabs.
- Introducing user editing of company attribution rules.

## Decisions

### 1. Reuse the existing company exposure aggregation
The stacked bars should be built from the same computed exposure model already used by the aggregated holdings view. That keeps the logic consistent with the current portfolio math and avoids duplicating calculations in a second path.

Alternatives considered:
- Recompute exposure specifically for the chart: unnecessary duplication.
- Push the calculation to the backend: more complex than needed for a view-layer change.

### 2. Render each company as a horizontal stacked bar
A horizontal bar is the best fit for ranked company exposure because it leaves room for long company names and makes percentage comparisons easier to scan from top to bottom.

Alternatives considered:
- Vertical bars: less natural for ranking long company names.
- Donut or pie charts: poor fit once the number of companies or ETF contributions grows.
- A pure table with progress bars: workable, but less expressive than a stacked bar layout.

### 3. Use ETF segments inside each bar
Each company bar should be split into ETF-specific segments so the user can see which ETF contributes what share. This directly answers the “who contributes how much” question and keeps the view interpretable when a company appears in multiple ETFs.

Alternatives considered:
- Single total bar with a separate ETF breakdown table: easier to implement, but the relationship is less immediate.
- Grouping by ETF outside the bar: less readable and more verbose.

### 4. Keep percentage labels visible with a tooltip fallback
The user asked for percentage numbers on the split segments. Inline labels should be shown where space allows, but small segments need a fallback so the information is not lost on narrow or dense rows.

Alternatives considered:
- Tooltip only: too hidden for the main use case.
- Always showing labels: unreadable when segments are small.

### 5. Preserve the ranked total exposure label at the row level
Each row should still show the company’s total exposure as a percentage of the whole portfolio, so the stacked segments do not obscure the overall importance of the holding.

Alternatives considered:
- Show only segment labels: loses the summary value.
- Use a separate total column: readable, but weaker than a label tied to the visual row.

## Risks / Trade-offs

- [Dense rows may become hard to read on mobile] → Use a single-column stacked layout, keep labels concise, and let the total exposure sit outside the bar.
- [Many ETF contributors can create tiny segments] → Preserve the segment in the bar and expose exact percentages in hover/detail text.
- [Color-only distinctions are weak] → Use visible percentages and ETF labels, not just color.
- [Long company names can crowd the chart] → Keep horizontal orientation and allow the text area to wrap independently of the bar.

## Migration Plan

1. Update the aggregated holdings view to consume the existing exposure data in a stacked-bar renderer.
2. Preserve the ranked list ordering and total exposure labels.
3. Add the ETF contribution labels and hover text for each bar segment.
4. Adjust the mobile layout so the stacked bars remain readable in a single column.
5. Verify that the old total-exposure semantics still match the computed portfolio data.

Rollback is straightforward because the underlying exposure model is unchanged. If needed, the view can fall back to the current ranked list presentation without changing data generation.

## Open Questions

- Should very small ETF contributions be grouped visually, or should every contributing ETF always remain separate?
- Should the bar labels show contribution as share of the company total only, or also include the portfolio-wide percentage at the segment level?
- Should the visual include a compact legend per company row, or rely on segment labels and hover text?

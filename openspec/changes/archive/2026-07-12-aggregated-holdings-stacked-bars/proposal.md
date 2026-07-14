## Why

The current aggregated holdings view explains which companies dominate the portfolio, but it does not make the ETF-level contribution to each company exposure obvious. A stacked horizontal bar view gives users a faster way to see which ETF is driving each company exposure and by how much.

## What Changes

- Replace or augment the aggregated holdings list with horizontal stacked bars for each ranked company.
- Split each company bar into ETF-specific segments that show the relative contribution from each ETF.
- Show percentage labels for each ETF segment so users can read the contribution without opening a tooltip.
- Keep the existing ranked-by-total-exposure ordering so the largest company exposures remain first.
- Preserve the aggregated portfolio percentage semantics so the bar totals still represent whole-portfolio exposure.

## Capabilities

### New Capabilities
- `stacked-holdings-contribution-bars`: ranked company exposure bars that are horizontally stacked by ETF contribution and labeled with contribution percentages.

### Modified Capabilities
- None.

## Impact

- Frontend aggregated holdings presentation and charting.
- Company exposure aggregation output formatting.
- Chart rendering logic for stacked horizontal bars and labels.
- Mobile layout behavior for the aggregated holdings section.

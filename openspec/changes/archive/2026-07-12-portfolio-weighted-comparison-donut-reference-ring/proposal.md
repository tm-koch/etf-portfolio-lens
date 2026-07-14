## Why

The comparison tab already shows one ring per selected ETF for sector, region, and currency exposure, but it does not provide a portfolio-level reference for the full portfolio. Adding a portfolio-weighted outer ring makes it easier to see how the selected ETFs compare to the overall portfolio mix at a glance.

## What Changes

- Add a portfolio-weighted reference ring to the sector comparison donut.
- Add a portfolio-weighted reference ring to the region comparison donut.
- Add a portfolio-weighted reference ring to the currency comparison donut.
- Weight the reference ring by portfolio share counts so the combined ring reflects the entire portfolio composition.
- Keep the existing per-ETF inner rings and the current comparison layout.

## Capabilities

### New Capabilities
- `comparison-donut-portfolio-reference-ring`: comparison charts render an outer reference ring that summarizes the entire portfolio using share-count weighting.

### Modified Capabilities
- None.

## Impact

- Affects the comparison data preparation and rendering path in `web/app.js` and `web/charts.js`.
- May adjust chart legends, tooltip text, and dataset ordering so the outer ring is clearly identifiable as the portfolio reference.
- No backend API or snapshot schema changes are expected.

## 1. Comparison Data Prep

- [x] 1.1 Add a portfolio-weighted reference series for sector, region, and currency comparison data.
- [x] 1.2 Derive the reference series from the full portfolio share counts so the outer ring tracks the current portfolio mix.
- [x] 1.3 Keep the existing per-ETF series unchanged and preserve the current category labels.

## 2. Chart Rendering

- [x] 2.1 Pass the new reference series into the comparison doughnut renderer as the outermost dataset.
- [x] 2.2 Update chart labels, legend text, or tooltips so the outer ring is clearly identified as the portfolio reference.
- [x] 2.3 Verify the sector, region, and currency charts still render correctly with multiple selected ETFs.

## 3. Validation

- [x] 3.1 Test that changing portfolio share counts updates the portfolio reference ring.
- [x] 3.2 Confirm the comparison tab handles the empty and zero-share states without rendering a reference ring.

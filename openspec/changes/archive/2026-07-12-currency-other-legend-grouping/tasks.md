## 1. Data preparation

- [x] 1.1 Add a currency grouping step that merges entries below 1% into `Other`.
- [x] 1.2 Merge any `Unknown` currency entry into the same `Other` bucket.
- [x] 1.3 Keep the resulting grouped currency labels in a chart-friendly order.

## 2. Chart rendering

- [x] 2.1 Pass the grouped currency data into the comparison donut renderer.
- [x] 2.2 Confirm the donut plot shows `Other` as a visible slice when grouping occurs.
- [x] 2.3 Confirm the legend shows the same `Other` label as the plot.

## 3. Validation

- [x] 3.1 Run syntax checks for the touched web files.
- [x] 3.2 Check the browser comparison view to confirm currency grouping and legend alignment.

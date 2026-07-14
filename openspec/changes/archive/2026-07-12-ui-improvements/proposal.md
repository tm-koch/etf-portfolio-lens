## Why

The current ETF Lens UI works, but the comparison and aggregated views still leave too much information density hidden in small charts and narrow bars. This change improves scanability and hover clarity so users can compare ETF exposures and company contributions faster.

## What Changes

- Increase the visual size of the comparison doughnut charts and reduce the ring thickness so each metric is easier to read.
- Update comparison hover details so each segment clearly identifies the ETF and the metric category being shown.
- Scale aggregated company bars relative to the largest holding so row length reflects total exposure at a glance.
- Preserve the existing stacked contributor segments inside each aggregated bar while improving the proportional emphasis between companies.

## Capabilities

### New Capabilities
- `comparison-donut-visual-refinement`: comparison charts render larger doughnuts with thinner rings and clearer hover labels.
- `aggregated-bar-scaling`: aggregated holdings render company bars with width normalized to the largest exposure while keeping internal contributor splits.

### Modified Capabilities
- None.

## Impact

- Affects the static web UI in `web/charts.js`, `web/app.js`, and `web/styles.css`.
- May change chart sizing, tooltip text, and aggregated bar layout behavior.
- No backend API or data model changes are expected.

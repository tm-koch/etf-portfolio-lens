# Proposal

## Why

The Explore view presents three related but different measures: portfolio-wide redundancy, pairwise ETF overlap, and company diversification. Users need concise explanations of what each measure counts, how to interpret it, and where incomplete holdings coverage affects it. The diversification explanation should also expand HHI as the Herfindahl-Hirschman Index.

## What Changes

- Add an information control to the upper-right corner of the redundancy score, pairwise product overlap heatmap, and diversification score sections.
- Open a dedicated, accessible explanation for each measure when its information control is activated.
- Explain the redundancy calculation as each underlying security's combined portfolio-weighted contribution minus its largest contribution from one selected ETF.
- Explain that pairwise overlap compares two ETFs using shared disclosed weights without scaling incomplete holdings to 100%, and that each ETF's coverage is shown.
- Explain diversification as the inverse Herfindahl-Hirschman Index (HHI) of normalized disclosed company weights, including how to interpret the effective number and its rating bands.
- Localize the controls and explanatory content in all supported locales.

## Capabilities

### New Capabilities

### Modified Capabilities
- `portfolio-redundancy-score`: Add an accessible explanation of the aggregate duplicate-exposure calculation and its availability limits.
- `pairwise-product-overlap`: Add an accessible explanation of shared disclosed weight, pairwise scope, and coverage.
- `portfolio-diversification-score`: Add an accessible explanation of HHI, the effective number, rating bands, and partial-coverage treatment.

## Impact

- Explore card headings and information-panel behavior in `web/index.html` and `web/app.js`.
- Responsive presentation and information-control styling in `web/styles.css`.
- Localized labels and explanations in `web/locales/`.
- Web contract coverage for the controls, accessible panel behavior, and required English terminology.

# Proposal

## Why

The pairwise heatmap shows how much two selected ETFs overlap, but not which shared companies produce that value. A holdings drill-down will make the overlap interpretable, and a developer-controlled row limit will let reviewers adjust its detail while preserving a useful default of 20 companies.

## What Changes

- Add a standalone pairwise holdings card, separate from the product-overlap heatmap, with two ETF selectors restricted to ETFs already selected in the portfolio.
- Show the pair's existing overlap total and both disclosed weights for each of the highest-contributing shared companies, up to a persisted developer-configured maximum that defaults to 20.
- Present the two ETF weights as centered, diverging butterfly bars with a distinct color and legend entry for each ETF, separated by a small clear center gap without an axis marker.
- Keep the two ETF selectors side by side, place each exact weight adjacent to its bar endpoint, and use light/dark theme-specific bar colors; keep the card title concise.
- Show bar weights without a percent suffix and place the percentage note and remaining overlap contribution together in a compact, left-aligned footer line without a layout gap; do not show separate per-ETF remaining-share totals.
- Put an information icon in the top-right of the drill-down header and use it to open the pairwise explanation dialog.
- Keep the pairwise heatmap and pair drill-down explanations in separate dialogs, each opened from its own card header.
- Ensure the heatmap and drill-down contents remain visible and usable on smartphone-sized viewports.
- Scale the largest displayed bar across the available chart width after reserving only its adjacent weight label and gap; separate the opposing bars with a narrow center gap and no visible axis marker.
- Rank companies by the smaller of their two weights, matching the pairwise metric; summarize contributions beyond the displayed rows without changing the total.
- Add a developer setting that accepts finite positive integers, persists valid values, and retains the last valid value or default when input is invalid.
- Extend the existing pairwise information explanation to cover the two displayed weights, contribution ranking, configurable limit, and remainder.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `pairwise-product-overlap`: Add a selected-pair holdings drill-down and a configurable maximum for its displayed companies.

## Impact

- Pairwise overlap rendering and snapshot holdings access in `web/app.js` and `web/pairwise-overlap.js`.
- Developer setting validation and persistence in `web/redundancy.js` and `web/app.js`.
- Pairwise and developer settings markup/styles in `web/index.html` and `web/styles.css`.
- Localized labels and explanatory copy in `web/locales/*.json`.
- Pairwise and developer-setting frontend contract and runtime tests.

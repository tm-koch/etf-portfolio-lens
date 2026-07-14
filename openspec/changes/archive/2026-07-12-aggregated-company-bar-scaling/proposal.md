## Why

The aggregated holdings view already identifies the top companies correctly, but the current bar treatment makes it too easy to misread bar width as an ETF-by-ETF split rather than as the total company exposure used for ranking. This change makes the visual encoding explicit so bar length and rank both reflect the same company total.

## What Changes

- Keep one stacked bar per company in the aggregated list.
- Make the full bar length proportional to the company's total exposure, using the same value that drives the ranking order.
- Preserve the internal ETF-colored segments inside each bar so users can still see how the total exposure is composed.
- Keep the company label and exact percentage visible alongside the bar so the normalized width is not confused with absolute portfolio value.

## Capabilities

### New Capabilities
- `aggregated-company-bar-scaling`: aggregated company rows render one stacked bar whose full width represents the total company exposure used for ranking.

### Modified Capabilities
- None.

## Impact

- Affects the aggregated holdings rendering in `web/app.js`.
- May require minor CSS adjustments in `web/styles.css` for bar presentation.
- Does not change the exposure data model or ranking calculation itself.

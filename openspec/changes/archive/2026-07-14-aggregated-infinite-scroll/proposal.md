## Why

The aggregated tab currently needs to present a long ranked list of holdings without overwhelming the viewport. Infinite scrolling lets the user inspect the highest-exposure holdings immediately while progressively revealing the rest as they scroll, which keeps the aggregated view usable on smaller screens and for large portfolios.

## What Changes

- Add an infinite-scroll experience to the aggregated tab holdings list.
- Show the top 20 holdings by default.
- Load additional holdings as the user scrolls downward until the full list is visible.
- Keep the existing ranking order stable while new items are appended.

## Capabilities

### New Capabilities
- `aggregated-infinite-scroll`: the aggregated holdings list initially shows the top 20 holdings and progressively appends remaining holdings as the user scrolls.

### Modified Capabilities
- None.

## Impact

- Affects the aggregated holdings rendering in `web/app.js`.
- May require supporting layout or sentinel styling in `web/styles.css`.
- Does not change aggregation math or portfolio data sources.

## Why

The current application wraps navigation and every destination in an outer framed layout. On smartphones, that frame consumes scarce horizontal space even though navigation already belongs to the viewport, while on desktop the card-based navigation does not provide a persistent separation from the active page. Treating navigation as app chrome and content as a separate reading column will make the interface more efficient and consistent across viewport sizes.

## What Changes

- Move the primary navigation before the destination content and present it as a persistent desktop app bar.
- Remove the outer page frame as a visual and layout wrapper.
- Keep desktop destination content centered within a constrained content column below the app bar.
- Make smartphone destination content full-bleed, retaining internal panel padding and bottom clearance for the fixed navigation bar.
- Preserve the existing Home, Portfolio, Compare, and Explore destinations, their order, active styling, accessibility state, persistence, and mobile safe-area behavior.
- Preserve the existing fixed bottom navigation on smartphone-sized viewports, using the same navigation element and destination rendering path.
- **BREAKING**: Change the desktop navigation placement contract from after the Home panel to before the active destination content.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bottom-navigation`: Make navigation a persistent app bar above destination content on desktop while retaining fixed bottom placement on smartphones.

## Impact

- `web/index.html`: Reorganize the navigation and destination-panel structure and remove the outer frame wrapper.
- `web/styles.css`: Add the desktop app-bar and constrained content-column layout, remove mobile outer gutters and panel framing where appropriate, and preserve bottom-navigation geometry and clearance.
- `openspec/specs/bottom-navigation/`: Update the responsive placement and framing requirements.
- No backend, data, URL-routing, persistence, or third-party dependency changes are required.

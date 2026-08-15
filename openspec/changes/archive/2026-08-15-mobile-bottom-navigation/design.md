## Context

The web app is a dependency-light static browser application. `web/index.html` currently contains a three-button tab bar, `web/app.js` switches the visible panels through `state.activeTab` and `setTab()`, and `web/styles.css` changes the tab bar to a vertical control on narrow screens. The requested navigation is a primary-destination control for Portfolio, Compare, and Explore, with Explore continuing to use the internal `aggregated` state and panel identifiers.

The change spans markup, client state, styling, and icon presentation. It does not introduce server routing, URL changes, or a new data model.

## Goals / Non-Goals

**Goals:**

- Replace the existing tab bar with an extensible primary navigation.
- Show an icon and text label for each destination.
- Keep the navigation in normal flow on desktop and fixed to the viewport bottom on mobile.
- Reserve space for mobile safe areas and navigation height so content remains readable.
- Restore the selected destination after reload using local browser storage.
- Preserve empty states and current panel behavior for all destinations.

**Non-Goals:**

- Add URL routing, browser-history entries, deep links, or server-side navigation.
- Rename the internal `aggregated` state or panel identifiers.
- Add navigation badges in this change.
- Redesign the destination content or summary cards.
- Introduce a frontend build system.

## Decisions

### Use a destination registry as the extension point

Define navigation entries as data containing an internal key, visible label, and icon name. Render the navigation from that registry and continue matching destination keys against the existing panel `data-panel` values. This keeps adding future destinations localized to the registry and panel markup instead of duplicating event and active-state logic.

An alternative is to keep three hard-coded buttons. That is simpler initially but makes future destinations and optional badges require changes in multiple places, so it does not meet the extensibility goal as well.

### Keep client-side state and persist only the selected key

Continue using `state.activeTab` for the active destination and add a separate versioned local-storage key for the selected navigation destination. On startup, accept only known registry keys and fall back to Portfolio for missing or invalid values. Navigation changes update the in-memory state and storage without touching the URL or browser history.

Persisting the whole rendered view is unnecessary, while URL-based routing would add browser-history behavior that is explicitly out of scope.

### Use Lucide icons with the existing browser-CDN approach

Use a pinned Lucide browser build and render the three initial icons from the navigation registry. Lucide provides consistent outline icons and a broad set of future navigation symbols without adding a bundler. The implementation must initialize icons after navigation markup is rendered and preserve accessible text labels even when icons are unavailable.

An npm dependency would provide stronger version management but would introduce build tooling that the current static app does not need. Hand-authored SVGs would avoid the dependency but would create an ongoing icon-maintenance burden.

### Use responsive fixed positioning only below the existing mobile breakpoint

At widths up to 760px, position the navigation at the viewport bottom with a solid background, elevated stacking order, and bottom padding based on `env(safe-area-inset-bottom)`. Add equivalent bottom clearance to the page content. Above 760px, keep the navigation in normal document flow where the current tab bar appears.

This preserves the app-like mobile interaction while avoiding a permanently occupied desktop viewport edge.

### Keep navigation semantics as a labeled nav of buttons

Use one `<nav>` with an accessible label and one button per destination. Buttons expose the active destination through `aria-current="page"` and retain visible text labels below the icons. This preserves keyboard operation and makes the control understandable to assistive technology.

## Risks / Trade-offs

- [Fixed navigation can cover content on short mobile screens] -> Add responsive content bottom padding equal to the navigation height plus the safe-area inset and verify the lowest controls remain reachable.
- [External icon CDN can be unavailable] -> Keep labels visible, use stable pinned assets, and ensure navigation functionality does not depend on icon rendering.
- [Stored navigation state can become invalid after future changes] -> Validate the stored key against the current destination registry and fall back to Portfolio.
- [A destination registry can drift from panel markup] -> Keep internal keys equal to existing panel identifiers and add focused tests or manual checks for every registry entry.
- [Changing the current tab bar may affect existing responsive styling] -> Remove or override the old tab-specific layout rules and verify desktop, tablet, and mobile widths.

## Migration Plan

1. Add the new navigation markup and pinned Lucide browser asset.
2. Render and bind destination entries through the existing active-panel switching path.
3. Persist and restore the active destination under a new versioned storage key.
4. Replace the old tab-bar styles with desktop flow and mobile fixed-navigation styles.
5. Validate empty states, reload behavior, keyboard access, and viewport layouts.

Rollback is limited to reverting the navigation markup, state handling, and styles. Existing portfolio storage remains unchanged, so rolling back does not require data migration.

## Open Questions

No product decisions remain open. The implementation should use the existing 760px responsive breakpoint and place the desktop navigation below the summary cards.

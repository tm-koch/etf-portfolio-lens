## Context

The static web app currently renders the product introduction and live portfolio summary before a primary navigation containing Portfolio, Compare, and Explore. The navigation is driven by `NAVIGATION_DESTINATIONS` and `state.activeTab` in `web/app.js`; panels are selected through matching `data-panel` values, and the selected destination is persisted in local storage.

This change adds a Home destination without introducing routing, a backend dependency, or a new portfolio data model. The existing summary calculation already produces the four requested values: selected ETF positions, share units, underlying holdings, and shared companies.

## Goals / Non-Goals

**Goals:**

- Make Home the first primary destination and the default for users without a valid stored destination.
- Place the existing product introduction and four live summary metrics inside the Home destination.
- Keep the build-provenance dialog reachable from the Home information area.
- Preserve Portfolio, Compare, and Explore behavior, including the internal `aggregated` key.
- Preserve desktop document flow, mobile fixed navigation, accessibility, and local destination persistence.

**Non-Goals:**

- Add URL routing, deep links, browser history entries, or server-side navigation.
- Change portfolio calculations, snapshot formats, catalog data, or local portfolio storage.
- Add new summary metrics, dashboard charts, or calls to action beyond the existing content.
- Redesign the existing Portfolio, Compare, or Explore panels.

## Decisions

### Model Home as a normal destination panel

Add `home` to the destination registry and add a matching Home panel. Move the existing hero information and summary grid into that panel so overview content is not globally duplicated around every destination. Keep the build dialog outside the panel only where required for dialog semantics, while retaining its trigger in the Home information area.

An alternative is to leave the hero and summary globally visible and make Home only a navigation label. That would not give Home a distinct content boundary and would leave the other destinations competing with persistent overview content.

### Reuse the existing summary renderer

Keep `updateSummary()` and its existing aggregation functions as the source of truth, changing only the location of `summary-grid` in the markup. This avoids divergent metric calculations and preserves the current empty-state behavior, including zero values when no positions are selected.

An alternative is to create a Home-specific summary calculation. That would duplicate business logic without adding user value.

### Preserve destination keys and validate stored state

Use `home` as the new internal key, keep `portfolio`, `comparison`, and `aggregated` unchanged, and retain the existing registry-based validation in `loadActiveTab()`. Change the default state from `portfolio` to `home`; invalid or missing stored keys therefore fall back to Home.

An alternative is to migrate the local-storage value explicitly. Because the existing key stores only a destination string and all previous keys remain valid, explicit migration is unnecessary.

### Update navigation specifications as a delta

Add a new `home-tab` capability spec and modify the existing `bottom-navigation` requirements for destination membership, icon identity, responsive placement, and default persistence. The implementation remains a single labeled navigation with Lucide icons and the existing 760px mobile breakpoint.

## Risks / Trade-offs

- [Moving the hero changes the current desktop document order] -> Verify that the Home panel remains the first visible destination and that navigation remains usable in normal document flow.
- [A stored `portfolio` selection will continue to open Portfolio after the change] -> Treat this as intentional persistence; only missing or invalid values default to Home.
- [The Home panel may make the first viewport taller] -> Reuse the current responsive grid and verify desktop, tablet, and mobile layouts.
- [A missing Lucide asset could remove the new icon] -> Keep the visible Home label and button behavior independent of icon initialization.
- [Existing bottom-navigation tests expect three destinations] -> Update the navigation contract and add focused checks for Home ordering and fallback behavior.

## Migration Plan

1. Add the Home panel and move the existing introduction and summary markup into it.
2. Add Home to the navigation registry and update the default destination.
3. Preserve the existing rendering, event delegation, and responsive styles, adjusting selectors only where the moved markup requires it.
4. Update the capability specifications and add focused tests or manual browser checks for Home selection, persistence, and responsive layout.

Rollback requires reverting the Home markup, registry entry, default key, styles, and associated specifications. Existing portfolio data and local storage remain compatible.

## Open Questions

No product decisions remain open based on the agreed direction. Implementation validation should confirm whether the existing hero card styles can be reused directly inside the Home panel without creating undesirable nested-card appearance; if not, the Home panel should absorb the hero styling while preserving the current visual hierarchy.

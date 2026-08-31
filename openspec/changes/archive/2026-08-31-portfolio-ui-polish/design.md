## Context

The static frontend already renders the Portfolio catalog, selected-position table, About this build dialog, and PDF import debug download from `web/app.js`, `web/index.html`, and `web/styles.css`. Snapshot paths are currently rendered directly under catalog items, the About dialog has a reusable metadata area and developer settings, and the import debug button is hidden or shown by import state alone.

## Goals / Non-Goals

**Goals:**

- Keep snapshot provenance available without occupying the Portfolio catalog layout.
- Make selected positions denser without changing their data or controls.
- Make share feedback visually easier to associate with the share action.
- Gate extracted PDF text download behind an explicitly enabled, persisted developer preference.
- Separate display metrics from weighting metrics so Share units always means share count and total portfolio value is calculated independently in CHF.
- Preserve responsive behavior and existing import, portfolio, and sharing workflows.

**Non-Goals:**

- Do not change snapshot loading, catalog data, PDF parsing, portfolio persistence, or share payloads.
- Do not use share counts as a substitute for a monetary total in the CHF value card.
- Do not compact catalog item typography; the ticker/name compaction applies only to selected positions.
- Do not expose extracted PDF text by default or upload it anywhere.

## Decisions

- Reuse the About dialog's existing metadata presentation for a dedicated Data section. Render the common ETF data timestamp and a current selected-ETF list with each catalog entry's snapshot path, so the displayed provenance follows the current selection.
- Keep the debug control in the existing Developer mode area and persist it with a dedicated local-storage key. The download button's effective visibility is the conjunction of the preference and the presence of extracted pages.
- Change only the selected-position identity markup and its local styles. The catalog renderer remains unchanged except for removing its visible snapshot-path line.
- Increase the sharing block's layout gap through its existing CSS rather than adding spacer markup, preserving the current feedback and fallback URL behavior.
- Calculate Share units by summing position share counts directly. Calculate total portfolio value by summing valid imported `valueChf` fields; show an unavailable state when no valid imported monetary values exist rather than presenting a misleading total.
- Cover the new behavior with web contract assertions and focused state/rendering tests where the existing test harness supports them.

## Risks / Trade-offs

- [Snapshot paths may be long on narrow screens] -> Keep them in the About dialog's metadata layout with wrapping or overflow-safe text styles.
- [A persisted debug preference may survive across sessions] -> Default missing or invalid values to false and provide an explicit switch to disable it.
- [The debug button could become stale after a new failed import] -> Recompute visibility whenever the preference or extracted-page state changes, and retain the existing page-state guard.
- [Adding selected ETF paths may make the About dialog lengthy] -> Render only selected positions, use the existing scrollable dialog, and avoid duplicating full snapshot payloads.
- [Some portfolios contain manual positions without imported monetary values] -> Keep the CHF value card explicitly unavailable unless at least one valid imported CHF value exists, while retaining share-count fallback for exposure weighting.

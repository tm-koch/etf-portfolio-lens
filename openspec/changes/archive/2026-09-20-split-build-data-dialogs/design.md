## Context

The Home panel currently exposes one `About this build` action that opens a single native dialog. That dialog combines build provenance, ETF and live-data provenance, developer preview/debug switches, and current-selection warnings. The rendering helpers and event handlers in `web/app.js` also assume one dialog and one return-focus target.

The application already has separate conceptual data sources and existing specifications for build provenance, compact preview behavior, live market data, and selection warnings. This change reorganizes the presentation boundary without changing those data sources or portfolio calculations.

## Goals / Non-Goals

**Goals:**

- Provide two clearly named entry points: `Build & preview` and `Data details`.
- Keep build source/deployment metadata and developer preview/debug controls together.
- Keep ETF/live-data provenance and current-selection warnings together.
- Preserve native dialog accessibility, Escape dismissal, focus restoration, local metadata fallback, and unchanged navigation.
- Reuse the existing metadata and warning rendering helpers where their data ownership remains valid.

**Non-Goals:**

- Change build metadata generation, live-data generation, ETF snapshots, or warning conditions.
- Change compact Explore preview or portfolio import debug persistence.
- Change portfolio, comparison, aggregation, or primary navigation behavior.
- Add URL routes or server-side state for either dialog.

## Decisions

### Use two sibling native dialogs

The Home panel will expose two sibling buttons and two sibling `<dialog>` elements. Each dialog will have its own heading, description, close control, open/close handlers, cancel handling, and return-focus reference.

This is preferred over a tabbed dialog because the user requested two pop-ups and because each surface has a distinct purpose. A single dialog with internal tabs would retain the mixed-container mental model and add tab keyboard behavior that is unnecessary here.

### Assign content by responsibility

`Build & preview` contains source commit, commit timestamp, publish timestamp, optional build details, compact Explore preview, and portfolio import debug. `Data details` contains ETF data timestamp, live-data timestamp/status, selected ETF snapshot paths, and current-selection warnings.

Warnings belong with Data details because they describe the selected portfolio's snapshot and aggregate data quality rather than the application build. The existing warning collection remains shared with the Explore warning panel.

### Keep shared render helpers, split DOM targets

The existing timestamp formatting, metadata row, warning item, and focus-safe dialog mechanics should be reused. Rendering functions should target separate build and data containers rather than duplicating provenance parsing or warning aggregation logic.

### Use explicit, accessible labels

The two triggers will use visible labels and suitable icons. Each dialog will expose a unique `aria-labelledby` and `aria-describedby` relationship, and each close control will identify which dialog it closes. Opening one dialog will not open or mutate the other.

## Risks / Trade-offs

- [Risk] Moving controls can make developer-only settings less discoverable. → Mitigation: keep both entry points together in the existing development/status area and use explicit labels.
- [Risk] Two dialogs increase focus and Escape handling paths. → Mitigation: use one shared dialog lifecycle helper or equivalent paired handlers, with one return-focus value per dialog.
- [Risk] Existing contract tests may assume IDs and text for the single dialog. → Mitigation: update focused web contract tests to assert both surfaces and preserve all unchanged metadata and warning behavior.
- [Risk] Data content may be tall for portfolios with many selected ETFs. → Mitigation: retain the existing responsive dialog width and overflow behavior, and keep the data sections semantically grouped.

## Migration Plan

1. Replace the single Home trigger and dialog markup with the two labeled triggers and dialogs.
2. Split element references, render targets, and dialog event handling while preserving the existing data loaders.
3. Apply shared dialog styling and verify desktop/mobile layouts and keyboard dismissal.
4. Update web contract tests and run focused plus full test suites.

Rollback is a frontend-only revert: restore the single trigger/dialog markup and its original event wiring. No persisted data or generated artifacts require migration.

## Open Questions

- Whether the product prefers the labels `Build & preview` / `Data details` or slightly shorter `Build` / `Data` labels. The proposal uses the more descriptive labels for discoverability.
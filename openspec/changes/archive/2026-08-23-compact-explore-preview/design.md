## Context

The web app is a static JavaScript frontend. The Explore tab currently renders `state.companyRanked`, produced by `aggregateCompanyExposure()` in `web/app.js`. Each ranked holding already contains its total portfolio exposure (`weight`) and per-ETF contributor records with the contributor's portfolio contribution (`weight`) and share of that holding (`shareOfCompany`).

The feature is a preview of an alternate presentation, so the existing Explore rendering must remain the default and must continue to work unchanged. The current UI has build/provenance details but no separate developer settings surface; the preview control can be added to that developer-oriented dialog without changing normal navigation.

## Goals / Non-Goals

**Goals:**

- Add a clearly labeled developer preview switch with an off-by-default persisted state.
- Render the existing ranked holdings as a compact matrix when enabled.
- Use the existing aggregation output as the only source for table values.
- Provide one column for each selected ETF, with horizontal scrolling on narrow screens.
- Preserve sorting, empty states, and the existing Explore view when preview mode is off.

**Non-Goals:**

- No backend, snapshot, catalog, or ingestion changes.
- No new portfolio or exposure calculations.
- No replacement of the existing visual Explore view.
- No user-facing preference or server-side synchronization.
- No pagination redesign; compact mode reuses the existing 20-row incremental loading behavior.

## Decisions

### Reuse the existing aggregation result

The compact renderer will consume `aggregateCompanyExposure(positions).ranked`. It will map each row's `company.name`, `company.displayWeight`, and `company.contributors`. The total column uses the existing rounded display weight. Each ETF cell uses the matching contributor's existing `shareOfCompany`, while absent contributors render as an em dash. This avoids divergent formulas and guarantees that the compact and existing views describe the same exposure model.

**Alternative considered:** Rebuild a holding-by-ETF matrix directly from snapshots. Rejected because it duplicates aggregation identity, weighting, rounding, and sorting behavior.

### Keep preview selection in local browser storage

Add a dedicated versioned storage key and a boolean loader that treats missing, malformed, or unsupported values as false. The switch change saves the value and rerenders only the Explore presentation. `localStorage` matches the app's existing persistence convention and survives reloads; `sessionStorage` would lose the preview selection too easily for a developer preview.

**Alternative considered:** Store the setting in the URL. Rejected because the requested state is browser-persistent and URLs would make preview mode easy to share accidentally.

### Place the switch in the developer build dialog

Add a Developer mode section to the existing build dialog, containing a labeled checkbox or switch for the compact Explore preview. The control remains available without adding a normal navigation item or changing the default user workflow.

**Alternative considered:** Add a toolbar control directly to Explore. Rejected because the request scopes the control to developer mode and the existing dialog is already the app's developer/provenance surface.

### Use a semantic table with a scroll shell

The compact view will use a semantic table inside an `overflow-x: auto` wrapper. The first column will have a stable width and remain sticky while ETF columns scroll; ETF columns will have stable narrow widths. Holding names will be clipped to a short line with a visual fade and a full-name hover title. The table header will identify each ETF by ticker, with an accessible full ETF name available through the header label/title. The wrapper will preserve the table's intrinsic width instead of compressing numeric columns into unreadable content.

Compact rows will use the existing `COMPANY_BATCH_SIZE` and `IntersectionObserver`: the table header is rendered immediately, the first 20 rows are appended to its body, and later batches are inserted as the sentinel becomes visible.

**Alternative considered:** CSS grid or card rows. Rejected because a semantic table better expresses the row/column comparison and supports keyboard and assistive-technology interpretation.

## Risks / Trade-offs

- [Risk] A portfolio containing many ETFs creates a wide table. → Keep the table horizontally scrollable and use stable numeric column widths.
- [Risk] Existing contributors are sorted by contribution, not by the catalog's ETF order. → Build columns from the selected position order and look up each contributor by ticker, keeping the matrix stable and comparable to the ETF selection.
- [Risk] Holding names or contributor values may be missing. → Reuse the existing holding-name fallback and render missing cells as `—` without creating new rows or calculations.
- [Risk] Large portfolios can make a full matrix heavier than the current incremental company list. → Preserve the existing ranked source and evaluate rendering performance with the published catalog before considering a separate virtualization change.
- [Risk] The preview flag may be malformed in storage. → Treat all values other than the explicit stored true value as disabled.

## Migration Plan

No data migration is required. Deploy the frontend with the new key absent; all existing browsers therefore remain in the current Explore view. Developers can enable the switch from the build dialog. Removing or disabling the preview later consists of ignoring the key and retaining the existing renderer.

## Open Questions

- Confirm whether the compact matrix should include all ranked holdings or retain the existing top-20/infinite-scroll boundary. The proposal currently targets all holdings available from the existing ranked result, while preserving the existing list's loading behavior may be preferable for performance.

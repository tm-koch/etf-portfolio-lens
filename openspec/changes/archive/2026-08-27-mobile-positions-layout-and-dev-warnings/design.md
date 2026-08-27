## Context

The static web application currently renders each selected ETF position as one four-column table row. The long ETF identity cell and fixed-width controls can make the table wider than a phone viewport, while the table wrapper permits horizontal scrolling. Explore already derives warnings from missing or empty snapshots and aggregate warnings, but the developer build dialog only shows build metadata and optional details.

The change must preserve the existing desktop interaction model, keep position editing and removal behavior intact, avoid new dependencies, and make the current selection diagnostics available where developers inspect build information.

## Goals / Non-Goals

**Goals:**

- Make every selected position usable at mobile widths without horizontal scrolling.
- Keep the ETF identity readable above a lower row containing Shares, Weight, and Remove.
- Preserve the existing desktop/tablet table presentation where it is usable.
- Provide a developer-dialog warning summary sourced from the same warning conditions as Explore.
- Keep warning text and counts consistent between the dialog and Explore.
- Keep the Selected positions Weight column concise by omitting inline warning counts.
- Preserve accessible names and keyboard operation for inputs and removal controls.

**Non-Goals:**

- Changing portfolio calculations, warning rules, ingestion behavior, or backend APIs.
- Redesigning the Explore warning panel.
- Changing the compact Explore holdings matrix overflow behavior.
- Adding a new warning severity system or external UI dependency.

## Decisions

### Use one semantic position row with responsive CSS reflow

The existing position row and four cells will remain the single source of markup. At the mobile breakpoint, the row will switch to a grid/card-like layout: the ETF identity spans the first row, and Shares, Weight, and Remove occupy the lower row. Explicit responsive labels or existing header associations will keep the controls understandable when table headers are no longer visually arranged as columns.

A separate mobile rendering would guarantee layout freedom but would duplicate rendering logic and increase the chance that editing, warning counts, or remove behavior diverge. Shrinking the existing table is rejected because it cannot reliably accommodate long ETF names and fixed controls.

### Keep desktop table behavior above the mobile breakpoint

The existing table layout remains active above the established responsive breakpoint. This limits the visual change to the problematic viewport range and avoids disrupting the established scanning pattern on larger screens.

### Share normalized warning records between surfaces

Warning generation will produce a reusable current-selection warning collection, and both the Explore warning panel and developer build dialog will consume it. The dialog will contain a labeled "Current selection warnings" section. When warnings exist, it will list the same warning messages and relevant ETF context; when none exist, it will show a concise no-warnings state or an equivalent empty section that does not imply a problem.

Duplicating the warning conditions in `renderBuildInfo()` is rejected because future warning changes could make the two surfaces disagree. Moving warning ownership into the backend is rejected because these are already available client-side and the feature does not require an API change.

### Keep warning summary subordinate to build metadata

The dialog will retain its existing metadata and optional-details structure, placing the warning summary as a dedicated diagnostics section rather than replacing or interleaving build metadata. This keeps the dialog useful for provenance while making selection problems visible during developer inspection.

### Keep mobile controls visually compact

The Selected positions Weight cell will display only the calculated percentage. On mobile, the Shares, Weight, and Remove cells will omit their repeated visual labels so the lower row reads as a compact control strip. The Remove button will use a trash icon with a tooltip and accessible name, while desktop retains its visible text label.

Keeping all labels visible would make the small cards feel vertically repetitive. Hiding only the visual labels is preferred to removing semantics: the Shares input and Remove button retain accessible names, and the Weight cell retains an accessible label while its value remains inline.

## Risks / Trade-offs

- [Risk] CSS reflow can weaken native table semantics on mobile. -> Mitigation: retain one row per position, provide explicit control labels, and test keyboard and screen-reader-relevant accessible names.
- [Risk] Long ETF names can still crowd the identity area. -> Mitigation: allow the identity cell to wrap within the card and constrain lower controls with stable flexible grid tracks.
- [Risk] Warning rendering can drift if one surface bypasses the shared collection. -> Mitigation: centralize warning record creation and add tests covering both Explore and dialog output.
- [Risk] Existing browser snapshots or selectors may depend on the four-cell desktop structure. -> Mitigation: preserve the cells and classes, changing only responsive layout and adding narrowly scoped dialog markup.

## Migration Plan

No data migration or deployment migration is required. Implement the shared warning collection and dialog markup, apply the mobile CSS reflow, then validate desktop and narrow viewport behavior. Rollback consists of reverting the web markup, rendering, and style changes; stored portfolio selections and build data are unaffected.

## Open Questions

- Confirm whether the no-warnings state should remain visible in the developer dialog or whether the warnings section should be hidden when empty; either choice must not change the warning records shown when warnings exist.

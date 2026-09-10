## Context

The frontend currently stores `valuationMode` on each imported position. The import dialog initializes that field from `state.importValuationMode`, but the selector is not available after confirmation, so an imported portfolio cannot switch valuation basis without re-importing the PDF. Effective valuation already centralizes live quote, FX conversion, imported fallback, and unavailable states in `web/valuation.js`.

The change must preserve imported broker fields and remain compatible with existing local-storage portfolios, shared portfolios, and percentage-only private portfolios.

## Goals / Non-Goals

**Goals:**

- Provide a portfolio-level control for full portfolios to choose latest published valuation or imported valuation.
- Re-render all price, CHF value, weight, and total displays immediately after a mode change.
- Keep imported values available for switching back and for live-data fallback.
- Persist the selected mode and preserve existing data formats where possible.
- Make the import dialog's selection initialize the portfolio-level mode.

**Non-Goals:**

- Changing live quote retrieval, FX providers, or artifact generation.
- Re-importing or recalculating broker source values from raw PDFs after confirmation.
- Adding live valuation to percentage-only private portfolios that intentionally omit absolute values.
- Introducing a server-side portfolio or account setting.

## Decisions

### Store valuation mode at portfolio level

Add a persisted full-portfolio `valuationMode` alongside `mode` and `portfolio`, with `latest` as the default for existing data. Keep the per-position field as a compatibility input for older local data and shares, but resolve the active full-portfolio mode centrally when rendering and calculating totals.

**Alternative considered:** Continue storing only per-position modes. Rejected because it requires mutating every position for a simple user preference and makes the UI state easy to desynchronize.

### Reuse the existing effective valuation function

Extend `getEffectiveValuation` or its call boundary with the selected mode, while preserving its current live, fallback, and unavailable result contract. `latest` permits live quote valuation and fallback; `imported` bypasses live quotes and uses persisted imported CHF values.

**Alternative considered:** Duplicate mode checks in each renderer. Rejected because prices, totals, weights, and charts could diverge.

### Place the control in the full-portfolio workflow

Add a compact control near the selected-positions heading or portfolio controls. Hide or disable it for percentage-only portfolios, where absolute valuation is intentionally unavailable. The import dialog keeps its existing selector as the initial mode for the confirmed portfolio.

**Alternative considered:** Keep the selector only inside the import dialog. Rejected because it cannot address the reported post-import switching problem.

### Persist and share mode conservatively

Persist the mode in the existing local-storage envelope. Include it in full portfolio share payloads only if the current share contract can accept the optional field without breaking legacy decoding; otherwise shared portfolios default to `latest`. Percentage-only shares remain mode-independent.

**Alternative considered:** Encode mode in every position in all share payloads. Rejected because it duplicates a portfolio-level preference and expands private payload data unnecessarily.

## Risks / Trade-offs

- [Existing local portfolios lack a portfolio mode] -> Default them to `latest`, preserving the current effective behavior for positions without `valuationMode`.
- [Imported mode has missing `valueChf`] -> Keep the existing unavailable state rather than deriving a value without a supported FX rate.
- [Mode changes affect many renderers] -> Route all monetary calculations through the existing effective valuation boundary and add runtime assertions covering totals and position rows.
- [Users expect the import preview to show live prices] -> Label the preview as imported source data and make the post-confirmation portfolio control the authoritative mode.
- [Browser cache serves an older shell] -> Update the relevant frontend cache/version markers and verify both fresh-load and reload behavior.

## Migration Plan

1. Add optional portfolio-level mode normalization with `latest` default.
2. Add the control and route render calculations through the selected mode.
3. Preserve the import dialog's selected mode when confirming an import.
4. Add tests and browser verification for mode switching and reload persistence.
5. Roll back by removing the control and ignoring the optional persisted field; existing portfolio and position data remains usable.

## Open Questions

- Should the mode control be shown as a segmented control or a select menu on narrow screens?
- Should full-portfolio share links preserve the sender's valuation mode, or always default shared links to latest published data?

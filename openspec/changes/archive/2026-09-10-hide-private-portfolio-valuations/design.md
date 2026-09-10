## Context

Private share links restore relative allocation units and intentionally exclude absolute valuation fields. The current Portfolio renderer nevertheless resolves current market data for every position and renders valuation columns, while the valuation selector is already unavailable in percentage mode. This creates a presentation and privacy mismatch without requiring new state or payload formats.

## Goals / Non-Goals

**Goals:**

- Make percentage-only private portfolios visibly valuation-free.
- Prevent unnecessary valuation resolution for percentage-only rows.
- Keep allocation weights and all non-valuation portfolio views unchanged.
- Preserve the existing full-portfolio valuation workflow and responsive layouts.

**Non-Goals:**

- Changing private payload encoding, validation, or persistence.
- Changing catalog, quote, FX, or imported valuation behavior.
- Removing summary cards or changing their established unavailable representation.

## Decisions

- **Branch the positions table by portfolio mode at render time.** Percentage mode will render identity, relative Shares, and Remove controls; full mode will retain the existing ETF, Shares, Price, Value CHF, Weight, and Remove columns. This keeps the private presentation compact while preserving the core position-management action.
- **Skip `getPositionValuation()` for percentage rows.** Relative weights will continue to derive from the normalized shares-unit total. This is preferable to resolving and discarding live values because it prevents both misleading output and unnecessary market-data dependency.
- **Keep the existing mode-control guard.** The valuation basis label and selector remain unavailable for percentage mode through the existing control rendering path; the change does not add a second control state or alter persistence.
- **Use mode-specific headers, cells, and empty-state spans.** The static valuation and Weight headers will be marked by column class and hidden for percentage mode, while Remove remains visible; row cells and empty-state spans match the three-column or six-column layout. Existing mobile grid rules continue to work because private rows contain identity, Shares, and Remove cells.
- **Add mobile table separation at the wrapper boundary.** The positions table wrapper will receive a mobile-only top margin so the first ETF row does not visually collide with the selected-position heading or valuation control. Desktop spacing remains unchanged.
- **Use one portfolio-level valuation source note.** The selected-position heading will show `Live` or `Imported` beside the valuation selector for full portfolios, while Value CHF cells remain numeric-only. The blue dot is visible and slowly animated only for live mode; imported mode keeps the same note style without the dot.
- **Align valuation controls as one row.** The selector and provenance note will share a flex row and align on their control baseline, with a narrow-screen fallback that stacks them without overflow.
- **Right-align the provenance note to the control.** The wider valuation row will fill the available heading width, place the note at the far right, and center it against the select control; the narrow fallback will keep the note below the selector.
- **Match the select top edge.** The provenance note will account for the selector label and control gap so its top edge aligns with the select box, not the `Valuation basis` text.

Alternatives considered: rendering `Unavailable` in Price and Value CHF was rejected because the requirement is to hide absolute valuation content, not merely redact values; clearing values in the position model was rejected because it would mutate valid full-portfolio data and blur the distinction between private and full state.

## Risks / Trade-offs

- [Risk] A future renderer could accidentally reintroduce valuation cells for percentage mode. -> Mitigation: add contract and runtime regression tests covering absent valuation headers/cells and non-invocation of valuation resolution.
- [Risk] Desktop and mobile table structures could diverge. -> Mitigation: test both the mode-specific column contract and the existing mobile percentage layout.

## Migration Plan

No data migration is required. Deploy the renderer and focused tests together; rollback is a code-only revert, and existing payloads remain compatible.

## Open Questions

None.
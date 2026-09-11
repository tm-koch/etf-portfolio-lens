## Context

Private share links load ETF positions as relative allocation units and set `state.portfolioMode` to `percentage`. The Portfolio renderer already calculates normalized weights from those units and already avoids resolving absolute valuations for percentage rows, but the current table contract omits the Weight column. The valuation-status element is also rendered from the same portfolio heading area as full-portfolio valuation controls; a valid private share view must not present it as `Live` or `Imported`.

The behavior must remain correct after startup, asynchronous snapshot loading, position edits, and all other paths that call the shared render routine.

## Goals / Non-Goals

**Goals:**

- Show each private position's normalized relative Weight beside its relative Shares value.
- Keep Price, Value CHF, valuation controls, and valuation provenance unavailable for private percentage-only portfolios.
- Ensure the valuation-status box stays hidden after every private-mode rerender.
- Preserve the existing full-portfolio Live/Imported status behavior.
- Add focused regression coverage for private and full modes.

**Non-Goals:**

- Changing private share payload encoding or validation.
- Resolving absolute prices, CHF values, or live quotes for private rows.
- Changing summary-card privacy behavior, exposure calculations, or backend data.

## Decisions

- **Use portfolio mode as the rendering boundary.** Treat `state.portfolioMode === 'percentage'` as the authoritative condition for both private table presentation and status-box suppression. This matches the decoded share payload and persisted state, and avoids adding a second privacy flag.
- **Render Weight from relative units.** Keep the existing `getPositionWeight()` calculation and emit the Weight cell in percentage mode. Private weights remain derived from relative units, never from valuation data.
- **Keep valuation status separate from table columns.** Hide the status element whenever percentage mode is active, while retaining its existing Live/Imported behavior for full portfolios. Do not infer visibility from whether a private share link was merely created; creating a link does not change the current portfolio mode.
- **Update responsive layout and empty-state spans together.** Private rows and headers must have four visible columns on desktop and a populated `shares weight remove` mobile row, with no empty valuation grid areas.
- **Test both state paths.** Add source/runtime coverage for valid private-link loading and rerender behavior, plus contract coverage proving full-mode provenance remains intact.

## Risks / Trade-offs

- [Risk] A future render path could reset the status box after private mode is loaded. -> Mitigation: assert the hidden state through the final render path and after representative private mutations.
- [Risk] Reintroducing Weight may accidentally call valuation resolution. -> Mitigation: retain the percentage-mode valuation guard and test that private rendering uses relative units only.
- [Risk] Desktop and mobile column definitions could drift. -> Mitigation: cover the four-column private table and mobile grid-area contract together.

## Migration Plan

No data migration is required. Existing private payloads remain compatible. Deploy the renderer, specification updates, and regression tests together; rollback is a code-only revert.

## Open Questions

None.

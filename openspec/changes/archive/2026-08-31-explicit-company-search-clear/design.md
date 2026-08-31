## Context

The compact Explore preview currently renders the company search as a native `type="search"` input and updates results on each `input` event. Native search cancel controls are user-agent specific: Chromium-based browsers may expose a WebKit cancel affordance, while Firefox and Firefox for Android do not support `::-webkit-search-cancel-button`. The ranked holding cell contains separate rank and name elements, but its layout does not explicitly prevent wrapping.

The change must remain within the existing vanilla JavaScript, HTML, and CSS frontend. It must preserve the current name-only filtering, stable ranks, empty-query pagination, accessibility semantics, and responsive 36vw mobile holding column.

## Goals / Non-Goals

**Goals:**

- Provide a consistent, application-owned clear action on desktop and mobile browsers, including Firefox mobile.
- Show the clear action only when the company search has a value.
- Clear the search, restore the initial ranked table, restore pagination, and retain input focus.
- Keep the rank and company name on one visual line while retaining responsive clipping and the existing hover title.
- Cover markup, state behavior, and layout hooks with focused contract tests and browser verification.

**Non-Goals:**

- Change the company matching rules, ranking order, or aggregated exposure calculations.
- Replace the semantic `type="search"` input or add a frontend dependency.
- Depend on browser-native search controls for the clear interaction.
- Add a clear control to unrelated catalog or portfolio inputs.

## Decisions

### Use an explicit button instead of native search decoration

Add a real button inside a positioned search control wrapper and toggle its visibility based on the current search value. The button will use an accessible label and a minimum 44px touch target. This is preferred over relying on `::-webkit-search-cancel-button` because that selector is non-standard and unsupported by Firefox and Firefox for Android; an explicit control gives the same visible interaction everywhere while retaining `type="search"` for semantics and mobile keyboard behavior. The WebKit cancel decoration will be suppressed where supported so Chromium does not show a duplicate cross; this is only visual cleanup and is not part of the clear behavior.

The clear handler will set the input value to an empty string, update `state.companySearchTerm`, invoke the existing company-list render path, and focus the input again. The existing input listener remains the source of truth for normal typing and keeps the control visibility synchronized.

### Keep the rank/name content in a single non-wrapping flex line

Use an inline flex wrapper with `flex-wrap: nowrap` and `white-space: nowrap`. Keep the rank at a fixed flex basis and allow the name to shrink with `min-width: 0` and `flex: 1 1 auto`. The name's existing overflow/fade behavior remains responsible for long labels, including the mobile 36vw constraint.

### Preserve the existing rendering modes

The clear operation will reuse `renderCompanyList()` rather than introducing a second table-reset implementation. An empty or whitespace-only value will continue through the existing first-batch and sentinel path; a non-empty query will continue to bypass pagination.

## Risks / Trade-offs

- [Risk] The clear button can reduce the text area on narrow screens. -> [Mitigation] Position it inside the existing input boundary, reserve right-side padding, and use a compact visual glyph with a 44px hit area.
- [Risk] A button nested inside the existing label could affect label-click or focus behavior. -> [Mitigation] Keep the button type explicit, stop its default label activation if needed, and verify keyboard and touch focus behavior in browser checks.
- [Risk] Flex shrinking could clip names earlier than before. -> [Mitigation] Treat the rank as fixed, give the name the remaining width, and preserve the cell title for the complete company name.

## Migration Plan

No data migration or dependency migration is required. Update the compact Explore markup, event wiring, styles, and web contract tests. Verify desktop and mobile layouts, then deploy the static frontend normally. Rollback consists of reverting the change commit.

## Open Questions

None. The explicit clear control is the chosen cross-browser behavior.

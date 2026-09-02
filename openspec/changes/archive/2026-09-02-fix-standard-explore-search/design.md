## Context

The static frontend aggregates selected ETF holdings into `state.companyRanked` in `web/app.js`. The company search input and application-owned clear button already exist in the Explore panel and already update compact preview mode. The standard presentation uses the same aggregated ranking but currently renders it without consulting `state.companySearchTerm`, while its input handlers only rerender when compact preview is enabled.

The change must preserve the current shared search control, aggregation calculations, standard company-row presentation, compact table behavior, and lazy loading when no search is active.

## Goals / Non-Goals

**Goals:**

- Make the existing company-name search apply to standard Explore rows.
- Keep live input and clear-button updates consistent across both presentations.
- Show every matching standard row during an active search and preserve its original full-list rank.
- Restore the standard first-20-plus-infinite-scroll flow for empty or whitespace-only searches.
- Keep filtered and unfiltered rendering deterministic and clean up observers during rerenders.

**Non-Goals:**

- Change the search field markup, visibility, label, or clear-button interaction.
- Search ETF names, tickers, ISINs, contributor data, or internal keys.
- Change aggregation, weighting, ordering, snapshot data, or backend behavior.
- Add debouncing, server-side search, pagination infrastructure, or dependencies.
- Change the compact preview’s established behavior.

## Decisions

### Filter the complete ranked list before standard rendering

Derive matches from the complete `ranked` result using the existing trimmed, case-insensitive company-name substring rule. When the search term is non-empty, render all matches directly and skip the sentinel and intersection observer. This mirrors compact preview semantics and ensures a search cannot hide matches behind lazy loading.

An alternative is to filter only the first rendered batch, but that would make results depend on scroll position and fail to find lower-ranked matching companies.

### Preserve original ranks while filtering

Map each ranked company to its original one-based index before filtering. Pass that original index into standard row rendering so a filtered company keeps its portfolio rank rather than being renumbered in the result subset.

An alternative is to filter first and use the filtered array index, but that changes the meaning of the displayed ranking and diverges from the complete exposure order.

### Share the input event path across presentation modes

The existing company search input and clear-button handlers should rerender whenever the active tab is `aggregated`, regardless of the preview preference. `renderCompanyList()` remains the single owner of mode-specific rendering and observer cleanup.

An alternative is to maintain separate standard and compact search handlers, but that duplicates state transitions and risks inconsistent clear behavior.

### Keep the empty-search path unchanged

After trimming, an empty search term follows the existing standard renderer: display the initial batch, add the sentinel when needed, and install the observer. Search rerenders already disconnect the previous observer before rebuilding the list, so clearing the field naturally restores incremental loading.

## Risks / Trade-offs

- [A broad search may render many standard rows at once] -> This is bounded by the already loaded aggregated portfolio and is required for complete search results.
- [Adding original rank handling to standard rows increases the renderer contract] -> Keep the change local to `renderCompanyList()` and the existing row builder, with focused contract assertions.
- [A stale observer could append rows after a search transition] -> Continue disconnecting the observer at the beginning of every company-list render and avoid creating one for active searches.
- [Search terms may be entered while another tab is active] -> Preserve the current state update and rerender only when Explore is active; the next Explore render uses the latest term.

## Migration Plan

No data migration is required. Update the standard Explore rendering and shared event guards, add contract assertions for both modes, and run the focused web tests plus the available full test suite. Rollback consists of restoring the standard-mode search guard and unfiltered renderer path.

## Open Questions

None. The existing company-name matching semantics, clear behavior, and presentation control are authoritative.

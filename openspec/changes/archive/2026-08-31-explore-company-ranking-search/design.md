## Context

The compact Explore preview is rendered from `state.companyRanked`, which is produced by `aggregateCompanyExposure()` in descending total portfolio exposure order. `renderCompanyList()` resets the visible count and `appendCompanyBatch()` renders the first 20 rows, adding an intersection-observer sentinel when more rows remain. The existing ETF catalog search is unrelated and filters portfolio-entry options.

The new behavior is limited to the compact Explore preview. It must make the existing ranking visible, allow users to find companies by name while typing, and preserve the current lazy-loading behavior when no search is active.

## Goals / Non-Goals

**Goals:**

- Display a rank number for every compact Explore company row.
- Derive ranks from the complete exposure-ranked list, before filtering.
- Add an accessible company-name search input to the compact Explore preview.
- Apply case-insensitive trimmed substring matching against `company.name` on every input event.
- Render every matching company while a search term is active.
- Render zero company rows for a non-matching term and restore the full ranked list when the term is cleared.
- Preserve the existing first-20-plus-infinite-scroll behavior when the search term is empty.

**Non-Goals:**

- Search ETF catalog entries, contributor tickers, ISINs, or internal company keys.
- Change aggregation calculations, company ordering, contribution values, or backend data.
- Renumber filtered results relative to the filtered subset.
- Change the standard non-compact Explore presentation.
- Add server-side search, debouncing, or a new dependency.

## Decisions

### Keep the complete ranked list as the source of truth

Continue assigning `state.companyRanked` from the result of `aggregateCompanyExposure(positions)`. Use each company's index in that full list as its displayed rank, and filter a derived array only for rendering. This ensures a search result such as a seventh-ranked company continues to display rank 7.

An alternative is to assign ranks after filtering, but that makes the number describe the search result set rather than the portfolio ranking and changes as the query changes.

### Put the rank in the sticky Holding cell

Add the rank number alongside the company name within the existing sticky Holding cell instead of adding a new table column. This preserves the current ETF column structure and keeps the ranking visible while horizontally scrolling.

An alternative is a separate rank column, but it would consume width and require another sticky-column decision on narrow viewports.

### Filter only compact preview rows

Add a dedicated `companySearchTerm` state value and a search input associated with the compact preview. The input handler updates the state and calls `renderCompanyList()` only when the compact preview is active; the catalog's existing `searchTerm` remains independent.

An alternative is to reuse `searchTerm`, but that would couple ETF catalog filtering to Explore filtering and cause unrelated rerenders.

### Bypass lazy batching while a search is active

When the trimmed search term is non-empty, render the filtered ranked results directly and do not add an infinite-scroll sentinel. This guarantees all matches are displayed immediately. When the term is empty, retain the existing batch and observer flow.

An alternative is to batch filtered results too, but that would violate the requirement that all matches be displayed and would make the result depend on scrolling.

### Keep the table structure for zero matches

For an active search with no matches, render the compact table with its header and an empty `tbody`; update the hint to communicate that no companies match. This keeps the result a valid table and avoids presenting a misleading company row.

## Risks / Trade-offs

- [A broad search term may render many rows at once] -> Company lists are bounded by the loaded portfolio data; keep the existing batch path for the empty query and avoid introducing unnecessary search infrastructure.
- [Adding rank text can reduce available name space] -> Place rank within the existing Holding cell and preserve its width and clipping behavior.
- [Filtering can leave an old intersection sentinel or observer active] -> Disconnect the observer and rebuild the company list on every search input before rendering the filtered rows.
- [Users may expect ticker or ETF searches] -> Label and document the field as company search and scope matching explicitly to company names only.

## Migration Plan

No data migration is required. Add the compact preview input and rendering state, then update focused web contract tests for the new markup and behavior. Verify empty, matching, multiple-match, and no-match queries at desktop and mobile widths. Rollback consists of removing the input, state, filtering branch, and rank markup.

## Open Questions

None. Matching is company-name-only, case-insensitive, trimmed substring search; filtered rows retain their original full-list portfolio ranks.

## 1. Compact Explore Controls

- [x] 1.1 Add an accessible company-name search field to the compact Explore preview near the Top companies heading.
- [x] 1.2 Add dedicated company-search state and wire the input event for live updates without reusing the ETF catalog search state.

## 2. Ranking and Filtering

- [x] 2.1 Add each company's one-based full-list portfolio rank to compact Explore rows while preserving the existing table columns and sticky Holding cell.
- [x] 2.2 Filter `state.companyRanked` by trimmed, case-insensitive substring matching against company names only.
- [x] 2.3 Render all matches for an active search, render no company rows for zero matches, and retain the original full-list rank on filtered rows.
- [x] 2.4 Preserve the existing first-20-plus-infinite-scroll behavior when the company search is empty, including observer cleanup when switching modes.

## 3. Styling and Contract Coverage

- [x] 3.1 Style the company search field and compact-row rank so they remain readable across widescreen and mobile layouts.
- [x] 3.2 Add web contract assertions for the search field, live-input wiring, rank rendering, name-only filtering, and filtered pagination behavior.

## 4. Verification

- [x] 4.1 Run the focused web contract tests and the full available test suite.
- [x] 4.2 Verify empty, whitespace-only, single-match, multiple-match, and no-match searches at desktop and mobile viewport sizes.

## 1. Standard Explore Search Rendering

- [x] 1.1 Update the company search input and clear-button handlers to rerender the active Explore tab in both standard and compact presentation modes.
- [x] 1.2 Apply the trimmed, case-insensitive company-name filter to the complete ranked list in standard Explore mode.
- [x] 1.3 Render every standard-mode match without lazy-loading pagination, render no company rows for zero matches, and preserve each matched company’s original full-list rank.
- [x] 1.4 Preserve the existing standard first-20-plus-infinite-scroll behavior, sentinel creation, and observer cleanup when the search is empty or whitespace-only.

## 2. Contract Coverage

- [x] 2.1 Add web contract assertions covering standard-mode search wiring, name-only filtering, all-match rendering, zero-match rendering, and original-rank preservation.
- [x] 2.2 Add coverage confirming clearing the search restores the standard first-20 list and infinite-scroll path while retaining existing compact-preview assertions.

## 3. Verification

- [x] 3.1 Run the focused web contract tests.
- [x] 3.2 Run the full available test suite and resolve any change-related failures.
- [x] 3.3 Verify standard and compact search behavior for empty, whitespace-only, single-match, multiple-match, and no-match terms at desktop and mobile viewport sizes.

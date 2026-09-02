## 1. Add Catalog Clear Control

- [x] 1.1 Update the ETF catalog search markup with a positioned control wrapper and accessible application-owned `x` clear button.
- [x] 1.2 Extend the existing search-control styling to provide the catalog clear button's reserved input space, 44px hit area, focus/hover states, and hidden state while suppressing duplicate native cancellation UI.

## 2. Wire Catalog Search Behavior

- [x] 2.1 Add catalog clear-button element references and update logic that follows Explore's raw-value visibility behavior, including whitespace-only input.
- [x] 2.2 Wire the clear action to empty the catalog input and `state.searchTerm`, rerender the unfiltered catalog, and restore focus to the catalog input without changing Explore search state.

## 3. Verify Contract

- [x] 3.1 Extend web contract tests for catalog clear-button markup, accessibility, styling, live filtering, whitespace visibility, clearing, and focus behavior.
- [x] 3.2 Run the focused web contract tests and full test suite, then run `git diff --check`.
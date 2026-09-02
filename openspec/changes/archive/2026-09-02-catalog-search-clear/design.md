## Context

The Portfolio tab renders the ETF catalog search as a labeled `type="search"` input and rerenders catalog entries on every input event. The compact Explore company search already wraps its input in a positioned control with an application-owned `x` button, hides that button when the raw input is empty, clears state on activation, rerenders, and restores focus.

The catalog search should gain the same interaction model without coupling its state to Explore's `companySearchTerm`. Catalog filtering already trims and lowercases the search value, so whitespace-only input remains visually clearable while behaving as an empty filter.

## Goals / Non-Goals

**Goals:**

- Give the ETF catalog search an accessible, application-owned clear button.
- Match Explore's raw-value button visibility behavior, including whitespace-only input.
- Restore the unfiltered catalog and focus the catalog input after clearing.
- Keep catalog search state and filtering independent from Explore search state.

**Non-Goals:**

- Change catalog matching fields, ordering, or filtering semantics.
- Change the Explore search control or its requirements.
- Add a dependency or alter backend/catalog data behavior.

## Decisions

- **Reuse the existing explicit clear-control pattern.** Add a catalog-specific control wrapper and clear button using the established icon, hit area, hidden-state, hover, and focus styling. This keeps the two search experiences consistent while allowing separate element references and handlers.
- **Use raw input for button visibility.** The clear button SHALL be visible when `input.value` is non-empty, rather than when the trimmed search term is non-empty. This exactly matches Explore and makes whitespace removable through the application-owned control.
- **Keep catalog state separate.** The catalog handler continues updating `state.searchTerm` and calling `renderCatalog`; the clear handler resets only that state and input, then rerenders and focuses the catalog input.
- **Suppress native cancellation UI for the catalog input.** Apply the existing vendor-specific suppression rule to avoid duplicate controls; the application-owned button remains the cross-browser behavior source.

## Risks / Trade-offs

- [Risk] Reusing the same CSS class names could accidentally couple future layout changes between search controls. -> Mitigation: share only visual control styles and use separate element IDs/state handlers.
- [Risk] The native search cancel affordance differs by browser. -> Mitigation: hide the vendor-native affordance and test the application-owned button contract and keyboard-accessible button behavior.
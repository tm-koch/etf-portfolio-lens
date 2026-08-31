## 1. Search Control Markup

- [x] 1.1 Wrap the compact Explore company search input in a positioned control with an explicit accessible clear button.
- [x] 1.2 Keep the search control hidden outside compact Explore preview mode and preserve the existing company-name-only input semantics.

## 2. Clear Behavior

- [x] 2.1 Toggle clear-button visibility from the current company search value on every input event.
- [x] 2.2 Clear the search value through the button, rerender the unfiltered first 20 ranked rows, restore the infinite-scroll sentinel, and return focus to the input.
- [x] 2.3 Ensure pointer, touch, and screen-reader interaction works without relying on browser-specific search cancel pseudo-elements.

## 3. Compact Row Layout

- [x] 3.1 Make the rank and holding-name wrapper explicitly non-wrapping.
- [x] 3.2 Allow the holding name to shrink into the remaining sticky-cell width while preserving the existing fade, mobile sizing, and hover title.

## 4. Tests and Verification

- [x] 4.1 Add web contract assertions for clear-button markup, visibility wiring, reset behavior, focus handling, and cross-browser-independent styling hooks.
- [x] 4.2 Run the focused web contract tests and full test suite.
- [x] 4.3 Verify desktop and mobile layouts, including Firefox mobile-sized behavior, clear-button visibility, focus retention, restored pagination, and single-line rank/name rendering.

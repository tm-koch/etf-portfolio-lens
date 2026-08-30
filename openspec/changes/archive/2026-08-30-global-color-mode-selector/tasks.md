## 1. Add Global Control Markup

- [x] 1.1 Add one app-level top-right utility area containing the existing color-mode button and menu outside the build-details dialog.
- [x] 1.2 Remove the color-mode setting row from the About this build dialog while retaining build metadata, warnings, and compact Explore settings.

## 2. Preserve and Wire Behavior

- [x] 2.1 Keep the existing color-mode element IDs and update bootstrap references only as needed for the moved markup.
- [x] 2.2 Preserve Bright, Automatic, and Dark menu options, local-storage persistence, Automatic system-preference handling, and comparison-chart refresh behavior.
- [x] 2.3 Verify the selector remains a single control across destination changes and does not duplicate when panels render.

## 3. Responsive and Accessible Presentation

- [x] 3.1 Style the desktop utility area at the top right without changing primary destination order or active-state behavior.
- [x] 3.2 Style the mobile utility area at the top right while keeping the fixed bottom navigation geometry and safe-area behavior unchanged.
- [x] 3.3 Preserve menu-button and menuitemradio semantics, focus behavior, accessible names, and a visible current-mode indication.

## 4. Contract Coverage and Validation

- [x] 4.1 Update web contract tests for global placement, absence from the build dialog, and responsive separation from bottom navigation.
- [x] 4.2 Add or update behavior checks for all three choices, persistence, Automatic system changes, and chart theme refresh.
- [x] 4.3 Run focused web contract tests, the full test suite, and OpenSpec validation; review the final diff for unrelated navigation regressions.

## 5. Refine Utility Placement

- [x] 5.1 Remove the standalone utility-row treatment while keeping one global color-mode control and its existing IDs.
- [x] 5.2 Align the desktop control with the active panel's primary title row and keep it top-right on mobile without affecting bottom navigation geometry.
- [x] 5.3 Update placement contracts and rerun focused and full validation.

## 6. Align With Active Panel Titles

- [x] 6.1 Retarget positioning to the active panel's primary title row across Home, Portfolio, Compare, and Explore.
- [x] 6.2 Add responsive spacing below title rows so the selector and subsequent text do not overlap.
- [x] 6.3 Verify title alignment at desktop and narrow mobile widths and rerun validation.

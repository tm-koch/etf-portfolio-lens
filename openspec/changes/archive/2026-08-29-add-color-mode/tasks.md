## 1. Theme State And Bootstrap

- [x] 1.1 Add the versioned color-mode preference model, validation, localStorage load/save helpers, and Automatic system-preference resolution in `web/app.js`.
- [x] 1.2 Add the synchronous document-head bootstrap that applies the stored or Automatic theme before deferred application code renders.
- [x] 1.3 Add live `prefers-color-scheme` change handling for Automatic mode and ensure explicit modes ignore system changes.

## 2. Color-Mode Control

- [x] 2.1 Add the compact icon control and three labeled Bright, Automatic, and Dark choices to the existing build dialog in `web/index.html`.
- [x] 2.2 Implement keyboard interaction, selected state, accessible naming, tooltip text, and sun/monitor/moon icon updates for the control.
- [x] 2.3 Connect selection changes to theme application, persistence, and effective-theme updates in `web/app.js`.

## 3. Bright And Dark Visual System

- [x] 3.1 Refactor shared colors in `web/styles.css` into semantic theme variables while preserving the existing Bright appearance.
- [x] 3.2 Add Dark values and verify page backgrounds, navigation, panels, cards, dialogs, forms, tables, badges, warnings, empty states, hover states, focus states, and mobile navigation.
- [x] 3.3 Add reduced-motion handling for color-mode control transitions and verify readable contrast at desktop and mobile breakpoints.

## 4. Chart Presentation

- [x] 4.1 Update `web/charts.js` to resolve theme-sensitive border, label, tooltip, and legend presentation colors from the effective theme.
- [x] 4.2 Redraw or update comparison charts when the effective theme changes, including changes caused by Automatic system preference updates.

## 5. Verification And Documentation

- [x] 5.1 Extend `tests/test_web_contract.py` with checks for the three modes, versioned persistence, Automatic fallback, accessible control hooks, and theme coverage.
- [x] 5.2 Run the focused web contract tests and any available frontend validation, then manually verify Bright, Automatic, and Dark behavior with populated charts on desktop and mobile-sized viewports.
- [x] 5.3 Update `web/README.md` with the color-mode behavior and local persistence note if the implemented control needs user-facing documentation.

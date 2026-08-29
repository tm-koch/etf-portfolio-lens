## Context

The web frontend is a static HTML, CSS, and JavaScript application. Its light palette is defined primarily in `web/styles.css`, while `web/app.js` owns UI state and existing versioned `localStorage` settings. Comparison charts are created by `web/charts.js` and currently contain fixed colors for dataset borders and chart-generated visual elements.

The feature must preserve the current bright appearance, add a dark appearance, and let users delegate the choice to their browser or operating system. It must work without a backend or account-level preference and must remain usable on desktop and mobile layouts.

## Goals / Non-Goals

**Goals:**

- Provide explicit `bright`, `automatic`, and `dark` preference states.
- Default missing or invalid preferences to `automatic`.
- Resolve `automatic` through `prefers-color-scheme` and respond to live system preference changes.
- Persist the preference locally and tolerate unavailable or failing browser storage.
- Provide a compact, accessible three-state color-mode control with sun, monitor, and moon icon states.
- Convert all user-facing surfaces and chart presentation colors to theme-aware values.
- Avoid a flash of the wrong theme during initial page load.

**Non-Goals:**

- Synchronizing preferences across devices or users.
- Adding a backend preferences API or user accounts.
- Allowing custom palettes or per-component theme overrides.
- Changing the existing chart data palettes or portfolio calculations.

## Decisions

### Keep preference state separate from effective theme

Store the selected preference as one of `bright`, `automatic`, or `dark`. Resolve it to an effective theme of `bright` or `dark` using `matchMedia('(prefers-color-scheme: dark)')` only when the preference is `automatic`. This keeps the UI selection stable while allowing the automatic result to change.

An HTML attribute such as `data-color-mode` or `data-theme` will be the CSS contract. CSS variables will define shared surfaces, text, borders, shadows, focus colors, and control states, with a dark override on the attribute selector. This is preferred over duplicating every component rule inside a dark-mode block.

### Use the existing build dialog as the settings surface

Place the control with the existing developer settings in the About this build dialog, avoiding a new navigation destination or persistent toolbar element. Use an icon button that opens a small menu or popover containing the three named choices. The icon and accessible label reflect the selected preference: sun for bright, monitor for automatic, and moon for dark. Each choice must be keyboard reachable, have a selected state, and close or update predictably after selection.

### Apply the initial theme before application bootstrap

Add a small synchronous preference bootstrap in the document head, before the stylesheet-dependent application renders. It will read the versioned localStorage key defensively, validate the value, resolve automatic mode from `matchMedia`, and set the HTML theme attribute. The full application state then loads the same preference and takes ownership of subsequent updates.

This avoids a light-to-dark flash caused by waiting for the deferred module to load. If storage or media-query APIs fail, the bootstrap will use automatic semantics and the bright fallback supplied by the document.

### Make charts theme-aware at render time

Expose chart colors from CSS variables or a small theme-color resolver in `web/charts.js`. Use the effective theme for dataset borders, tooltip text/background, and any Chart.js defaults that are otherwise hard-coded. Re-render or update comparison charts after the effective theme changes so hidden and visible chart canvases remain synchronized.

The categorical data palette remains unchanged for identity and comparison consistency. Only neutral presentation colors such as borders, labels, grid-like surfaces, and tooltip styling vary by theme.

### Persist with a versioned localStorage key

Use a dedicated key such as `etf-lens.theme.v1`. Missing, malformed, or unsupported values resolve to `automatic`. Saving is wrapped in the same defensive pattern used by the existing compact Explore setting; a storage failure must not prevent theme switching for the current page.

## Risks / Trade-offs

- [Hard-coded light colors remain in a component] -> Audit `web/styles.css` and replace surface, text, border, focus, and shadow literals with semantic variables; add contract checks for representative dark-mode selectors.
- [Chart canvases retain colors from the previous theme] -> Re-render comparison charts after every effective-theme change and test switching while the Compare tab is active.
- [Storage is unavailable in private or restricted contexts] -> Catch read and write errors and continue with in-memory state and automatic resolution.
- [Automatic mode changes while the app is open] -> Register a `MediaQueryList` change listener only for automatic mode and remove or ignore it when an explicit mode is selected.
- [Theme bootstrap duplicates application logic] -> Keep bootstrap parsing and validation minimal, use the same key and allowed values, and let the application establish the long-lived event listeners.
- [Icon-only control is unclear] -> Provide a tooltip/title, an accessible name, visible selected state, and text labels in the opened menu.

## Migration Plan

No data migration is required. On first load, users without `etf-lens.theme.v1` receive automatic mode. Existing portfolio, active-tab, and compact-preview storage keys remain unchanged. Rollback consists of removing the theme control and theme attribute handling; unknown theme storage values are ignored by design.

## Open Questions

- Whether the three choices should use a native disclosure menu or a custom popover depends on the browser support and interaction pattern chosen during implementation.
- The final dark palette contrast values should be checked visually at desktop and mobile sizes, especially for chart tooltips, warning text, and sticky mobile navigation.

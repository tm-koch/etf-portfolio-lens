## 1. Preview State And Developer Control

- [x] 1.1 Add a versioned localStorage key and loader/saver for the compact Explore preview, defaulting invalid or missing values to disabled.
- [x] 1.2 Add the developer-mode preview switch to the existing build dialog and wire changes to persist the preference and rerender the active Explore presentation.

## 2. Compact Explore Rendering

- [x] 2.1 Add compact Explore markup with a semantic table shell while preserving the existing aggregated view markup and default behavior.
- [x] 2.2 Implement a compact matrix renderer that consumes `aggregateCompanyExposure(...).ranked`, uses `displayWeight` for the total column, and maps `shareOfCompany` into ETF columns in selected-position order.
- [x] 2.3 Render an em dash for missing ETF contributors and preserve the existing empty-state behavior when no holdings are available.
- [x] 2.4 Switch between the existing company list and compact matrix based on the persisted preview state without duplicating aggregation or sorting logic.

## 3. Responsive Presentation

- [x] 3.1 Style the compact matrix as a dense results table with stable holding and numeric column widths.
- [x] 3.2 Add contained horizontal scrolling for wide ETF matrices and verify cells remain readable without overlap on mobile-sized viewports.
- [x] 3.3 Add accessible table headers and labels for ETF tickers and full ETF names.

## 4. Verification

- [x] 4.1 Verify the default Explore tab remains unchanged when the preview preference is disabled.
- [x] 4.2 Verify enabling the switch persists across reloads and displays the compact matrix.
- [x] 4.3 Verify rows are sorted by existing total portfolio exposure and ETF contribution values match the existing company chips.
- [x] 4.4 Verify empty, single-ETF, shared-holding, missing-contributor, and wide-table cases in desktop and mobile-sized browser viewports.

## 5. Follow-up Refinements

- [x] 5.1 Keep the holding-name column sticky while ETF columns scroll horizontally.
- [x] 5.2 Reduce compact table typography and constrain mobile holding names to half the viewport line width with a fade and full-name hover tip.
- [x] 5.3 Replace the developer preview checkbox presentation with an accessible switch control.
- [x] 5.4 Verify the refined table geometry, switch semantics, hover title, and mobile overflow in the browser.
- [x] 5.5 Reduce the mobile holding-name column to 36vw while preserving clipping, fade, and horizontal scrolling.

## 6. Compact Table Loading Refinement

- [x] 6.1 Render only the first 20 compact holdings initially and append additional batches through the existing intersection observer.
- [x] 6.2 Reduce ETF percentage columns to 62px while preserving readable values and horizontal scrolling.
- [x] 6.3 Verify compact rows load dynamically as the user scrolls.

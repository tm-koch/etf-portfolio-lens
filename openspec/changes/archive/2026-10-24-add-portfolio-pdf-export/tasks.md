# Tasks

## 1. Local Export Resources

- [x] 1.1 Vendor a pinned html2pdf.js distribution and required dependencies under `web/vendor`, retain their license notices, and verify the export resources load from same-origin paths without a CDN.
- [x] 1.2 Bundle the website font for local use with its license, add the PDF library, font, and report resources to the service-worker shell and cache-generation checks, and verify `python -m unittest discover -s tests -p 'test_pwa_cache_generation.py'` passes with assertions for the new resources.

## 2. Report Data and Localization

- [x] 2.1 Add a report snapshot builder for current-portfolio and full-catalog scopes that captures portfolio, valuation mode, locale, available prices/snapshots, and build metadata together; verify focused tests prove catalog scope does not broaden analytics inputs.
- [x] 2.2 Derive summary metrics, exposure rollups, scores, ranked Top 20 companies, and one contribution value per current portfolio ETF without relying on rendered Explore rows; verify focused tests cover ranking, missing data, allocation-only output, and both scopes.
- [x] 2.3 Add localized Export controls and report labels using existing locale and number/date/currency formatting; verify the web contract tests cover every supported locale and the exact three section titles.

## 3. Export View and PDF Report

- [x] 3.1 Add the utility-bar export entry and accessible Export view with current-portfolio default, full-catalog selection, allocation-only switch, and generation state; verify web runtime tests cover view opening and confirm portfolio, valuation, and color-mode state are unchanged.
- [x] 3.2 Build the report-only bright DOM with the portfolio list, analytics, Top 20 contribution matrix, sector/region/currency charts, and pairwise heatmap while omitting the pairwise drill-down table; verify focused browser tests cover required content, localization, and allocation-only redaction.
- [x] 3.3 Generate an A4 landscape PDF with readable vertical and horizontal continuation, repeated matrix identity columns, per-page provenance, page numbering, and a clickable product link; verify generated-PDF tests cover multi-page output, all rows/ETF contributions, exact section titles, metadata, and link annotations.
- [x] 3.4 Close the Export dialog automatically after successful PDF generation while leaving it open on failure; verify focused coverage confirms the close occurs only after successful generation.
- [x] 3.5 Initialize report doughnut charts only after their canvases are connected to the visible report layout; verify the report root and chart host are attached before Chart.js construction.
- [x] 3.6 Constrain report doughnuts to compact fixed-size frames and render them without animation so all plots appear within the landscape page.
- [x] 3.7 Reduce the wide Top Holdings company-name column by 40% while preserving readable wrapping.
- [x] 3.8 Add visible bounding boxes around portfolio analytics metrics, scores, and exposure rollups.
- [x] 3.9 Start each numbered report section on a new page while retaining continuation-page behavior.
- [x] 3.10 Keep analytics within page margins and double the Top Holdings company-name column width.
- [x] 3.11 Keep the portfolio table inside the printable width with a visible right boundary.
- [x] 3.12 Keep analytics metric and exposure boxes inset from the right edge of the report section.
- [x] 3.13 Start Top Companies on a fresh page and slightly reduce its table row height.
- [x] 3.14 Enlarge exposure doughnuts and separate them from their legends.
- [x] 3.15 Start pairwise ETF overlap on a fresh page.
- [x] 3.16 Increase doughnut diameter by 40% and provide more legend clearance.
- [x] 3.17 Fit the report canvas to printable A4 width and increase legend clearance to prevent clipping and overlap.
- [x] 3.18 Right-align Top Companies percentage columns and display missing ETF contributions as an em dash.

## 4. Offline and Integrated Verification

- [x] 4.1 Verify an installed PWA can generate the report offline after its shell, catalog, and required snapshots are cached, with no CDN request or portfolio upload; add or update the PWA runtime test for this workflow.
- [x] 4.2 Run the focused PDF, web runtime, web contract, and PWA cache test suites together and verify current-portfolio and full-catalog reports preserve the agreed scope, page, and provenance behavior.

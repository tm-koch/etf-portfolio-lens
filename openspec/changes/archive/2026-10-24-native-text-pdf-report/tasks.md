# Tasks

## 1. Local PDF dependencies and shared assets

- [x] 1.1 Add pinned jsPDF and table-plugin dependencies, create browser-ready local bundles, and provide a PDF-compatible Space Grotesk font with Latin Extended coverage; verify package installation and that each asset loads locally.
- [x] 1.2 Move the bright chart palette to a shared module consumed by both comparison charts and PDF charts; add a focused test proving the two renderers use the same ordered colors.

## 2. Native PDF report layout

- [x] 2.1 Replace the HTML-to-canvas report body with jsPDF-native section headings, labels, metrics, and table content driven by the existing localized snapshot and analytics; verify generated PDF text extraction can select/search/copy representative content in all supported locales.
- [x] 2.2 Implement measured wrapping, table continuation, repeated headers, and the existing horizontal company-matrix panels; verify long portfolio/catalog and company tables continue without clipping or missing rows.
- [x] 2.3 Embed completed Chart.js donut plots as graphics and draw legends as native text using the shared bright palette; verify chart images render and legend labels remain extractable text.
- [x] 2.4 Preserve numbered section page starts and begin Pairwise ETF Overlap plus its heatmap on a fresh page; verify page order and that the heading stays with the first heatmap panel.

## 3. PDF delivery and offline integration

- [x] 3.1 Retain the post-layout provenance footer, page totals, clickable website link, A4 landscape format, and direct dated-file download; verify each generated page has the expected footer text and link annotation.
- [x] 3.2 Update service-worker and cache-generation asset lists for the local PDF dependencies and font, retaining PDF.js import assets; verify export generation succeeds from the installed PWA's cached offline resources.
- [x] 3.3 Update PDF export documentation to describe native selectable text and graphics-only chart plots; verify documented behavior matches the spec and generated PDF.
- [x] 3.4 Run focused PDF, web-contract, and PWA cache tests together; verify the new renderer passes without regressions in export behavior.

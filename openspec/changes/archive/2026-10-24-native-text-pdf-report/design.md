# Design

## Context

See [proposal.md](proposal.md) for motivation and [the spec delta](specs/portfolio-pdf-export/spec.md) for externally visible behavior. The report currently derives localized content from a report model and dedicated renderer, then passes the DOM through html2pdf/html2canvas. That makes the body rasterized; page provenance and the clickable website link are already stamped afterward with jsPDF. The app is static, and the PDF generator and font resources must remain available from the installed PWA's local cache.

## Goals / Non-Goals

**Goals:**
- Keep report calculations, snapshot inputs, localization, and portfolio data boundaries unchanged while replacing only PDF layout and rendering.
- Render text and table content with jsPDF so PDF viewers can select, search, and copy it.
- Preserve page-level metadata, website links, and current page-break semantics.
- Make chart colors a shared source of truth between the website and report.

**Non-Goals:**
- Change the report's scope controls, analytics, valuations, or localized wording.
- Convert donut plot geometry into PDF vector paths; charts may remain embedded graphics.
- Change the report's direct-download interaction or upload portfolio data to a service.

## Decisions

### Use a PDF-native layout with local dependencies

Create the A4 landscape jsPDF document directly and lay out report sections with native text, drawing, and table APIs. Use a pinned local jsPDF dependency and a local table plugin such as jsPDF-AutoTable for row measurement, wrapping, and page continuation; retain project-shipped browser bundles under `web/vendor` rather than introducing a CDN or runtime build dependency. Replace html2pdf's raster-capture path once the native renderer covers the report.

Alternative considered: use browser print-to-PDF. It preserves HTML text with less custom layout code, but makes direct download, page numbering, and footer/link placement browser-dependent. Keeping html2pdf would continue rasterizing the report body.

### Keep report data generation separate from PDF layout

Continue to build one localized snapshot and analytics model from existing application logic. Change the report rendering boundary to consume that model and issue PDF layout operations; do not derive report content from the current screen or from parsed HTML. Use shared layout helpers for text wrapping, available page height, margins, section headings, and table continuation. Emit the Top Companies section on a fresh page and preserve its horizontal contribution panels. Start Pairwise ETF Overlap on a fresh page, keeping the heading with the first heatmap panel; allow long heatmaps to continue on later pages.

Alternative considered: preserve the report DOM as the layout source and extract text into PDF afterward. DOM-to-PDF text matching is brittle when wrapping, table cells, or page breaks differ, so a single PDF-native layout source is more predictable.

### Embed Chart.js plots and render legends as text

Continue using the existing report chart data and Chart.js for donut plots. Render each chart to a local canvas, embed its completed image in the PDF, and draw the corresponding legend labels and swatches with native PDF text and shapes. Move the categorical palette to a shared exported source so regular charts and PDF charts use the same bright-mode values without reading dark-mode CSS tokens.

Alternative considered: draw each donut segment as jsPDF vector paths. That adds chart geometry and multi-ring handling without improving the requested text selection, so plots remain graphics.

### Embed Space Grotesk with required character coverage

Register an embeddable Space Grotesk font with jsPDF, including Latin Extended characters required by supported locales. The web currently packages WOFF2 subsets; provide a PDF-compatible font asset derived from the same family and retain the existing font license. Verify Polish and accented German text by extracting generated PDF text, not only by visual inspection.

Alternative considered: use jsPDF's standard fonts. They do not preserve the website typography or reliably cover all localized characters.

### Stamp page metadata after layout and save directly

After all content pages are created, reuse the existing footer pass for generation/build/snapshot/live-price provenance, page numbering, and clickable website annotation. The final operation saves the finished jsPDF document under the existing dated filename. This keeps totals correct for variable page counts and preserves the direct-download flow.

### Keep all resources offline-capable

Bundle jsPDF, its table plugin, and the embeddable font locally. Update the service-worker shell and cache-generation validation lists together, retaining the separate PDF.js resources used by portfolio import. No network call is added to report generation.

## Risks / Trade-offs

- [Native layout can wrap differently from the current CSS report] -> Define dimensions in PDF units, measure text before placement, and test representative short and long portfolios, catalog listings, and localized strings.
- [Tables or matrices can cross page and width boundaries] -> Use measured row heights, repeat table headers on continuation pages, preserve the existing horizontal contribution panels, and test page edges and missing values.
- [Font conversion or embedding can omit localized glyphs] -> Include Latin Extended coverage, keep the font license, and test text extraction for every supported locale.
- [Replacing html2pdf can accidentally remove offline support] -> Keep local vendor assets in both service-worker and cache-generation manifests and verify the export using the cached offline path.
- [A chart image can be blank or incomplete when embedded] -> Wait for each Chart.js render to complete before adding its canvas image and before saving the PDF.
- [A dependency upgrade can alter layout or bundle behavior] -> Pin dependencies and verify generated PDF text, links, page count, dimensions, and chart rendering in focused tests.

## Migration Plan

1. Add and pin the local jsPDF/table dependencies and make a PDF-compatible Space Grotesk font available with its license.
2. Implement the PDF-native renderer against the existing report snapshot/analytics model and preserve the page footer and save behavior.
3. Share the website chart palette with the report renderer, and replace html2pdf resources in shell/cache lists only after the native path is covered.
4. Validate text extraction, tables, page breaks, footer annotations, charts, and offline export before removing the old raster path and its unused dependency.

Rollback is to restore the html2pdf rendering path and its local cache entries; report data and portfolio state are unaffected by either renderer.

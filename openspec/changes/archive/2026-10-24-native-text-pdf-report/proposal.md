# Proposal

## Why

The current PDF export rasterizes the report body, leaving only the separately stamped footer as selectable text. This makes report titles, figures, and tables difficult to copy, search, and reuse, and the report's donut colors do not match the website's bright-mode palette.

## What Changes

- Render report titles, labels, tables, metrics, legends, and provenance as native selectable PDF text using jsPDF text and table APIs; keep chart plots as graphics.
- Match PDF donut colors to the regular website's bright-mode chart palette.
- Preserve direct PDF download, A4 landscape output, localized content, and the existing numbered footer with provenance and clickable website link.
- Preserve pagination and continuation behavior, including starting Pairwise ETF Overlap and its heatmap on a fresh page.
- Keep generation local and usable in the installed PWA, including offline after required resources and data are cached.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-pdf-export`: Require native selectable text and table content, the website's bright-mode donut palette, direct download with the existing footer, and fresh-page pairwise overlap pagination.

## Impact

- `web/pdf-export.js` and `web/pdf-report-renderer.js`: Replace DOM rasterization with PDF-native layout and table rendering while retaining localized report data and download behavior.
- `web/charts.js` and report chart rendering: Reuse the regular website's bright-mode donut palette; donut plots remain graphics while their legends are text.
- `web/vendor`, `web/sw.js`, and PWA cache validation: Include any PDF-native table dependency and ensure the export remains available offline.
- PDF and web contract/runtime tests: Verify selectable text, chart palette consistency, page breaks, page numbering, footer links, and offline generation.

# Proposal

## Why

Users can inspect fund positions and computed exposure analytics in the app, but cannot carry a consistent, printable report away from the browser. A client-side PDF report will preserve the selected portfolio, its key analytics, data provenance, and exposure visuals in a shareable A4 document without uploading private portfolio data.

## What Changes

- Add an Export view opened by an export icon in the app utility bar, with scope selection for the current portfolio (default) or all ETFs in the catalog, and an allocation-only export switch.
- Generate a bright-mode, currently localized, A4 landscape report using the website font, with the numbered section titles `1 · Portfolio`, `2 · Portfolio Analytics`, and `3 · Exposure Analysis`.
- Include portfolio funds and valuation/allocation details, current-portfolio metrics, the ranked Top 20 underlying-company matrix with one contribution column per ETF in the portfolio, comparison charts, and the pairwise heatmap. Omit the pairwise drill-down table.
- Allow additional continuation pages when report content does not fit legibly; show page numbering separately from section titles.
- Include report generation time, website build identifier, ETF snapshot timestamp, live-price timestamp, and a clickable ETF Portfolio Lens website link.
- Support generation in the installed PWA, including offline use after required app and data resources have been cached.

## Capabilities

### New Capabilities

- `portfolio-pdf-export`: Configure and generate a localized, client-side PDF report for the current portfolio or full ETF catalog, including current-portfolio analytics and provenance.

### Modified Capabilities

None.

## Impact

- `web/index.html`, `web/app.js`, and `web/styles.css`: Export entry point, view, and report presentation.
- `web/vendor`, `web/sw.js`, and `scripts/pwa-cache-generation.ps1`: Locally available PDF generation and font resources, PWA shell caching, and cache-generation validation.
- `web/locales`: Localized Export controls and report labels.
- Existing portfolio, comparison, aggregation, valuation, and build-provenance data paths; focused web, PDF-output, and PWA tests.

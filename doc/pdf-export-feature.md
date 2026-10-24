# PDF Report Export

The browser generates portfolio reports with locally vendored jsPDF and jsPDF-AutoTable. The standalone first page presents the cached PWA launcher icon, the ETF Portfolio Lens title, and generation, build, ETF snapshot, and live-price provenance in a grouped two-column layout without individual boxes. Report headings, metrics, table cells, chart legends, and the footer are embedded as selectable PDF text. Donut plots remain chart images, using the same bright-mode palette as the website.

The report downloads directly as an A4 landscape PDF. The numbered Portfolio section starts after the cover and includes a localized link to the current portfolio, preserving shares-based or relative-allocation sharing. Top Companies pages show `2 · Portfolio Analytics` above a smaller category title; Pairwise ETF Overlap pages show `3 · Exposure Analysis` above a smaller category title, including on continuation pages. Pairwise ETF Overlap starts on a fresh page. Each exposure rollup shows up to 20 named values and groups any remainder into one localized total. Sector, region, and currency charts have thin gray title separators and 10 mm column gutters; the currency legend uses four columns. Every page footer contains only `ETF Portfolio Lens | Generated: <timestamp>`, with a website link over the `ETF Portfolio Lens` label only.

The jsPDF fonts, JavaScript bundles, rendering modules, and launcher icon are served locally and included in the PWA shell cache, so report generation does not require a CDN or an upload. PDF.js remains a separate dependency for importing broker statements.

To verify the export and offline assets, run:

```powershell
python .venv/Scripts/python.exe -m pytest tests/test_web_runtime.py tests/test_web_contract.py tests/test_pwa_cache_generation.py
```

# PDF Report Export

The browser generates portfolio reports with locally vendored jsPDF and jsPDF-AutoTable. Report headings, metrics, table cells, chart legends, and footer metadata are embedded as selectable PDF text. Donut plots remain chart images, using the same bright-mode palette as the website.

The report downloads directly as an A4 landscape PDF. Portfolio, analytics, top-company, exposure, and pairwise-overlap sections retain their numbered headings and page layout; Pairwise ETF Overlap starts on a fresh page. Each page includes the generation time, build and data provenance, page number, and a clickable website link.

The jsPDF fonts, JavaScript bundles, and rendering modules are served locally and included in the PWA shell cache, so report generation does not require a CDN or an upload. PDF.js remains a separate dependency for importing broker statements.

To verify the export and offline assets, run:

```powershell
python .venv/Scripts/python.exe -m pytest tests/test_web_runtime.py tests/test_web_contract.py tests/test_pwa_cache_generation.py
```

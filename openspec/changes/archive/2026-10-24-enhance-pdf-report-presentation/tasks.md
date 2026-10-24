# Tasks

## 1. Report Analytics and Portfolio Link

- [x] 1.1 Fix roll-up aggregation for positions with captured weights and add regression coverage for sector, region, and currency results; verify with `python -m pytest tests/test_web_runtime.py -q`.
- [x] 1.2 Add the localized PDF portfolio link using the existing full/private share semantics, with coverage for both modes, empty portfolios, and the PDF link annotation; verify with `python -m pytest tests/test_web_runtime.py -q`.

## 2. Cover and Provenance Footer

- [x] 2.1 Add the cover with the cached PWA icon and provenance, keep provenance in footers, link the visible `ETF Portfolio Lens` footer label without printing the URL, and count the cover in page totals; verify cover contents, footer text/link, and page numbers in `python -m pytest tests/test_web_runtime.py -q`.
- [x] 2.2 Update `doc/pdf-export-feature.md` to describe the cover and footer presentation; verify the documentation matches the PDF spec and renderer behavior.

## 3. Section Headers and Exposure Accents

- [x] 3.1 Add parent-section headers and subordinate category titles to Top Companies and Pairwise ETF Overlap pages, including continuation pages, and add title-aligned decorative exposure bars with 10 mm column gutters; verify heading hierarchy, bar geometry, and layout boundaries in `python -m pytest tests/test_web_runtime.py tests/test_web_contract.py -q`.
- [x] 3.2 Update `doc/pdf-export-feature.md` to document the category-page hierarchy and decorative chart accents; verify the documented behavior matches the spec and renderer.

## 4. Integrated Export Verification

- [x] 4.1 Run the PDF, web-contract, and PWA-cache suites together and verify the cover icon and generated report remain available through the offline PWA path with `python -m pytest tests/test_web_runtime.py tests/test_web_contract.py tests/test_pwa_cache_generation.py -q`.
- [x] 4.2 Version and cache the updated share module so app initialization populates navigation with cached and fresh assets; verify navigation in the browser and run `python -m pytest tests/test_pwa_cache_generation.py -q`.

## 5. Follow-up Report Layout

- [x] 5.1 Replace the footer with the single generated line and group cover provenance without individual boxes; update focused footer and cover tests.
- [x] 5.2 Limit each exposure rollup to its top 20 labels plus one localized aggregate remainder, with coverage for both capped and uncapped data.
- [x] 5.3 Change chart separators to thin gray rules and render the currency legend in four columns; verify layout with runtime tests.
- [x] 5.4 Update the PDF export documentation and verify the full web runtime, contract, and PWA-cache suites.
- [x] 5.5 Hyperlink only the `ETF Portfolio Lens` footer label to the website while preserving the exact single-line footer text; add a focused PDF link regression.
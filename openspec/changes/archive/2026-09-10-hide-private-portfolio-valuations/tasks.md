## 1. Portfolio Rendering

- [x] 1.1 Update percentage-only position table rendering to omit Price and Value CHF headers and cells, while preserving relative Shares controls and the full-portfolio Weight and Remove columns.
- [x] 1.2 Skip position valuation resolution for percentage-only rows and keep weight calculations based on relative allocation units.
- [x] 1.3 Adjust percentage-mode empty-state table spanning and verify the existing mobile grid remains stable with valuation columns omitted.
- [x] 1.4 Hide the static valuation and Weight headers and omit valuation and Weight cells for percentage-only rows, while retaining Remove controls.
- [x] 1.5 Initialize the portfolio valuation control hidden and reveal it only for full portfolios after state is known.
- [x] 1.6 Restore the Remove header and cell for percentage-only rows while keeping the Weight column hidden.
- [x] 1.7 Add mobile-only top spacing before the positions table so the first ETF row is visually separated from the heading area.
- [x] 1.8 Add a portfolio-level Live/Imported valuation note, remove per-row source suffixes, and animate the live dot slowly.
- [x] 1.9 Align the valuation source note beside the valuation selector on wider layouts with a responsive stacking fallback.
- [x] 1.10 Right-align the valuation source note and center it against the selector control rather than the selector label.
- [x] 1.11 Align the top of the valuation source note with the valuation select box.

## 2. Regression Coverage

- [x] 2.1 Add contract coverage proving the valuation basis control and valuation columns are absent for private percentage-only portfolios.
- [x] 2.2 Add runtime coverage proving relative-unit edits do not invoke valuation resolution and that full portfolios retain valuation behavior.
- [x] 2.3 Run the focused web tests and the complete test suite, then confirm the OpenSpec scenarios are satisfied.
- [x] 2.4 Add regression coverage for the compact private table and initial valuation-control visibility, then rerun the full suite.
- [x] 2.5 Update regression coverage for the restored private Remove control and validate the corrected table contract.
- [x] 2.6 Add contract coverage for the mobile table spacing and rerun the full suite.
- [x] 2.7 Add contract coverage for valuation provenance presentation and validate the full suite.
- [x] 2.8 Add contract coverage for the horizontal valuation-control layout and validate the full suite.
- [x] 2.9 Add contract coverage for right alignment against the selector control and validate the full suite.
- [x] 2.10 Add contract coverage for select-top alignment and validate the full suite.
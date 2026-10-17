# Tasks

## 1. Backend Pairwise Data

- [x] 1.1 Implement pairwise overlap and disclosed-coverage calculation from snapshot holdings; add focused tests for ISIN matching, company-identity fallback, smaller-weight contribution, incomplete coverage, and unavailable comparisons.
- [x] 1.2 Extend catalog generation to publish versioned unordered pair records for the selected successful ETF set; test full and partial selections, registry ordering, and failure-safe catalog replacement.
- [x] 1.3 Document the pairwise catalog fields and refresh behavior; verify the documented full fixture catalog command succeeds and produces pair records for its published ETFs.
- [x] 1.4 Match residual weights by stable company identity when ISINs differ, prevent double counting, and verify the SMI/CSSMI pair against its source snapshots.

## 2. Explore Interface

- [x] 2.1 Add the persisted developer near-identical threshold with a 90% default and validation; test default, valid updates, and rejection of invalid values.
- [x] 2.2 Load and index optional catalog pair data, then render the selected-ETF lower triangle with coverage, unavailable states, and threshold marks; verify selection changes and threshold changes update the matrix.
- [x] 2.3 Add the localized near-identical warning with icon and affected ETF names at the bottom of the redundancy-score box without changing score calculation; verify warning presence and absence at either side of the threshold.
- [x] 2.4 Add bounded two-axis matrix scrolling and sticky header row and first column; verify narrow and wide viewport layouts keep labels readable without page-level horizontal overflow.
- [x] 2.5 Add or update English, German, and Polish strings for the heatmap, coverage, unavailable state, threshold setting, and warning; verify all displayed strings resolve in each supported locale.
- [x] 2.6 Compact the mobile matrix to ticker labels and smaller cells, hide full names and per-cell coverage visually, add a localized color/threshold/coverage legend, and hide scrollbar tracks without disabling scrolling.
- [x] 2.7 Set a uniform height for every heatmap body cell while preserving header sizing; use the same light neutral for column headers and ETF row labels, with diagonal and unused cells slightly lighter.
- [x] 2.8 Align the mobile Rollups, pairwise heatmap, and Top companies card heading inset, top spacing, and title size with the Redundancy score heading.

## 3. Catalog and Integration Verification

- [x] 3.1 Regenerate the checked-in fixture catalog and verify it contains pair data aligned with its ETF entries, with one record per unordered pair.
- [x] 3.2 Run focused backend and web contract/runtime tests, then verify the refreshed heatmap works from the offline web app with both a complete and a partial portfolio selection.

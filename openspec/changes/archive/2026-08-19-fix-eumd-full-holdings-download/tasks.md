## 1. Registry and download resolution

- [x] 1.1 Update the EUMD registry source URL to the direct iShares full holdings CSV export with `fileType=csv`, `fileName=EUMD_holdings`, and `dataType=fund`.
- [x] 1.2 Extend HTML link discovery to recognize `fileType=csv`, `fileType=xls`, and `fileType=xlsx` query parameters and resolve relative links correctly.
- [x] 1.3 Add source-format validation before table parsing so unresolved HTML and incompatible responses fail with explicit errors.

## 2. Complete holdings safeguards

- [x] 2.1 Ensure the live EUMD path uses the existing `ishares_csv_v1` parser and retains every valid holdings row.
- [x] 2.2 Reject top-ten or otherwise incomplete EUMD data before normalization and snapshot generation.
- [x] 2.3 Preserve fixture-mode behavior, including offline use of `data/example/EUMD_holdings.csv`.

## 3. Regression coverage and verification

- [x] 3.1 Add a test for resolving an iShares HTML page to its query-parameter CSV link.
- [x] 3.2 Add a test proving a full EUMD response produces more than ten holdings and does not truncate rows.
- [x] 3.3 Add tests for HTML, top-ten, and malformed-source rejection without creating partial snapshots.
- [x] 3.4 Run focused EUMD tests, the full backend test suite, and `python -m etf_ingestion_backend --isin IE00BF20LF40` against the live endpoint.

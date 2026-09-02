## 1. Registry And Enrichment

- [x] 1.1 Add CSSMI metadata to `data/etf_registry.json` with ISIN `CH0008899764`, ticker `CSSMI`, the verified iShares CSV URL, `ishares_csv_v1`, and `data/example/CSSMI_holdings.csv`.
- [x] 1.2 Add a scoped `LOGN` override for the CSSMI provider name variant and verify it supplies the exact Logitech instrument and canonical company identity.
- [x] 1.3 Update cash and derivative identity handling so `USD CASH`, collateral, foreign-currency cash, and futures rows cannot resolve to unrelated company records through ticker-only matching while remaining in normalized holdings.

## 2. Tests

- [x] 2.1 Add registry metadata assertions for CSSMI and fixture structure assertions for its 25-row iShares export.
- [x] 2.2 Add normalization and strict-mode tests proving all 20 CSSMI equity rows resolve and all CSSMI cash/derivative rows are excluded from company identity requirements.
- [x] 2.3 Add snapshot and catalog assertions for CSSMI identity, holdings count, weight total, canonical identities, and source provenance.
- [x] 2.4 Run the focused ingestion and catalog tests, then run the complete Python test suite and address regressions caused by the shared cash/derivative handling change.

## 3. Generated Outputs

- [x] 3.1 Run fixture ingestion for CSSMI with the repository security master and overrides and verify the dated snapshot contains 25 holdings and weights totaling approximately 99.99%.
- [x] 3.2 Regenerate `web/data/catalog.json` from the successful ingestion result and verify CSSMI references its generated snapshot.
- [x] 3.3 Run OpenSpec validation and repository contract checks, confirming no partial CSSMI snapshot or catalog entry is published on strict validation failure.

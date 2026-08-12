## 1. Backend onboarding

- [x] 1.1 Add the EUMD ETF as a separate registry entry in `data/etf_registry.json` using the existing iShares CSV source metadata.
- [x] 1.2 Add or update the committed fixture for the new source so offline ingestion can reproduce the ETF snapshot.
- [x] 1.3 Extend ingestion tests to cover the new ETF snapshot generation and confirm the new ISIN ingests successfully.

## 2. Publish and verify selection

- [x] 2.1 Regenerate the published snapshot and catalog data so the new ETF appears in `web/data/catalog.json`.
- [x] 2.2 Verify the portfolio tab search can find the new ETF and the user can add it to a saved portfolio.

## 1. Registry And Catalog Metadata

- [x] 1.1 Update the `LU0908500753` registry name to `Amundi Core Stoxx Europe 600 UCITS ETF Acc`.
- [x] 1.2 Replace the legacy Amundi source URL with the current canonical product page URL.
- [x] 1.3 Preserve the registry ISIN, ticker, provider, expected format, parser ID, and fixture path.
- [x] 1.4 Synchronize the matching `web/data/catalog.json` name by ISIN.

## 2. Verification

- [x] 2.1 Validate both JSON files and confirm registry/catalog names match exactly.
- [x] 2.2 Verify historical files under `data/raw/` are unchanged.
- [x] 2.3 Run focused ingestion tests confirming the existing Amundi parser and fixture behavior remain valid.
- [x] 2.4 Confirm the change does not attempt to resolve or hardcode the dynamic Amundi holdings download endpoint.
- [x] 2.5 Create and verify a new fixture-based snapshot for `LU0908500753` using the corrected metadata.

## 1. Registry Integration

- [x] 1.1 Add the UBS SMIM ETF registry entry for ISIN `CH0111762537`, including ticker, name, fund-page URL, `xls` format, `ubs_xml_xls_v1`, and its local fixture path.
- [x] 1.2 Add the UBS SMI ETF registry entry for ISIN `CH1447931341`, including ticker, name, fund-page URL, `xls` format, `ubs_xml_xls_v1`, and its local fixture path.
- [x] 1.3 Confirm both configured fixture paths exist and the registry remains valid JSON.

## 2. Fixture And Parser Validation

- [x] 2.1 Add focused tests asserting the SMIM registry metadata and 30-row fixture shape.
- [x] 2.2 Add focused tests asserting the SMI registry metadata and 20-row fixture shape.
- [x] 2.3 Assert all retained UBS rows have ISIN and numeric weight fields, weights total approximately 100%, and legal footer text is excluded.
- [x] 2.4 Run fixture ingestion for both new ISINs and verify snapshot ETF identity, parser ID, holdings count, and preserved provider source fields.

## 3. Live Source Validation

- [x] 3.1 Run a live smoke check against both UBS product-page URLs and record whether the generic downloader resolves a constituent workbook.
- [x] 3.2 If live pages expose stable workbook links, verify the downloaded files parse through `ubs_xml_xls_v1`; if they remain cookie-gated or dynamic, document the explicit failure and keep the integration fixture-supported.
- [x] 3.3 Verify HTML responses without downloadable links fail before parsing and do not publish partial snapshots.

## 4. Verification And Publication

- [x] 4.1 Run the focused UBS ingestion tests and the complete backend test suite.
- [x] 4.2 Inspect generated snapshots for unresolved or ambiguous holdings and add only verified, narrowly scoped overrides if strict validation requires them.
- [x] 4.3 Regenerate `web/data/catalog.json` through the existing `--update-catalog` workflow when the new ETFs are ready for frontend publication.
- [x] 4.4 Confirm existing UBS entries, historical snapshots, and non-UBS providers remain unchanged.
## 1. Registry and Fixture

- [x] 1.1 Add `CH1553162921` to `data/etf_registry.json` with ticker `SPIEXT`, name `UBS SPI® Extra ETF`, UBS provider metadata, canonical English product URL, `xls` format, `ubs_xml_xls_v1`, and the supplied fixture path.
- [x] 1.2 Confirm the updated fixture is tracked at `data/example/UBSFunds_Constituents_1786975364611.xls` and remains compatible with the existing OOXML workbook detection.

## 2. Backend Verification

- [x] 2.1 Add fixture-based registry and ingestion tests for the new ETF identity and parser selection.
- [x] 2.2 Add assertions that the new fixture produces 179 holdings, preserves valid zero-weight rows, totals within aggregation tolerance, and excludes post-table UBS disclaimer rows.
- [x] 2.3 Run the full backend test suite and confirm all existing ETF sources remain supported.

## 3. Snapshot and Catalog Integration

- [x] 3.1 Run fixture ingestion for the new ETF and verify the snapshot contains the expected identity, parser ID, source metadata, holdings, aggregates, and provenance.
- [x] 3.2 Regenerate `web/data/catalog.json` from the successful registry selection and verify the new entry has ticker `SPIEXT`, canonical name, provider `UBS`, and the dated snapshot path.
- [x] 3.3 Verify catalog failure safety by ensuring an unsuccessful ingestion does not publish a dangling new catalog entry.

## 4. Frontend End-to-End Validation

- [x] 4.1 Load the local web app with the regenerated catalog and confirm UBS SPI® Extra appears in ETF selection/search.
- [x] 4.2 Confirm the existing Portfolio, Compare, and Explore workflows can load and render the new snapshot without ETF-specific frontend code.

## 5. Documentation and Release Checks

- [x] 5.1 Update ingestion or registry documentation if the new registry entry or fixture workflow requires user-facing explanation.
- [x] 5.2 Record that live UBS product-page retrieval continues using the current generic approach and that provider-specific dynamic-page/403 handling remains future work.

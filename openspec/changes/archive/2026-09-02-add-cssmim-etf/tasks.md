## 1. Registry And Fixture

- [x] 1.1 Add CSSMIM metadata to `data/etf_registry.json` with ISIN `CH0019852802`, ticker `CSSMIM`, the verified iShares CSV URL, `ishares_csv_v1`, and `data/example/CSSMIM_holdings.csv`.
- [x] 1.2 Verify the supplied CSSMIM fixture remains present, parses through the existing table parser, contains 34 holdings, and retains provider source fields.

## 2. Tests And Enrichment

- [x] 2.1 Add registry and fixture structure assertions for CSSMIM, including the source URL, parser ID, row count, and `100.0%` weight total.
- [x] 2.2 Add strict CSSMIM ingestion coverage proving all equity rows have exact identity data, existing overrides resolve `HBAN`, `BAER`, `RO`, and `SCHP`, and cash/derivative rows remain excluded from company identity requirements.
- [x] 2.3 Add snapshot and catalog assertions for CSSMIM identity, holdings count, weight total, match statuses, raw source fields, and generated snapshot linkage.
- [x] 2.4 Run focused ingestion/catalog tests and the complete Python test suite; address only regressions caused by this change.

## 3. Generated Outputs And Validation

- [x] 3.1 Run fixture ingestion for CSSMIM with the repository security master and overrides in strict mode, verifying a dated snapshot with 34 holdings and weights totaling `100.0%`.
- [x] 3.2 Regenerate `web/data/catalog.json` from the successful ingestion result and verify CSSMIM references the generated snapshot.
- [x] 3.3 Run OpenSpec validation and repository contract checks, confirming failed strict validation publishes neither a partial CSSMIM snapshot nor a catalog entry.

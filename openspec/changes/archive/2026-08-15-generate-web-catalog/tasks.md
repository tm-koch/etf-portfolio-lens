## 1. Catalog Generation

- [x] 1.1 Add a reusable catalog-generation module that builds the existing manifest schema from successful ingestion results.
- [x] 1.2 Generate `generatedAt`, `basis`, registry-ordered ETF entries, and root-absolute snapshot paths for the selected run.
- [x] 1.3 Write the catalog atomically and preserve the previous catalog when generation or serialization fails.
- [x] 1.4 Add the opt-in `--update-catalog` CLI flag and invoke catalog generation only after successful ingestion.

## 2. Documentation And Tests

- [x] 2.1 Add the combined `python -m etf_ingestion_backend --all --fixtures --update-catalog` command to the root README.
- [x] 2.2 Add tests for full catalog generation, partial selection, registry ordering, and current snapshot references.
- [x] 2.3 Add tests proving ordinary ingestion does not update the catalog and failures preserve the existing catalog.
- [x] 2.4 Run backend tests and verify the generated catalog loads successfully in the web application.

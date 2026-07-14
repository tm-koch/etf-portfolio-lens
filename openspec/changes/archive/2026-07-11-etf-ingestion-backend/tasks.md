## 1. Foundation

- [x] 1.1 Create the Python package structure for registry loading, provider adapters, normalization, enrichment, and snapshot generation.
- [x] 1.2 Define the ETF source registry format and add the five current ETF source entries.
- [x] 1.3 Add shared data models for normalized holdings, ETF snapshots, and provenance metadata.
- [x] 1.4 Define the date-stamped output folder convention under `data/raw/<run-date>/`.

## 2. Source Retrieval and Parsing

- [x] 2.1 Implement the shared fetch layer for remote holdings downloads and local fixture loading.
- [x] 2.2 Implement the SSGA adapter for the SPDR MSCI ACWI holdings source.
- [x] 2.3 Implement the Amundi adapter for the Stoxx Europe 600 holdings source.
- [x] 2.4 Implement the iShares CSV adapter for the EMUM holdings source.
- [x] 2.5 Implement the iShares CSV adapter for the CHSPI holdings source.
- [x] 2.6 Implement the UBS adapter for the SPI Mid holdings source.
- [x] 2.7 Preserve downloaded source files in the date-stamped output folder.

## 3. Normalization and Enrichment

- [x] 3.1 Implement row normalization to the canonical holding schema.
- [x] 3.2 Implement security master lookup against `data/tickers.csv` with ISIN, ticker-plus-exchange, and alias fallback.
- [x] 3.3 Implement missing field enrichment for sector, country, exchange, asset class, and names.
- [x] 3.4 Record raw source fields and enrichment warnings in provenance metadata.
- [x] 3.5 Emit console warnings for holdings that cannot be fully matched or enriched.

## 4. Aggregation and Snapshot Output

- [x] 4.1 Implement sector, region, and currency exposure aggregation from normalized holdings.
- [x] 4.2 Implement top-holdings summarization and count metadata.
- [x] 4.3 Write versioned JSON snapshots per ETF and as-of date into the date-stamped output folder.
- [x] 4.4 Persist or expose source metadata needed for traceability and reprocessing.
- [x] 4.5 Add support for on-demand snapshot generation for one ETF or the full registry.

## 5. Validation and Operability

- [x] 5.1 Add validation for required identifiers, schema completeness, and parser output shape.
- [x] 5.2 Add fixture-based tests for all five ETF sources using the sample files in `data/example/`.
- [x] 5.3 Add a command or entry point to run ingestion for one ETF or the full registry.
- [x] 5.4 Document the snapshot format and registry usage for future ETF additions.
- [x] 5.5 Document the date-stamped output folder and raw download retention behavior.

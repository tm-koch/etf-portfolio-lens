## Why

The website needs a stable backend contract for ETF holdings data before any visualization work can be reliable. The current source files are heterogeneous across providers and formats, so the backend must fetch, normalize, and enrich holdings data into one predictable shape for the frontend and future ETF additions.

## What Changes

- Add a Python backend that retrieves holdings data from multiple ETF providers.
- Support provider-specific source handling for CSV, XLS/XLSX, and landing-page download flows.
- Normalize holdings into a canonical JSON snapshot format for the website.
- Generate snapshots on demand into a date-stamped output folder under `data/raw/<run-date>/`.
- Keep downloaded source files alongside each run for traceability and reprocessing.
- Enrich incomplete source data using the security master in `data/tickers.csv`.
- Generate derived aggregates for holdings comparison, sector breakdown, region breakdown, and currency exposure.
- Introduce a registry for ETF source metadata and parser selection so new ETFs can be added without changing the website contract.
- Preconfigure the five currently supported ETF sources and their download links in the ingestion registry.

## Capabilities

### New Capabilities
- `etf-holdings-ingestion`: Fetch, parse, enrich, and normalize ETF holdings data into structured JSON snapshots with consistent fields and derived aggregates.

### Modified Capabilities
- None.

## Impact

- New Python ingestion code for source adapters, parsers, enrichment, and JSON snapshot generation.
- New structured JSON outputs consumed by the static website.
- New date-based storage layout for generated snapshots and retained raw downloads.
- New dependency usage for spreadsheet and CSV parsing, plus HTTP retrieval and content detection.
- Existing ticker master data becomes the enrichment source for missing sector, country, exchange, and alias resolution.

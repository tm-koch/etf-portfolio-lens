## Why

The security master currently lives in the repository as a bundled `data/tickers.csv` file, which creates an unnecessary redistribution risk and can drift from the latest upstream ticker database. Fetching the latest CSV at ingestion time keeps enrichment data current while removing the need to ship a copy in the repo.

## What Changes

- **BREAKING** Download the latest `tickers.csv` from the upstream source during each ingestion run instead of reading a repo-bundled fallback copy.
- Store the downloaded security master in the run's raw output directory so the exact file used for enrichment is preserved with the snapshot set.
- Load security-master enrichment from the downloaded run-local CSV before any ETF holdings are normalized.
- Remove the repository copy of `data/tickers.csv` from the ingestion contract so the backend no longer depends on a tracked fallback file.
- Keep the published GitHub Pages output unchanged; the download is an ingestion-time concern only.

## Capabilities

### New Capabilities
- `security-master-refresh`: the ingestion system downloads the latest ticker/security-master CSV for each run, persists the file with that run's raw inputs, and uses it as the enrichment source for snapshots.

### Modified Capabilities
- None.

## Impact

- `etf_ingestion_backend/cli.py` and the ingestion pipeline will need to download and stage the CSV before loading the security master.
- `etf_ingestion_backend/security_master.py` will continue to read CSV input, but from a run-local file rather than a repository copy.
- `data/tickers.csv` is no longer part of the runtime contract and can be removed from the repository.
- Snapshot provenance should record the downloaded security-master source and location so generated data stays auditable.
- Tests and fixture generation will need to account for the downloaded security master file.
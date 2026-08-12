## 1. Download and staging

- [x] 1.1 Add a security-master download step that fetches the latest `tickers.csv` before enrichment starts.
- [x] 1.2 Persist the downloaded file in the run's raw output tree and pass that path into security-master loading.
- [x] 1.3 Fail the ingestion run if the upstream security-master download cannot be completed.

## 2. Runtime contract updates

- [x] 2.1 Remove the repository fallback path for `data/tickers.csv` from the CLI and pipeline defaults.
- [x] 2.2 Remove the tracked `data/tickers.csv` file from the repository once the run-local download path is in place.
- [x] 2.3 Update snapshot provenance so the downloaded security-master source remains auditable.

## 3. Verification

- [x] 3.1 Update ingestion tests to load the run-local security-master file instead of the repo copy.
- [x] 3.2 Add a regression test that verifies the ingestion run fails when the security-master download is unavailable.
- [x] 3.3 Validate that published GitHub Pages output still excludes the security-master file while retaining the generated snapshots.
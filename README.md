# ETF Portfolio Lens

This repository now contains a Python backend for retrieving, normalizing, and storing ETF holdings snapshots for ETF Portfolio Lens.

## Ingestion

Use the CLI to generate snapshots on demand:

```bash
python -m etf_ingestion_backend --all --fixtures
```

Holdings identity corrections are maintained in `data/security_overrides.json`.
Use `--overrides <path>` to select another file. Exchange labels are normalized
before matching, and resolved snapshots contain both the exact instrument fields
and a canonical `company_id`/name for aggregation. Add `--strict` to terminate
when any selected holding cannot be resolved to a canonical identity; strict
runs stage output and do not publish partial snapshots.

To regenerate the frontend catalog from the newly generated snapshots, use the
explicit catalog update option:

```bash
python -m etf_ingestion_backend --all --fixtures --update-catalog
```

Without `--update-catalog`, ingestion updates snapshots only and leaves
`web/data/catalog.json` unchanged.

Outputs are written under `data/raw/<run-date>/`:

- `data/raw/<run-date>/downloads/` retains the downloaded or copied source files
- `data/raw/<run-date>/snapshots/` contains the normalized JSON snapshots

## Registry

The source registry lives in `data/etf_registry.json`. Each entry defines:

- ETF ISIN
- ticker and name
- provider
- source URL
- expected source format
- parser identifier
- local fixture path for offline testing

## Snapshot Format

Each snapshot is a JSON document with:

- ETF metadata
- snapshot metadata
- normalized holdings
- sector, region, currency, and top-holdings aggregates
- provenance data including retained raw source fields and warnings

## Notes

- The backend downloads the security master CSV at ingestion time and uses the run-local copy for enrichment.
- Missing matches print warnings to the console and do not stop the ingestion run.
- Overrides are applied before the security master and preserve raw provider values in snapshot provenance.
- `company_id` identifies the canonical company, while ISIN/ticker/exchange identify the exact traded instrument.
- The registry includes UBS SPI® Extra ETF (`CH1553162921`, ticker `SPIEXT`) using the existing UBS holdings parser and fixture workflow.
- UBS live product-page retrieval continues to use the current generic downloader; provider-specific handling for dynamic pages or HTTP 403 responses is deferred.

## Frontend

Run the local web app from the repository root:

```bash
.\.venv\Scripts\python.exe web\server.py
```

Open `http://localhost:8000/web/` in a desktop browser to test the UI. If you need access from another device on the same network, start the server with `--host 0.0.0.0` and use the machine's LAN IP.

## GitHub Pages

For a root-hosted GitHub Pages deployment, publish the site so the frontend files sit at the branch root and the published data remains under `data/raw/`:

```text
/
├─ index.html
├─ styles.css
├─ app.js
├─ data.js
├─ charts.js
├─ package.json
├─ data/
│  ├─ catalog.json
│  └─ raw/
│     └─ <date>/
│        └─ snapshots/
│           ├─ *.json
└─ README.md
```

The frontend loads `data/catalog.json` and the snapshot JSON files under `data/raw/<date>/snapshots/`, so those paths must be preserved when publishing to GitHub Pages.

Use `scripts/publish-gh-pages.ps1` to publish the current working tree to the `gh-pages` branch and push it to the configured GitHub remote.

```powershell
pwsh -NoProfile -File .\scripts\publish-gh-pages.ps1
```

Add `-NoPush` if you want to build and commit the publish tree locally without pushing it yet.

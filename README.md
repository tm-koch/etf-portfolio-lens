# ETF Portfolio Lens

This repository now contains a Python backend for retrieving, normalizing, and storing ETF holdings snapshots for ETF Portfolio Lens.

## Ingestion

Use the CLI to generate snapshots on demand:

```bash
python -m etf_ingestion_backend --all --fixtures
```

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

- The backend uses the security master in `data/tickers.csv` for enrichment.
- Missing matches print warnings to the console and do not stop the ingestion run.

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

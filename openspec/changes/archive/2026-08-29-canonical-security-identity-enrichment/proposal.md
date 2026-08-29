## Why

ETF holdings currently use provider-specific tickers, exchange labels, and names directly. Because tickers are only unique within an exchange and source data can contain missing or incorrect identifiers, the same portfolio can produce order-dependent Explore results or merge unrelated companies.

The ingestion pipeline needs a deterministic, auditable identity-resolution layer that fills incomplete holdings, supports controlled corrections, and prevents unresolved ambiguity from silently entering published snapshots.

## What Changes

- Add a version-controlled override source for correcting missing or contradictory holding identity and enrichment data.
- Normalize exchange labels into stable exchange codes before matching.
- Resolve holdings using override-first precedence, followed by security-master matching by ISIN, ticker plus exchange/country, and holding name.
- Assign a stable `company_id` and canonical company name to every successfully resolved holding, while retaining the exact instrument identity.
- Add strict validation mode that reports unresolved, ambiguous, or incomplete holdings and terminates ingestion without publishing partial results.
- Persist resolved identity, canonical names, match diagnostics, and source provenance in future snapshots.
- Make web company aggregation consume the canonical company identity and use deterministic ordering independent of ETF insertion order.
- Add regression coverage for the ACWD/CHSPI Roper/Roche case and other known cross-company identifier collisions.

## Capabilities

### New Capabilities

- `security-identity-enrichment`: Resolve and enrich ETF holdings through normalized identifiers, override mappings, canonical company identities, and strict validation.

### Modified Capabilities

- `etf-holdings-ingestion`: Extend snapshot contents and ingestion behavior with canonical identities, override precedence, and optional strict failure handling.

## Impact

- Backend matching and normalization in `etf_ingestion_backend/security_master.py` and `normalization.py`.
- Pipeline and CLI configuration for loading overrides and selecting strict mode.
- New version-controlled override data under `data/`.
- Snapshot schema and provenance data.
- Frontend company aggregation in `web/app.js`.
- Ingestion, snapshot, and web contract tests.

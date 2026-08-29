## Why

The CHSPI holdings source reports Richemont as ticker `CFR` on SIX without an ISIN, while the security master contains `CFR` for Cullen/Frost Bankers on NYSE. The resolver rejects the exchange-specific lookup but then accepts the globally unique ticker, silently assigning the wrong company and emitting no warning.

This is a high-impact identity error because it changes company attribution and portfolio exposure while appearing to be a successful match.

## What Changes

- Prevent ticker-only resolution when the holding supplies exchange or country context that conflicts with the candidate record.
- Preserve the holding as unresolved or ambiguous and emit a diagnostic when contextual matching fails instead of guessing from a global ticker match.
- Add a controlled override for the verified Swiss Richemont `CFR` listing, including its authoritative instrument identity and canonical company identity.
- Add regression coverage for CFR/Richemont versus Cullen/Frost and for the resulting warning behavior.
- Regenerate affected snapshots and the web catalog after the correction.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `security-identity-enrichment`: require exchange and country context to constrain ticker matching and prohibit a conflicting global ticker fallback.

## Impact

- `etf_ingestion_backend/security_master.py` matching precedence and diagnostics.
- `data/security_overrides.json` identity correction data.
- Ingestion snapshots under `data/raw/<run-date>/` and `web/data/catalog.json`.
- Backend regression tests and potentially strict-mode validation outcomes for previously misassigned holdings.

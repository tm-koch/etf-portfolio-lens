## Why

The fixture ingestion still reports unresolved or ambiguous company identities after the initial identity-cleanup work. The remaining cases are concentrated in four exact-name collisions and 37 ticker/context conflicts, while the reviewed missing-ISIN mappings now provide enough evidence to complete the supported identity set. Resolving these cases will make canonical aggregation deterministic without discarding provider context or raw audit data.

## What Changes

- Add verified exact-ISIN identity mappings for the externally reviewed missing-ISIN holdings.
- Preserve provider exchange and country as source context when they differ from security-master venue labels.
- Resolve the `QIA` provider rows as Qiagen NV using `NL0015002SN0`, while documenting the Xetra-provider versus LSE-master venue discrepancy.
- Add verified mappings for the four remaining exact-name collisions: `AVIVA PLC`, `TELECOM ITALIA`, `AEROPORTS DE PARIS SA`, and `QIAGEN NV`.
- Resolve or explicitly classify the 37 ticker/context conflicts using exact ISINs rather than ticker-only inference.
- Keep liquidity-fund rows `ICSEAGD` and `ICSSAGD` excluded from company identity aggregation.
- Preserve raw provider fields, match diagnostics, override selector provenance, and venue discrepancies in generated snapshots.
- Regenerate fixtures, catalog data, and focused regression coverage; ensure unresolved identity diagnostics are reduced to only genuinely missing decisions.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `security-identity-enrichment`: require verified exact-ISIN resolution for the reviewed provider identities and preserve provider-versus-master venue provenance.
- `etf-holdings-ingestion`: update identity diagnostics and snapshot expectations for the newly resolved holdings and explicitly excluded liquidity funds.

## Impact

- `data/security_overrides.json` and generated raw snapshots.
- `etf_ingestion_backend/overrides.py`, `security_master.py`, and normalization/provenance behavior.
- Ingestion regression tests, catalog generation, and web match-warning counts.
- No public API break is intended; existing raw source fields and snapshot schemas remain backward-compatible.

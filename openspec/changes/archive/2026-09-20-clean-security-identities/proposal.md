## Why

The fixture ingestion run currently reports 826 identity warnings. The largest group consists of holdings with valid provider ISINs that are absent from the bundled security master, while many other warnings are caused by different provider names for the same ISIN. This makes company aggregation inconsistent and obscures the smaller set of genuinely unresolved securities.

The project already supports exact-ISIN identity overrides, so the immediate opportunity is to use verified canonical names and stable company IDs consistently, with ACWD as the preferred naming source where it provides an unambiguous occurrence.

## What Changes

- Add verified exact-ISIN canonical-name and company-ID overrides for the 202 company-name conflicts that have one unambiguous ACWD name.
- Resolve the 19 same-ISIN naming conflicts without an ACWD occurrence using a documented preferred source and exact-ISIN overrides.
- Add verified identity overrides for actionable missing-ISIN, ticker/context-conflict, and ambiguous holdings where the instrument can be identified reliably.
- Add an ISIN-only normalization outcome for valid source ISINs that are absent from the security master, retaining the source identity without inventing ticker or exchange data.
- Distinguish unresolved company securities from cash, liquidity funds, futures, collateral, and other non-company instruments in diagnostics.
- Preserve raw provider names and fields while exposing one canonical company name and stable company ID for aggregation.
- Add validation and regression tests for canonical naming, company merging, ISIN-only rows, non-company exclusions, and warning counts.

## Capabilities

### New Capabilities

- `security-identity-normalization`: Defines exact-ISIN canonical identity overrides, company-level merging, ISIN-only outcomes, and diagnostic classification for unresolved and non-company holdings.

### Modified Capabilities

- `etf-holdings-ingestion`: Extends controlled identity overrides and enrichment diagnostics to cover the audited cross-provider naming conflicts and valid source ISINs missing from the security master.

## Impact

- `data/security_overrides.json` will gain verified exact-ISIN identity mappings and canonical company IDs.
- `etf_ingestion_backend/normalization.py` and `security_master.py` will gain the ISIN-only and diagnostic behavior.
- Snapshot provenance and warning output will expose the distinction between overridden, ISIN-only, unresolved, ambiguous, and excluded holdings.
- Existing company aggregation and web catalog generation will consume the canonical identity fields without changing the underlying instrument ISINs.
- Fixture snapshots and catalog data will be regenerated after implementation; historical data handling must remain explicit.
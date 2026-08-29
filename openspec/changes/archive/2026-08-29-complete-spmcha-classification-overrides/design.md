## Context

The SPMCHA UBS fixture provides exact ISINs and CHF currency values, but not sector, country, exchange, or asset class. The current security master does not contain the 11 supplied Swiss instruments, so identity-only overrides would resolve strict validation while leaving sector and region aggregates classified as `Unknown`.

## Goals / Non-Goals

**Goals:**

- Add one exact-ISIN override for each affected SPMCHA equity.
- Provide an explicit manual worksheet for `company_id`, `canonical_name`, `sector`, `asset_class`, `country`, and `exchange`.
- Preserve UBS currency and raw source fields.
- Derive `region` from the manually supplied country through the existing mapping.
- Confirm strict ingestion and non-unknown classification aggregates after manual values are entered.

**Non-Goals:**

- Guessing classification values or silently accepting incomplete manual entries.
- Replacing the security-master data source or changing UBS parsing.
- Adding overrides for non-equity metadata rows.

## Decisions

- Match overrides by `isin` only. The UBS rows have no ticker or exchange, while each supplied ISIN is exact and provider-sourced; name-only matching would be less stable.
- Store classification values in the existing `set` object alongside identity fields. This keeps override provenance and normalization behavior consistent with the current override registry.
- Require manual completion before strict validation. Each entry must provide `company_id`, `canonical_name`, `sector`, `asset_class`, `country`, and `exchange`; `region` remains derived rather than duplicated.
- Prefer the existing canonical company IDs and names where already established by CHSPI overrides. Landis + Gyr requires an explicit manual canonical identity decision because it is not represented by the exact Swiss ISIN in the current master.

## Risks / Trade-offs

- [Risk] A manually entered classification may be stale or incorrect. -> Mitigation: preserve the UBS source fields, record override provenance, and require review of the 11-entry worksheet before regeneration.
- [Risk] An incomplete override still leaves an `Unknown` aggregate. -> Mitigation: add strict tests asserting required classification fields and expected sector/region aggregate membership.
- [Risk] An ISIN may be mistyped. -> Mitigation: test every override against the UBS fixture's exact ISIN and assert all 11 rows resolve.

## Migration Plan

1. Fill the manual classification worksheet with verified values.
2. Add the completed ISIN-scoped entries to `data/security_overrides.json`.
3. Run strict SPMCHA ingestion and regenerate its snapshot/catalog only after validation succeeds.
4. Roll back by removing the new entries and restoring the prior generated outputs if validation exposes incorrect classifications.

## Resolved Decisions

- `CH0371153492` uses `company_id` `landis-gyr-group-ag` and display name `Landis+Gyr Group AG`.
- All 11 overrides use the security-master exchange convention `SIX`.
- Country is stored as `Switzerland` so the existing taxonomy derives region `Europe`.

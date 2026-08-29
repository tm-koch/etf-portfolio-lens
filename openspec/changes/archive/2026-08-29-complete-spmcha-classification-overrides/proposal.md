## Why

Strict SPMCHA ingestion now identifies the 11 affected holdings by their exact UBS-provided ISINs, but their classification fields are still missing because those instruments are absent from the current security master. As a result, the positions appear under `Unknown` for sector and region even though their currency is available from the UBS file.

## What Changes

- Add classification override entries for the 11 SPMCHA equity ISINs:
  - `CH0466642201` HELVETIA BALOISE HOLDING AG
  - `CH0102484968` JULIUS BAER GROUP LTD
  - `CH0025751329` LOGITECH INTERNATIONAL-REG
  - `CH0360826991` COMET HOLDING AG-REG
  - `CH0038388911` SULZER AG-REG
  - `CH0025536027` BURCKHARDT COMPRESSION HOLDI
  - `CH0024590272` ALSO HOLDING AG-REG
  - `CH0371153492` LANDIS + GYR GROUP AG
  - `CH0468525222` MEDACTA GROUP SA
  - `CH0406705126` SENSIRION HOLDING AG
  - `CH1484953687` SMG SWISS MARKETPLACE GROUP
- Prepare explicit override fields for manual completion: `company_id`, `canonical_name`, `sector`, `asset_class`, `country`, and `exchange`.
- Derive `region` from the manually supplied country using the existing country-to-region mapping.
- Preserve UBS currency data and existing raw source provenance.
- Validate that strict SPMCHA ingestion succeeds and its sector, region, and currency aggregates no longer classify these equities as unknown.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `etf-holdings-ingestion`: Require complete, manually verified classification overrides for SPMCHA instruments absent from the security master.

## Impact

- `data/security_overrides.json` will gain 11 ISIN-scoped classification entries.
- SPMCHA snapshots and the generated web catalog will be regenerated after strict validation.
- Ingestion normalization will apply override classification fields while retaining source fields and provenance.
- No provider download format or public CLI option changes are expected.

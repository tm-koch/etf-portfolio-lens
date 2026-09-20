## Why

The security master currently supplies the Traditional Chinese legal name `台灣積體電路製造股份有限公司` for TSMC (`TW0002330008`). That value is preserved as the canonical display name and is difficult to read in the application for users expecting the company’s English name. The existing identity-override mechanism can provide a stable English alias while preserving the provider’s raw source data.

## What Changes

- Add an exact-ISIN identity override for `TW0002330008` with the display name `Taiwan Semiconductor Manufacturing Co.`.
- Preserve the original security-master/provider name in snapshot provenance and source fields.
- Regenerate affected current snapshots and catalog data so the alias appears in the published application.
- Add regression coverage proving the override wins over the security-master name and does not affect unrelated securities.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `etf-holdings-ingestion`: Support verified exact-ISIN canonical-name aliases through the existing identity override mechanism.

## Impact

- `data/security_overrides.json` gains one exact-ISIN identity correction.
- Current generated snapshots containing `TW0002330008` and the derived web catalog may be regenerated.
- Ingestion normalization and tests are affected; no frontend rendering API or valuation behavior needs to change because the web already prefers `canonical_name`.

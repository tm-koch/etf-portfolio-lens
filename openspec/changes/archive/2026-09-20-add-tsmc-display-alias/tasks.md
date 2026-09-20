## 1. Identity Override

- [x] 1.1 Add an exact-ISIN `TW0002330008` entry to `data/security_overrides.json` with company ID `taiwan-semiconductor-manufacturing-co` and canonical name `Taiwan Semiconductor Manufacturing Co.`
- [x] 1.2 Verify the override preserves raw holding and security-master provenance while changing only normalized identity fields.

## 2. Regression Coverage

- [x] 2.1 Add a focused ingestion test proving the TSMC override takes precedence over the Chinese security-master name and sets the expected company ID and canonical name.
- [x] 2.2 Add coverage proving an unrelated ISIN does not receive the TSMC alias and existing override behavior remains intact.

## 3. Current Data Regeneration

- [x] 3.1 Regenerate affected current snapshots containing `TW0002330008` through the existing ingestion workflow without rewriting historical snapshots.
- [x] 3.2 Regenerate or validate `web/data/catalog.json` so the published application references the updated current snapshots.

## 4. Verification

- [x] 4.1 Run focused ingestion and web contract tests and confirm the alias is displayed through the existing `canonical_name` path.
- [x] 4.2 Run the full test suite and inspect the diff for unrelated changes.

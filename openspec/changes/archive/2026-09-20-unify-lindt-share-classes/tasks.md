## 1. Identity Override

- [x] 1.1 Add an exact-ISIN override for `CH0010570759` (`LISN`) with the shared Lindt company ID and canonical name.
- [x] 1.2 Add an exact-ISIN override for `CH0010570767` (`LISP`) with the shared Lindt company ID and canonical name.
- [x] 1.3 Verify raw provider names, tickers, ISINs, instrument fields, and override provenance remain preserved.

## 2. Regression Coverage

- [x] 2.1 Add normalization coverage proving `CH0010570759` resolves to the shared Lindt identity.
- [x] 2.2 Add normalization coverage proving `CH0010570767` resolves to the shared Lindt identity.
- [x] 2.3 Add aggregation regression coverage proving both share classes use one `company_id` while remaining separate instruments.
- [x] 2.4 Add unrelated-ISIN isolation coverage so the Lindt mapping cannot apply to other securities.

## 3. Current Data

- [x] 3.1 Regenerate affected current snapshots under `data/raw/2026-09-20/`.
- [x] 3.2 Validate combined Lindt exposure and web catalog references without modifying historical snapshots.

## 4. Verification

- [x] 4.1 Run focused ingestion and web contract tests.
- [x] 4.2 Run the full test suite and inspect the final diff scope.

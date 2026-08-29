## 1. Supply Manual Classification Values

- [x] 1.1 Manually verify and fill `company_id`, `canonical_name`, `sector`, `asset_class`, `country`, and `exchange` for `CH0466642201`, `CH0102484968`, `CH0025751329`, `CH0360826991`, `CH0038388911`, `CH0025536027`, `CH0024590272`, `CH0371153492`, `CH0468525222`, `CH0406705126`, and `CH1484953687`.
- [x] 1.2 Resolve the open canonical identity and exchange-convention decisions, especially for Landis + Gyr (`CH0371153492`).

Manual worksheet fields for each ISIN:

```text
ISIN | UBS name | company_id | canonical_name | sector | asset_class | country | exchange
CH0466642201 | HELVETIA BALOISE HOLDING AG | helvetia-baloise-holding-ag | Helvetia Baloise Holding AG | Financials | Equity | Switzerland | SIX
CH0102484968 | JULIUS BAER GROUP LTD | julius-baer-group-ag | Julius Baer Group AG | Financials | Equity | Switzerland | SIX
CH0025751329 | LOGITECH INTERNATIONAL-REG | logitech-international-sa | Logitech International S.A. | Information Technology | Equity | Switzerland | SIX
CH0360826991 | COMET HOLDING AG-REG | comet-holding-ag | Comet Holding AG | Information Technology | Equity | Switzerland | SIX
CH0038388911 | SULZER AG-REG | sulzer-ag | Sulzer AG | Industrials | Equity | Switzerland | SIX
CH0025536027 | BURCKHARDT COMPRESSION HOLDI | burckhardt-compression-holding-ag | Burckhardt Compression Holding AG | Industrials | Equity | Switzerland | SIX
CH0024590272 | ALSO HOLDING AG-REG | also-holding-ag | ALSO Holding AG | Information Technology | Equity | Switzerland | SIX
CH0371153492 | LANDIS + GYR GROUP AG | landis-gyr-group-ag | Landis+Gyr Group AG | Industrials | Equity | Switzerland | SIX
CH0468525222 | MEDACTA GROUP SA | medacta-group-sa | Medacta Group SA | Health Care | Equity | Switzerland | SIX
CH0406705126 | SENSIRION HOLDING AG | sensirion-holding-ag | Sensirion Holding AG | Information Technology | Equity | Switzerland | SIX
CH1484953687 | SMG SWISS MARKETPLACE GROUP | smg-swiss-marketplace-group-ag | SMG Swiss Marketplace Group AG | Communication Services | Equity | Switzerland | SIX
```

## 2. Implement Classification Overrides

- [x] 2.1 Add one exact-ISIN override per worksheet row to `data/security_overrides.json` with all required completed fields.
- [x] 2.2 Ensure provider currency and raw UBS source fields remain preserved and override provenance identifies the applied selector.
- [x] 2.3 Ensure region is derived from the supplied country without duplicating a manually entered region value.

## 3. Test SPMCHA Classification

- [x] 3.1 Add focused tests for all 11 exact-ISIN overrides and their required identity/classification fields.
- [x] 3.2 Run `python -m etf_ingestion_backend --isin CH0130595124 --fixtures --update-catalog --strict` and confirm no affected equity is unresolved.
- [x] 3.3 Confirm sector and region aggregates contain the supplied classifications rather than `Unknown`, while currency remains `CHF`.
- [x] 3.4 Regenerate snapshots/catalog only after strict validation succeeds and run the full test suite.

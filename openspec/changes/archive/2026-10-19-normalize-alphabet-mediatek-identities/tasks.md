# Tasks

## 1. Add verified identity mappings

- [x] 1.1 Confirm the exact provider ISIN and ticker/name context for Alphabet Class A (`US02079K3059`, `GOOGL`), Alphabet Class C (`US02079K1079`, `GOOG`), and MediaTek (`TW0002454006`, `2454`) from the ACWD provider rows; use no guessed or ticker-only selectors.
- [x] 1.2 Add three exact-ISIN overrides in `data/security_overrides.json`: both Alphabet classes share `company_id: alphabet-inc` and canonical name `Alphabet Inc`, while MediaTek uses `company_id: mediatek-inc` and canonical name `MediaTek Inc.`; verify the registry loads without duplicate selectors.
- [x] 1.3 Add normalization regression tests proving the Alphabet rows share company identity but retain distinct ISINs and tickers, and MediaTek displays `MediaTek Inc.` while retaining the exact raw `Security Name` in `source_fields`; verified with `python -m unittest discover -s tests -p test_ingestion.py` (59 tests passed).

## 2. Verify generated snapshot behavior

- [x] 2.1 Regenerate the current normalized snapshots and catalog for all 12 registry ETFs; verify ACWD and WEBGCHF show the shared Alphabet identity and MediaTek display name, preserve instrument details and provider source fields, retain all 66 catalog pairs, and leave earlier snapshots and downloaded sources unchanged.
- [x] 2.2 Add or extend a pairwise-overlap regression for different Alphabet class ISINs sharing one company identity; verified no double-counting with `python -m unittest discover -s tests -p test_pairwise_overlap.py` (10 tests passed).
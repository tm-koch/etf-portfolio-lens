## 1. Verify Source Identities
- [x] 1.1 Build an auditable verification table for all 35 non-excluded CHSPI equities: ALC, HBAN, DSFIR, BAER, LOGN, SCHP, COTN, SUN, AMS, BCHN, ALSN, MOVE, SENS, AERO, BLKB, COPN, SMG, PLAN, CHAM, MED, IREN, CICN, PMN, ASCN, MEDX, MTG, CNTL, INFRAC, LMN, MCHN, GAM, MMTX, STRN, SPEX, THAG.
- [x] 1.2 Confirm each exact ISIN, exchange instrument, canonical company ID, and canonical name using authoritative references.
- [x] 1.3 Confirm the DSFIR and SCHP instrument identities before implementation.


## 2. Add Scoped Overrides
- [x] 2.1 Add complete, scoped overrides for every verified non-excluded CHSPI equity.
- [x] 2.2 Keep the five requested cash or market-instrument exclusions out of the override document.
- [x] 2.3 Verify override loading, exact-instrument resolution, canonical identity output, and provenance.


## 3. Test Identity Safety
- [x] 3.1 Add focused tests for every CHSPI override selector and expected identity.
- [x] 3.2 Add a regression test for unrelated same-ticker collision rejection.
- [x] 3.3 Add strict-mode tests for exclusions and unresolved equities.


## 4. Validate and Regenerate
- [x] 4.1 Run the exact strict CHSPI fixture command and confirm no non-excluded failures remain.
- [x] 4.2 Regenerate snapshots and catalog only after strict validation succeeds.
- [x] 4.3 Run focused ingestion, contract, and full test suites and review the diff.

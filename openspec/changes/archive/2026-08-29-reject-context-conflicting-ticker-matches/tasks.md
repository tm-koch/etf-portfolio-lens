## 1. Verify Correction Data

- [x] 1.1 Verify the authoritative ISIN for the Swiss SIX `CFR` Richemont listing from a trusted provider source.
- [x] 1.2 Add a narrowly scoped `CFR` + `SIX` + Richemont name override with the verified ISIN and canonical `company_id`/name.
- [x] 1.3 Validate that the override registry accepts the selector and does not overlap with the existing Cullen/Frost identity.

## 2. Harden Ticker Resolution

- [x] 2.1 Change security-master matching so a supplied exchange or country constrains ticker resolution and blocks contradictory global ticker fallback.
- [x] 2.2 Preserve attempted strategies, context mismatch details, and an explicit warning for unresolved or ambiguous context conflicts.
- [x] 2.3 Confirm holdings without exchange and country retain the existing unique-ticker behavior.

## 3. Validate The Pipeline

- [x] 3.1 Add a resolver test proving CHSPI `CFR` on SIX cannot resolve to Cullen/Frost on NYSE.
- [x] 3.2 Add tests proving non-strict mode warns and strict mode rejects the conflict without publishing a partial snapshot.
- [x] 3.3 Add an override test proving the same CHSPI row resolves to Richemont and retains raw provider fields in provenance.
- [x] 3.4 Add a regression test proving a NYSE Cullen/Frost `CFR` row is unaffected by the Richemont override.

## 4. Regenerate And Review Outputs

- [x] 4.1 Regenerate the affected fixture snapshots using the corrected override registry.
- [x] 4.2 Regenerate `web/data/catalog.json` and verify it references the corrected snapshot date.
- [x] 4.3 Inspect CHSPI output and portfolio aggregation to confirm Richemont and Cullen/Frost remain separate canonical companies.
- [x] 4.4 Run the full backend and web contract test suites and review the final diff for unrelated generated files.

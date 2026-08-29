## 1. Identity Data Model

- [x] 1.1 Extend normalized holding and snapshot serialization models with instrument identity, `company_id`, canonical company name, normalized exchange code, and resolution diagnostics.
- [x] 1.2 Define the version-controlled override document schema, validation rules, and initial data location under `data/`.
- [x] 1.3 Add exchange alias normalization with configured aliases for current provider values such as SIX and Nasdaq variants.

## 2. Resolution Engine

- [x] 2.1 Implement override loading and selector indexes for ISIN, ticker plus normalized exchange/country, and holding name.
- [x] 2.2 Implement override-first resolution that applies corrections and fills only remaining fields from the security master.
- [x] 2.3 Update security-master matching to use normalized exchange and country context, preserve ambiguity, and support holding-name matching.
- [x] 2.4 Assign stable canonical company IDs and names to all uniquely resolved holdings without using ticker alone as identity.
- [x] 2.5 Add validation for contradictory overrides, ambiguous matches, unresolved holdings, and missing required identity fields.

## 3. Pipeline and CLI

- [x] 3.1 Add CLI options for the override document path and opt-in strict validation mode.
- [x] 3.2 Integrate resolution into ingestion before aggregation and persist canonical identity plus override/security-master provenance in snapshots.
- [x] 3.3 Ensure strict failures are collected and reported before successful snapshots or catalog updates are published.
- [x] 3.4 Preserve non-strict warning behavior and offline fixture workflows.

## 4. Initial Corrections and Regeneration

- [x] 4.1 Add explicit overrides for ACWD/CHSPI Roche and Roper source conflicts and other verified cross-company identifier collisions.
- [x] 4.2 Regenerate representative fixture snapshots and verify canonical names and company IDs are present.
- [x] 4.3 Verify raw provider values remain available in snapshot provenance and corrected fields are auditable.

## 5. Frontend Aggregation

- [x] 5.1 Update Explore company aggregation to use persisted `company_id` and canonical company name, with a documented legacy fallback for old snapshots if required.
- [x] 5.2 Add deterministic secondary sorting so equal exposures have stable order independent of ETF insertion order.
- [x] 5.3 Verify ETF contribution values, overlap counts, and compact Explore rows remain correct after canonical consolidation.

## 6. Tests and Documentation

- [x] 6.1 Add resolver unit tests for precedence, exchange aliases, unique name matching, ambiguity, and override corrections.
- [x] 6.2 Add pipeline tests for strict failure, no partial publication, default warnings, provenance, and snapshot schema.
- [x] 6.3 Add regression tests asserting ACWD/CHSPI results are identical in either portfolio insertion order and Roche is not renamed to Roper.
- [x] 6.4 Add coverage for the other known cross-company collisions and harmless name/casing variations.
- [x] 6.5 Update README and ingestion documentation with override maintenance, identity semantics, and strict-mode usage.

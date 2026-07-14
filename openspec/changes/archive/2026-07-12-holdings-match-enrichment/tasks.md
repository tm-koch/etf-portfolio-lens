## 1. Matching Model

- [x] 1.1 Add structured match diagnostics to the normalized holding output.
- [x] 1.2 Define a stable list of missing-element labels for unresolved holdings.
- [x] 1.3 Preserve match strategy order in the output provenance.

## 2. Security Master Enrichment

- [x] 2.1 Extend security-master lookup to support unique ticker-only fallback.
- [x] 2.2 Copy the ISIN from the matched security master record when the ticker match is unique.
- [x] 2.3 Detect ambiguous ticker matches and keep them unresolved.

## 3. Warning and Output Behavior

- [x] 3.1 Emit console warnings that include the missing elements for unresolved holdings.
- [x] 3.2 Mark unresolved holdings explicitly in the normalized snapshot output.
- [x] 3.3 Preserve unresolved holdings in the output rather than dropping them.

## 4. Validation

- [x] 4.1 Add fixture-based tests that verify missing-element diagnostics in generated snapshots.
- [x] 4.2 Add tests that verify unique ticker-only matches populate missing ISIN values.
- [x] 4.3 Add tests that verify ambiguous ticker-only matches remain unresolved and warn.

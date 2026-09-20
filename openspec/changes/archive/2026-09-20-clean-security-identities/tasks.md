## 1. Audit And Mapping Data

- [x] 1.1 Generate a reviewed exact-ISIN mapping table for the 202 conflicts with one unambiguous ACWD name.
- [x] 1.2 Resolve and document preferred names for the 19 same-ISIN conflicts without ACWD coverage.
- [ ] 1.3 Verify actionable missing-ISIN, ticker/context-conflict, and ambiguous holdings against issuer or exchange evidence.
- [x] 1.4 Exclude cash, collateral, liquidity-fund, futures, placeholder, and other non-company rows from company mapping tables.

## 2. Override Registry

- [x] 2.1 Add exact-ISIN canonical names and stable company IDs for the reviewed ACWD mappings.
- [x] 2.2 Add exact-ISIN overrides for the reviewed non-ACWD conflicts and verified unresolved holdings.
- [x] 2.3 Validate that mappings preserve instrument ISINs and do not merge distinct share classes or instruments.
- [x] 2.4 Add regression tests for override precedence, provenance, canonical names, and shared company IDs.

## 3. ISIN-Only Normalization

- [x] 3.1 Add an explicit ISIN-only match status for valid source ISINs absent from the security master.
- [x] 3.2 Preserve source name and ISIN while leaving unverified ticker and exchange fields empty.
- [x] 3.3 Ensure complete exact-ISIN overrides upgrade ISIN-only rows to overridden identity without requiring a master record.
- [x] 3.4 Keep ambiguous and genuinely unresolved rows visible in default diagnostics.
- [x] 3.5 Add tests covering missing-master ISINs, invalid or ambiguous identities, and non-company exclusions.

## 4. Diagnostics And Aggregation

- [x] 4.1 Update snapshot diagnostics and warning formatting to distinguish overridden, ISIN-only, ambiguous, unmatched, and excluded holdings.
- [x] 4.2 Verify company-level aggregation uses canonical `company_id` while retaining separate instrument-level ISINs.
- [x] 4.3 Verify the web warning count excludes complete overrides and non-company exclusions but retains genuine incomplete identities.

## 5. Generated Data And Validation

- [x] 5.1 Run fixture ingestion with catalog generation and review semantic snapshot changes separately from timestamp changes.
- [x] 5.2 Confirm the audited canonical-name conflicts collapse to one company identity per mapped ISIN.
- [x] 5.3 Confirm remaining warnings are limited to documented unresolved, ambiguous, or intentionally excluded cases.
- [x] 5.4 Run the focused ingestion and web contract tests.
- [x] 5.5 Run the complete test suite and record the final warning summary.

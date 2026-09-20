## 1. Capture Reviewed Identity Decisions

- [x] 1.1 Add exact-ISIN overrides for the reviewed missing-ISIN identities listed in the security review report.
- [x] 1.2 Add the `QIA` mapping to Qiagen NV with ISIN `NL0015002SN0`, preserving Deutsche Börse Xetra / Germany provider context and documenting the LSE security-master label.
- [x] 1.3 Add explicit non-company exclusions for `ICSEAGD` and `ICSSAGD`.
- [x] 1.4 Add verified exact-ISIN mappings for the four name-only collisions and the reviewed ticker/context conflicts, or leave each unsupported row explicitly diagnosed.

## 2. Implement Provenance and Normalization Behavior

- [x] 2.1 Ensure context-scoped overrides are rechecked after an override supplies an ISIN and exact-ISIN precedence is preserved.
- [x] 2.2 Preserve provider exchange, country, raw source fields, and any security-master venue discrepancy in snapshot provenance.
- [x] 2.3 Ensure excluded liquidity-fund rows remain representable without company IDs or fabricated equity identities.

## 3. Add Regression Coverage

- [x] 3.1 Add focused tests for each reviewed missing-ISIN mapping pattern, including share classes and special instruments.
- [x] 3.2 Add tests proving `QIA` resolves to Qiagen and retains the Xetra provider context plus LSE master-label discrepancy.
- [x] 3.3 Add tests for explicit liquidity-fund exclusions and unresolved ticker/context diagnostics.

## 4. Regenerate and Validate Outputs

- [x] 4.1 Run fixture ingestion and regenerate normalized snapshots and the web catalog.
- [x] 4.2 Verify expected match-status counts, canonical identities, exclusions, raw-field retention, and residual diagnostics.
- [x] 4.3 Run focused identity tests and the complete test suite.
- [x] 4.4 Review generated diffs and publish only the intended report, overrides, snapshots, catalog, and OpenSpec artifacts.

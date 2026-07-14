## 1. Normalization Fallback

- [x] 1.1 Add a source-name fallback path for unresolved holdings in the normalization flow.
- [x] 1.2 Keep the canonical security-master name unchanged when a holding matches successfully.
- [x] 1.3 Preserve unresolved status, warnings, and match diagnostics when the fallback name is used.

## 2. Verification

- [x] 2.1 Add or update fixture-based tests for unresolved holdings that should retain a source name.
- [x] 2.2 Add or update tests proving matched holdings still use canonical names.
- [x] 2.3 Run the full ingestion test suite and confirm the new fallback does not change existing match behavior.

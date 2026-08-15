## 1. Amundi Request Discovery

- [x] 1.1 Capture the exact product API request and response used by the full-fund holdings control, distinguishing it from the top-ten breakdown.
- [x] 1.2 Record the required country, language, investor-profile, product, and request context needed to reproduce the full composition.
- [x] 1.3 Capture a representative complete XLSX response and known top-ten/invalid responses for validation testing.

## 2. Fetcher Architecture

- [x] 2.1 Add an optional registry `fetcher_id` and explicit Amundi context fields without changing existing parser IDs.
- [x] 2.2 Add provider-specific fetcher dispatch while preserving the generic static URL fetcher and fixture mode.
- [x] 2.3 Implement the Amundi full-holdings resolver using the captured product API contract and return the actual API location for provenance.
- [x] 2.4 Validate content type/shape and reject HTML, empty, or non-JSON responses before normalization.

## 3. Workbook And Parser Validation

- [x] 3.1 Validate the attached complete XLSX fixture and API composition structure with required identity/weight fields.
- [x] 3.2 Reject top-ten-only or otherwise incomplete composition results without writing a partial snapshot.
- [x] 3.3 Confirm fractional weight semantics and retain `amundi_landing_xlsx_v1` when totals and normalized values are valid.
- [x] 3.4 Preserve canonical `source_url` and actual resolved API response location in generated snapshot metadata.

## 4. Tests And Verification

- [x] 4.1 Add deterministic resolver and workbook/API fixtures for complete, top-ten, HTML, malformed, and changed-weight cases.
- [x] 4.2 Add focused backend tests covering context, dispatch, validation failures, parser compatibility, and fixture mode.
- [x] 4.3 Run the full backend test suite and a live Amundi API smoke test.
- [x] 4.4 Verify existing providers and historical snapshots are unaffected.

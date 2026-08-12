## 1. Normalization

- [x] 1.1 Add a shared sector alias mapping in the backend so all currently observed sector variants normalize to GIC-style names.
- [x] 1.2 Apply the normalization step to both source-row sector parsing and security-master fallback enrichment.
- [x] 1.3 Preserve the original source sector text in provenance or source fields.

## 2. Validation

- [x] 2.1 Add regression tests covering `Communication` → `Communication Services`.
- [x] 2.2 Add coverage for at least one localized sector label and one additional sector alias to verify the mapping scales beyond a single string replacement.
- [x] 2.3 Verify sector aggregates and snapshot output use the normalized sector labels without affecting region or currency summaries.
## 1. Correct Warning Classification

- [x] 1.1 Update the frontend warning predicate to count only `ambiguous` and `unmatched` holding statuses.
- [x] 1.2 Preserve the existing warning text, per-ETF aggregation, provenance details, and visualization data paths.

## 2. Add Regression Coverage

- [x] 2.1 Add a web contract regression test proving `overridden` holdings are excluded from incomplete-match warnings.
- [x] 2.2 Add or update fixture-level coverage proving genuine `ambiguous` and `unmatched` holdings remain reported.

## 3. Validate and Publish

- [x] 3.1 Run the focused web and ingestion tests and confirm the CHSPI warning count reflects only genuinely incomplete holdings.
- [x] 3.2 Review the diff and update generated or documented outputs only if required by the implementation.

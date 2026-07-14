## 1. Aggregate Calculation

- [x] 1.1 Update the aggregate calculation flow so sector, region, and currency weights are derived from the finalized holdings collection.
- [x] 1.2 Ensure aggregate computation uses the same holding values that are written to the snapshot after enrichment and fallback handling.
- [x] 1.3 Keep the snapshot schema and aggregate field names unchanged.

## 2. Verification

- [x] 2.1 Add or update regression tests to confirm aggregate summaries reflect the final normalized holdings output.
- [x] 2.2 Add or update snapshot-based tests to prove missing-field enrichment does not leave aggregates stale.
- [x] 2.3 Run the ingestion test suite and confirm the regenerated snapshots still pass.

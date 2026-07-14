## Context

The ingestion pipeline already normalizes holdings, enriches missing security data, and then computes aggregates for sector, region, currency, and top holdings. The issue is that aggregate output needs to be guaranteed to reflect the final normalized holdings state, including any fallback or enrichment applied during normalization.

## Goals / Non-Goals

**Goals:**
- Ensure aggregate weights are derived from the final holding records after normalization and enrichment.
- Keep aggregate categories aligned with the fields written into the snapshot.
- Preserve the existing snapshot shape and downstream consumers.

**Non-Goals:**
- Changing the snapshot schema.
- Adding new aggregate categories.
- Altering normalization or matching behavior beyond using the finalized holdings as aggregate input.

## Decisions

- Compute aggregates from the in-memory list of finalized holdings immediately before snapshot serialization.
  - Rationale: this guarantees the aggregate view matches the exact holdings that will be written.
  - Alternative considered: recompute during parsing or normalization. Rejected because the final data needed for aggregation may be filled in later.

- Keep aggregate generation centralized in the existing aggregation step rather than duplicating category calculations in normalization.
  - Rationale: aggregate logic remains in one place and stays easier to test.
  - Alternative considered: distribute aggregate updates across normalization and enrichment. Rejected because it would make the data flow harder to reason about.

- Derive sector, region, and currency weights from the same finalized holdings collection.
  - Rationale: all three summary views should use a single authoritative source of truth.
  - Alternative considered: compute each summary from separate intermediate structures. Rejected because it risks divergence.

## Risks / Trade-offs

- Finalized holdings with missing weights may still produce zero or partial aggregate totals if the source data does not supply all exposure values → Keep existing missing-value handling and verify with regression tests.
- Changing the aggregate input boundary could affect downstream expectations for unresolved holdings → Lock behavior with snapshot-based tests.

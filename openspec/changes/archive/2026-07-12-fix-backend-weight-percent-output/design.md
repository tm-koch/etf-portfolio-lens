## Context

The ingestion pipeline currently parses provider source weights as fractions and writes them into the canonical snapshot as `weight_pct` without converting the unit. The website and other consumers read those fields as percentages, which creates a contract mismatch and can lead to 100x display errors.

The change is limited to the backend snapshot contract, but it affects every consumer of the published JSON snapshots.

## Goals / Non-Goals

**Goals:**
- Emit `weight_pct` values in holdings and aggregate summaries as percentage numbers in the 0-100 range.
- Keep the snapshot schema shape stable so consumers continue to read the same field names.
- Preserve existing enrichment, matching, and aggregation behavior aside from the unit conversion.
- Make the generated snapshots self-consistent so the backend output can be consumed directly without additional interpretation.

**Non-Goals:**
- Renaming snapshot fields.
- Changing the meaning of any non-weight exposure fields.
- Reworking the UI presentation beyond what is required to consume the corrected snapshot values.

## Decisions

- Convert provider weights to percentages in the normalization layer before they are stored on `NormalizedHolding`.
  - Rationale: the field name already implies percent semantics, and converting at the boundary ensures all downstream code works with a single unit.
  - Alternatives considered:
    - Convert only in aggregation output. Rejected because holdings would still expose fraction values and the snapshot contract would remain inconsistent.
    - Leave backend fractions and convert in the UI. Rejected because the published JSON would remain misleading and other consumers would still be wrong.

- Keep aggregate generation using the same unit as holdings.
  - Rationale: sector, region, currency, and top-holdings summaries should be derived from the same canonical unit that appears in the holdings array.
  - Alternatives considered:
    - Store fractions internally and convert only at serialization. Rejected because it increases the chance of mixed-unit bugs across the codebase.

- Treat the contract change as breaking for downstream consumers.
  - Rationale: existing snapshots and any code that assumed `weight_pct` was a fraction will need to adjust its expectations.

## Risks / Trade-offs

- Downstream consumers may still assume `weight_pct` is a fraction. → Mitigation: update the snapshot contract documentation and regenerate sample snapshots.
- Any latent code that divides by 100 again will understate exposures. → Mitigation: run focused validation against the MEUD snapshot and inspect a few representative aggregates.
- Historical snapshots will remain on the old unit convention unless regenerated. → Mitigation: document the cutoff and only apply the new unit contract to newly generated snapshots unless a backfill is explicitly requested.

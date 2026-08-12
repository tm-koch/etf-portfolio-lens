## Context

The backend currently accepts sector text from ETF source files and from `data/tickers.csv` enrichment with minimal interpretation. That keeps the pipeline simple, but it also means equivalent business sectors can appear under source-specific labels or localized sector names. The comparison charts and sector aggregates already rely on the normalized holdings produced by the backend, so the best place to standardize sector names is before aggregation and snapshot serialization.

## Goals / Non-Goals

**Goals:**
- Normalize sector labels to a GIC-style taxonomy in the backend for the full observed sector vocabulary.
- Make `Communication` resolve to `Communication Services`.
- Normalize other common aliases and localized labels to the same canonical GIC buckets.
- Keep the raw source sector text available in provenance for auditability.
- Ensure sector rollups and downstream UI outputs read the normalized sector names.

**Non-Goals:**
- Rewrite existing snapshot schema fields beyond sector normalization.
- Change region or currency inference behavior.
- Introduce a new external taxonomy service or dependency.

## Decisions

- Add a shared sector normalization mapping in the ingestion layer.
  - Rationale: one canonical mapping keeps source parsers and security-master enrichment aligned and makes it possible to cover the full current sector vocabulary in one place.
  - Alternatives considered: embedding ad hoc replacements in each parser or in the frontend. Rejected because it would fragment the taxonomy and make maintenance harder.

- Apply normalization before aggregation and snapshot serialization.
  - Rationale: downstream consumers should see one canonical sector label, and aggregates should not need to reconcile multiple names.
  - Alternatives considered: normalizing only in the UI or only in aggregate generation. Rejected because snapshots would still contain inconsistent sector text.

- Preserve raw sector text in provenance rather than overwriting it.
  - Rationale: users can still inspect the original source label while the normalized field drives analysis.
  - Alternatives considered: mutating the source field in place. Rejected because it would remove traceability.

- Keep a small, explicit fallback for anything outside the GIC vocabulary.
  - Rationale: some rows are not business sectors at all, such as cash, derivatives, or placeholders, and they should not be forced into the canonical taxonomy.
  - Alternatives considered: coercing every label into a sector bucket. Rejected because it would create misleading classifications.

## Risks / Trade-offs

- Alias coverage gaps → Mitigation: keep the mapping table centralized and add regression tests for new aliases as they appear.
- Non-sector labels such as cash or placeholders → Mitigation: leave them in a clear fallback bucket instead of forcing them into a business sector.
- Inconsistent expectations for existing snapshots → Mitigation: treat normalization as a backend contract change and regenerate snapshots when needed.
- Over-normalization of uncommon sector labels → Mitigation: only translate known aliases and leave unknown sectors unchanged.

## Migration Plan

1. Introduce the sector alias mapping and normalize sectors during ingestion.
2. Update regression tests for the canonical GIC name(s), especially `Communication Services`, and at least one localized alias.
3. Regenerate any affected snapshots if a stable published catalog is required.
4. Verify sector rollups and comparison charts render the normalized labels without changing region or currency behavior.

Rollback is straightforward: remove the alias mapping and revert the backend normalization step, then regenerate snapshots if necessary.

## Open Questions

The current data set already reveals a finite alias list, so the main open question is whether we want to treat any additional non-sector rows as `Unknown`, `Other`, or another explicit fallback bucket.
## Context

The backend already preserves unresolved holdings and emits match diagnostics when security-master enrichment fails. In those cases, `security.name` can remain `null` even though the source provider often supplies a readable label in the raw row. This change improves the usability of unresolved holdings in the JSON snapshot without changing matching behavior.

## Goals / Non-Goals

**Goals:**
- Preserve a source-provided name for holdings that remain unresolved after enrichment.
- Keep canonical security-master names unchanged for matched holdings.
- Preserve existing unresolved status, warnings, and match diagnostics.

**Non-Goals:**
- Do not alter match ordering or add new matching heuristics.
- Do not treat the fallback name as a successful enrichment result.
- Do not introduce a new external data source or dependency.

## Decisions

1. Use the source row label only as a fallback for unresolved holdings.
   - Rationale: the source label is useful for human review, but it should not override a canonical security-master record.
   - Alternative considered: always copy the source label into `security.name`. Rejected because it would overwrite canonical names on matched holdings and make the snapshot less reliable.

2. Derive the fallback from the provider row already stored in provenance.
   - Rationale: the ingestion pipeline already captures raw source fields, so no new input data is needed.
   - Alternative considered: add a dedicated source-name field to the output model. Rejected because the current JSON shape already has a single `security.name` field and the fallback is only needed for unresolved records.

3. Preserve unresolved diagnostics exactly as they are.
   - Rationale: the fallback name is a presentation aid, not a change in enrichment status.
   - Alternative considered: mark fallback-named holdings as partially resolved. Rejected because it would complicate downstream logic and weaken the meaning of unresolved warnings.

## Risks / Trade-offs

- [Raw source labels may be inconsistent or long] → Limit the fallback to unresolved holdings and keep the raw label in provenance for traceability.
- [Downstream consumers may assume non-null name means canonical enrichment] → Keep the unresolved status and diagnostics intact so consumers can distinguish fallback naming from a real match.
- [Some rows may still have no usable label] → Leave `security.name` null when the source provides nothing appropriate.

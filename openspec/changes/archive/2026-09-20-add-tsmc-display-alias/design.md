## Context

The ingestion pipeline matches holdings against the downloaded ticker security master by ISIN and copies the matched master name into `canonical_name`. The current master record for `TW0002330008` uses the Traditional Chinese legal name `台灣積體電路製造股份有限公司`. The web already displays `canonical_name` before the raw security name, and the pipeline already supports verified identity overrides in `data/security_overrides.json`.

The change is therefore a data-quality correction at the existing enrichment boundary, not a frontend localization feature. The raw provider and security-master values must remain available for auditability.

## Goals / Non-Goals

**Goals:**

- Display TSMC as `Taiwan Semiconductor Manufacturing Co.` in current generated holdings snapshots.
- Match the correction by exact ISIN `TW0002330008` so other tickers or similarly named companies are unaffected.
- Preserve the original Chinese security-master/provider values in snapshot provenance.
- Keep aggregation identity stable with an explicit company ID.
- Regenerate the current snapshots that contain the instrument and verify the web catalog continues pointing to valid data.

**Non-Goals:**

- Do not modify the downloaded security master or its source data.
- Do not add frontend-specific name mapping or alter the valuation pipeline.
- Do not rewrite historical snapshots unless a separate data-history migration is requested.
- Do not translate other Taiwanese company names as part of this change.

## Decisions

1. **Use the existing exact-ISIN override mechanism.** Add one entry to `data/security_overrides.json` matching `TW0002330008`. This is preferable to a frontend mapping because snapshots, aggregation, and all consumers receive the same canonical identity.

2. **Set both `company_id` and `canonical_name`.** Use a stable slug such as `taiwan-semiconductor-manufacturing-co` and the requested display name. This avoids deriving an identity from the provider’s Chinese name and keeps aggregation independent of the security-master naming language.

3. **Keep source fields untouched.** The override changes normalized identity fields only. The raw holding row and security-master provenance remain available so the correction is explainable and reversible.

4. **Regenerate current derived data only.** Re-run fixture ingestion for the current data date and update the catalog. Historical snapshots remain immutable; rollback is removing the override and regenerating a future snapshot.

5. **Test through normalization and generated snapshot contracts.** Add a unit test proving an exact-ISIN override wins over a conflicting security-master name, plus an ingestion assertion for the affected current snapshots and a non-match assertion for an unrelated ISIN.

## Risks / Trade-offs

- [Risk] A future provider or security-master record could use a different ISIN for the same company. → Mitigation: scope this correction explicitly to the verified instrument `TW0002330008`; add another override only after verification.
- [Risk] Existing historical snapshots retain the Chinese name. → Mitigation: document historical immutability and verify the current catalog points to regenerated snapshots.
- [Risk] Changing `company_id` could affect aggregate grouping between old and new snapshots. → Mitigation: use a stable company slug and validate current aggregate/company output in tests.

## Migration Plan

1. Add the exact-ISIN override and focused tests.
2. Regenerate affected current snapshots and `web/data/catalog.json` through the existing ingestion workflow.
3. Run the focused ingestion and web contract tests, then the full suite.
4. If rollback is needed, remove the override and regenerate a new current snapshot; do not mutate historical snapshot files.

## Open Questions

None. The requested display name and affected instrument ISIN are confirmed.

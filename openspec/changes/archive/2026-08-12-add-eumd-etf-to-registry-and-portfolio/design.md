## Context

The backend already supports registry-driven ingestion, snapshot generation, and fixture-based offline runs. The web app does not read the registry directly; it loads the published catalog from `web/data/catalog.json`, and the portfolio tab uses that catalog as the source of truth for searchable, addable ETFs.

## Goals / Non-Goals

**Goals:**
- Add the iShares EUMD ETF as a separate supported registry entry.
- Reuse the existing iShares CSV ingestion path and generate a snapshot for the new ETF.
- Publish the new ETF into the catalog so it is selectable in the portfolio UI.
- Preserve the behavior and availability of the existing ETF entries.

**Non-Goals:**
- Introduce a new parser for iShares CSV sources.
- Change portfolio weighting logic, comparison charts, or aggregated exposure calculations.
- Add live pricing or valuation for ETF shares.

## Decisions

- Reuse the existing `ishares_csv_v1` parser.
  - The linked source uses the same holdings CSV shape as the existing iShares sources, so a new parser would add maintenance cost without new capability.
  - Alternative considered: create a dedicated EUMD parser. Rejected because it would duplicate behavior already covered by the shared CSV parser.

- Treat the catalog as the frontend contract, not the registry.
  - The web app already loads `web/data/catalog.json`, so the new ETF should become selectable by regenerating published data rather than by hardcoding a UI exception.
  - Alternative considered: add a static frontend whitelist for EUMD. Rejected because it would create a second source of truth and make future onboarding harder.

- Add fixture coverage for the new ETF source.
  - The backend tests and offline ingestion path are fixture-driven, so a committed fixture keeps the change reproducible.
  - Alternative considered: rely only on live fetching. Rejected because it would make the new registry entry harder to validate in CI and locally.

## Risks / Trade-offs

- Fixture or source drift → Refresh the committed fixture and regenerated snapshot together when the upstream iShares download changes.
- Catalog refresh omissions → Validate that the regenerated catalog includes the new ISIN before treating the change as complete.
- Upstream layout changes in the iShares CSV → Keep the source URL and parser choice aligned with the existing iShares CSV handling so any future parser adjustment is shared.

## Migration Plan

1. Add the new registry entry and its local fixture path.
2. Run backend ingestion to generate the new snapshot under `data/raw/<date>/snapshots/`.
3. Regenerate `web/data/catalog.json` so the portfolio selector sees the new ETF.
4. Verify the frontend can search for and add the new ETF without any manual wiring.

Rollback is straightforward: remove the registry entry, regenerate the catalog, and republish the static data. Existing ETFs remain unchanged.

## Open Questions

None.

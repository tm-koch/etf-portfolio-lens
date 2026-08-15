## Context

The ingestion pipeline writes snapshots under `data/raw/<date>/snapshots/`, while the frontend reads the separately maintained `web/data/catalog.json`. The catalog contains a generated date, weighting basis, and one entry per published ETF with a snapshot path. There is currently no backend command that refreshes this projection after ingestion.

The requested workflow is an explicit combined command such as `python -m etf_ingestion_backend --all --fixtures --update-catalog`. Catalog generation must use the same run's successful results and must not silently publish stale or missing snapshot references.

## Goals / Non-Goals

**Goals:**

- Add an opt-in `--update-catalog` flag to the existing CLI.
- Generate the catalog from successful ingestion results for the current run date.
- Preserve the current frontend catalog schema and root-absolute snapshot paths.
- Preserve registry ordering and include only successfully generated snapshots.
- Write the catalog atomically after all selected ingestion work succeeds.
- Document the combined command in the root README.

**Non-Goals:**

- Change the frontend catalog schema or runtime loader.
- Update the catalog during ordinary ingestion without the flag.
- Scan arbitrary historical dates by default.
- Rewrite or delete historical snapshots.
- Add a separate publishing/deployment command.

## Decisions

### Generate from pipeline results

The catalog generator should receive the `IngestionResult` objects returned by the current pipeline, or an equivalent validated result list, instead of rediscovering files by globbing. This ties catalog entries to snapshots that succeeded in the same command and avoids accidentally selecting stale files from another run.

### Preserve the existing catalog contract

Write the current fields: `generatedAt` as the run date, `basis` as `share_weighted`, and ETF entries containing ISIN, ticker, name, provider, and `/data/raw/<date>/snapshots/<isin>.json` snapshot paths. Keep registry order so the catalog remains stable and predictable.

### Make catalog replacement atomic

Serialize the complete manifest, write it to a temporary file beside `web/data/catalog.json`, then replace the target only after serialization succeeds. If ingestion or generation fails, leave the previous catalog untouched.

### Keep the flag opt-in

The default CLI behavior remains snapshot-only. `--update-catalog` explicitly requests mutation of the frontend asset. This prevents library, test, and routine ingestion calls from unexpectedly changing web data.

An alternative is a separate `catalog` subcommand, but the requested combined command is more discoverable for the common “ingest then publish current data” workflow. The generation logic should still live in a reusable module so a future standalone command can call it.

## Risks / Trade-offs

- [A partial selected run could produce a catalog missing other ETFs] -> Define catalog scope from the selected registry entries and successful results, and document that `--all` is required for a complete catalog.
- [A failed ingestion could leave stale catalog data] -> Perform catalog replacement only after all selected ingestion results and manifest validation succeed.
- [Absolute snapshot paths can break under a repository-subpath deployment] -> Preserve the existing root-hosted path contract and README deployment guidance.
- [Manual catalog edits can be overwritten] -> Make the opt-in flag explicit and treat the catalog as generated output.

## Migration Plan

1. Add a reusable catalog generator module.
2. Add `--update-catalog` to the CLI and invoke it after successful ingestion.
3. Add unit tests for manifest content, ordering, partial selection, and atomic failure behavior.
4. Document the command in the root README.
5. Run the command once to refresh the checked-in catalog for the latest snapshot set.

Rollback removes the flag integration and catalog generator; existing catalog files and snapshots remain valid.

## Open Questions

No product questions remain. The explicit combined command is `python -m etf_ingestion_backend --all --fixtures --update-catalog`.

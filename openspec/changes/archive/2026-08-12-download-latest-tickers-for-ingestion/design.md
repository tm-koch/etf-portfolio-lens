## Context

The ingestion backend currently loads the security master from the tracked repository file `data/tickers.csv` before processing ETF holdings. That makes enrichment deterministic for local development, but it also ties the runtime to a bundled file that the repository no longer needs to ship if the latest upstream CSV can be fetched per run.

The existing pipeline already separates source-file retrieval from normalization, and it writes downloaded ETF inputs into `data/raw/<date>/downloads/`. That is the natural place to stage the security master as well, so the exact file used for enrichment is preserved alongside the snapshot set.

## Goals / Non-Goals

**Goals:**
- Download the latest security-master CSV once for every ingestion run.
- Store the downloaded file in the run's raw output tree and use that file for security-master enrichment.
- Remove the repository copy of `data/tickers.csv` from the runtime path so snapshots do not depend on a bundled fallback.
- Preserve provenance for the downloaded file so generated snapshots remain auditable.

**Non-Goals:**
- Change the ETF holdings parsing or sector normalization logic.
- Introduce a new security-master data model or database.
- Change GitHub Pages runtime behavior.

## Decisions

- Download the security master before constructing the `SecurityMaster` object.
  - Rationale: the ingestion run should use a single, run-local source of truth for every holding match.
  - Alternatives considered: downloading lazily during matching or per ETF. Rejected because it would complicate provenance and could produce inconsistent enrichment within one run.

- Persist the downloaded CSV under the date-stamped raw output tree.
  - Rationale: the raw directory already captures the input files that produced each snapshot, so the security master belongs there too.
  - Alternatives considered: storing it in a separate cache directory or leaving it in the repository root. Rejected because those locations would not travel naturally with the generated snapshots.

- Remove the repository fallback copy entirely.
  - Rationale: the user explicitly wants to avoid keeping a tracked copy for copyright reasons, and falling back to a repo file would preserve the undesirable dependency.
  - Alternatives considered: keeping the repo file as an offline fallback. Rejected by requirement.

- Treat download failure as a hard ingestion failure.
  - Rationale: if the system cannot fetch the security master, it should not silently produce snapshots from stale or bundled data.
  - Alternatives considered: reusing a prior local copy or continuing with partial enrichment. Rejected because it would defeat the freshness guarantee and the removal of the fallback copy.

## Risks / Trade-offs

- Upstream availability → Mitigation: fail fast with a clear error so the user knows the security master could not be refreshed.
- Reproducibility drift over time → Mitigation: record the downloaded file path and source metadata in snapshot provenance.
- Larger raw output trees → Mitigation: the CSV is small relative to the ETF download artifacts, and the per-run copy is intentional for auditability.
- Local offline development becomes less convenient → Mitigation: document that the run now depends on the upstream CSV or an explicit override path.

## Migration Plan

1. Add a download-and-stage step for the security master before enrichment starts.
2. Update the CLI and tests to load the run-local CSV instead of a tracked repository file.
3. Remove the repository `data/tickers.csv` file after the new path is verified.
4. Regenerate snapshots so the new provenance references the downloaded security master.

Rollback is straightforward: restore the repository file and switch the CLI back to a local fallback path if the upstream source becomes unavailable, but that would reintroduce the tracked dependency this change removes.

## Open Questions

Whether the downloaded security master should keep the exact upstream filename or a normalized run-local name is an implementation detail; the design assumes the run-local raw tree will keep the file easy to identify.
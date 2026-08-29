## Context

Snapshots distinguish normal security-master matches (`matched`), successful controlled overrides (`overridden`), ambiguous matches, and unmatched holdings. The website's company-exposure warning summary currently treats every status other than `matched` as incomplete, so valid override resolutions are presented as warnings.

## Goals / Non-Goals

**Goals:**

- Make the warning summary reflect only holdings whose identity remains incomplete or ambiguous.
- Preserve visibility of genuine `ambiguous` and `unmatched` holdings.
- Keep override provenance and all existing visualization data unchanged.
- Add a focused regression assertion for the warning classification.

**Non-Goals:**

- Changing ingestion status values or snapshot serialization.
- Removing incomplete holdings from sector, region, currency, or company visualizations.
- Re-enriching the five intentional CHSPI cash/derivative exclusions.

## Decisions

- Define warning statuses explicitly as `ambiguous` and `unmatched`, rather than using a negated equality check. This makes successful `overridden` records non-warning by construction and keeps future statuses from being silently classified as failures.
- Keep the existing warning message format and per-ETF count so the user-facing change is limited to accuracy.
- Test the frontend contract at the source level, consistent with the repository's existing web contract tests, and include a fixture-level status-count check where practical.

## Risks / Trade-offs

- [Risk] A newly introduced incomplete status could be omitted from warnings. -> Mitigation: keep the status predicate centralized and document the recognized incomplete statuses in the delta spec and test.
- [Risk] Users may interpret the remaining warnings as data loss. -> Mitigation: retain the existing detailed provenance and visualization behavior; only successful overrides disappear from the warning count.

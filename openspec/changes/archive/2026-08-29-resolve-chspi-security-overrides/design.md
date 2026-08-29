## Context

The CHSPI fixture contains 39 non-cash equity rows that fail strict identity enrichment. Most failures are caused by a stale or incomplete security master: the same ticker can identify an unrelated instrument on another venue, while several Swiss listings are absent entirely. The pipeline already supports version-controlled complete overrides and provenance, so the change should be data-led and preserve the existing normalization contract.

The source rows are the authority for the selector context: provider ticker, provider name, `SIX Swiss Exchange`, source country, and (for the DSM-Firmenich row) the provider country value. The target identity must be independently verified before it is written. The requested `WISS MKT IX SEP 26` is treated as the apparent typo `SWISS MKT IX SEP 26`; it is an excluded cash-like market instrument, not a company security.

## Goals / Non-Goals

**Goals:**


**Non-Goals:**


## Decisions

1. **Use complete scoped overrides as the resolution mechanism.** Existing override support can resolve an instrument missing from the security master and records provenance. A code-path exception would duplicate identity rules and make future updates harder to audit. Every entry must include the source selector and complete target identity.

2. **Require authoritative identity verification before data entry.** SIX share-detail or IPO pages, issuer investor-relations pages, and equivalent primary instrument references are acceptable. Search snippets or an unrelated same-ticker security-master record are not sufficient. `DSFIR` uses `CH1216478797` for the SIX listing, and Schindler participation shares use `CH0024638196`, subject to final review against the exact source row.

3. **Prefer exact security identity over company-only identity.** Where a company has multiple listed instruments, the override must identify the exact holding represented by the source row, including participation or registered-share distinctions. Canonical company identity may be shared only after the exact instrument ISIN is established.

4. **Keep exclusions out of the override document.** Cash and collateral rows do not represent companies and should continue to be handled by existing unresolved/non-equity behavior. Adding placeholder ISINs would make the catalog less truthful.

5. **Regenerate outputs only after strict validation.** Run the focused CHSPI strict command first, then regenerate snapshots/catalog using the repository's normal workflow. If verification is incomplete, leave the corresponding row unresolved and do not publish a partial catalog.

## Risks / Trade-offs


## Migration Plan

1. Build a verification table for all 39 non-excluded rows from the CHSPI fixture.
2. Add only verified complete entries to `data/security_overrides.json`, with selectors matching the raw source context.
3. Add or update focused unit and contract tests for override resolution, collision rejection, exclusions, and provenance.
4. Run strict CHSPI fixture ingestion and inspect the resulting snapshot warnings.
5. Regenerate affected snapshots and catalog only after strict validation passes.
6. Roll back by removing the new override entries and generated outputs if an identity review finds a mismatch; no schema migration is required.

## Open Questions

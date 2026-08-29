## Context

The ingestion resolver receives holdings with mixed identifier quality. CHSPI supplies Richemont as ticker `CFR` on `SIX Swiss Exchange` without an ISIN, while the downloaded security master contains `CFR` for Cullen/Frost Bankers on `NYSE`. The current matcher correctly fails the contextual `ticker+exchange` lookup but then accepts the only global ticker result. Because a record is returned, normalization marks the holding as matched and emits no warning.

The security master also contains an OTC Richemont record under `CFRUY`, not the Swiss `CFR` listing. The correction therefore needs both a conservative matcher rule and a version-controlled override for the verified Swiss instrument.

## Goals / Non-Goals

**Goals:**

- Treat explicit exchange or country context as a constraint on ticker matching.
- Preserve a diagnostic when contextual matching cannot uniquely resolve a holding.
- Resolve the CHSPI Richemont listing through a specific override with an authoritative ISIN and canonical company identity.
- Ensure strict mode rejects the unresolved case if the override is absent or invalid.
- Add regression coverage and regenerate affected snapshots and catalog data.

**Non-Goals:**

- Treating every ticker mismatch as proof of a new company without authoritative data.
- Replacing the downloaded security master.
- Inferring Richemont’s instrument ISIN from the ticker or from the unrelated OTC listing.
- Changing portfolio exposure calculations or frontend aggregation rules.

## Decisions

### Context-constrained ticker fallback

When a holding has an exchange or country, the resolver will accept a ticker match only if the candidate satisfies that context. A globally unique ticker may be used only when no exchange and no country context is present. If context is present but no candidate matches it, matching continues through name and alias strategies; otherwise the result is unresolved or ambiguous with a warning.

This prevents a unique but contradictory ticker from silently overriding stronger source context. An alternative is to keep the current fallback and add warnings after matching, but that would leave the wrong canonical identity in the snapshot and could still corrupt aggregation.

### Explicit Richemont override

Add a selector covering the source ticker `CFR`, normalized exchange `SIX`, and holding name `COMPAGNIE FINANCIERE RICHEMONT SA`. The `set` values will use an authoritative Swiss-listing ISIN, `company_id` for Richemont, and its canonical name. The exact ISIN must be verified from a trusted provider source before implementation.

A ticker-only override is rejected because it could also match Cullen/Frost. An override keyed only by the OTC Richemont ISIN is insufficient because CHSPI does not provide an ISIN.

### Diagnostics and validation

Return `unmatched` or `ambiguous` when contextual identity cannot be resolved, preserving attempted strategies and missing fields. Emit the existing warning in non-strict mode. Strict mode will then fail before publishing snapshots, as it does for other unresolved identities.

### Regression data

Add a focused resolver test with a `CFR`/SIX holding and a Cullen/Frost/NYSE security-master record. Add an override-backed test for Richemont resolution and a snapshot assertion that the raw source name remains auditable. Regenerate CHSPI and any portfolio fixtures that include Richemont after the override is verified.

## Risks / Trade-offs

- [Risk] Some valid providers omit exchange or country. -> Retain the global unique-ticker fallback only when both contextual fields are absent.
- [Risk] A provider may use a non-equivalent exchange label. -> Reuse the existing exchange alias normalization and retain the raw label in provenance.
- [Risk] The authoritative Richemont ISIN may be confused with an OTC or alternate share class. -> Require verification from the provider or an authoritative listing source and test the exact instrument identity.
- [Risk] More holdings may become unresolved after the safety change. -> Preserve diagnostics and use targeted overrides rather than broad ticker rules.

## Migration Plan

1. Verify the Swiss Richemont `CFR` listing’s authoritative ISIN and add the scoped override.
2. Change ticker matching so contextual conflicts cannot fall through to global ticker-only matching.
3. Add resolver, warning, strict-mode, and snapshot regression tests.
4. Regenerate CHSPI snapshots and the web catalog for the current run date.
5. Review other newly unresolved holdings before enabling strict publishing.

## Open Questions

- Which authoritative source should be recorded or linked in the override maintenance documentation for the Swiss Richemont ISIN?
- Should a context conflict be classified as `ambiguous` rather than `unmatched` when the security master has a unique contradictory ticker record?
- Are there other provider rows where a valid local ticker differs from the global security-master ticker because the primary listing is absent?

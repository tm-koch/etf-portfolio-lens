# Spec Delta

## ADDED Requirements

### Requirement: Enrich holdings with verified country identifiers
Security identity enrichment SHALL populate a normalized ISO 3166-1 alpha-2 country identifier from an exact security-master match or verified override when available, without inferring a country from ticker alone.

#### Scenario: Exact identity provides a country identifier
- **WHEN** a holding resolves to a security-master record with a valid country identifier
- **THEN** enrichment assigns that identifier while preserving provider country and venue provenance

#### Scenario: Verified override provides a country identifier
- **WHEN** a holding matches a verified override with a valid country identifier
- **THEN** enrichment uses the override identifier and records the existing override provenance

#### Scenario: Country identity is ambiguous
- **WHEN** no exact identity or verified override establishes the holding's country
- **THEN** enrichment leaves the normalized country identifier unavailable and retains diagnostics rather than guessing

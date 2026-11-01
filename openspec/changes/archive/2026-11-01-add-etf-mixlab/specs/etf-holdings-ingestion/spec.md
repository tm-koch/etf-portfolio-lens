# Spec Delta

## ADDED Requirements

### Requirement: Persist normalized country identifiers for holdings
Newly generated holding snapshots SHALL include a normalized ISO 3166-1 alpha-2 country identifier when it is available from the source, verified override, or security master, while retaining the source country label.

#### Scenario: Country identifier is available
- **WHEN** a holding's country is known and maps to a valid ISO 3166-1 alpha-2 identifier
- **THEN** the snapshot stores that identifier and retains the original country label

#### Scenario: Country identifier is unavailable
- **WHEN** a holding's country is absent, ambiguous, or cannot be mapped confidently
- **THEN** the snapshot leaves the normalized identifier unavailable and preserves available source data and diagnostics

#### Scenario: Historical snapshots remain unchanged
- **WHEN** the country-identifier field is added to future snapshots
- **THEN** existing files under `data/raw/` are not rewritten by the change

# Spec Delta

## ADDED Requirements

### Requirement: Publish optimizer metadata in the web catalog
Generated catalog entries SHALL publish each ETF's validated TER, distribution policy, and explicit investment-universe classifications when those values are present in the registry.

#### Scenario: Catalog publishes MixLab metadata
- **WHEN** a registry ETF with valid optimizer metadata has a successful snapshot
- **THEN** its generated catalog entry exposes the TER, distribution policy, and investment-universe classifications alongside its existing identity and snapshot path

#### Scenario: Catalog does not invent missing metadata
- **WHEN** a registry ETF lacks optional optimizer metadata
- **THEN** catalog generation preserves the missing value as unavailable and does not infer a value from the ETF name or ticker

#### Scenario: Existing catalog consumers remain compatible
- **WHEN** the generated catalog includes optimizer metadata
- **THEN** existing catalog identity, snapshot, and pairwise-overlap fields retain their current meaning and schema compatibility

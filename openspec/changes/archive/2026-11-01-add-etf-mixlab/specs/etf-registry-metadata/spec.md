# Spec Delta

## ADDED Requirements

### Requirement: Store ETF cost and distribution metadata
The ETF registry SHALL provide a non-negative TER value and an explicit accumulating or distributing policy for each ETF eligible for MixLab. Missing or invalid values SHALL prevent an ETF from being ranked by cost or distribution policy.

#### Scenario: Registry contains valid optimizer metadata
- **WHEN** a MixLab-eligible registry entry is loaded
- **THEN** it provides a TER value in a documented unit and a supported distribution policy

#### Scenario: Registry metadata is missing or invalid
- **WHEN** a registry entry lacks a valid TER or distribution policy
- **THEN** it is excluded from cost-ranked or distribution-filtered MixLab candidates and the omission is diagnosable

### Requirement: Classify eligible fund sleeves explicitly
The ETF registry SHALL identify each MixLab-eligible product's investment universe using explicit, validated classifications that distinguish developed World, all-country World, emerging markets, Europe, and Switzerland where applicable.

#### Scenario: Product has an explicit sleeve classification
- **WHEN** a registry entry is eligible for a custom fund-sleeve mode
- **THEN** its sleeve classification is available without inferring it from its ticker or display name

#### Scenario: Product universe is unknown
- **WHEN** a registry entry has no verified sleeve classification
- **THEN** it is unavailable in custom sleeve matching and remains identifiable in catalog data

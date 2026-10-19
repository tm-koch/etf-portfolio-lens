# Spec Delta

## MODIFIED Requirements

### Requirement: Configure the pairwise holdings display maximum
Developer settings SHALL provide a persisted maximum number of companies for the pairwise holdings drill-down, defaulting to 10, and accept only finite positive integers.

#### Scenario: No valid setting has been saved
- **WHEN** the pairwise holdings drill-down is initialized without a valid saved maximum
- **THEN** its maximum displayed company count SHALL be 10

#### Scenario: A valid maximum is configured
- **WHEN** the developer enters a finite positive integer maximum
- **THEN** the setting SHALL be persisted and applied to the pairwise holdings drill-down

#### Scenario: An invalid maximum is entered
- **WHEN** the developer enters a non-finite, non-integer, zero, or negative maximum
- **THEN** the invalid value SHALL NOT be applied or persisted, and the last valid maximum or default SHALL remain active
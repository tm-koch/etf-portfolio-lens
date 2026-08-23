## ADDED Requirements

### Requirement: Compact Explore preview styling
The compact Explore preview SHALL apply the requested light palette to its existing semantic holdings matrix without changing the matrix data, ordering, loading behavior, or responsive interaction model.

#### Scenario: Preview uses the styled matrix
- **WHEN** compact Explore preview mode is enabled
- **THEN** the existing holdings matrix is rendered with the specified header and alternating body-row colors

#### Scenario: Preview data behavior is unchanged
- **WHEN** the styled compact matrix renders or appends holdings
- **THEN** it preserves the existing ranked rows, ETF contribution values, incremental loading, and empty-state behavior

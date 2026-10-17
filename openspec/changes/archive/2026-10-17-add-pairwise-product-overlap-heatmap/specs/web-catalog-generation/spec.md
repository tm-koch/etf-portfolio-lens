# Spec Delta

## ADDED Requirements

### Requirement: Publish pairwise overlap with the generated catalog
When `--update-catalog` is requested, the generated catalog SHALL include offline pairwise overlap results and holdings coverage derived from the same successful snapshot set as its ETF entries.

#### Scenario: Full catalog update publishes pair data
- **WHEN** a full catalog refresh successfully generates snapshots for its selected ETFs
- **THEN** the catalog SHALL contain one pairwise result for each unordered pair of published ETFs, aligned with the same run date and ETF set

#### Scenario: Partial catalog update publishes only selected pair data
- **WHEN** a catalog refresh selects a subset of registry entries
- **THEN** the catalog pairwise data SHALL cover only the ETF entries published by that run and SHALL NOT imply comparisons to unselected ETFs

#### Scenario: Catalog pair data cannot be generated
- **WHEN** pairwise data generation fails before the catalog is complete
- **THEN** the CLI SHALL report failure and preserve the previous catalog unchanged

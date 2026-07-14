## ADDED Requirements

### Requirement: Aggregated holdings load in batches
The aggregated tab SHALL display the top 20 holdings by default and SHALL progressively append remaining holdings as the user scrolls downward.

#### Scenario: Initial aggregated render
- **WHEN** the aggregated tab is opened
- **THEN** the tab SHALL render the top 20 holdings first
- **AND** it SHALL leave remaining holdings undisplayed until the user scrolls further down

#### Scenario: Scroll reveals more holdings
- **WHEN** the user scrolls downward and reaches the list continuation point
- **THEN** the next batch of remaining holdings SHALL be appended in ranked order
- **AND** the existing rendered holdings SHALL remain in place

#### Scenario: End of list is reached
- **WHEN** all holdings have been appended
- **THEN** the aggregated tab SHALL stop requesting additional holdings
- **AND** the full ranked list SHALL be visible

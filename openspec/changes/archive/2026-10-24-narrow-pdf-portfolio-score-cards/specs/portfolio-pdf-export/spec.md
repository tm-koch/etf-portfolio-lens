# Spec Delta

## ADDED Requirements

### Requirement: Keep portfolio score cards to one column wide
The PDF SHALL render each portfolio score card at the width of one column in the three-column exposure-rollup group, with the two cards side by side and aligned to the first two rollup columns.

#### Scenario: Portfolio score cards use one-column width
- **WHEN** the Portfolio Analytics score section is rendered
- **THEN** each score card is as wide as one exposure-rollup card
- **AND** the redundancy and diversification cards remain side by side in the first two columns
- **AND** the existing score values, verdicts, and order remain unchanged

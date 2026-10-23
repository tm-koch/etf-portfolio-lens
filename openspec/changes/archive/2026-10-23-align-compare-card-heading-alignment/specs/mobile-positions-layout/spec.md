# Spec Delta

## ADDED Requirements

### Requirement: Selected positions heading aligns with the Redundancy score title
At all supported viewport widths, the Selected positions heading SHALL use the same top inset from its card edge as the Redundancy score title in Explore.

#### Scenario: Compact Selected positions heading shares the reference inset
- **WHEN** the Portfolio and Explore panels are viewed at a viewport width of 760px or less
- **THEN** the Selected positions heading begins at the same vertical inset from its card top edge as the Redundancy score title

#### Scenario: Wider Selected positions heading shares the reference inset
- **WHEN** the Portfolio and Explore panels are viewed at a viewport width greater than 760px
- **THEN** the Selected positions heading begins at the same vertical inset from its card top edge as the Redundancy score title
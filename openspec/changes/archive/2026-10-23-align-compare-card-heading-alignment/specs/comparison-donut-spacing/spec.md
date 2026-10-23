# Spec Delta

## ADDED Requirements

### Requirement: Comparison and Rollups headings align with the Redundancy score title
At all supported viewport widths, titles in the Compare metric cards and the Rollups section heading SHALL use the same top inset from their card edge as the Redundancy score title in the Explore panel.

#### Scenario: Compact headings share one inset
- **WHEN** the Compare and Explore panels are viewed at a viewport width of 760px or less
- **THEN** each Compare metric-card title and the Rollups section heading begin at the same vertical inset from their card top edges as the Redundancy score title

#### Scenario: Wider headings share one inset
- **WHEN** the Compare and Explore panels are viewed at a viewport width greater than 760px
- **THEN** each Compare metric-card title and the Rollups section heading begin at the same vertical inset from their card top edges as the Redundancy score title

#### Scenario: All comparison metric titles share one inset
- **WHEN** the sector, region, and currency cards are rendered in the Compare panel at any supported viewport width
- **THEN** all three card titles use the same vertical inset from their card top edges
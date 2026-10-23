# Spec Delta

## ADDED Requirements

### Requirement: Compact comparison header-to-donut spacing
The comparison view SHALL keep the vertical gap between each metric card's heading/description block and its donut chart frame at 8 CSS pixels or less, consistently across supported viewport widths.

#### Scenario: Sector, region, and currency charts use a compact header gap
- **WHEN** the comparison view renders the sector, region, and currency cards at any supported viewport width
- **THEN** the vertical gap from each card's text block to its chart frame SHALL be no greater than 8 CSS pixels
- **AND** all three cards SHALL use the same gap
- **AND** spacing between each chart frame and its legend SHALL remain unchanged

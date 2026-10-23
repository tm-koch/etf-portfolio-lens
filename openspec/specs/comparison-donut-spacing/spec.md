## Purpose

Defines spacing behavior for comparison donuts, headings, and legends across supported viewport widths.

## Requirements

### Requirement: Shared comparison donut spacing rhythm
The comparison view SHALL use a consistent spacing rhythm on smartphone-sized viewports so the title, donut, and legend feel evenly separated and the donut's horizontal inset matches the surrounding vertical spacing.

#### Scenario: Smartphone spacing stays balanced
- **WHEN** the comparison view is rendered on a smartphone-sized viewport
- **THEN** the spacing above the donut, below the donut, and around the donut's left and right edges SHALL feel visually consistent within the chart stack
- **AND** the legend SHALL remain compact without changing the balanced spacing around the donut

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

### Requirement: Compact comparison header-to-donut spacing
The comparison view SHALL keep the vertical gap between each metric card's heading/description block and its donut chart frame at 8 CSS pixels or less, consistently across supported viewport widths.

#### Scenario: Sector, region, and currency charts use a compact header gap
- **WHEN** the comparison view renders the sector, region, and currency cards at any supported viewport width
- **THEN** the vertical gap from each card's text block to its chart frame SHALL be no greater than 8 CSS pixels
- **AND** all three cards SHALL use the same gap
- **AND** spacing between each chart frame and its legend SHALL remain unchanged

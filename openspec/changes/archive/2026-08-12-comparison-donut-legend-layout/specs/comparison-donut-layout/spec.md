## ADDED Requirements

### Requirement: Consistent comparison donut sizing
The comparison view SHALL render the sector, region, and currency doughnut charts with a consistent effective ring size so that the multi-ring visuals appear equally sized across the three metrics.

#### Scenario: Comparison metrics share the same donut scale
- **WHEN** the comparison view renders the sector, region, and currency charts for a selected portfolio
- **THEN** each chart SHALL use the same effective donut sizing rules so their visible ring thickness and overall donut footprint match
- **AND** no metric SHALL render with a visibly smaller or thinner donut purely because of its legend contents

### Requirement: Fully visible comparison legends
The comparison view SHALL render each chart legend completely within the available layout so legend entries are not clipped or hidden.

#### Scenario: Dense sector legend remains readable
- **WHEN** the sector comparison chart renders with many legend entries
- **THEN** the legend SHALL remain fully visible
- **AND** all legend labels SHALL be readable without being cut off by the chart container

#### Scenario: Narrow layout preserves legend visibility
- **WHEN** the comparison view is rendered in a narrower viewport
- **THEN** the chart layout SHALL preserve the full legend content without clipping
- **AND** the donut visualization SHALL remain visible alongside the legend

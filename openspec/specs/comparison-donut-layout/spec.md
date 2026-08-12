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

#### Scenario: Smartphone legend stays compact
- **WHEN** the comparison view is rendered on a smartphone-sized viewport
- **THEN** the legend SHALL allow multiple entries to share the same row when space permits instead of forcing one item per line
- **AND** the legend SHALL remain readable while using less vertical space than the single-column mobile layout

### Requirement: Smartphone comparison donut spacing is symmetric
The comparison view SHALL keep the donut stack visually balanced on smartphone-sized viewports so the effective whitespace around the donut is consistent with the spacing to the title and the legend.

#### Scenario: Mobile chart stack uses the same spacing rhythm
- **WHEN** the comparison view is rendered on a smartphone-sized viewport
- **THEN** the donut SHALL retain matching effective spacing to the surrounding title and legend blocks
- **AND** the left and right donut inset SHALL feel visually equivalent to the top and bottom spacing in the chart stack

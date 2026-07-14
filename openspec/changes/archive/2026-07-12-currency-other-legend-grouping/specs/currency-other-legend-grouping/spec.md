## ADDED Requirements

### Requirement: Currency slices below one percent are grouped
The currency comparison view SHALL group all currency entries below 1% into a single `Other` category before rendering the donut chart.

#### Scenario: Small currency entries are consolidated
- **WHEN** the currency comparison data contains currency entries below 1% of the total
- **THEN** those entries SHALL be combined into `Other`
- **AND** the donut chart SHALL render a single `Other` slice for the grouped entries

### Requirement: Unknown currency values are grouped
The currency comparison view SHALL group any currency entry labeled `Unknown` into the `Other` category before rendering the donut chart.

#### Scenario: Unknown currency values are consolidated
- **WHEN** the currency comparison data contains an entry labeled `Unknown`
- **THEN** that entry SHALL be included in `Other`
- **AND** the resulting chart SHALL NOT show a separate `Unknown` slice

### Requirement: Other appears in legend and plot
The currency comparison view SHALL display the `Other` category in both the donut plot and the legend when grouping occurs.

#### Scenario: Legend reflects grouped currency bucket
- **WHEN** the currency comparison view groups small or unknown currency entries into `Other`
- **THEN** the legend SHALL include `Other`
- **AND** the donut plot SHALL show the same `Other` label for the grouped slice
- **AND** the grouped amount SHALL be visible to the user as part of the rendered comparison

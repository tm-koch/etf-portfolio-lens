## ADDED Requirements

### Requirement: Comparison doughnuts are visually larger
The comparison view SHALL render doughnut charts with enough visible area to make each ring easy to inspect on desktop and mobile layouts.

#### Scenario: Chart renders with expanded presence
- **WHEN** the user opens the comparison view with available ETF data
- **THEN** each doughnut chart SHALL occupy a larger chart frame than the default compact layout
- **AND** the chart SHALL remain fully visible without clipping

### Requirement: Comparison doughnuts use a thinner ring
The comparison view SHALL render doughnut charts with a thinner colored ring so the slice labels and segment boundaries are easier to distinguish.

#### Scenario: Ring thickness is reduced
- **WHEN** a comparison doughnut chart is drawn
- **THEN** the inner cutout SHALL be large enough to produce a thinner ring than the current compact style
- **AND** the chart SHALL still preserve readable segment separation

### Requirement: Comparison hover text identifies the ETF
The comparison view SHALL show hover tooltips that identify the ETF and the metric category for the hovered segment.

#### Scenario: Hover tooltip exposes ETF and metric
- **WHEN** the user hovers over a doughnut segment in the comparison view
- **THEN** the tooltip SHALL include the ETF name
- **AND** the tooltip SHALL include the metric category such as sector, region, or currency
- **AND** the tooltip SHALL include the segment value as a percentage

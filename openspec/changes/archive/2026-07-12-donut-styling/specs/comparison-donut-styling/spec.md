## ADDED Requirements

### Requirement: Distinct donut slice colors
The comparison donut charts SHALL assign visually distinct categorical colors to visible slices so adjacent categories are easy to tell apart.

#### Scenario: Multiple categories in one donut
- **WHEN** a donut chart contains more than one category
- **THEN** each visible slice SHALL use a distinct categorical color where practical
- **AND** the chart SHALL avoid reusing the same short color sequence for the initial visible categories

#### Scenario: Consistent category identity
- **WHEN** the same category appears in different comparison donuts
- **THEN** the category SHALL use the same color mapping across those donuts

### Requirement: Blue-anchored harmonic palette
The comparison donut charts SHALL use a harmonic palette anchored around cool blue hues and MAY include adjacent cyan, teal, green, indigo, and violet accents.

#### Scenario: Visual harmony
- **WHEN** the chart renders sector, region, or currency exposure
- **THEN** the slice colors SHALL feel cohesive rather than rainbow-like
- **AND** the palette SHALL remain visually centered on cool tones

### Requirement: Slightly increased saturation
The comparison donut charts SHALL use slice colors with enough saturation to remain distinguishable at small slice sizes.

#### Scenario: Small slices remain readable
- **WHEN** a donut contains a small category slice
- **THEN** the slice color SHALL remain visibly separate from neighboring slices on the same ring

### Requirement: White slice separator
The comparison donut charts SHALL render slice borders in white to separate adjacent slices.

#### Scenario: Adjacent wedges
- **WHEN** two slices touch in a donut ring
- **THEN** the border between them SHALL be white
- **AND** the separator SHALL remain visible against saturated slice colors

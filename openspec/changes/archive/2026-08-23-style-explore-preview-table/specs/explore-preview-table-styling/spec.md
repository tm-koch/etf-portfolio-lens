## ADDED Requirements

### Requirement: Compact Explore table palette
The compact Explore holdings table SHALL use `rgb(232, 236, 244)` for its header background. Its body rows SHALL alternate between `rgb(244, 246, 251)` and white, beginning with `rgb(244, 246, 251)` on the first row.

#### Scenario: Header uses the requested background
- **WHEN** the compact Explore table is rendered
- **THEN** every header cell uses `rgb(232, 236, 244)` as its resting background

#### Scenario: Body rows alternate backgrounds
- **WHEN** the compact Explore table contains multiple holdings
- **THEN** odd rows use `rgb(244, 246, 251)` and even rows use white

#### Scenario: Appended rows continue alternation
- **WHEN** additional holdings are appended during incremental loading
- **THEN** the row colors continue alternating according to each row's position in the table body

### Requirement: Sticky holding column preserves row palette
The sticky holding-name cells in the compact Explore table SHALL use the same resting background as their corresponding body row and SHALL use the header background when they are header cells.

#### Scenario: Sticky body cells match their rows
- **WHEN** the user horizontally scrolls a compact Explore table
- **THEN** the sticky holding-name cells retain the alternating background of their corresponding rows

#### Scenario: Sticky header matches other headers
- **WHEN** the compact Explore table header is visible
- **THEN** the sticky Holding header uses `rgb(232, 236, 244)` like the other header cells

### Requirement: Existing table interaction remains intact
The palette change SHALL preserve the compact Explore table's existing hover feedback, sticky positioning, horizontal overflow, stable numeric column widths, and holding-name clipping behavior.

#### Scenario: Hover feedback remains available
- **WHEN** the pointer rests over a compact Explore table row
- **THEN** the existing row hover treatment remains visible without changing the table structure

#### Scenario: Responsive behavior remains available
- **WHEN** the compact Explore table is wider than its viewport
- **THEN** horizontal scrolling, sticky holding cells, and stable numeric columns continue to operate while the requested resting palette remains available

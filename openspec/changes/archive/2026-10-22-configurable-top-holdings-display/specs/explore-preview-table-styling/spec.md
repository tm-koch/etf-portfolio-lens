# Spec Delta

## MODIFIED Requirements

### Requirement: Existing table interaction remains intact
The palette change SHALL preserve the compact Explore table's existing hover feedback, horizontal overflow, stable numeric column widths, and holding-name clipping behavior. During normal page scrolling, the table header SHALL remain visible at the viewport top while the table intersects the page's scroll range and SHALL stop sticking at the table's end. Horizontal scrolling SHALL keep the header columns aligned with the table columns, and the sticky holding-name column SHALL remain usable.

#### Scenario: Hover feedback remains available
- **WHEN** the pointer rests over a compact Explore table row
- **THEN** the existing row hover treatment remains visible without changing the table structure

#### Scenario: Responsive behavior remains available
- **WHEN** the compact Explore table is wider than its viewport
- **THEN** horizontal scrolling, sticky holding cells, and stable numeric columns continue to operate while the requested resting palette remains available

#### Scenario: First header column remains visible during horizontal scrolling
- **WHEN** the user horizontally scrolls the compact Explore table
- **THEN** the visual header's holding column SHALL remain pinned to the left edge of the table viewport while the remaining header columns stay aligned with their body columns

#### Scenario: Portfolio and fund headings are right-aligned
- **WHEN** the compact Explore table header is displayed
- **THEN** the Portfolio and fund heading labels SHALL fit within their assigned columns and be right-aligned, while the holding heading remains left-aligned

#### Scenario: Header sticks during page scrolling
- **WHEN** the user scrolls the page and the compact Explore table extends below the viewport
- **THEN** the table header SHALL remain visible at the viewport top and its columns SHALL stay aligned with the table's horizontal position

#### Scenario: Header stops at the end of the table
- **WHEN** the user scrolls the page past the bottom of the compact Explore table
- **THEN** the sticky header SHALL stop at the table boundary and SHALL NOT remain fixed over subsequent page content

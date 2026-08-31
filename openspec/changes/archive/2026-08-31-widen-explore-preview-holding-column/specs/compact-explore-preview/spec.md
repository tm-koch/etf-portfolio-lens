## MODIFIED Requirements

### Requirement: Responsive table overflow
The compact holdings matrix SHALL remain readable when its intrinsic width exceeds the viewport by providing horizontal scrolling within the table container. Numeric columns SHALL retain stable widths, the holding-name column SHALL remain visible while horizontally scrolling, and table content SHALL remain accessible on desktop and mobile-sized viewports. On widescreen layouts, the sticky holding-name column SHALL provide a minimum width of `300px`, and holding names SHALL be allowed up to `300px` of visible width. Holding names that exceed the available mobile width SHALL be visually faded toward their clipped end and SHALL expose the full name through a hover tip. The sticky holding-name body column SHALL be slightly transparent so horizontally scrolling cells remain faintly visible beneath it, while the sticky header SHALL remain opaque for readability.

#### Scenario: Wide ETF matrix on a narrow viewport
- **WHEN** the number of selected ETF columns exceeds the available viewport width
- **THEN** the table container SHALL allow horizontal scrolling without shrinking or overlapping table cells, while the holding-name column remains visible and the horizontally moving cells are faintly visible through the sticky body column

#### Scenario: Sticky column at rest
- **WHEN** the compact Explore matrix is displayed on a widescreen viewport before horizontal scrolling
- **THEN** the sticky body holding column SHALL provide at least `300px` of width, and its holding-name content SHALL be allowed up to `300px` before clipping, while the sticky header remains opaque

#### Scenario: Long holding name on mobile
- **WHEN** a holding name exceeds half of the available mobile line width
- **THEN** the displayed name SHALL be clipped with a visual fade and its full value SHALL be available through the cell hover tip while the sticky cell remains readable and sized responsively to `36vw`

#### Scenario: Hovered holding row
- **WHEN** the user hovers over a compact Explore holdings row
- **THEN** the sticky holding cell SHALL show the row's hover treatment with sufficient contrast while preserving the slightly transparent view of horizontally moving cells

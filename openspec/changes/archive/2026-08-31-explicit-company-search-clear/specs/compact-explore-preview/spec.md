## MODIFIED Requirements

### Requirement: Responsive table overflow
The compact holdings matrix SHALL remain readable when its intrinsic width exceeds the viewport by providing horizontal scrolling within the table container. Numeric columns SHALL retain stable widths, the holding-name column SHALL remain visible while horizontally scrolling, and table content SHALL remain accessible on desktop and mobile-sized viewports. On widescreen layouts, the sticky holding-name column SHALL provide a minimum width of `300px`, and holding names SHALL be allowed up to `300px` of visible width. Holding names that exceed the available mobile width SHALL be visually faded toward their clipped end and SHALL expose the full name through a hover tip. The sticky holding-name body column SHALL be slightly transparent so horizontally scrolling cells remain faintly visible beneath it, while the sticky header SHALL remain opaque for readability. The rank and holding name within each sticky cell SHALL remain on one visual line, with the name taking the remaining available width and retaining the existing clipping and hover disclosure behavior.

#### Scenario: Wide ETF matrix on a narrow viewport
- **WHEN** the number of selected ETF columns exceeds the available viewport width
- **THEN** the table container SHALL allow horizontal scrolling without shrinking or overlapping table cells, while the holding-name column remains visible and the horizontally moving cells are faintly visible through the sticky body column

#### Scenario: Sticky column at rest
- **WHEN** the compact Explore matrix is displayed on a widescreen viewport before horizontal scrolling
- **THEN** the sticky body holding column SHALL provide at least `300px` of width, and its rank and holding-name content SHALL remain on one line while the holding-name content is allowed up to `300px` before clipping and the sticky header remains opaque

#### Scenario: Long holding name on mobile
- **WHEN** a holding name exceeds half of the available mobile line width
- **THEN** the displayed rank and name SHALL remain on one line, the name SHALL be clipped with a visual fade, and its full value SHALL be available through the cell hover tip while the sticky cell remains readable and sized responsively to `36vw`

#### Scenario: Hovered holding row
- **WHEN** the user hovers over a compact Explore holdings row
- **THEN** the sticky holding cell SHALL show the row's hover treatment with sufficient contrast while preserving the slightly transparent view of horizontally moving cells

### Requirement: Live company-name filtering
The compact Explore preview SHALL provide a company search field that updates the displayed table on every input event. Matching SHALL use the trimmed search value, case-insensitively, as a substring of the aggregated company name only. The search control SHALL provide an application-owned clear button that is visible when the search contains text and is usable with pointer, touch, and keyboard input. When activated, the clear button SHALL empty the search, restore the unfiltered first-20 ranked rows and their infinite-scroll sentinel, and return focus to the search input. When the search value is empty, the preview SHALL restore the complete ranked list using its existing first-20-plus-infinite-scroll behavior. When the search value is non-empty, the preview SHALL display every matching company and SHALL display no company rows when there are no matches.

#### Scenario: Search updates while typing
- **WHEN** the user types or edits a value in the company search field
- **THEN** the compact Explore table SHALL update immediately without requiring a submit action or page reload, and the clear button SHALL reflect whether the field contains text

#### Scenario: Company name substring match
- **WHEN** the search value matches part of one or more aggregated company names regardless of letter case
- **THEN** the table SHALL display every matching company and no non-matching company rows

#### Scenario: Clear button restores the full table
- **WHEN** the user activates the visible clear button after entering a company search value
- **THEN** the search input SHALL become empty, the unfiltered first 20 ranked company rows SHALL be displayed, the infinite-scroll sentinel SHALL be restored when more rows remain, and focus SHALL return to the search input

#### Scenario: Clear button is available across browsers
- **WHEN** the compact Explore search is displayed in a browser without a native search cancel control, including Firefox mobile
- **THEN** the application-owned clear button SHALL remain visible for non-empty values and SHALL provide a touch target of at least 44px without relying on vendor-specific search pseudo-elements for its clear behavior

#### Scenario: Empty search restores ranked loading
- **WHEN** the company search value is empty or contains only whitespace
- **THEN** the preview SHALL restore the unfiltered ranking and its existing incremental loading behavior

#### Scenario: Search result bypasses pagination
- **WHEN** the company search value is non-empty and matching companies exist
- **THEN** all matching company rows SHALL be displayed without requiring scrolling to load additional matches

#### Scenario: No company matches
- **WHEN** the company search value is non-empty and no aggregated company name contains the value
- **THEN** the compact Explore table SHALL contain no company rows

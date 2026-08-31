# compact-explore-preview Specification

## Purpose
TBD - created by archiving change compact-explore-preview. Update Purpose after archive.
## Requirements
### Requirement: Persisted developer preview selection

The application SHALL provide a developer-mode control for enabling the compact Explore preview, with the control disabled by default when no valid preference has been stored. The application SHALL persist the selection in browser storage and restore it on reload.

#### Scenario: Existing Explore view is the default
- **WHEN** the preview preference is absent, invalid, or set to false
- **THEN** the Explore tab SHALL render the existing aggregated presentation

#### Scenario: Developer enables compact preview
- **WHEN** the developer-mode preview control is changed to enabled
- **THEN** the application SHALL persist the enabled state and render the compact Explore presentation

#### Scenario: Preview preference survives reload
- **WHEN** the application is reloaded after the compact preview was enabled
- **THEN** the developer-mode control SHALL be enabled and the Explore tab SHALL use the compact presentation

### Requirement: Compact holdings matrix

When compact Explore preview mode is enabled, the application SHALL render a semantic holdings table using the existing aggregated holding result. The table SHALL contain one row per aggregated holding and SHALL order rows by total portfolio exposure from largest to smallest.

#### Scenario: Holdings are ranked by total exposure
- **WHEN** the compact Explore presentation has aggregated holdings
- **THEN** the first rows SHALL be the holdings with the largest existing total portfolio exposure values

#### Scenario: Empty portfolio
- **WHEN** compact preview is enabled and no selected positions provide aggregated holdings
- **THEN** the table area SHALL show the existing empty-state behavior for unavailable company exposure

### Requirement: Portfolio and ETF contribution columns

The compact holdings matrix SHALL display the holding name, the existing total portfolio contribution, and one column for every selected ETF. Each ETF cell SHALL display that ETF contributor's existing share of the holding total, and SHALL display an em dash when that ETF does not contribute to the holding. The matrix SHALL NOT introduce a separate holding-level exposure data source. Portfolio contribution calculations SHALL weight each selected ETF position by its valid imported CHF-normalized market value; positions without imported valuation data SHALL use the existing share-count fallback. The matrix SHALL initially display the first 20 ranked holdings and SHALL append further ranked holdings in batches as the user scrolls toward the end.

#### Scenario: Shared holding contribution breakdown
- **WHEN** a holding has contributors from multiple selected ETFs
- **THEN** its total column SHALL use the existing aggregated portfolio value and each contributing ETF column SHALL use the existing contributor share-of-holding value

#### Scenario: Imported values determine portfolio weighting
- **WHEN** selected positions have valid imported CHF-normalized market values
- **THEN** their relative portfolio contribution SHALL be calculated from those values rather than share counts alone

#### Scenario: Manual positions retain fallback weighting
- **WHEN** a selected position has no valid imported valuation data
- **THEN** that position SHALL use the existing share-count fallback without preventing other positions from using imported value weighting

#### Scenario: Holding absent from an ETF
- **WHEN** an aggregated holding has no contributor record for a selected ETF
- **THEN** that ETF's cell SHALL display an em dash and SHALL not affect the row's existing total

#### Scenario: ETF columns follow selected positions
- **WHEN** the selected portfolio contains multiple ETFs
- **THEN** the table SHALL provide one distinct column per selected ETF in the selected-position order

#### Scenario: More holdings load while scrolling
- **WHEN** the user scrolls toward the end of the currently rendered compact rows and more ranked holdings remain
- **THEN** the application SHALL append the next batch of ranked rows without replacing the existing rows

### Requirement: Responsive table overflow
The compact holdings matrix SHALL remain readable when its intrinsic width exceeds the viewport by providing horizontal scrolling within the table container. Numeric columns SHALL retain stable widths, the holding-name column SHALL remain visible while horizontally scrolling, and table content SHALL remain accessible on desktop and mobile-sized viewports. On widescreen layouts, the sticky holding-name column SHALL provide a minimum width of `300px`, and holding names SHALL be allowed up to `300px` of visible width. Holding names that exceed the available mobile width SHALL be visually faded toward their clipped end and SHALL expose the full name through a hover tip. The sticky holding-name body column SHALL be slightly transparent so horizontally scrolling cells remain faintly visible beneath it, while the sticky header SHALL remain opaque for readability. The rank and holding name within each sticky cell SHALL remain on one visual line, with the name taking the remaining available width and retaining the existing clipping and hover disclosure behavior.

#### Scenario: Wide ETF matrix on a narrow viewport
- **WHEN** the number of selected ETF columns exceeds the available viewport width
- **THEN** the table container SHALL allow horizontal scrolling without shrinking or overlapping table cells, while the holding-name column remains visible and the horizontally moving cells are faintly visible through the sticky body column

#### Scenario: Sticky column at rest
- **WHEN** the compact Explore matrix is displayed on a widescreen viewport before horizontal scrolling
- **THEN** the sticky body holding column SHALL provide at least `300px` of width, and its rank and holding-name content SHALL remain on one line while the holding-name content is allowed up to `300px` before clipping, while the sticky header remains opaque

#### Scenario: Long holding name on mobile
- **WHEN** a holding name exceeds half of the available mobile line width
- **THEN** the displayed rank and name SHALL remain on one line, the name SHALL be clipped with a visual fade, and its full value SHALL be available through the cell hover tip while the sticky cell remains readable and sized responsively to `36vw`

#### Scenario: Hovered holding row
- **WHEN** the user hovers over a compact Explore holdings row
- **THEN** the sticky holding cell SHALL show the row's hover treatment with sufficient contrast while preserving the slightly transparent view of horizontally moving cells

### Requirement: Compact Explore preview styling
The compact Explore preview SHALL apply the requested light palette to its existing semantic holdings matrix without changing the matrix data, ordering, loading behavior, or responsive interaction model.

#### Scenario: Preview uses the styled matrix
- **WHEN** compact Explore preview mode is enabled
- **THEN** the existing holdings matrix is rendered with the specified header and alternating body-row colors

#### Scenario: Preview data behavior is unchanged
- **WHEN** the styled compact matrix renders or appends holdings
- **THEN** it preserves the existing ranked rows, ETF contribution values, incremental loading, and empty-state behavior

### Requirement: Explore warning surface

When compact Explore preview mode is enabled, the application SHALL render the compact holdings presentation without a warnings panel in the Explore `/aggregated` tab. When compact preview mode is disabled, the standard aggregated Explore presentation SHALL also omit the warnings panel. Current-selection warnings SHALL remain available in the About this build dialog.

#### Scenario: Compact preview has no Explore warnings panel
- **WHEN** compact Explore preview mode is enabled and the user opens the `/aggregated` tab
- **THEN** the tab SHALL render the compact holdings presentation and SHALL NOT render an Explore warnings panel at the bottom

#### Scenario: Standard Explore has no warnings panel
- **WHEN** compact Explore preview mode is disabled and the user opens the `/aggregated` tab
- **THEN** the tab SHALL render the standard aggregated presentation and SHALL NOT render an Explore warnings panel at the bottom

#### Scenario: Build dialog retains warnings
- **WHEN** the user opens About this build
- **THEN** the dialog SHALL continue to render current-selection warnings in its existing warnings section

### Requirement: Ranked compact Explore holdings
The compact Explore preview SHALL display a visible positive integer rank for every company row. Each rank SHALL represent the company's position in the complete compact Explore ranking ordered by total portfolio exposure, and SHALL remain unchanged when other companies are hidden by a search filter.

#### Scenario: Ranked rows display portfolio positions
- **WHEN** the compact Explore preview displays ranked company holdings
- **THEN** every company row SHALL include its one-based position in the complete total-exposure ranking

#### Scenario: Filtered row keeps original rank
- **WHEN** a company is displayed after other companies have been excluded by search
- **THEN** the company SHALL retain its rank from the unfiltered portfolio ranking rather than being renumbered from one

### Requirement: Live company-name filtering
The compact Explore preview SHALL provide a company search field that updates the displayed table on every input event. Matching SHALL use the trimmed search value, case-insensitively, as a substring of the aggregated company name only. The search control SHALL provide an application-owned clear button that is visible when the search contains text and is usable with pointer, touch, and keyboard input. When activated, the clear button SHALL empty the search, restore the unfiltered first-20 ranked rows and their infinite-scroll sentinel, and return focus to the search input. The implementation MAY suppress vendor-native search cancel UI only to avoid displaying duplicate clear controls; clear behavior SHALL remain owned by the application. When the search value is empty, the preview SHALL restore the complete ranked list using its existing first-20-plus-infinite-scroll behavior. When the search value is non-empty, the preview SHALL display every matching company and SHALL display no company rows when there are no matches.

#### Scenario: Search updates while typing
- **WHEN** the user types or edits a value in the company search field
- **THEN** the compact Explore table SHALL update immediately without requiring a submit action or page reload
- **THEN** the compact Explore table SHALL update immediately without requiring a submit action or page reload, and the clear button SHALL reflect whether the field contains text

#### Scenario: Clear button restores the full table
- **WHEN** the user activates the visible clear button after entering a company search value
- **THEN** the search input SHALL become empty, the unfiltered first 20 ranked company rows SHALL be displayed, the infinite-scroll sentinel SHALL be restored when more rows remain, and focus SHALL return to the search input

#### Scenario: Clear button is available across browsers
- **WHEN** the compact Explore search is displayed in a browser without a native search cancel control, including Firefox mobile
- **THEN** the application-owned clear button SHALL remain visible for non-empty values and SHALL provide a touch target of at least 44px without relying on vendor-specific search pseudo-elements for its clear behavior

#### Scenario: Company name substring match
- **WHEN** the search value matches part of one or more aggregated company names regardless of letter case
- **THEN** the table SHALL display every matching company and no non-matching company rows

#### Scenario: Empty search restores ranked loading
- **WHEN** the company search value is empty or contains only whitespace
- **THEN** the preview SHALL restore the unfiltered ranking and its existing incremental loading behavior

#### Scenario: Search result bypasses pagination
- **WHEN** the company search value is non-empty and matching companies exist
- **THEN** all matching company rows SHALL be displayed without requiring scrolling to load additional matches

#### Scenario: No company matches
- **WHEN** the company search value is non-empty and no aggregated company name contains the value
- **THEN** the compact Explore table SHALL contain no company rows

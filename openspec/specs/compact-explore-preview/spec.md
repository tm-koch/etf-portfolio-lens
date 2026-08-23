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

The compact holdings matrix SHALL display the holding name, the existing total portfolio contribution, and one column for every selected ETF. Each ETF cell SHALL display that ETF contributor's existing share of the holding total, and SHALL display an em dash when that ETF does not contribute to the holding. The matrix SHALL NOT introduce a separate exposure calculation or data source. The matrix SHALL initially display the first 20 ranked holdings and SHALL append further ranked holdings in batches as the user scrolls toward the end.

#### Scenario: Shared holding contribution breakdown
- **WHEN** a holding has contributors from multiple selected ETFs
- **THEN** its total column SHALL use the existing aggregated portfolio value and each contributing ETF column SHALL use the existing contributor share-of-holding value

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

The compact holdings matrix SHALL remain readable when its intrinsic width exceeds the viewport by providing horizontal scrolling within the table container. Numeric columns SHALL retain stable widths, the holding-name column SHALL remain visible while horizontally scrolling, and table content SHALL remain accessible on desktop and mobile-sized viewports. Holding names that exceed the available mobile width SHALL be visually faded toward their clipped end and SHALL expose the full name through a hover tip.

#### Scenario: Wide ETF matrix on a narrow viewport
- **WHEN** the number of selected ETF columns exceeds the available viewport width
- **THEN** the table container SHALL allow horizontal scrolling without shrinking or overlapping table cells, while the holding-name column remains visible

#### Scenario: Long holding name on mobile
- **WHEN** a holding name exceeds half of the available mobile line width
- **THEN** the displayed name SHALL be clipped with a visual fade and its full value SHALL be available through the cell hover tip

### Requirement: Compact Explore preview styling
The compact Explore preview SHALL apply the requested light palette to its existing semantic holdings matrix without changing the matrix data, ordering, loading behavior, or responsive interaction model.

#### Scenario: Preview uses the styled matrix
- **WHEN** compact Explore preview mode is enabled
- **THEN** the existing holdings matrix is rendered with the specified header and alternating body-row colors

#### Scenario: Preview data behavior is unchanged
- **WHEN** the styled compact matrix renders or appends holdings
- **THEN** it preserves the existing ranked rows, ETF contribution values, incremental loading, and empty-state behavior

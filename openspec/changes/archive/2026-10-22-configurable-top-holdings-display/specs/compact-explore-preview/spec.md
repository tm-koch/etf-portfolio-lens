# Spec Delta

## ADDED Requirements

### Requirement: Developer-configurable top holdings maximum
The application SHALL provide a persisted developer-mode numeric maximum for the unfiltered top holdings displayed in both standard and compact Explore presentations. A value of zero SHALL mean unlimited, and the default SHALL be zero.

#### Scenario: No saved maximum
- **WHEN** no valid maximum has been saved
- **THEN** both Explore presentations SHALL display the complete ranked list through their existing incremental loading behavior

#### Scenario: Positive maximum limits the unfiltered list
- **WHEN** a positive maximum is configured
- **THEN** both Explore presentations SHALL display no more than that number of top-ranked holdings

#### Scenario: Zero maximum is unlimited
- **WHEN** the configured maximum is zero
- **THEN** both Explore presentations SHALL allow the complete ranked list to be displayed through incremental loading

#### Scenario: Maximum preference survives reload
- **WHEN** a developer changes the maximum and reloads the application
- **THEN** the saved maximum SHALL be restored and applied to both Explore presentations

#### Scenario: Search bypasses the maximum
- **WHEN** a non-empty search matches holdings ranked below the configured maximum
- **THEN** every matching holding from the complete ranking SHALL be displayed with its original rank

## MODIFIED Requirements

### Requirement: Compact holdings matrix
When compact Explore preview mode is enabled, the application SHALL render a semantic holdings table using the existing aggregated holding result. The table SHALL contain up to the configured maximum number of top-ranked holdings, or all ranked holdings when the maximum is zero, ordered by total portfolio exposure from largest to smallest. It SHALL initially display up to the first 20 permitted holdings and SHALL append further permitted holdings in batches as the user scrolls toward the end.

#### Scenario: Holdings are ranked by total exposure
- **WHEN** the compact Explore presentation has aggregated holdings
- **THEN** the first rows SHALL be the holdings with the largest existing total portfolio exposure values

#### Scenario: Configured maximum limits compact rows
- **WHEN** a positive maximum is lower than the number of aggregated holdings
- **THEN** the compact table SHALL contain no more than the configured maximum number of rows

#### Scenario: Unlimited compact rows
- **WHEN** the maximum is zero
- **THEN** the compact table SHALL allow every aggregated holding to be appended in batches

#### Scenario: Empty portfolio
- **WHEN** compact preview is enabled and no selected positions provide aggregated holdings
- **THEN** the table area SHALL show the existing empty-state behavior for unavailable company exposure

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

#### Scenario: More permitted holdings load while scrolling
- **WHEN** the user scrolls toward the end of the currently rendered compact rows and more holdings remain within the configured maximum
- **THEN** the application SHALL append the next batch of ranked rows without replacing existing rows

### Requirement: Live company-name filtering
The Explore company search SHALL provide a company search field that updates the displayed company presentation on every input event in both standard and compact preview modes. Matching SHALL use the trimmed search value, case-insensitively, as a substring of the aggregated company name only. The search control SHALL provide an application-owned clear button that is visible when the search contains text and is usable with pointer, touch, and keyboard input. When activated, the clear button SHALL empty the search, restore the unfiltered top holdings up to the configured maximum in the active presentation, and return focus to the search input. A zero maximum SHALL restore the existing first-20-plus-infinite-scroll behavior. When the search value is non-empty, the maximum SHALL NOT restrict results: both presentations SHALL display every matching company from the complete ranking and SHALL display no company rows when there are no matches. Filtered companies SHALL retain their ranks in the complete total-exposure ranking.

#### Scenario: Search updates while typing in standard Explore
- **WHEN** the user types or edits a value in the company search field while standard Explore presentation is active
- **THEN** the standard company list SHALL update immediately without requiring a submit action or page reload, and the clear button SHALL reflect whether the field contains text

#### Scenario: Search updates while typing in compact preview
- **WHEN** the user types or edits a value in the company search field while compact Explore preview is active
- **THEN** the compact Explore table SHALL update immediately without requiring a submit action or page reload, and the clear button SHALL reflect whether the field contains text

#### Scenario: Clear button restores the standard list
- **WHEN** the user activates the visible clear button after entering a search value while standard Explore presentation is active
- **THEN** the search input SHALL become empty, the unfiltered top holdings up to the configured maximum SHALL be displayed, an incremental-loading sentinel SHALL be restored when more permitted rows remain, and focus SHALL return to the search input

#### Scenario: Clear button restores the compact table
- **WHEN** the user activates the visible clear button after entering a search value while compact Explore presentation is active
- **THEN** the search input SHALL become empty, the unfiltered top holdings up to the configured maximum SHALL be displayed, an incremental-loading sentinel SHALL be restored when more permitted rows remain, and focus SHALL return to the search input

#### Scenario: Clear button is available across browsers
- **WHEN** the Explore search is displayed in a browser without a native search cancel control, including Firefox mobile
- **THEN** the application-owned clear button SHALL remain visible for non-empty values and SHALL provide a touch target of at least 44px without relying on vendor-specific search pseudo-elements for its clear behavior

#### Scenario: Company name substring match in standard Explore
- **WHEN** the search value matches part of one or more aggregated company names regardless of letter case while standard Explore presentation is active
- **THEN** the standard company list SHALL display every matching company from the complete ranking and no non-matching company rows, regardless of the configured maximum

#### Scenario: Company name substring match in compact preview
- **WHEN** the search value matches part of one or more aggregated company names regardless of letter case while compact Explore preview is active
- **THEN** the compact Explore table SHALL display every matching company from the complete ranking and no non-matching company rows, regardless of the configured maximum

#### Scenario: Empty search restores ranked loading in standard Explore
- **WHEN** the company search value is empty or contains only whitespace while standard Explore presentation is active
- **THEN** the standard presentation SHALL restore the unfiltered ranking up to the configured maximum using first-20-plus-incremental-loading behavior, or all rows when the maximum is zero

#### Scenario: Empty search restores ranked loading in compact preview
- **WHEN** the company search value is empty or contains only whitespace while compact Explore preview is active
- **THEN** the compact preview SHALL restore the unfiltered ranking up to the configured maximum using first-20-plus-incremental-loading behavior, or all rows when the maximum is zero

#### Scenario: Search result bypasses pagination in standard Explore
- **WHEN** the company search value is non-empty and matching companies exist while standard Explore presentation is active
- **THEN** all matching standard company rows SHALL be displayed without requiring scrolling to load additional matches

#### Scenario: Search result bypasses pagination in compact preview
- **WHEN** the company search value is non-empty and matching companies exist while compact Explore preview is active
- **THEN** all matching compact company rows SHALL be displayed without requiring scrolling to load additional matches

#### Scenario: No company matches in standard Explore
- **WHEN** the company search value is non-empty and no aggregated company name contains the value while standard Explore presentation is active
- **THEN** the standard company presentation SHALL contain no company rows

#### Scenario: No company matches in compact preview
- **WHEN** the company search value is non-empty and no aggregated company name contains the value while compact Explore preview is active
- **THEN** the compact Explore table SHALL contain no company rows

#### Scenario: Filtered rows retain their complete-list ranks
- **WHEN** a company is displayed after other companies have been excluded by search in either Explore presentation
- **THEN** the company SHALL retain its one-based rank from the complete total-exposure ranking rather than being renumbered from one

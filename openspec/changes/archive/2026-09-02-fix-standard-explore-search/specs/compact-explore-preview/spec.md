## MODIFIED Requirements

### Requirement: Live company-name filtering
The Explore company search SHALL provide a company search field that updates the displayed company presentation on every input event in both standard and compact preview modes. Matching SHALL use the trimmed search value, case-insensitively, as a substring of the aggregated company name only. The search control SHALL provide an application-owned clear button that is visible when the search contains text and is usable with pointer, touch, and keyboard input. When activated, the clear button SHALL empty the search, restore the unfiltered first 20 ranked company rows and their infinite-scroll sentinel in the active presentation, and return focus to the search input. The implementation MAY suppress vendor-native search cancel UI only to avoid displaying duplicate clear controls; clear behavior SHALL remain owned by the application. When the search value is empty, the standard and compact presentations SHALL restore their existing complete ranked lists using first-20-plus-infinite-scroll behavior. When the search value is non-empty, both presentations SHALL display every matching company and SHALL display no company rows when there are no matches.

#### Scenario: Search updates while typing in standard Explore
- **WHEN** the user types or edits a value in the company search field while standard Explore presentation is active
- **THEN** the standard company list SHALL update immediately without requiring a submit action or page reload, and the clear button SHALL reflect whether the field contains text

#### Scenario: Search updates while typing in compact preview
- **WHEN** the user types or edits a value in the company search field while compact Explore preview is active
- **THEN** the compact Explore table SHALL update immediately without requiring a submit action or page reload, and the clear button SHALL reflect whether the field contains text

#### Scenario: Clear button restores the standard list
- **WHEN** the user activates the visible clear button after entering a company search value while standard Explore presentation is active
- **THEN** the search input SHALL become empty, the unfiltered first 20 ranked standard company rows SHALL be displayed, the infinite-scroll sentinel SHALL be restored when more rows remain, and focus SHALL return to the search input

#### Scenario: Clear button restores the compact table
- **WHEN** the user activates the visible clear button after entering a company search value while compact Explore preview is active
- **THEN** the search input SHALL become empty, the unfiltered first 20 ranked compact company rows SHALL be displayed, the infinite-scroll sentinel SHALL be restored when more rows remain, and focus SHALL return to the search input

#### Scenario: Clear button is available across browsers
- **WHEN** the Explore search is displayed in a browser without a native search cancel control, including Firefox mobile
- **THEN** the application-owned clear button SHALL remain visible for non-empty values and SHALL provide a touch target of at least 44px without relying on vendor-specific search pseudo-elements for its clear behavior

#### Scenario: Company name substring match in standard Explore
- **WHEN** the search value matches part of one or more aggregated company names regardless of letter case while standard Explore presentation is active
- **THEN** the standard company list SHALL display every matching company and no non-matching company rows

#### Scenario: Company name substring match in compact preview
- **WHEN** the search value matches part of one or more aggregated company names regardless of letter case while compact Explore preview is active
- **THEN** the compact Explore table SHALL display every matching company and no non-matching company rows

#### Scenario: Empty search restores ranked loading in standard Explore
- **WHEN** the company search value is empty or contains only whitespace while standard Explore presentation is active
- **THEN** the standard presentation SHALL restore the unfiltered ranking and its existing first-20-plus-infinite-scroll behavior

#### Scenario: Empty search restores ranked loading in compact preview
- **WHEN** the company search value is empty or contains only whitespace while compact Explore preview is active
- **THEN** the compact preview SHALL restore the unfiltered ranking and its existing first-20-plus-infinite-scroll behavior

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

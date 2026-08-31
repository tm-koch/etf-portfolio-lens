## ADDED Requirements

### Requirement: Ranked compact Explore holdings
The compact Explore preview SHALL display a visible positive integer rank for every company row. Each rank SHALL represent the company's position in the complete compact Explore ranking ordered by total portfolio exposure, and SHALL remain unchanged when other companies are hidden by a search filter.

#### Scenario: Ranked rows display portfolio positions
- **WHEN** the compact Explore preview displays ranked company holdings
- **THEN** every company row SHALL include its one-based position in the complete total-exposure ranking

#### Scenario: Filtered row keeps original rank
- **WHEN** a company is displayed after other companies have been excluded by search
- **THEN** the company SHALL retain its rank from the unfiltered portfolio ranking rather than being renumbered from one

### Requirement: Live company-name filtering
The compact Explore preview SHALL provide a company search field that updates the displayed table on every input event. Matching SHALL use the trimmed search value, case-insensitively, as a substring of the aggregated company name only. When the search value is empty, the preview SHALL restore the complete ranked list using its existing first-20-plus-infinite-scroll behavior. When the search value is non-empty, the preview SHALL display every matching company and SHALL display no company rows when there are no matches.

#### Scenario: Search updates while typing
- **WHEN** the user types or edits a value in the company search field
- **THEN** the compact Explore table SHALL update immediately without requiring a submit action or page reload

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

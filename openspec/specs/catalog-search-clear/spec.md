# catalog-search-clear Specification

## Purpose

Provide a consistent, accessible clear interaction for the ETF catalog search.

## Requirements

### Requirement: Clearable ETF catalog search

The Portfolio tab SHALL provide an application-owned clear button for the ETF catalog search. The button SHALL be visible whenever the search input contains any raw value, including whitespace, and SHALL be hidden when the input is empty.

#### Scenario: Clear button appears for catalog search text
- **WHEN** the user enters any non-empty value in the ETF catalog search input
- **THEN** the application-owned clear button is visible

#### Scenario: Clear button appears for whitespace input
- **WHEN** the user enters one or more whitespace characters in the ETF catalog search input
- **THEN** the clear button remains visible even though filtering uses the trimmed value

#### Scenario: Clear button hides for an empty catalog search
- **WHEN** the ETF catalog search input is empty
- **THEN** the clear button is hidden

### Requirement: Clearing restores the ETF catalog

Activating the visible ETF catalog search clear button SHALL empty the search input, clear the catalog search state, restore the unfiltered catalog, and return focus to the catalog search input. The control SHALL be usable with pointer, touch, and keyboard input.

#### Scenario: Clear button restores catalog results
- **WHEN** the user activates the catalog search clear button after entering a search value
- **THEN** the search input is empty, the full unfiltered ETF catalog is displayed, and focus returns to the search input

#### Scenario: Clear button removes whitespace-only input
- **WHEN** the user activates the catalog search clear button after entering only whitespace
- **THEN** the whitespace is removed, the full unfiltered ETF catalog is displayed, and focus returns to the search input

### Requirement: Preserve catalog filtering semantics

The ETF catalog search SHALL continue to filter entries on every input event using the trimmed, case-insensitive search value against the existing catalog search text.

#### Scenario: Catalog filtering remains live
- **WHEN** the user types or edits a non-empty catalog search value
- **THEN** matching ETF catalog entries update immediately without a submit action or page reload

#### Scenario: Whitespace-only input behaves as an empty filter
- **WHEN** the catalog search contains only whitespace
- **THEN** the catalog displays the same entries as an empty search while the clear button remains visible

## MODIFIED Requirements

### Requirement: Developer dialog selection warning summary

The Data details dialog SHALL provide a clearly labeled current-selection warning section sourced from the same warning conditions used by the Explore warning panel. When warnings exist, the section SHALL show each current warning with enough context to identify the affected selection or aggregate condition.

#### Scenario: Data dialog shows current selection warnings
- **WHEN** the Data details dialog is opened and the current selection has one or more warnings
- **THEN** the dialog SHALL show a labeled current-selection warning section containing those warnings

#### Scenario: Data dialog includes snapshot warnings
- **WHEN** a selected ETF has a missing or empty snapshot warning
- **THEN** the Data details dialog warning section SHALL include the corresponding existing warning message and ETF context

#### Scenario: Data dialog includes aggregate warnings
- **WHEN** the current build has an existing aggregate warning
- **THEN** the Data details dialog warning section SHALL include that aggregate warning

### Requirement: Warning consistency across views

The Data details dialog and Explore warning panel SHALL use the same current-selection warning records, messages, and warning conditions. Updating the warning collection SHALL update both surfaces without requiring separate rule changes.

#### Scenario: Both surfaces show the same warning set
- **WHEN** the same current selection is displayed in Explore and in the Data details dialog
- **THEN** both surfaces SHALL represent the same warning records and messages

#### Scenario: No current warnings
- **WHEN** the current selection has no missing snapshots, empty snapshots, or aggregate warnings
- **THEN** the Data details dialog SHALL show a concise no-current-warnings state or omit the warning list without displaying stale warnings
## ADDED Requirements

### Requirement: Organize Portfolio data provenance
The Portfolio tab SHALL omit snapshot file paths from catalog item content. The About this build dialog SHALL provide a Data section that shows the published ETF data timestamp and the snapshot path for each currently selected ETF.

#### Scenario: Catalog items omit snapshot paths
- **WHEN** the Portfolio tab renders ETF catalog items
- **THEN** the item content SHALL show the existing ETF identity and selection controls without displaying a snapshot path

#### Scenario: About dialog shows data provenance
- **WHEN** the user opens About this build
- **THEN** the Data section SHALL show the ETF data timestamp and every selected ETF's ticker or identity together with its snapshot path

#### Scenario: Data provenance follows selection
- **WHEN** the selected ETF positions change and the About dialog is opened or refreshed
- **THEN** the Data section SHALL reflect the current selected ETFs and their catalog snapshot paths

### Requirement: Compact selected-position identities
The selected-position table SHALL display each selected ETF's ticker and ETF name on one visual line, separated by a middle dot. This compact identity presentation SHALL apply only to the selected-position table and SHALL not alter catalog item identity presentation.

#### Scenario: Selected position uses compact identity
- **WHEN** the Portfolio tab renders a selected position
- **THEN** its ticker and ETF name SHALL appear on one line separated by `·`

#### Scenario: Catalog identity remains unchanged
- **WHEN** the Portfolio tab renders a catalog item
- **THEN** its existing name-first identity layout SHALL remain in use

### Requirement: Space Portfolio sharing feedback
The Portfolio sharing area SHALL provide a visibly increased separation between the Share portfolio button and its feedback text while preserving the existing feedback and fallback-link behavior.

#### Scenario: Share feedback is separated from action
- **WHEN** the Portfolio sharing area is rendered
- **THEN** the feedback text SHALL have more visual space below the Share portfolio button than the current compact layout

### Requirement: Display accurate portfolio summary metrics
The Portfolio summary SHALL display Share units as the sum of the selected positions' actual share counts, independently of the weighting method used for exposure calculations. It SHALL also provide a Total value CHF card that sums valid imported CHF-normalized monetary values and SHALL show an unavailable state when no valid imported monetary value exists.

#### Scenario: Share units use actual share counts
- **WHEN** selected positions include imported CHF values that differ from their share counts
- **THEN** the Share units summary SHALL equal the sum of the positions' share counts and SHALL not equal the monetary weighting total

#### Scenario: Total CHF value uses imported values
- **WHEN** selected positions have one or more valid imported CHF-normalized values
- **THEN** the Total value CHF summary SHALL show their sum as a monetary CHF amount

#### Scenario: Total CHF value is unavailable without imported values
- **WHEN** no selected position has a valid imported CHF-normalized value
- **THEN** the Total value CHF summary SHALL show an unavailable state rather than treating share counts as currency

### Requirement: Opt-in Portfolio import debug download
The About this build dialog SHALL provide a Portfolio import debug switch that defaults to off and persists its state locally. The extracted PDF text download button SHALL be shown only when the switch is enabled and extracted PDF pages are available.

#### Scenario: Debug download is disabled by default
- **WHEN** no valid debug preference is stored or the user has disabled the switch
- **THEN** the extracted PDF text download button SHALL not be shown

#### Scenario: Debug download is enabled after extraction
- **WHEN** the user enables the debug switch and extracted PDF pages are available
- **THEN** the extracted PDF text download button SHALL be shown

#### Scenario: Debug download remains hidden without extracted pages
- **WHEN** the debug switch is enabled but no extracted PDF pages are available
- **THEN** the extracted PDF text download button SHALL remain hidden

#### Scenario: Debug preference persists
- **WHEN** the user changes the debug switch and reloads the application
- **THEN** the switch SHALL restore its stored state, defaulting to disabled when the stored value is absent or invalid

#### Scenario: Disabling debug hides the button
- **WHEN** the user disables the debug switch after extracted PDF pages have been created
- **THEN** the extracted PDF text download button SHALL be hidden immediately

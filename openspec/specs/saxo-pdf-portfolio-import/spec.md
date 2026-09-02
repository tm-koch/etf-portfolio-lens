## Purpose
Define local Saxo Bank holdings PDF import, review, currency normalization, and portfolio replacement behavior.
## Requirements
### Requirement: Import a Saxo holdings PDF locally
The Portfolio tab SHALL provide a file drop and file-selection control that accepts PDF files and parses them entirely in the browser using PDF.js without sending the file to a server. The importer SHALL recognize Saxo Bank transaction and balance reports and SHALL reject unsupported or unrecognized documents without changing the existing portfolio.

#### Scenario: User selects a Saxo PDF
- **WHEN** the user drops or selects a readable Saxo Bank PDF
- **THEN** the application extracts its page text locally and begins parsing the supported holdings sections

#### Scenario: User selects an unsupported document
- **WHEN** the selected file is not a readable PDF or does not contain the expected Saxo Bank report markers
- **THEN** the application shows an actionable import error and leaves the existing portfolio unchanged

### Requirement: Parse supported Saxo holdings sections
The Saxo importer SHALL inspect the holdings sections headed `Bestände - (account), CHF` and `Bestände - EUR`, identify ETF rows by normalized ISIN, and extract the number of shares, current price, source currency, and market value for each row. It SHALL parse German-formatted numbers and calculate market value from shares multiplied by price when necessary.

#### Scenario: CHF holdings are extracted
- **WHEN** the Saxo PDF contains the CHF holdings section with valid ETF rows
- **THEN** each row is proposed with its ISIN, shares, current price, CHF currency, and calculated value

#### Scenario: EUR holdings are extracted
- **WHEN** the Saxo PDF contains the EUR holdings section with valid ETF rows
- **THEN** each row is proposed with its ISIN, shares, current price, EUR currency, and calculated value

#### Scenario: Row data is incomplete
- **WHEN** an ISIN-anchored row lacks a valid share count or price
- **THEN** the row is shown as an extraction warning and cannot be applied until corrected in review

### Requirement: Match imported rows to the ETF catalog
The importer SHALL match proposed rows to the published ETF catalog by case-insensitive normalized ISIN. Rows whose ISIN is absent from the catalog SHALL remain visible as unmatched and SHALL be excluded from the applied portfolio.

#### Scenario: ISIN matches the catalog
- **WHEN** an extracted ISIN exists in the current ETF catalog
- **THEN** the row displays the catalog ETF identity and is eligible for inclusion

#### Scenario: ISIN is not in the catalog
- **WHEN** an extracted ISIN does not exist in the current ETF catalog
- **THEN** the row is marked unmatched, remains visible with its raw values, and cannot be included

### Requirement: Review and edit proposed import values
Before applying an import, the application SHALL show a review dialog containing every extracted row, its match status, and editable inclusion, shares, price, and currency fields. The dialog SHALL show calculated value and CHF-normalized value for each included valid row using the selected source currency, exactly two decimal places, and apostrophe-separated thousands for displayed monetary values, with an explicit fixed conversion of `1 EUR = 1 CHF`.

#### Scenario: User corrects an extracted row
- **WHEN** the user edits shares, price, or currency in the review dialog
- **THEN** the row's value and CHF value recalculate immediately and display exactly two decimal places with apostrophe-separated thousands

#### Scenario: User excludes a matched row
- **WHEN** the user clears the inclusion control for a matched row
- **THEN** the row is omitted from the replacement portfolio while other included rows remain eligible

#### Scenario: Review is canceled
- **WHEN** the user closes or cancels the review dialog
- **THEN** the existing portfolio remains unchanged and no imported values are persisted

### Requirement: Replace and persist the confirmed portfolio
The application SHALL replace the complete existing portfolio only when the user confirms the review with at least one valid, included catalog-matched row. Each applied position SHALL persist its ISIN, shares, price, currency, calculated value, and CHF-normalized value across reloads.

#### Scenario: User confirms a reviewed import
- **WHEN** the user confirms a review containing valid included matched rows
- **THEN** the existing portfolio is replaced atomically by those rows and all Portfolio, Compare, and Explore views rerender from the new positions

#### Scenario: Review has no applicable rows
- **WHEN** the user confirms with no valid included catalog-matched rows
- **THEN** the application reports that no positions can be imported and preserves the existing portfolio

#### Scenario: Imported values survive reload
- **WHEN** the application reloads after a confirmed import
- **THEN** the imported shares, price, currency, value, and CHF value are restored from local storage

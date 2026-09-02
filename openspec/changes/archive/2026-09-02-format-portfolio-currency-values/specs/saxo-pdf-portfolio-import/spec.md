## MODIFIED Requirements

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

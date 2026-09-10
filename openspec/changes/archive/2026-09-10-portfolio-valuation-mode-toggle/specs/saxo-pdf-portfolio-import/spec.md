## ADDED Requirements

### Requirement: Initialize portfolio valuation mode from import review
The Saxo import review SHALL use the selected valuation basis as the initial portfolio-level valuation mode when the user confirms a valid import, while retaining imported price, value, currency, and CHF-normalized fields for later switching and fallback.

#### Scenario: Import latest valuation
- **WHEN** the user selects latest published valuation and confirms valid imported rows
- **THEN** the new full portfolio starts in latest mode and retains all imported fields

#### Scenario: Import broker valuation
- **WHEN** the user selects imported valuation and confirms valid imported rows
- **THEN** the new full portfolio starts in imported mode and retains all imported fields

#### Scenario: Cancel does not change mode
- **WHEN** the user cancels the import review
- **THEN** neither the existing portfolio nor its valuation mode changes

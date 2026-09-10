## MODIFIED Requirements

### Requirement: Review and edit proposed import values
Before applying an import, the application SHALL show a review dialog containing every extracted row, its match status, and editable inclusion, shares, price, and currency fields. The dialog SHALL show calculated value and CHF-normalized value for each included valid row using the selected source currency, current supported FX data when current valuation is selected, exactly two decimal places, and apostrophe-separated thousands for displayed monetary values. The dialog SHALL preserve the imported value for hybrid fallback.

#### Scenario: User corrects an extracted row
- **WHEN** the user edits shares, price, or currency in the review dialog
- **THEN** the row's imported value and effective CHF value recalculate immediately using the selected valuation mode and display exactly two decimal places with apostrophe-separated thousands

#### Scenario: User chooses imported valuation
- **WHEN** the user selects imported valuation during review
- **THEN** the confirmed position uses the broker-imported price/value and retains the imported CHF value as its effective value

#### Scenario: User chooses latest valuation
- **WHEN** the user selects latest valuation during review and a valid live quote and FX rate exist
- **THEN** the confirmed position uses live valuation while retaining the imported fields for fallback

#### Scenario: Review is canceled
- **WHEN** the user closes or cancels the review dialog
- **THEN** the existing portfolio remains unchanged and no imported or live valuation choice is persisted

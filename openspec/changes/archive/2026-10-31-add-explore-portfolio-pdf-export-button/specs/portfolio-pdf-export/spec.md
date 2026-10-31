# Spec Delta

## MODIFIED Requirements

### Requirement: Configure report scope and allocation-only output
The app SHALL provide an accessible Export view with scope choices for the current portfolio and the full ETF catalog, defaulting to the current portfolio, and an allocation-only output switch. The Export view SHALL be available from the global application utility bar and from a labeled action near the top of the Explore / Aggregated portfolio view.

#### Scenario: Export view is opened
- **WHEN** the user activates the export icon in the application utility bar
- **THEN** the app opens its Export view without changing the current portfolio, valuation mode, or color-mode preference

#### Scenario: Explore export action is visible before portfolio insights
- **WHEN** the user views the Explore / Aggregated portfolio view at a supported viewport width
- **THEN** a labeled portfolio-PDF export action is available near the top of the view before its insight sections

#### Scenario: Export view is opened from Explore
- **WHEN** the user activates the labeled portfolio-PDF export action in Explore
- **THEN** the app opens the same Export view as the global utility-bar icon without changing the current portfolio, valuation mode, or color-mode preference
- **AND** the current portfolio scope is selected

#### Scenario: Default report scope
- **WHEN** the Export view opens without a report-scope preference for the current export session
- **THEN** the current portfolio scope is selected

#### Scenario: Full catalog report
- **WHEN** the user selects the full ETF catalog scope
- **THEN** the report lists every ETF in the published catalog while calculated portfolio analytics remain limited to ETFs in the current portfolio

#### Scenario: Allocation-only output
- **WHEN** the user enables allocation-only output
- **THEN** the report omits share quantities, unit prices, and monetary values while retaining portfolio allocation percentages and their dependent analytics
- **AND** the option does not change or persist the portfolio's entry mode or valuation mode

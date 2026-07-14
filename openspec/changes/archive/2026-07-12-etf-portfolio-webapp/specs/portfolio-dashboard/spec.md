## ADDED Requirements

### Requirement: Static ETF data source
The system MUST load supported ETF data from backend-generated snapshot JSON and MUST NOT require live calls to external ETF provider APIs at runtime.

#### Scenario: Load portfolio data from snapshot files
- **WHEN** the user opens the application
- **THEN** the system SHALL populate the ETF catalog from the available snapshot data set
- **AND THEN** the system SHALL be able to operate without live network access to ETF provider endpoints

### Requirement: Portfolio entry and persistence
The system MUST allow the user to build a portfolio by selecting supported ETFs and entering a share count for each position, and it MUST persist the portfolio in the browser between sessions.

#### Scenario: Add and save a position
- **WHEN** the user selects a supported ETF and enters a share count
- **THEN** the system SHALL add the position to the portfolio
- **AND THEN** the system SHALL retain the portfolio after the browser is reloaded

#### Scenario: Edit or remove a position
- **WHEN** the user changes the share count or removes a position
- **THEN** the system SHALL update the portfolio immediately
- **AND THEN** the saved browser state SHALL reflect the change

### Requirement: Comparison charts for selected ETFs
The system MUST provide a comparison view that renders sector, region, and currency composition for selected ETFs using Chart.js doughnut charts, including concentric multi-ring charts when multiple ETFs are compared.

#### Scenario: Compare multiple ETFs
- **WHEN** the user selects two or more ETFs for comparison
- **THEN** the system SHALL display sector, region, and currency charts for the selected ETFs
- **AND THEN** at least one of those charts SHALL support multiple concentric rings to distinguish ETF compositions

#### Scenario: Compare a single ETF
- **WHEN** the user selects only one ETF for comparison
- **THEN** the system SHALL still display the sector, region, and currency composition for that ETF

### Requirement: Aggregated portfolio exposure
The system MUST compute aggregated portfolio exposure across all positions by weighting each ETF by its portfolio position size and combining the underlying holdings into a single ranked company exposure view.

#### Scenario: Rank company exposure across overlapping ETFs
- **WHEN** the user portfolio contains ETFs that share underlying companies such as Novartis or Nestle
- **THEN** the system SHALL sum the indirect exposure for each company across all portfolio positions
- **AND THEN** the system SHALL rank the companies from largest exposure to smallest exposure
- **AND THEN** the system SHALL express each company as a percentage of the whole portfolio

#### Scenario: Identify duplicated company exposure
- **WHEN** a company appears in more than one ETF in the portfolio
- **THEN** the system SHALL indicate that the company is present in multiple ETFs

### Requirement: Weighted portfolio rollups
The system MUST aggregate sector, region, and currency exposure for the full portfolio using the portfolio position weights, so the totals reflect the relative size of each ETF holding.

#### Scenario: Combine sector exposure across positions
- **WHEN** the user portfolio contains multiple ETFs with different sector mixes
- **THEN** the system SHALL produce a portfolio-level sector breakdown weighted by each ETF position size

#### Scenario: Combine region and currency exposure across positions
- **WHEN** the user portfolio contains multiple ETFs with different region and currency mixes
- **THEN** the system SHALL produce portfolio-level region and currency breakdowns weighted by each ETF position size

### Requirement: Responsive browser UI and local dev server
The system MUST provide a responsive browser interface that is usable on smartphone-sized screens and a local development server for desktop testing.

#### Scenario: Use on a smartphone screen
- **WHEN** the application is opened on a narrow mobile viewport
- **THEN** the layout SHALL remain usable without horizontal scrolling for the main workflow

#### Scenario: Run locally on desktop
- **WHEN** a developer starts the local development server
- **THEN** the web application SHALL be available in a desktop browser for testing

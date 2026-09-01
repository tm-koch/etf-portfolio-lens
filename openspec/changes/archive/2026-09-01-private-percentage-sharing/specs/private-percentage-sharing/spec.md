## ADDED Requirements

### Requirement: Create a private percentage-only share link

The Portfolio tab SHALL provide an accessible private sharing action that calculates each selected ETF's current derived portfolio weight, stores that weight as relative `shares` units, and encodes only each ETF ISIN and relative unit value in a versioned URL fragment. The private payload MUST NOT contain share counts from the source portfolio, prices, currencies, monetary values, or CHF-normalized values.

#### Scenario: Share a populated portfolio privately

- **WHEN** the user activates private sharing with one or more selected positions
- **THEN** the application creates a versioned private payload containing every selected ETF ISIN and its derived relative allocation units, and reveals the generated share-link fallback as in the existing sharing flow

#### Scenario: Private link contains no absolute valuation data

- **WHEN** a private share payload is decoded
- **THEN** every position contains only its ISIN and relative `shares` unit, with no price, currency, value, or valueChf field

#### Scenario: Share an empty portfolio privately

- **WHEN** the user activates private sharing with no selected positions
- **THEN** the application reports that there is no portfolio to share and does not create a private link

### Requirement: Load a private percentage-only portfolio

The application SHALL recognize a valid private payload during startup, load its ETF positions as relative weighting units, select the Portfolio tab, and resolve all derived exposure using the latest deployed catalog and snapshots.

#### Scenario: Valid private link is present

- **WHEN** the application starts with a supported private payload
- **THEN** the encoded positions become the active portfolio, private mode is retained in state and local persistence, and the Portfolio tab is selected

#### Scenario: Private payload overrides local state

- **WHEN** both a valid private payload and a different local portfolio exist
- **THEN** the private payload replaces the local portfolio for the current browser

#### Scenario: Latest published data resolves a private portfolio

- **WHEN** snapshots finish loading for a valid private portfolio
- **THEN** Portfolio, Compare, and Explore views calculate using the encoded relative units and the latest deployed ETF data

### Requirement: Validate private allocation units

The application SHALL accept private positions only when the payload has a supported version and private mode marker, contains a duplicate-free array of valid ISINs, and contains finite non-negative relative `shares` units with at least one positive unit. The application SHALL treat malformed private payloads as non-fatal and SHALL reject partial private state.

#### Scenario: Invalid private payload is ignored

- **WHEN** a private payload is malformed, unsupported, contains duplicate or invalid ISINs, or contains invalid unit values
- **THEN** the application preserves the local portfolio and reports that the shared link could not be loaded

#### Scenario: Edited private units are normalized

- **WHEN** a recipient changes one or more private Shares inputs
- **THEN** the application recalculates the total relative units and derives each ETF's displayed and aggregated weight from its unit divided by the total unit sum

### Requirement: Keep the existing portfolio GUI for private mode

The application SHALL use the existing selected-position table and Shares inputs for private portfolios and SHALL communicate that the values are relative weighting units through the portfolio hint or share feedback. It SHALL not require a separate percentage allocation editor.

#### Scenario: Private portfolio is displayed

- **WHEN** a recipient opens a valid private link
- **THEN** the existing no-price portfolio presentation remains available, including editable Shares inputs, and price and value cells display the established unavailable state because those fields were not shared

#### Scenario: Private portfolio supports scenario exploration

- **WHEN** a recipient edits a relative Shares unit and the change is valid
- **THEN** the edited portfolio is persisted and all existing portfolio weights, charts, and look-through exposure update from the normalized relative units

### Requirement: Redact absolute summary values in private mode

The application SHALL retain the existing absolute-value summary cards in private mode but SHALL display `0` for share-count totals and `Not available` or the established zero/unavailable representation for monetary totals when the private payload contains no absolute data.

#### Scenario: Private summary does not expose absolute values

- **WHEN** a private portfolio is active
- **THEN** the summary cards remain visible, the Share units card does not expose the source portfolio's share count, and the Total value card does not expose a monetary value

#### Scenario: Full portfolio summary remains unchanged

- **WHEN** a normal local portfolio or version 1 full share link is active
- **THEN** existing share-count and imported monetary summary behavior is preserved

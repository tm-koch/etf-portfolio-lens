## Purpose
Define the versioned, serverless sharing and startup validation contract for ETF portfolios.
## Requirements
### Requirement: Create a shareable portfolio link

The Portfolio tab SHALL provide an accessible share action that serializes the current ETF positions, share counts, and any persisted imported price, currency, value, and CHF-normalized value into a versioned URL fragment without requiring a server-side share service. The fallback share-link label and URL input SHALL remain hidden in both visibility and layout until the share action generates a valid URL.

#### Scenario: Share a populated portfolio

- **WHEN** the user activates the share action with one or more selected positions
- **THEN** the application creates a URL containing a versioned encoded representation of every selected position's ISIN, share count, and available imported valuation fields, and reveals the share-link label and URL input

#### Scenario: Share link is initially hidden

- **WHEN** the Portfolio tab is rendered before the user has generated a share URL
- **THEN** the share-link label and URL input are hidden, occupy no layout space, and the accessible share action remains available

#### Scenario: Share an empty portfolio

- **WHEN** the user activates the share action with no selected positions
- **THEN** the application reports that there is no portfolio to share, does not create a link containing an invalid portfolio, and keeps the share-link label and URL input hidden without reserving layout space

#### Scenario: Clipboard access is available

- **WHEN** the generated link is copied successfully
- **THEN** the application reports that the share link is ready to send and keeps the share-link label and URL input visible with the generated URL

#### Scenario: Clipboard access is unavailable

- **WHEN** the application cannot write to the clipboard
- **THEN** the generated link remains available through a user-operable fallback, the share-link label and URL input are visible, and the application reports that automatic copying was unavailable

### Requirement: Load a shared portfolio during startup

The application SHALL inspect the URL for a supported portfolio share payload during startup and SHALL apply a valid linked portfolio, including optional imported valuation fields, before falling back to the recipient's locally stored portfolio.

#### Scenario: Valid shared portfolio is present

- **WHEN** the application starts with a supported, valid portfolio payload in the URL fragment
- **THEN** the linked positions and valuation fields become `state.portfolio`, are persisted to local storage, and the Portfolio tab is selected

#### Scenario: No shared portfolio is present

- **WHEN** the application starts without a portfolio share payload
- **THEN** the application preserves the existing local-storage portfolio initialization behavior

#### Scenario: Shared portfolio overrides local state

- **WHEN** both a valid shared portfolio and a different local-storage portfolio are present
- **THEN** the valid shared portfolio is loaded and replaces the local-storage portfolio

### Requirement: Validate shared portfolio payloads safely

The application SHALL accept only supported payload versions containing a duplicate-free array of positions with non-empty string ISINs, finite non-negative share counts, and optional finite non-negative imported valuation fields with a supported currency. The application SHALL treat malformed payloads as non-fatal.

#### Scenario: Payload is malformed or unsupported

- **WHEN** the URL fragment cannot be decoded, is not valid JSON, or uses an unsupported version
- **THEN** the application ignores the payload, preserves normal startup, and reports that the shared link could not be loaded

#### Scenario: Payload contains invalid positions

- **WHEN** a decoded payload contains missing identifiers, invalid share counts, invalid valuation fields, duplicate positions, or an invalid portfolio structure
- **THEN** the application rejects the shared portfolio without applying partial state

#### Scenario: Payload contains an unknown ETF identifier

- **WHEN** a valid payload refers to an ISIN not present in the latest deployed catalog
- **THEN** the application preserves that position for display and exposes it through the existing unknown-position or warning behavior

### Requirement: Resolve shared portfolios using latest published data

The application SHALL resolve ETF metadata, holdings, and exposure calculations for a shared portfolio from the latest catalog and snapshots deployed with the application, without requiring historical data retrieval or a share database.

#### Scenario: Latest catalog data is available

- **WHEN** a valid shared portfolio is loaded and the current catalog and snapshots finish loading
- **THEN** all existing Portfolio, Compare, and Explore views calculate from the imported positions using that latest data

#### Scenario: Latest data changes after link creation

- **WHEN** a recipient opens an otherwise valid link after the deployed catalog or snapshots have changed
- **THEN** the ETF selections and share counts remain those encoded in the link while derived exposure reflects the latest deployed data

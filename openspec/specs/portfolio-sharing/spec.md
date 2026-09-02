## Purpose
Define the versioned, serverless sharing and startup validation contract for ETF portfolios.
## Requirements
### Requirement: Create a shareable portfolio link

The Portfolio tab SHALL provide accessible full and private share actions that serialize the current ETF positions into a versioned URL fragment without requiring a server-side share service. A full share action SHALL serialize selected ETF ISINs, share counts, and available persisted imported valuation fields. A private share action SHALL serialize selected ETF ISINs and derived relative weighting units only, excluding all absolute valuation fields. The fallback share-link label and URL input SHALL remain hidden in both visibility and layout until a share action generates a valid URL.

#### Scenario: Share a populated portfolio fully

- **WHEN** the user activates the full share action with one or more selected positions
- **THEN** the application creates a URL containing a versioned encoded representation of every selected position's ISIN, share count, and available imported valuation fields, and reveals the share-link label and URL input

#### Scenario: Share a populated portfolio privately

- **WHEN** the user activates the private share action with one or more selected positions
- **THEN** the application creates a URL containing a supported private representation of every selected position's ISIN and derived relative allocation units, excluding source share counts and all imported valuation fields, and reveals the share-link label and URL input

#### Scenario: Share link is initially hidden

- **WHEN** the Portfolio tab is rendered before the user has generated a share URL
- **THEN** the share-link label and URL input are hidden, occupy no layout space, and the accessible share actions remain available

#### Scenario: Share an empty portfolio

- **WHEN** the user activates either share action with no selected positions
- **THEN** the application reports that there is no portfolio to share, does not create a link containing an invalid portfolio, and keeps the share-link label and URL input hidden without reserving layout space

#### Scenario: Clipboard access is available

- **WHEN** the generated link is copied successfully
- **THEN** the application reports that the share link is ready to send and keeps the share-link label and URL input visible with the generated URL

#### Scenario: Clipboard access is unavailable

- **WHEN** the application cannot write to the clipboard
- **THEN** the generated link remains available through a user-operable fallback, the share-link label and URL input are visible, and the application reports that automatic copying was unavailable

### Requirement: Load a shared portfolio during startup

The application SHALL inspect the URL for a supported portfolio share payload during startup and SHALL apply a valid linked portfolio before falling back to the recipient's locally stored portfolio. A full payload SHALL restore its optional imported valuation fields. A private payload SHALL restore only relative weighting units, retain private mode, and contain no absolute valuation fields.

#### Scenario: Valid full shared portfolio is present

- **WHEN** the application starts with a supported full portfolio payload in the URL fragment
- **THEN** the linked positions and valuation fields become state.portfolio, are persisted to local storage, and the Portfolio tab is selected

#### Scenario: Valid private shared portfolio is present

- **WHEN** the application starts with a supported private portfolio payload in the URL fragment
- **THEN** the linked positions and relative units become state.portfolio, private mode is persisted, no absolute valuation fields are restored, and the Portfolio tab is selected

#### Scenario: No shared portfolio is present

- **WHEN** the application starts without a portfolio share payload
- **THEN** the application preserves the existing local-storage portfolio initialization behavior

#### Scenario: Shared portfolio overrides local state

- **WHEN** both a valid shared portfolio and a different local-storage portfolio are present
- **THEN** the valid shared portfolio is loaded and replaces the local-storage portfolio

### Requirement: Validate shared portfolio payloads safely

The application SHALL accept only supported payload versions containing a duplicate-free array of positions with non-empty string ISINs and finite non-negative numeric weighting data. Full payloads SHALL validate share counts and optional finite non-negative imported valuation fields with a supported currency. Private payloads SHALL validate the private mode marker and relative unit values, and SHALL not accept absolute valuation fields as private data. The application SHALL treat malformed payloads as non-fatal.

#### Scenario: Payload is malformed or unsupported

- **WHEN** the URL fragment cannot be decoded, is not valid JSON, or uses an unsupported version or mode
- **THEN** the application ignores the payload, preserves normal startup, and reports that the shared link could not be loaded

#### Scenario: Payload contains invalid positions

- **WHEN** a decoded payload contains missing identifiers, invalid numeric weighting data, invalid valuation fields for a full payload, duplicate positions, or an invalid portfolio structure
- **THEN** the application rejects the shared portfolio without applying partial state

#### Scenario: Private payload contains absolute values

- **WHEN** a decoded private payload contains price, currency, value, or valueChf fields
- **THEN** the application does not restore those fields into the private portfolio and treats the private representation as invalid if its privacy contract is violated

#### Scenario: Payload contains an unknown ETF identifier

- **WHEN** a valid payload refers to an ISIN not present in the latest deployed catalog
- **THEN** the application preserves that position for display and exposes it through the existing unknown-position or warning behavior

### Requirement: Resolve shared portfolios using latest published data

The application SHALL resolve ETF metadata, holdings, and exposure calculations for full and private shared portfolios from the latest catalog and snapshots deployed with the application, without requiring historical data retrieval or a share database. Private portfolio calculations SHALL use normalized relative units rather than any absolute valuation data.

#### Scenario: Latest catalog data is available

- **WHEN** a valid full or private shared portfolio is loaded and the current catalog and snapshots finish loading
- **THEN** all existing Portfolio, Compare, and Explore views calculate from the imported positions using that latest data

#### Scenario: Latest data changes after link creation

- **WHEN** a recipient opens an otherwise valid full or private link after the deployed catalog or snapshots have changed
- **THEN** the ETF selections and encoded weighting data remain those encoded in the link while derived exposure reflects the latest deployed data

### Requirement: Clear shared-portfolio feedback after portfolio changes

After a valid shared portfolio has been loaded and its share-loading feedback is displayed, the application SHALL clear that feedback after any successful mutation of the current portfolio. Mutations include replacing the portfolio through confirmed PDF import, adding a new ETF position, changing an existing position's share count, and removing an ETF position. Clearing the feedback SHALL NOT remove or rewrite the portfolio share URL fragment.

#### Scenario: Editing shares clears private-load feedback

- **WHEN** a user changes the share count of an existing position in a private portfolio loaded from a share link
- **THEN** the private portfolio loaded feedback SHALL no longer be displayed, and the share URL fragment SHALL remain unchanged

#### Scenario: Adding an ETF clears private-load feedback

- **WHEN** a user adds a new ETF position to a private portfolio loaded from a share link
- **THEN** the private portfolio loaded feedback SHALL no longer be displayed, and the share URL fragment SHALL remain unchanged

#### Scenario: Removing an ETF clears private-load feedback

- **WHEN** a user removes an ETF position from a private portfolio loaded from a share link
- **THEN** the private portfolio loaded feedback SHALL no longer be displayed, and the share URL fragment SHALL remain unchanged

#### Scenario: Confirming a PDF import clears private-load feedback

- **WHEN** a user confirms a valid PDF import that replaces a private portfolio loaded from a share link
- **THEN** the private portfolio loaded feedback SHALL no longer be displayed, and the share URL fragment SHALL remain unchanged

#### Scenario: Non-mutating import actions preserve feedback

- **WHEN** a user opens or cancels PDF import review without confirming a portfolio replacement
- **THEN** the existing private portfolio loaded feedback SHALL remain unchanged

#### Scenario: Refresh reloads the original shared portfolio

- **WHEN** the browser is refreshed after a portfolio mutation while the original share URL fragment remains present
- **THEN** the application SHALL reload the original portfolio encoded in that URL and SHALL display the corresponding shared-portfolio feedback again

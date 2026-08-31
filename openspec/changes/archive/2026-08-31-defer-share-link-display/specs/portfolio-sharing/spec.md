## MODIFIED Requirements

### Requirement: Create a shareable portfolio link

The Portfolio tab SHALL provide an accessible share action that serializes the current ETF positions, share counts, and any persisted imported price, currency, value, and CHF-normalized value into a versioned URL fragment without requiring a server-side share service. The fallback share-link label and URL input SHALL remain hidden until the share action generates a valid URL.

#### Scenario: Share a populated portfolio

- **WHEN** the user activates the share action with one or more selected positions
- **THEN** the application creates a URL containing a versioned encoded representation of every selected position's ISIN, share count, and available imported valuation fields, and reveals the share-link label and URL input

#### Scenario: Share link is initially hidden

- **WHEN** the Portfolio tab is rendered before the user has generated a share URL
- **THEN** the share-link label and URL input are hidden while the accessible share action remains available

#### Scenario: Share an empty portfolio

- **WHEN** the user activates the share action with no selected positions
- **THEN** the application reports that there is no portfolio to share, does not create a link containing an invalid portfolio, and keeps the share-link label and URL input hidden

#### Scenario: Clipboard access is available

- **WHEN** the generated link is copied successfully
- **THEN** the application reports that the share link is ready to send and keeps the share-link label and URL input visible with the generated URL

#### Scenario: Clipboard access is unavailable

- **WHEN** the application cannot write to the clipboard
- **THEN** the generated link remains available through a user-operable fallback, the share-link label and URL input are visible, and the application reports that automatic copying was unavailable

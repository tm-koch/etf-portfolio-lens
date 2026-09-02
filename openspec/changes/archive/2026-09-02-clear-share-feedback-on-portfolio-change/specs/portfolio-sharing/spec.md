## ADDED Requirements

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

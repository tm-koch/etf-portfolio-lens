## ADDED Requirements

### Requirement: Publish the live-price artifact
The GitHub Pages publishing process SHALL copy the validated `data/live_prices.json` artifact to the published root data tree and SHALL fail before pushing when the required artifact is missing or invalid.

#### Scenario: Live artifact is published
- **WHEN** a valid live-data artifact exists during publication
- **THEN** the deployed site exposes it at `data/live_prices.json` alongside the catalog and snapshots

#### Scenario: Live artifact is invalid
- **WHEN** the live-data artifact is missing, malformed, incomplete, or contains prohibited secret/source fields
- **THEN** publication exits unsuccessfully and does not push an invalid Pages tree

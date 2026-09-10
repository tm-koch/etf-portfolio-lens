## MODIFIED Requirements

### Requirement: Publish the live-price artifact
The GitHub Pages publishing process SHALL consume the validated `data/live_prices.json` artifact from the publication workspace, copy it to the published root data tree, and push the resulting site tree to the configured `gh-pages` branch. It SHALL fail before pushing when the required artifact is missing or invalid, and it SHALL not require or create a generated-data commit on `main`.

#### Scenario: Live artifact is published

- **WHEN** a valid live-data artifact exists in the publication workspace
- **THEN** the deployed `gh-pages` site exposes it at `data/live_prices.json` alongside the catalog and snapshots, without requiring a corresponding generated-data update on `main`

#### Scenario: Live artifact is invalid

- **WHEN** the live-data artifact is missing, malformed, incomplete, or contains prohibited secret/source fields
- **THEN** publication exits unsuccessfully before pushing and does not publish an invalid Pages tree

#### Scenario: Pages branch receives the publication

- **WHEN** the workflow completes live-data generation and validation successfully
- **THEN** the publisher pushes the assembled site to `origin/gh-pages` while the workflow does not commit or push the generated artifact to `main`

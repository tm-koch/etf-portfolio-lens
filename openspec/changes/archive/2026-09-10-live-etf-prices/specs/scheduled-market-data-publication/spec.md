## ADDED Requirements

### Requirement: Run the scheduled market-data workflow
The repository SHALL provide a GitHub Actions workflow with manual dispatch and a daily schedule at 21:00 UTC, representing fixed 22:00 CET (UTC+1) year-round.

#### Scenario: Scheduled run starts
- **WHEN** the configured daily schedule reaches its declared execution time
- **THEN** the workflow runs the live quote and FX update command with the required repository permissions and secrets

#### Scenario: Manual run starts
- **WHEN** an authorized user manually dispatches the workflow
- **THEN** the same validation and publication pipeline runs without weakening failure or secret-handling rules

### Requirement: Keep provider configuration secret
The workflow SHALL make each configured quote-template secret available to the fetch command, SHALL redact secret values from logs, and SHALL publish no provider URL, credential, raw response, or provider identity.

#### Scenario: Public artifact is inspected
- **WHEN** the generated live-data JSON and build metadata are published
- **THEN** they contain normalized quote/FX data and timestamps but no source URL or secret value

### Requirement: Publish updates atomically
The workflow SHALL publish a new live-data artifact and dated commit only after every required quote, parser validation, and FX retrieval succeeds. If any required operation fails, the workflow SHALL exit unsuccessfully and preserve the previous artifact and published site.

#### Scenario: One source fails
- **WHEN** any configured ETF source or required FX source fails or produces invalid data
- **THEN** the workflow publishes no new prices, creates no successful update commit, and leaves the previous live-data artifact available

#### Scenario: Complete update succeeds
- **WHEN** all configured quotes and FX rates validate successfully
- **THEN** the workflow writes the artifact, commits with the update date, and invokes the GitHub Pages publisher

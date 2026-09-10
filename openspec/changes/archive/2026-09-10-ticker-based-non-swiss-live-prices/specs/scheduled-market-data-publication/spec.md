## MODIFIED Requirements

### Requirement: Run the scheduled market-data workflow
The repository SHALL provide a GitHub Actions workflow with manual dispatch, a daily schedule at 21:00 UTC representing fixed 22:00 CET (UTC+1) year-round, and a push trigger limited to relevant changes on `main`. Relevant changes include live-data source/configuration, workflow, backend, parser, and publication inputs; generated `data/live_prices.json` changes SHALL be excluded from the push paths.

#### Scenario: Scheduled run starts
- **WHEN** the configured daily schedule reaches its declared execution time
- **THEN** the workflow runs the live quote and FX update command with the required repository permissions and secrets

#### Scenario: Manual run starts
- **WHEN** an authorized user manually dispatches the workflow
- **THEN** the same validation and publication pipeline runs without weakening failure or secret-handling rules

#### Scenario: Relevant main push starts
- **WHEN** a relevant live-data, configuration, workflow, backend, parser, or publication input changes on `main`
- **THEN** the workflow runs the same validation and publication pipeline

#### Scenario: Generated artifact push does not restart the workflow
- **WHEN** the workflow commits only the generated `data/live_prices.json` artifact
- **THEN** the push trigger does not start another live-data workflow run

### Requirement: Keep provider configuration secret
The workflow SHALL make each configured quote-template secret available to the fetch command, including `YAHOO_QUOTE_URL_TEMPLATE` for ticker-based entries, SHALL redact secret values from logs, and SHALL publish no provider URL, credential, raw response, or provider identity.

#### Scenario: Public artifact is inspected
- **WHEN** the generated live-data JSON and build metadata are published
- **THEN** they contain normalized quote/FX data and timestamps but no source URL or secret value

#### Scenario: Yahoo template is available at runtime
- **WHEN** a configured ticker-based quote is fetched in CI
- **THEN** the workflow resolves `YAHOO_QUOTE_URL_TEMPLATE` from the repository secret mapping and passes it to the fetch command without writing its value to logs or artifacts

### Requirement: Publish updates atomically
The workflow SHALL publish a new live-data artifact and dated commit only after every required quote, parser validation, and FX retrieval succeeds. If any required operation fails, the workflow SHALL exit unsuccessfully and preserve the previous artifact and published site.

#### Scenario: One source fails
- **WHEN** any configured ETF source or required FX source fails or produces invalid data
- **THEN** the workflow publishes no new prices, creates no successful update commit, and leaves the previous live-data artifact available

#### Scenario: Complete update succeeds
- **WHEN** all configured Swiss and ticker-based quotes and FX rates validate successfully
- **THEN** the workflow writes the artifact, commits with the update date, and invokes the GitHub Pages publisher

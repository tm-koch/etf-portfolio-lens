## MODIFIED Requirements

### Requirement: Run the scheduled market-data workflow
The repository SHALL provide a GitHub Actions workflow with manual dispatch, a daily schedule at 21:00 UTC representing fixed 22:00 CET (UTC+1) year-round, and a push trigger limited to relevant changes on `main`. Relevant changes include live-data source/configuration, workflow, backend, parser, and publication inputs; generated `data/live_prices.json` changes SHALL be excluded from the push paths. The workflow SHALL generate and validate live data in the Actions workspace and SHALL invoke the GitHub Pages publisher without committing or pushing the generated artifact to `main`.

#### Scenario: Scheduled run starts

- **WHEN** the configured daily schedule reaches its declared execution time
- **THEN** the workflow runs the live quote and FX update command with the required repository permissions and secrets

#### Scenario: Manual run starts

- **WHEN** an authorized user manually dispatches the workflow
- **THEN** the same validation and publication pipeline runs without weakening failure or secret-handling rules

#### Scenario: Relevant main push starts

- **WHEN** a relevant live-data, configuration, workflow, backend, parser, or publication input changes on `main`
- **THEN** the workflow runs the same validation and publication pipeline

#### Scenario: Generated artifact does not update main

- **WHEN** the workflow successfully generates and validates `data/live_prices.json`
- **THEN** the workflow invokes the Pages publisher without creating a generated-data commit or pushing the artifact to `main`

### Requirement: Publish updates atomically
The workflow SHALL publish a new live-data artifact to the GitHub Pages branch only after every required quote, parser validation, and FX retrieval succeeds. If any required operation fails, the workflow SHALL exit unsuccessfully, SHALL not push a new Pages publication, SHALL not create a generated-data commit on `main`, and SHALL preserve the previous artifact and published site.

#### Scenario: One source fails

- **WHEN** any configured ETF source or required FX source fails or produces invalid data
- **THEN** the workflow publishes no new prices, creates no generated-data commit on `main`, and leaves the previous live-data artifact and published site available

#### Scenario: Complete update succeeds

- **WHEN** all configured Swiss and ticker-based quotes and FX rates validate successfully
- **THEN** the workflow writes the validated artifact in the Actions workspace, publishes it to the GitHub Pages branch, and leaves `main` unchanged

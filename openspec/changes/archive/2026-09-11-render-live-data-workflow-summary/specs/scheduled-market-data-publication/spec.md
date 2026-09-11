## MODIFIED Requirements

### Requirement: Run the scheduled market-data workflow

The repository SHALL provide a GitHub Actions workflow with manual dispatch, a daily schedule at 21:00 UTC representing fixed 22:00 CET (UTC+1) year-round, and a push trigger limited to relevant changes on `main`. Relevant changes include live-data source/configuration, workflow, backend, parser, and publication inputs; generated `data/live_prices.json` changes SHALL be excluded from the push paths. The workflow SHALL generate and validate live data in the Actions workspace, SHALL render a Markdown summary from the validated artifact, SHALL expose that Markdown as a named step output, and SHALL invoke the GitHub Pages publisher without committing or pushing the generated artifact to `main`.

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

#### Scenario: Validated data is rendered in the workflow summary

- **WHEN** the generated live-data artifact passes validation
- **THEN** the workflow run summary contains a Markdown quote table with every configured quote's ISIN and price including currency, an exchange-rate table with every FX pair and rate, the artifact generation timestamp, and `Unavailable` for unavailable values

#### Scenario: Summary Markdown is available as a workflow output

- **WHEN** the summary report step completes successfully
- **THEN** the exact Markdown written to the rendered step summary is available through its named GitHub Actions step output

#### Scenario: Summary generation fails safely

- **WHEN** the validated artifact cannot be parsed or formatted into the required report
- **THEN** the workflow fails before publication and does not invoke the GitHub Pages publisher

### Requirement: Keep provider configuration secret

The workflow SHALL make each configured quote-template secret available to the fetch command, including `YAHOO_QUOTE_URL_TEMPLATE` for ticker-based entries, SHALL redact secret values from logs, and SHALL publish no provider URL, credential, raw response, or provider identity.

#### Scenario: Public artifact is inspected

- **WHEN** the generated live-data JSON and build metadata are published
- **THEN** they contain normalized quote/FX data and timestamps but no source URL or secret value

#### Scenario: Yahoo template is available at runtime

- **WHEN** a configured ticker-based quote is fetched in CI
- **THEN** the workflow resolves `YAHOO_QUOTE_URL_TEMPLATE` from the repository secret mapping and passes it to the fetch command without writing its value to logs or artifacts

### Requirement: Publish updates atomically

The workflow SHALL publish a new live-data artifact to the GitHub Pages branch only after every required quote, parser validation, and FX retrieval succeeds. If any required operation fails, the workflow SHALL exit unsuccessfully, SHALL not push a new Pages publication, SHALL not create a generated-data commit on `main`, and SHALL preserve the previous artifact and published site.

#### Scenario: One source fails

- **WHEN** any configured ETF source or required FX source fails or produces invalid data
- **THEN** the workflow publishes no new prices, creates no generated-data commit on `main`, and leaves the previous live-data artifact and published site available

#### Scenario: Complete update succeeds

- **WHEN** all configured Swiss and ticker-based quotes and FX rates validate successfully
- **THEN** the workflow writes the validated artifact in the Actions workspace, renders the report, publishes it to the GitHub Pages branch, and leaves `main` unchanged

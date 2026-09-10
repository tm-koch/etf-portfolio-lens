## MODIFIED Requirements

### Requirement: Normalize live ETF quotes
The live-data pipeline SHALL produce a versioned JSON artifact containing at least one normalized quote record per configured ETF, with ISIN, numeric price, currency, quote timestamp, trading date when available, status, and provider lookup ticker when the configured adapter requires one. Provider URLs, credentials, raw responses, and provider identities SHALL NOT appear in the artifact. The artifact SHALL remain keyed by ISIN.

#### Scenario: Swiss CSV quote is normalized
- **WHEN** a configured Swiss ETF source returns a valid dated CSV containing `Time;Price;Volume` rows
- **THEN** the pipeline selects the greatest valid combined timestamp and writes its numeric price and currency to the normalized artifact keyed by the ETF ISIN

#### Scenario: Yahoo ticker quote is normalized
- **WHEN** a configured ticker-based source returns a valid chart response with a finite non-negative EUR market price and Unix quote timestamp
- **THEN** the pipeline writes the price, EUR currency, UTC timestamp, configured ticker, and ETF ISIN to the normalized artifact under the ETF ISIN key

#### Scenario: No valid quote exists
- **WHEN** a configured source returns no row or response with a valid timestamp and non-negative finite price
- **THEN** the pipeline fails the run and does not replace the previously published artifact

### Requirement: Support provider-specific quote adapters
The pipeline SHALL select a quote URL formatter and parser by configuration so providers can use different response formats and lookup identifiers without changing the normalized artifact contract. Each configured ETF SHALL identify its own secret-backed URL template environment name and adapter. An adapter that requires a ticker SHALL have a configured ticker, and an adapter that requires an ISIN SHALL use the configured ETF ISIN.

#### Scenario: ISIN is inserted into a secret URL template
- **WHEN** a configured ISIN-based adapter is invoked for an ETF ISIN
- **THEN** the runtime reads that ETF's secret-backed URL template, formats it with the ISIN, dispatches to the configured adapter, and does not persist the resolved URL

#### Scenario: Ticker is inserted into a secret URL template
- **WHEN** a configured ticker-based adapter is invoked for an ETF with ticker `EUMD.L`
- **THEN** the runtime reads the configured ticker-template secret, formats it with `EUMD.L`, dispatches to the ticker adapter, and does not persist the resolved URL

#### Scenario: Missing required ticker is rejected
- **WHEN** a ticker-based quote entry has no ticker or has an empty ticker
- **THEN** configuration validation fails before a request is made

#### Scenario: Local test supplies the Swiss template
- **WHEN** the fetch command receives an explicit Swiss URL-template parameter
- **THEN** it uses that parameter for every configured Swiss ETF without requiring a repository secret

### Requirement: Parse and validate ticker-based chart responses
The ticker-based adapter SHALL parse the chart response's regular market price, currency metadata, and Unix market timestamp. It SHALL reject provider-reported errors, missing required chart metadata, unsupported currency, non-finite or negative prices, and invalid timestamps.

#### Scenario: Valid EUR chart response is accepted
- **WHEN** the chart response contains EUR metadata, a finite non-negative regular market price, and a valid Unix market timestamp
- **THEN** the adapter returns a normalized quote with the configured ISIN, ticker, EUR currency, numeric price, and UTC quote timestamp

#### Scenario: Chart provider error is rejected
- **WHEN** the chart response contains a provider error or omits the required result metadata
- **THEN** the adapter reports a quote failure and the pipeline does not publish a replacement artifact

#### Scenario: Unsupported or invalid chart data is rejected
- **WHEN** the chart response currency is not EUR, the price is negative or non-finite, or the timestamp is invalid
- **THEN** the adapter reports a validation failure and the pipeline does not publish a replacement artifact

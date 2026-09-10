## ADDED Requirements

### Requirement: Normalize live ETF quotes
The live-data pipeline SHALL produce a versioned JSON artifact containing at least one normalized quote record per configured ETF, with ISIN, numeric price, currency, quote timestamp, trading date when available, and status. Provider URLs, credentials, raw responses, and provider identities SHALL NOT appear in the artifact.

#### Scenario: Swiss CSV quote is normalized
- **WHEN** a configured Swiss ETF source returns a valid dated CSV containing `Time;Price;Volume` rows
- **THEN** the pipeline selects the greatest valid combined timestamp and writes its numeric price and currency to the normalized artifact

#### Scenario: No valid quote exists
- **WHEN** a configured source returns no row with a valid timestamp and non-negative finite price
- **THEN** the pipeline fails the run and does not replace the previously published artifact

### Requirement: Support provider-specific quote adapters
The pipeline SHALL select a quote URL formatter and parser by configuration so additional providers can use different response formats without changing the normalized artifact contract. Each configured ETF SHALL identify its own secret-backed URL template environment name and adapter.

#### Scenario: ISIN is inserted into a secret URL template
- **WHEN** a configured adapter is invoked for an ETF ISIN
- **THEN** the runtime reads that ETF's secret-backed URL template, formats it with the ISIN, dispatches to the configured adapter, and does not persist the resolved URL

#### Scenario: Local test supplies the Swiss template
- **WHEN** the fetch command receives an explicit Swiss URL-template parameter
- **THEN** it uses that parameter for every configured Swiss ETF without requiring a repository secret

### Requirement: Normalize supported daily FX reference rates
The pipeline SHALL retrieve and publish timestamped latest daily reference rates for EUR/CHF and USD/CHF from Frankfurter, and SHALL support CHF as an identity conversion currency.

#### Scenario: EUR position is valued in CHF
- **WHEN** a valid EUR/CHF rate exists
- **THEN** the valuation layer converts the EUR quote or imported EUR value to CHF using that rate

#### Scenario: USD position is valued in CHF
- **WHEN** a valid USD/CHF rate exists
- **THEN** the valuation layer converts the USD quote or imported USD value to CHF using that rate

### Requirement: Preserve timestamps without age rejection
The pipeline SHALL retain quote and FX timestamps and SHALL NOT reject an otherwise valid FX or market quote solely because it is older than the current workflow time.

#### Scenario: Weekend execution uses the latest available data
- **WHEN** the action runs on a weekend and the source returns the most recent available quote or FX observation
- **THEN** the data is published with its original timestamp and status rather than being rejected solely for age

### Requirement: Provide hybrid effective valuation
The application SHALL calculate each full-portfolio position using a valid live quote and supported FX rate when available, fall back to the persisted imported CHF-normalized value when live valuation is unavailable, and mark the effective source. A position with neither valid source SHALL remain unavailable.

#### Scenario: Live valuation is available
- **WHEN** a position has shares, a valid published live quote, and a required FX rate
- **THEN** its effective CHF value uses shares multiplied by live price and FX conversion and is marked live

#### Scenario: Live valuation is unavailable
- **WHEN** a position lacks a valid live quote or required FX rate but has a persisted imported CHF value
- **THEN** its effective CHF value uses the imported value and is marked imported fallback

#### Scenario: Both valuations are unavailable
- **WHEN** a position has neither a usable live valuation nor an imported CHF value
- **THEN** its effective value is unavailable and is excluded from monetary totals while remaining visible

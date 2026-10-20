# Spec Delta

## MODIFIED Requirements

### Requirement: Support provider-specific quote adapters
The pipeline SHALL select a quote URL formatter and parser by configuration so providers can use different response formats and lookup identifiers without changing the normalized artifact contract. Each configured ETF SHALL identify its own secret-backed URL template environment name and adapter. An adapter that requires a ticker SHALL have a configured ticker, and an adapter that requires an ISIN SHALL use the configured ETF ISIN. URL templates SHALL support formatting with the configured quote currency when required by the adapter.

#### Scenario: ISIN is inserted into a secret URL template
- **WHEN** a configured ISIN-based adapter is invoked for an ETF ISIN
- **THEN** the runtime reads that ETF's secret-backed URL template, formats it with the ISIN, dispatches to the configured adapter, and does not persist the resolved URL

#### Scenario: Ticker is inserted into a secret URL template
- **WHEN** a configured ticker-based adapter is invoked for an ETF with ticker `EUMD.L`
- **THEN** the runtime reads the configured ticker-template secret, formats it with `EUMD.L`, dispatches to the ticker adapter, and does not persist the resolved URL

#### Scenario: Currency is inserted into a secret URL template
- **WHEN** a configured adapter's URL template contains `{currency}`
- **THEN** the runtime formats that placeholder with the configured quote currency before dispatching to the adapter

#### Scenario: Missing required ticker is rejected
- **WHEN** a ticker-based quote entry has no ticker or has an empty ticker
- **THEN** configuration validation fails before a request is made

#### Scenario: Local test supplies the Swiss template
- **WHEN** the fetch command receives an explicit Swiss URL-template parameter
- **THEN** it uses that parameter for every configured Swiss ETF without requiring a repository secret

## ADDED Requirements

### Requirement: Configure live quotes for refreshable requested ETFs
The live market-data configuration SHALL include normalized quote entries for EIMI and IMEA using their intended quote currencies.

#### Scenario: EIMI quote is configured in USD
- **WHEN** quote configuration is loaded for `IE00BKM4GZ66`
- **THEN** it selects the Swiss CSV adapter and USD quote currency

#### Scenario: IMEA quote is configured in CHF
- **WHEN** quote configuration is loaded for `IE00B4K48X80`
- **THEN** it selects the Swiss CSV adapter and CHF quote currency

### Requirement: Omit live quote for fixture-only UBS entry
The live market-data configuration SHALL NOT include `IE00BD4TXV59` while its registry entry is fixture-only.

#### Scenario: Fixture-only UBS ETF has no automated quote
- **WHEN** live quote configuration is loaded
- **THEN** it contains no quote entry for `IE00BD4TXV59`

### Requirement: Normalize USD Swiss CSV quotes
The Swiss CSV adapter SHALL accept a configured USD quote and publish its normalized record keyed by the configured ETF ISIN.

#### Scenario: EIMI USD quote is normalized
- **WHEN** the configured EIMI source returns a valid dated CSV quote
- **THEN** the artifact contains the numeric price, USD currency, quote timestamp, and ISIN `IE00BKM4GZ66`
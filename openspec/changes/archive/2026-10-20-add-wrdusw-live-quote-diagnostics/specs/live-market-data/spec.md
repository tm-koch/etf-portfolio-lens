# Spec Delta

## MODIFIED Requirements

### Requirement: Omit live quote for fixture-only UBS entry
The live market-data configuration SHALL omit an automated quote for `IE00BD4TXV59` only while no independently supported quote source is configured. Its registry `fixture_only` status SHALL continue to control holdings ingestion and SHALL NOT by itself prohibit a separately configured live quote.

#### Scenario: Fixture-only UBS ETF has no automated quote
- **WHEN** no supported live quote source is configured for `IE00BD4TXV59`
- **THEN** the live quote configuration contains no entry for that ISIN

#### Scenario: CHF live quote is configured independently
- **WHEN** a supported CHF quote source is configured for `IE00BD4TXV59`
- **THEN** the live quote configuration includes it without changing the registry's fixture-only holdings-ingestion status

## ADDED Requirements

### Requirement: Configure a CHF live quote for UBS Core MSCI World
The live market-data configuration SHALL include `IE00BD4TXV59` using the Swiss CSV adapter, CHF currency, and the existing secret-backed Swiss URL template.

#### Scenario: UBS Core MSCI World quote is configured
- **WHEN** quote configuration is loaded
- **THEN** `IE00BD4TXV59` has adapter `swiss_csv_v1`, currency CHF, and the Swiss quote-template secret name

#### Scenario: CHF quote is normalized
- **WHEN** the configured source returns a valid dated Swiss trade CSV for `IE00BD4TXV59`
- **THEN** the artifact contains a CHF quote keyed by `IE00BD4TXV59` and retains its source trade timestamp

### Requirement: Identify quote failures with privacy-safe diagnostics
The live refresh SHALL identify the failing ETF ISIN and adapter when quote fetching or parsing fails, and SHALL keep private URLs, credentials, and raw provider responses out of logs. Debug mode SHALL report per-ETF progress without exposing those private values.

#### Scenario: Swiss CSV parsing failure identifies the ETF
- **WHEN** a configured Swiss CSV response has no recognized trading date
- **THEN** the failure identifies the affected ISIN and adapter while preserving the previous live-price artifact

#### Scenario: Debug mode reports quote progress safely
- **WHEN** the live refresh runs with debug logging enabled
- **THEN** logs identify each quote's ISIN and processing outcome without including a resolved URL, credential, or raw provider response

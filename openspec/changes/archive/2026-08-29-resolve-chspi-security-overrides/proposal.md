## Why

Strict fixture ingestion of the CHSPI ETF currently reports 44 identity failures. Five are intentional cash or collateral rows, but the remaining 39 listed securities are real instruments whose Swiss exchange tickers are absent from, or confused with unrelated instruments in, the downloaded security master. This prevents strict catalog regeneration and risks incorrect identity enrichment if ticker-only matches are accepted.

## What Changes


## Capabilities

### New Capabilities

### Modified Capabilities


## Impact

## ADDED Requirements

### Requirement: Cache published live market data
The service worker SHALL treat the same-origin `data/live_prices.json` artifact as runtime data, use network-first behavior while online, and return a previously cached valid artifact when offline.

#### Scenario: Online live-data refresh
- **WHEN** the application requests `data/live_prices.json` while online
- **THEN** the network response is used and stored in the versioned runtime cache

#### Scenario: Offline live-data fallback
- **WHEN** the application requests live data without network access and a prior artifact is cached
- **THEN** the cached artifact is returned and the UI exposes its generation timestamp

#### Scenario: No live-data cache exists
- **WHEN** live data is unavailable online and no prior artifact is cached
- **THEN** the application keeps imported-value fallback behavior and reports live data as unavailable

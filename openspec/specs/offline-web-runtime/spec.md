# offline-web-runtime Specification

## Purpose
TBD - created by archiving change pwa-android-app. Update Purpose after archive.
## Requirements
### Requirement: Cache the application shell

The service worker SHALL precache the published application shell, manifest, icons, and locally served critical frontend libraries needed to start the app and render its core views.

#### Scenario: First online visit prepares offline startup

- **WHEN** a user loads the published app successfully while online
- **THEN** the service worker installs and caches the required shell resources

#### Scenario: Previously visited app starts offline

- **WHEN** a user revisits the app after the shell has been cached and network access is unavailable
- **THEN** the service worker serves the application shell and the app reaches its normal startup path

### Requirement: Cache runtime catalog and snapshot data

The service worker SHALL use a versioned runtime cache for successful same-origin catalog and ETF snapshot responses, using network-first behavior so an available newer response replaces stale cached data.

#### Scenario: Online data refresh

- **WHEN** the app requests the catalog or an ETF snapshot while online
- **THEN** the request uses the network response and a successful response is stored for later offline use

#### Scenario: Offline data fallback

- **WHEN** the app requests a previously cached catalog or snapshot while offline
- **THEN** the cached response is returned to the application

#### Scenario: Uncached data remains an explicit failure

- **WHEN** the app requests data that is neither available from the network nor present in the runtime cache
- **THEN** the request fails normally and the existing application error state is shown

### Requirement: Update and bound caches

The service worker SHALL identify cache versions explicitly, delete obsolete versions during activation, and apply a bounded retention policy to runtime snapshot entries.

#### Scenario: New release activates

- **WHEN** a newly versioned service worker activates
- **THEN** obsolete application-shell and runtime cache versions are removed while the current caches remain available

#### Scenario: Runtime cache reaches its retention limit

- **WHEN** successful runtime data responses exceed the configured retention policy
- **THEN** older entries are evicted without affecting the application-shell cache

### Requirement: Keep critical offline resources same-origin

The offline startup and PDF import paths SHALL NOT require a third-party CDN response after the app has been installed and its shell has been cached.

#### Scenario: Offline chart and icon rendering

- **WHEN** an installed user opens a cached portfolio offline
- **THEN** chart rendering and icon usage use locally served or cached critical libraries

#### Scenario: Offline PDF import

- **WHEN** an installed user selects a supported local PDF while offline
- **THEN** PDF.js and its worker are available from the local app resources and the import workflow can proceed

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


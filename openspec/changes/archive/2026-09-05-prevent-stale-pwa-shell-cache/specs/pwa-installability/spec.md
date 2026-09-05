## MODIFIED Requirements

### Requirement: Provide an installable web app manifest

The published site SHALL provide a valid same-origin web app manifest with application name and short name `ETF Portfolio Lens`, a stable `id` for the published application, standalone display mode, start URL, theme color, background color, and the supplied valid 192x192 and 512x512 PNG icons copied from `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png`. The manifest SHALL be served as part of the same cache generation as the published document and service worker.

#### Scenario: Browser discovers the manifest

- **WHEN** a browser loads the published site
- **THEN** the document references a same-origin manifest and the manifest responds with valid JSON, the exact application title, stable application identity, required installability fields, and the supplied icon declarations

#### Scenario: Android launches the installed app

- **WHEN** a user launches the installed application
- **THEN** it opens at the configured site start URL in standalone display mode without requiring the browser address bar

#### Scenario: Corrected manifest replaces a stale cached manifest

- **WHEN** a new publication changes the manifest identity or installability metadata
- **THEN** the service-worker update uses a new cache generation and serves the corrected manifest after activation instead of the prior cached manifest

### Requirement: Register a same-origin service worker

The application SHALL register a service worker from the published site root when the browser supports service workers, and registration failure SHALL not prevent normal application startup. The worker SHALL use the cache generation associated with the current publication and SHALL update when cache-sensitive shell assets change.

#### Scenario: Supported browser registers the worker

- **WHEN** the application starts in a secure context
- **THEN** it attempts registration using a same-origin root-scoped service-worker URL

#### Scenario: Unsupported browser remains usable

- **WHEN** service workers are unavailable or registration fails
- **THEN** the existing static application continues to load and operate online

#### Scenario: Worker update receives the current shell

- **WHEN** a controlled browser detects a published service worker with a new cache generation
- **THEN** the new worker activates with the current shell assets and removes obsolete versioned caches

### Requirement: Preserve installed application workflows

The installed PWA SHALL preserve local portfolio persistence, URL-fragment sharing, ETF calculations, charts, responsive navigation, and browser PDF import behavior supported by the target Android browser.

#### Scenario: Existing portfolio opens in standalone mode

- **WHEN** an installed user opens the app with a locally stored portfolio
- **THEN** the portfolio and its derived views load using the same data and state behavior as the browser site

#### Scenario: Shared portfolio opens in standalone mode

- **WHEN** an installed user opens a valid shared portfolio URL
- **THEN** the URL fragment is processed and the linked portfolio loads before local fallback state

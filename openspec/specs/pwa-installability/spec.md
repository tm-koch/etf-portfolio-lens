# pwa-installability Specification

## Purpose
TBD - created by archiving change pwa-android-app. Update Purpose after archive.
## Requirements
### Requirement: Provide an installable web app manifest

The published site SHALL provide a valid same-origin web app manifest with application name and short name `ETF Porfolio Lens`, standalone display mode, start URL, theme color, background color, and the supplied valid 192x192 and 512x512 PNG icons copied from `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png`.

#### Scenario: Browser discovers the manifest

- **WHEN** a browser loads the published site
- **THEN** the document references a same-origin manifest and the manifest responds with valid JSON, the exact application title, required installability fields, and the supplied icon declarations

#### Scenario: Android launches the installed app

- **WHEN** a user launches the installed application
- **THEN** it opens at the configured site start URL in standalone display mode without requiring the browser address bar

### Requirement: Register a same-origin service worker

The application SHALL register a service worker from the published site root when the browser supports service workers, and registration failure SHALL not prevent normal application startup.

#### Scenario: Supported browser registers the worker

- **WHEN** the application starts in a secure context
- **THEN** it attempts registration using a same-origin root-scoped service-worker URL

#### Scenario: Unsupported browser remains usable

- **WHEN** service workers are unavailable or registration fails
- **THEN** the existing static application continues to load and operate online

### Requirement: Preserve installed application workflows

The installed PWA SHALL preserve local portfolio persistence, URL-fragment sharing, ETF calculations, charts, responsive navigation, and browser PDF import behavior supported by the target Android browser.

#### Scenario: Existing portfolio opens in standalone mode

- **WHEN** an installed user opens the app with a locally stored portfolio
- **THEN** the portfolio and its derived views load using the same data and state behavior as the browser site

#### Scenario: Shared portfolio opens in standalone mode

- **WHEN** an installed user opens a valid shared portfolio URL
- **THEN** the URL fragment is processed and the linked portfolio loads before local fallback state


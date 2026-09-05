## MODIFIED Requirements

### Requirement: Provide an installable web app manifest

The published site SHALL provide a valid same-origin web app manifest with application name and short name `ETF Portfolio Lens`, a stable `id` for the published application, standalone display mode, start URL, theme color, background color, and the supplied valid 192x192 and 512x512 PNG icons copied from `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png`.

#### Scenario: Browser discovers the manifest

- **WHEN** a browser loads the published site
- **THEN** the document references a same-origin manifest and the manifest responds with valid JSON, the exact application title, stable application identity, required installability fields, and the supplied icon declarations

#### Scenario: Android launches the installed app

- **WHEN** a user launches the installed application
- **THEN** it opens at the configured site start URL in standalone display mode without requiring the browser address bar

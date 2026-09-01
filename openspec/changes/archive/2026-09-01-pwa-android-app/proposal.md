## Why

ETF Portfolio Lens is already a responsive static web application, but Android users cannot install it as an app or reliably use previously loaded portfolio data when connectivity is unavailable. Adding a standards-based PWA layer creates an installable Android experience while preserving the existing serverless deployment and browser-based portfolio workflows.

## What Changes

- Add a web app manifest titled `ETF Porfolio Lens`, with standalone display configuration, theme colors, and the supplied installable app icons from `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png`.
- Add and register a service worker that caches the application shell and uses runtime caching for the published catalog and ETF snapshots.
- Make critical frontend dependencies available without requiring a third-party CDN for normal offline operation, including Chart.js, Lucide, and PDF.js where practical.
- Extend the GitHub Pages publishing script to include the manifest, service worker, icons, and any bundled frontend dependencies.
- Preserve local portfolio persistence, URL-fragment sharing, ETF calculations, charts, and PDF import behavior in installed mode.
- Add validation guidance for installability, offline startup, cache updates, responsive Android layouts, and PDF import.

## Capabilities

### New Capabilities

- `pwa-installability`: Defines the manifest, icons, service-worker registration, standalone launch behavior, and installability requirements.
- `offline-web-runtime`: Defines application-shell caching, runtime data caching, cache versioning, and graceful online/offline behavior.
- `pwa-publishing`: Defines how GitHub Pages publishes the PWA assets and preserves the runtime data paths.

### Modified Capabilities

None.

## Impact

- `web/index.html` and `web/app.js`: manifest metadata and service-worker registration.
- New `web/manifest.json`, `web/sw.js`, and app icon assets copied from `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png`.
- `web/` dependency handling: local or otherwise reliably cacheable copies of critical browser libraries.
- `scripts/publish-gh-pages.ps1`: publish the new PWA assets and dependencies to the `gh-pages` branch.
- New PWA publishing contract alongside the existing catalog-generation contract.
- `tests/`: static contract tests and browser validation for installability, caching, and existing workflows.
- No backend service, authentication, or server-side data store is introduced.

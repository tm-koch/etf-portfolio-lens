# pwa-publishing Specification

## Purpose
TBD - created by archiving change pwa-android-app. Update Purpose after archive.
## Requirements
### Requirement: Publish all PWA assets

The GitHub Pages publishing process SHALL copy the manifest, service worker, the supplied `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png` files, locally served critical frontend dependencies, and the install-promotion application code into the published site at paths reachable by the application. The publication validation SHALL verify the public HTTPS responses for the manifest, service worker, and icons after deployment.

#### Scenario: Publisher creates a PWA-ready site

- **WHEN** the publisher publishes the web application
- **THEN** the generated Pages tree contains the PWA assets and both supplied launcher icon files alongside `index.html`, JavaScript, CSS, and data files

#### Scenario: Service worker is available at its expected scope

- **WHEN** a browser requests the published root service-worker URL
- **THEN** the response is a JavaScript service-worker file with scope covering the published application

#### Scenario: Published installability assets are reachable

- **WHEN** a deployment validation checks the public HTTPS site
- **THEN** the manifest, service worker, and both icon URLs respond successfully with usable content types and the page's manifest link resolves to the same origin

### Requirement: Preserve published runtime data paths

The PWA publishing process SHALL preserve the existing catalog and snapshot URL paths used by the frontend, including the root-relative `data/` tree and generated build metadata.

#### Scenario: Published catalog remains reachable

- **WHEN** the published application requests `data/catalog.json`
- **THEN** the request resolves to the catalog generated for that Pages publication

#### Scenario: Published snapshot remains reachable

- **WHEN** the application follows a catalog snapshot path
- **THEN** the corresponding snapshot JSON is present at the published path and can be cached by the service worker

### Requirement: Make publication repeatable

The publisher SHALL fail clearly when a required PWA asset is missing and SHALL not silently produce a site that advertises installability without its manifest, service worker, or required icons.

#### Scenario: Required PWA asset is missing

- **WHEN** publication is run with a required PWA asset absent
- **THEN** the script reports the missing asset and exits unsuccessfully

#### Scenario: Complete publication succeeds

- **WHEN** all required web and PWA assets are present
- **THEN** publication completes with a self-contained site tree suitable for installability validation


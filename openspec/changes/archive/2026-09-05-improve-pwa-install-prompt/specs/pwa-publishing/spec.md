## MODIFIED Requirements

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

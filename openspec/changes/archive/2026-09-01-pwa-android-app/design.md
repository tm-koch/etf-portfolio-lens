## Context

ETF Portfolio Lens is a vanilla JavaScript static site published to GitHub Pages. The publisher flattens the `web/` directory into the published site root and copies the catalog plus dated snapshot data under `data/`. The app stores portfolio state and color preferences in `localStorage`, reads shared portfolios from URL fragments, fetches catalog and snapshot JSON at runtime, and imports Saxo PDFs through browser file input and PDF.js loaded from a CDN.

The target is an installable Android experience with a clear path to Trusted Web Activity packaging. The implementation must preserve the existing browser experience and remain serverless. Offline behavior should be useful after a first online visit without requiring all historical snapshots to be bundled into the initial cache.

## Goals / Non-Goals

**Goals:**

- Make the published site installable as a standalone PWA on Android.
- Cache the application shell so the app can open after a network interruption.
- Cache catalog and requested snapshot data using versioned, bounded runtime strategies.
- Ensure PWA assets are included by the GitHub Pages publishing script.
- Keep portfolio persistence, URL-fragment sharing, charts, and responsive layouts working in installed mode.
- Provide a verifiable foundation for later Trusted Web Activity packaging.

**Non-Goals:**

- Building a separate native Android project or committing an Android Studio project.
- Submitting the app to Google Play or configuring Play Console metadata.
- Adding authentication, server-side synchronization, push notifications, or background jobs.
- Guaranteeing first-launch operation without network access.
- Caching arbitrary third-party resources outside the app's origin.

## Decisions

### Use a standards-based PWA as the Android foundation

Add a same-origin manifest and service worker rather than introducing Capacitor or another native wrapper. The manifest application title SHALL be `ETF Porfolio Lens`. The current app has no native API requirement, and a PWA keeps the deployment and code model unchanged while remaining compatible with Trusted Web Activity packaging later.

Alternative: Capacitor would provide a native project immediately, but it would add a build toolchain and platform maintenance before the app needs native capabilities.

### Use the published root as the service-worker scope

The publisher places `index.html`, JavaScript, CSS, manifest, and service worker at the GitHub Pages site root. The service worker will therefore be registered with a root-relative URL and will control the published application shell and `data/` paths.

Alternative: registering from `/web/` would work only for local development and would not control the root-hosted GitHub Pages app.

### Separate precache and runtime caching

Precache only the shell, manifest, icons, and locally served critical libraries. Cache `data/catalog.json` and snapshot JSON at runtime with network-first behavior and a bounded cache. This ensures new published ETF data can replace stale data while allowing previously loaded portfolios to remain useful offline.

Alternative: precaching every dated snapshot would increase install size and make each deployment expensive; cache-first data would make updates less visible.

### Bundle critical frontend libraries locally

Serve Chart.js, Lucide, and PDF.js from the published site or otherwise ensure they are available to the service worker. PDF.js worker configuration must point to the same-origin copy for offline PDF import. External fonts can remain an enhancement and must not block app startup.

Alternative: leave all dependencies on CDNs; this preserves the smallest source tree but makes standalone/offline behavior depend on third-party availability.

### Use cache versioning and graceful fallback

The service worker will use explicit cache names and clean old versions during activation. Navigation requests will fall back to the cached app shell when network access is unavailable. Data requests will fall back to cached responses and the UI will retain its existing error handling when no cached data exists.

### Use the supplied launcher icons

Copy `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png` to the published web asset locations and reference those files from the manifest. Do not substitute generated artwork. Maskable variants may be added if the supplied artwork supports them, but the baseline installability contract requires the supplied standard sizes.

## Risks / Trade-offs

- [A stale service worker may hide a newly published release] -> Version caches explicitly, clean old caches on activation, and test update behavior after a new deployment.
- [Snapshot caches may grow without bound] -> Use a named runtime cache with a documented retention or cleanup policy and cache only successful same-origin JSON responses.
- [CDN dependencies may fail offline] -> Bundle critical libraries and the PDF worker locally; treat remote fonts as optional.
- [GitHub Pages path assumptions may differ between repository and custom-domain hosting] -> Publish at the configured root, use relative asset URLs where possible, and verify the actual Pages URL in an installed browser.
- [Browser storage quotas may limit cached data] -> Keep shell precache small and avoid precaching the full historical data tree.
- [Android file-picker behavior may differ between browsers and Trusted Web Activity] -> Verify PDF selection and import on a physical Android device before packaging.
- [The service worker cannot intercept cross-origin CDN requests reliably for this app] -> Do not make offline correctness depend on cross-origin resources.

## Migration Plan

1. Add the manifest, icons, service worker, registration, and local critical dependencies without changing portfolio data formats.
2. Extend the GitHub Pages publisher to copy all PWA assets and verify the generated root tree.
3. Add static contract tests and browser checks for manifest, registration, cache fallback, installability metadata, and existing app startup.
4. Deploy to GitHub Pages and test first online launch, subsequent offline launch, data refresh, PDF import, sharing, and responsive Android layouts.
5. If the PWA layer must be rolled back, remove the manifest link and registration and stop publishing the service worker; the underlying static app remains usable.

## Open Questions

- Whether the final Android distribution should use Trusted Web Activity or Capacitor after the PWA is validated.
- Whether PDF.js and other CDN libraries should be vendored into the repository or downloaded as part of a repeatable publish step.
- How many snapshot responses should be retained in the runtime cache before eviction.
- Whether maskable variants are needed in addition to the supplied standard icons.

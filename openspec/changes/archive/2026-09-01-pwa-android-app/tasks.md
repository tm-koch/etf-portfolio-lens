## 1. PWA metadata and assets

- [x] 1.1 Copy `doc/launchericon-192x192.png` and `doc/launchericon-512x512.png` into the published web asset locations and verify their PNG dimensions and validity.
- [x] 1.2 Add `web/manifest.json` with name and short name `ETF Porfolio Lens`, start URL, standalone display, colors, icon declarations for the supplied PNGs, and appropriate metadata for Android installation.
- [x] 1.3 Add the manifest reference and theme metadata to `web/index.html` without changing existing navigation or layout behavior.

## 2. Local critical dependencies

- [x] 2.1 Select repeatable, version-pinned local copies of Chart.js, Lucide, PDF.js, and the PDF.js worker compatible with the current frontend APIs.
- [x] 2.2 Update frontend references and PDF worker configuration to use same-origin dependency paths while retaining a clear development fallback where needed.
- [x] 2.3 Verify existing chart, icon, and PDF import workflows with the local dependency copies.

## 3. Service worker and offline runtime

- [x] 3.1 Add a root-scoped `web/sw.js` with explicit shell and runtime cache version names.
- [x] 3.2 Add install handling that precaches the application shell, manifest, icons, and local critical dependencies.
- [x] 3.3 Add activate handling that removes obsolete cache versions and claims clients according to the chosen update behavior.
- [x] 3.4 Add navigation fallback and same-origin runtime handling for catalog and snapshot JSON using network-first behavior.
- [x] 3.5 Add bounded eviction for runtime data entries and ensure failed or non-successful responses are not cached.
- [x] 3.6 Register the service worker from the application without blocking startup when registration is unavailable or fails.

## 4. GitHub Pages publishing

- [x] 4.1 Extend `scripts/publish-gh-pages.ps1` to copy the manifest, service worker, both supplied launcher icons, and local dependencies into the published root.
- [x] 4.2 Add explicit required-file checks so publication fails before advertising an incomplete installable site.
- [x] 4.3 Confirm the existing catalog, build metadata, and dated snapshot paths remain unchanged in the generated Pages tree.

## 5. Validation and Android readiness

- [x] 5.1 Add or update static contract tests for manifest metadata, service-worker registration, cache paths, publisher coverage, and local dependency references.
- [x] 5.2 Add browser validation for first online load, installability metadata, offline shell startup, cached catalog/snapshot fallback, cache update, and uncached-data failure behavior.
- [x] 5.3 Verify portfolio persistence, URL-fragment sharing, chart rendering, navigation, responsive layouts, and PDF import in standalone Android Chrome or an equivalent test environment.
- [x] 5.4 Document the validated PWA URL requirements and remaining steps for a future Trusted Web Activity package, explicitly excluding native project creation and Play Store submission from this change.

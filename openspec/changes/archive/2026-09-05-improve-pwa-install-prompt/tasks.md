## 1. Manifest Identity

- [x] 1.1 Correct the manifest name and short name to `ETF Portfolio Lens` and add a stable published-app `id`.
- [x] 1.2 Update the document title and PWA documentation to use the corrected application name and explain browser-controlled prompt timing.

## 2. Install Promotion

- [x] 2.1 Add a hidden install action to the existing utility surface with accessible labeling and existing icon/style conventions.
- [x] 2.2 Capture `beforeinstallprompt`, defer and store the browser event, and reveal the install action only when the event is available.
- [x] 2.3 Invoke the deferred prompt once per event, clear it after `userChoice`, and handle acceptance, dismissal, and prompt errors without blocking startup.
- [x] 2.4 Handle `appinstalled` and standalone display-mode detection so installed users do not see an install action.

## 3. Contract And Browser Validation

- [x] 3.1 Extend web contract tests for corrected identity, manifest `id`, install control, event handling, and graceful unsupported-browser behavior.
- [x] 3.2 Add or update browser validation for manifest resolution, service-worker control, standalone detection, and the install-event lifecycle where the test browser supports it.
- [x] 3.3 Add a deployment validation check for the public HTTPS page, manifest, service worker, and launcher icon status and content types.

## 4. Verification

- [x] 4.1 Run the focused test suite and verify existing portfolio, sharing, offline shell, and PDF import behavior remains unchanged.
- [x] 4.2 Publish or stage the updated Pages tree and manually verify Chrome's install badge/menu and the conditional in-app install action on a supported browser.

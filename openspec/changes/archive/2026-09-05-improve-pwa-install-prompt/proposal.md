## Why

The published ETF Portfolio Lens has the basic PWA files, but Chrome does not consistently offer the visible install prompt that appears for other installable sites. The project currently has no explicit install-promotion flow and no browser-level validation proving that the deployed manifest, service worker, and installability state are recognized by Chrome.

## What Changes

- Correct the user-facing PWA application identity and add a stable manifest identity.
- Capture Chrome's `beforeinstallprompt` event and expose an install action only when the browser reports that installation is available.
- Keep browser-driven installation behavior intact and provide a graceful fallback when the event is unavailable, dismissed, or the app is already installed.
- Add validation for the live/deployed PWA assets, manifest semantics, service-worker control, and install-promotion lifecycle.
- Document that Chrome's automatic popup remains engagement- and browser-policy-controlled; the feature provides an explicit in-app route when Chrome makes one available.

## Capabilities

### New Capabilities

- `pwa-install-promotion`: Exposes an install action based on the browser's installability event and handles supported and unsupported browser states.

### Modified Capabilities

- `pwa-installability`: Corrects the application identity and adds the stable manifest identity required for reliable app recognition.
- `pwa-publishing`: Extends publication validation to cover the install-promotion assets and deployed installability checks.

## Impact

- `web/manifest.json` and `web/index.html` for application identity and install metadata.
- `web/app.js` and the existing web UI for the conditional install action and event lifecycle.
- `tests/test_web_contract.py` plus browser/deployment validation for regression coverage.
- `web/README.md` and project PWA documentation for user-visible installation expectations.
- No new runtime dependency, server API, data format, or native Android project.

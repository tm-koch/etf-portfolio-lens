## Why

The published PWA can serve a new `index.html` and `app.js` while an already-installed service worker continues returning an older cached manifest and shell. This leaves browsers with mixed application versions and can suppress installability signals even after a corrected deployment. The deployment path needs an explicit freshness contract now that PWA identity and install promotion depend on those assets being consistent.

## What Changes

- Establish a deployment cache-coherence capability for the PWA shell and installability assets.
- Ensure service-worker cache identity changes whenever cache-sensitive shell or manifest assets change.
- Validate that the published document, manifest, service worker, and critical shell assets represent the same build or freshness generation.
- Add regression coverage for stale-cache prevention and public deployment validation.

## Capabilities

### New Capabilities

- `pwa-cache-coherence`: Keeps the published PWA shell, manifest, and service-worker cache generation synchronized across deployments.

### Modified Capabilities

- `pwa-publishing`: Require deployment validation to detect mixed-generation PWA assets and verify cache freshness metadata.
- `pwa-installability`: Require browsers to receive the current manifest and service-worker-controlled shell after a new deployment.

## Impact

- Affects `web/sw.js`, `web/index.html`, `web/manifest.json`, and the GitHub Pages publishing and validation scripts.
- Extends web contract and deployment tests; no application API or user portfolio data format changes are intended.
- Existing cached clients may need one service-worker update cycle or a site-data reset to receive the corrected shell.

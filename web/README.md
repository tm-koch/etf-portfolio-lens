# ETF Portfolio Lens Web App

Run the local development server from the repository root:

```bash
python web/server.py
```

Then open `http://127.0.0.1:8000/web/` in a desktop browser or use the same URL on a smartphone on the same network.

The About this build dialog includes a color-mode control with Bright, Automatic, and Dark options. Automatic follows the browser or operating-system preference. The selected mode is persisted locally in the browser with `localStorage`.

The Portfolio tab can create a share link containing the selected ETF ISINs and share counts. The link is self-contained and readable by anyone who receives it; it does not contain private account information. When opened, it replaces the recipient's local portfolio and calculates exposure using the latest catalog and ETF snapshots deployed with the app.

The published site is an installable PWA named `ETF Portfolio Lens`. It requires HTTPS (GitHub Pages satisfies this) and a first online visit to cache the application shell and any data needed offline. Chrome controls when its automatic install prompt appears; when Chrome exposes `beforeinstallprompt`, the app provides an `Install app` action in the utility bar. The PWA assets are published by `scripts/publish-gh-pages.ps1`; validate installation, offline startup, cached catalog and snapshot loading, PDF import, sharing, and responsive Android layouts before packaging a future Trusted Web Activity. Native Android project creation and Play Store submission are outside this change.

Each publication derives a cache generation from the shell and manifest assets. The publisher injects that generation into the published service worker and validates it before committing the Pages tree, so a changed manifest or shell cannot silently reuse an older cache. Existing browsers update on the normal service-worker lifecycle; republish rollbacks through the same publisher rather than reusing a previous cache generation.

# ETF Portfolio Lens Web App

Run the local development server from the repository root:

```bash
python web/server.py
```

Then open `http://127.0.0.1:8000/web/` in a desktop browser or use the same URL on a smartphone on the same network.

The About this build dialog includes a color-mode control with Bright, Automatic, and Dark options. Automatic follows the browser or operating-system preference. The selected mode is persisted locally in the browser with `localStorage`.

The Portfolio tab can create a share link containing the selected ETF ISINs and share counts. The link is self-contained and readable by anyone who receives it; it does not contain private account information. When opened, it replaces the recipient's local portfolio and calculates exposure using the latest catalog and ETF snapshots deployed with the app.

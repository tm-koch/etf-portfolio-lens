# Proposal

## Why

ETF Portfolio Lens is currently English-only, limiting usability for German-speaking investors. Supporting a user-controlled English/German language choice with Swiss locale conventions will make the website and installed PWA accessible to both audiences, including when used offline.

## What Changes

- Add runtime language selection for English (`en-CH`) and German (`de-CH`), persist the user's choice, and choose a supported browser language when no preference has been saved, defaulting to English otherwise.
- Translate static and dynamically rendered UI, accessibility labels, chart labels/tooltips, import and share feedback, and other user-facing messages.
- Translate sector, region, and other supported taxonomy labels for display while preserving canonical ETF, company, ticker, and security data.
- Apply locale-aware number, currency, and date formatting according to the selected locale.
- Cache both languages' translation resources for offline website and PWA use; retain the stable branded installed-app name.

## Capabilities

### New Capabilities

- `web-localization`: Runtime English/German localization, locale-aware presentation, and offline language resources for the website and PWA.

### Modified Capabilities

None.

## Impact

- `web/index.html` and `web/app.js` for language selection, static strings, and runtime rendering.
- `web/charts.js` and portfolio import/rendering flows for generated text, labels, and accessible descriptions.
- New locale resources and a browser-compatible localization runtime.
- `web/sw.js` and PWA publication/cache validation for offline locale resources.
- `tests/test_web_contract.py` and browser/runtime coverage for locale selection, fallback, rendering, formatting, and offline behavior.

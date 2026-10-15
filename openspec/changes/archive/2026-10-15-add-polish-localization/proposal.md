# Proposal

## Why

The website currently serves English and German interfaces, leaving Polish-speaking investors without a localized experience. Adding Polish as a first-class locale will extend the existing language preference and offline behavior while preserving the site's Swiss-market financial data.

## What Changes

- Add Polish (`pl-PL`) as a persisted runtime language, displayed as `PL` in the language selector and selected when the browser prefers Polish and no saved language exists.
- Translate application-authored static and dynamic interface text, accessibility labels, chart content, import and sharing messages, and supported taxonomy labels; preserve canonical ETF, company, provider, ticker, and ISIN values.
- Format numbers, percentages, dates, and CHF/EUR/USD values using `pl-PL`, including grammatically correct Polish plural forms for count-bearing messages.
- Keep the Polish resource available offline and include it in publishing, cache generation, tests, and localization documentation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `web-localization`: Extend supported runtime language selection, browser preference resolution, translated interface coverage, locale-aware formatting, and offline resources to Polish (`pl-PL`).

## Impact

- `web/localization.js`, `web/app.js`, and `web/formatting.js` for locale registration, language selection, translation, pluralization, and presentation.
- A new Polish translation resource alongside the existing English and German resources.
- `web/sw.js`, GitHub Pages publication and cache-generation allowlists, and web documentation for offline delivery.
- Localization, runtime, and PWA contract tests for three locales, Polish browser preference, translation-key parity, plural forms, and cached resources.

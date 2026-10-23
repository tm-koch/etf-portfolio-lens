# Proposal

## Why

The Home headline currently emphasizes responsive readability but does not communicate the product's privacy-first positioning. A concise, localized headline can express both the privacy emphasis and clear ETF portfolio exposure across screen sizes.

## What Changes

- Replace the Home headline with `Privacy-first ETF portfolio exposure, clear on any screen.` in English.
- Provide concise, natural equivalents for German and Polish that preserve the same privacy-first and cross-screen meaning.
- Keep the existing hero layout, supporting description, and privacy behavior unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `web-localization`: Specify the localized Home headline in English, German, and Polish.

## Impact

Update the existing `ui.heroTitle` translations in `web/locales/en-CH.json`, `web/locales/de-CH.json`, and `web/locales/pl-PL.json`. No layout, API, dependency, or data-handling changes are expected.
# Tasks

## 1. Locale selection

- [x] 1.1 Add `pl-PL` to supported-locale resolution, browser preference mapping, and the language selector as `PL`; verify saved selection, Polish browser preference, unsupported-language fallback, and `<html lang>` behavior with runtime tests.

## 2. Polish translations and formatting

- [x] 2.1 Add the complete Polish resource for all existing static, dynamic, accessibility, chart, import, sharing, and taxonomy keys; verify static and dynamic key coverage and three-locale parity with contract tests.
- [x] 2.2 Add grammatically correct Polish plural forms and pass raw numeric counts separately from locale-formatted display values; verify `one`, `few`, `many`, and `other` behavior with representative integer and fractional counts.
- [x] 2.3 Use `pl-PL` for displayed counts, percentages, dates, and CHF/EUR/USD values without changing numeric amounts or currency codes; verify representative outputs with formatting tests.

## 3. Offline delivery and documentation

- [x] 3.1 Add `locales/pl-PL.json` to the service-worker shell, GitHub Pages required assets, and cache-generation inputs; verify the resource is published and precached through PWA contract tests.
- [x] 3.2 Update the web README with Polish selection, browser fallback, locale formatting, and offline support; verify documented locale codes and fallback match the shipped resources.

## 4. Integration verification

- [x] 4.1 Verify English, German, and Polish switching, persistence across reload, translated dynamic/chart content, and offline switching after shell caching in desktop and 390px/320px browser layouts; confirm no clipping or horizontal overflow.

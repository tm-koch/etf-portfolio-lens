# Tasks

## 1. Localization runtime and preference

- [x] 1.1 Add a pinned i18next dependency and local browser bundle plus `en-CH` and `de-CH` resource files; verify the bundle and both resource files load locally without a CDN.
- [x] 1.2 Resolve the saved locale, map supported browser language preferences to `en-CH` or `de-CH`, default unsupported preferences to `en-CH`, and add the runtime language selector; verify switch, reload persistence, fallback, and `<html lang>` behavior with focused tests.

## 2. Translate interface content

- [x] 2.1 Add translation keys to static HTML, document metadata, form labels, placeholders, and accessibility text; verify every static key exists in both locale resources.
- [x] 2.2 Localize dynamically rendered navigation, portfolio, summary, import, share, warning, and status text; verify rerendering after a language switch with focused runtime tests.
- [x] 2.3 Localize chart titles, legends, tooltips, and taxonomy display labels while preserving canonical data and unknown-label fallback; verify both locale labels and unchanged source values.

## 3. Locale-aware formatting

- [x] 3.1 Format counts, percentages, dates, and CHF/EUR/USD amounts using `en-CH` or `de-CH` without changing stored numeric values or currencies; verify representative outputs with formatting tests.

## 4. Offline delivery and documentation

- [x] 4.1 Add the i18next bundle and both locale resources to the service-worker shell, GitHub Pages required assets, and PWA cache-generation inputs; verify the cache-generation and publishing validations include every asset.
- [x] 4.2 Document language selection, browser fallback, supported locales, and offline behavior in the web README; verify the documented locales match the shipped resources.

## 5. End-to-end verification

- [x] 5.1 In the browser, switch between English and German on desktop and 390px/320px phone widths, reload, and then switch languages offline after the shell is cached; verify translated static/dynamic content, chart labels, locale formatting, accessible labels, and no clipping or horizontal overflow.

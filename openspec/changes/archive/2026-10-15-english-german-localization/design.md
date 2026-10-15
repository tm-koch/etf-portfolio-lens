# Design

## Context

See `proposal.md` for motivation and `specs/web-localization/spec.md` for observable behavior. The UI is a static vanilla-JavaScript app with no frontend build pipeline. `app.js` builds many screens and messages dynamically; `renderAll()` is the central refresh path. The PWA shell and GitHub Pages publisher each maintain explicit asset lists, and cache generations hash a separate explicit list.

## Goals / Non-Goals

**Goals:**
- Support runtime switching between `en-CH` and `de-CH` without a page reload.
- Keep translation lookup consistent across static markup, dynamic renders, charts, imports, and accessible names.
- Keep both locales available offline and make locale asset changes invalidate the PWA cache generation.
- Preserve canonical values in portfolio, catalog, snapshot, and share data.

**Non-Goals:**
- Translate ETF, provider, or company proper names, or alter source data and share payloads.
- Localize the installed PWA's manifest name; retain the stable product brand.
- Add server-side locale negotiation or translate imported PDF source content.

## Decisions

- Use i18next for key lookup, interpolation, pluralization, and English fallback. Ship a pinned browser UMD build as a local vendor asset rather than loading a CDN or introducing a bundler; this follows the existing static/vendor deployment model while avoiding a hand-built translation engine.
- Keep `en-CH` and `de-CH` resources in separate local JSON files. Load both resources before the app's first render, initialize i18next with them, and then bootstrap the UI. This supports immediate switching, avoids network-dependent language changes, and prevents a German-preference user from seeing untranslated generated content after startup.
- Resolve the initial locale from a saved choice first, then map the browser's preferred language (`en` or `de`) to the corresponding Swiss locale, and otherwise use `en-CH`. Store the selected locale separately from portfolio and theme state.
- Mark static interface strings in HTML with translation keys, including labels, placeholders, accessibility text, and document metadata. Use i18next keys and interpolation in JavaScript templates and status messages. After a language switch, update the document language/title metadata and rerun the central render path; refresh any open import-review content and charts as well.
- Use `Intl.NumberFormat` and `Intl.DateTimeFormat` with the selected locale for counts, percentages, currency amounts, and dates. Keep currency codes and numeric values unchanged; formatting must never imply currency conversion.
- Translate taxonomy labels through presentation mappings keyed by canonical sector/region values. Unknown values fall back to their original text; security, ETF, company, and provider names remain canonical.
- Add the locale JSON resources and local i18next bundle to the service-worker shell list, publisher's required asset list, and cache-generation inputs. Keep the manifest's installed-app brand stable and localize the page title/description instead.

## Risks / Trade-offs

- [German text is longer and can overflow compact layouts] -> Review mobile views at narrow and common phone widths, and allow translated controls/headings to wrap without clipping.
- [A missing key can leave mixed-language screens] -> Add parity checks for locale resource keys and checks that static translation keys exist in both resources; configure English fallback for runtime safety.
- [Locale-aware currency formatting can look unfamiliar or be mistaken for conversion] -> Preserve currency codes, use explicit `en-CH`/`de-CH` formatters, and verify representative CHF, EUR, and USD amounts.
- [A new cached asset can be absent from one deployment allowlist] -> Validate that every locale/runtime asset is copied, precached, and included in the cache-generation hash before publishing.

## Migration Plan

No user data migration is needed. Existing users without a saved locale use browser-language detection with an English fallback. The chosen locale is stored under a new independent preference key. Deploy the local runtime and both resources as part of the application shell so existing PWA clients receive a new cache generation through the normal service-worker lifecycle.

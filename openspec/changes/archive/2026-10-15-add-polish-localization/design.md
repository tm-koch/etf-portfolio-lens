# Design

## Context

See `proposal.md` for motivation and `specs/web-localization/spec.md` for the observable behavior. The website is a static vanilla-JavaScript PWA using a locally vendored i18next runtime and flat locale JSON resources. Locale support is explicitly enumerated in the resolver, language selector, tests, service-worker shell, GitHub Pages asset list, and PWA cache-generation inputs. Number, date, and currency formatting follows the selected locale.

## Goals / Non-Goals

**Goals:**
- Add `pl-PL` consistently to persisted selection, browser preference resolution, interface rendering, formatting, and offline delivery.
- Translate every application-authored string while preserving ETF, company, provider, ticker, and ISIN source values.
- Render Polish count messages with correct grammatical plural categories and locale-formatted counts.
- Retain the existing local-only runtime and offline-first deployment model.

**Non-Goals:**
- Change the product name, manifest branding, portfolio data, or share payloads.
- Add a translation service, build pipeline, or network dependency.
- Decouple interface language from number/date formatting; Polish uses `pl-PL` for both.

## Decisions

- **Extend the existing `web-localization` capability.** Add a `pl-PL` locale resource and show `PL` in the existing language selector. Map Polish browser language tags to `pl-PL`; keep saved choices higher priority and retain `en-CH` as the unsupported-language fallback. This reuses the current preference contract rather than introducing a separate Polish-only path.
- **Keep locale resources key-compatible.** Add a Polish translation for each existing flat key, including static HTML, dynamic app/chart/import/share messages, accessibility labels, and taxonomy labels. Preserve canonical source labels for ETF and company data and retain fallback for unknown taxonomy values.
- **Use i18next Polish plural categories.** Provide the locale's supported cardinal forms (`one`, `few`, `many`, and `other`) for count-bearing messages. Pass the raw numeric count to plural selection and a separate `pl-PL`-formatted interpolation value for display; several existing call sites currently format counts before passing them to i18next, which is insufficient for reliable plural selection at grouped values.
- **Use `pl-PL` for presentation.** Route Polish counts, percentages, dates, and CHF/EUR/USD amounts through the existing `Intl` formatters with `pl-PL`. Keep numeric values and currency codes unchanged.
- **Ship the resource as a shell asset.** Add `locales/pl-PL.json` to the service-worker shell, GitHub Pages required assets, and cache-generation inputs. This keeps language switching offline and ensures resource changes invalidate the cache generation.
- **Expand locale-aware verification.** Update resource parity and runtime tests to cover three locales, Polish browser preference, plural categories and formatted interpolation, and update PWA contract checks and documentation. Retain browser checks at narrow phone widths and after the shell is cached offline.

## Risks / Trade-offs

- [Missing or inconsistent Polish keys can leave mixed-language screens] -> Require key parity across all three resources and check static and dynamic keys.
- [Incorrect Polish plural text or category selection can produce ungrammatical counts] -> Test representative values such as 1, 2, 5, 12, and fractional values; keep numeric selection separate from formatted display.
- [Polish wording may be longer than existing translations] -> Verify 390px and 320px layouts for clipping and horizontal overflow.
- [Translation nuance may be lost in financial terminology] -> Review terminology consistently, especially portfolio weights, exposure, valuation, and imported holdings.
- [An explicit asset list may omit the new resource] -> Validate the service-worker shell, publisher, and cache-generation inputs together.

## Migration Plan

No user data migration is required. Existing saved English and German preferences remain valid. After deployment, a saved Polish preference or a Polish browser preference selects `pl-PL`; unsupported or invalid saved values continue through existing locale resolution and fall back to English when no supported browser preference exists. Rollback can remove Polish from the selector and supported-locale list and omit its resource from shell assets; existing portfolio and share data remain unchanged.

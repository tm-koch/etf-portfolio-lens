export const LOCALE_STORAGE_KEY = 'etf-lens.locale.v1';
export const SUPPORTED_LOCALES = ['en-CH', 'de-CH', 'pl-PL'];

function mapBrowserLanguage(language) {
  const baseLanguage = String(language || '').trim().toLowerCase().split('-')[0];
  if (baseLanguage === 'de') return 'de-CH';
  if (baseLanguage === 'en') return 'en-CH';
  if (baseLanguage === 'pl') return 'pl-PL';
  return null;
}

export function resolveLocale(savedLocale, browserLanguages = []) {
  if (SUPPORTED_LOCALES.includes(savedLocale)) {
    return savedLocale;
  }
  for (const language of browserLanguages) {
    const mappedLocale = mapBrowserLanguage(language);
    if (mappedLocale) return mappedLocale;
  }
  return 'en-CH';
}

function readSavedLocale(storage) {
  try {
    return storage?.getItem(LOCALE_STORAGE_KEY);
  } catch {
    return null;
  }
}

export async function initializeLocalization({ i18n = globalThis.i18next, storage, browserLanguages } = {}) {
  if (!i18n) {
    throw new Error('The local i18next runtime is unavailable.');
  }
  const savedLocale = readSavedLocale(storage ?? globalThis.localStorage);
  const languages = browserLanguages ?? globalThis.navigator?.languages ?? [globalThis.navigator?.language];
  const locale = resolveLocale(savedLocale, languages);
  const resources = Object.fromEntries(await Promise.all(
    SUPPORTED_LOCALES.map(async (supportedLocale) => {
      const response = await fetch(new URL(`./locales/${supportedLocale}.json`, import.meta.url));
      if (!response.ok) {
        throw new Error(`Could not load the ${supportedLocale} language resources.`);
      }
      return [supportedLocale, await response.json()];
    })
  ));
  await i18n.init({
    lng: locale,
    fallbackLng: 'en-CH',
    supportedLngs: SUPPORTED_LOCALES,
    keySeparator: false,
    resources,
    interpolation: { escapeValue: false },
  });
  if (globalThis.document?.documentElement) {
    globalThis.document.documentElement.lang = locale;
  }
  return i18n;
}

export async function selectLocale(locale, { i18n = globalThis.i18next, storage } = {}) {
  if (!SUPPORTED_LOCALES.includes(locale)) {
    throw new RangeError(`Unsupported locale: ${locale}`);
  }
  await i18n.changeLanguage(locale);
  try {
    (storage ?? globalThis.localStorage)?.setItem(LOCALE_STORAGE_KEY, locale);
  } catch {
    // Keep the runtime language usable when browser storage is unavailable.
  }
  if (globalThis.document?.documentElement) {
    globalThis.document.documentElement.lang = locale;
  }
  return locale;
}

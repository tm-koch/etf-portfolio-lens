const SUPPORTED_LOCALES = new Set(['en-CH', 'de-CH', 'pl-PL']);

function normalizeLocale(locale) {
  return SUPPORTED_LOCALES.has(locale) ? locale : 'en-CH';
}

export function formatCount(value, locale) {
  return new Intl.NumberFormat(normalizeLocale(locale), { maximumFractionDigits: 0 }).format(value);
}

export function formatPercent(value, locale) {
  return new Intl.NumberFormat(normalizeLocale(locale), {
    style: 'percent',
    maximumFractionDigits: 1,
  }).format(Number(value) / 100);
}

export function formatPercentNumber(value, locale) {
  return new Intl.NumberFormat(normalizeLocale(locale), {
    maximumFractionDigits: 1,
  }).format(Number(value));
}

export function formatCurrencyValue(value, currency = 'CHF', locale) {
  const resolvedLocale = normalizeLocale(locale);
  const numberOptions = {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  };
  const numberFormat = new Intl.NumberFormat(resolvedLocale, numberOptions);
  const currencyParts = new Intl.NumberFormat(resolvedLocale, {
    style: 'currency',
    currency,
    currencyDisplay: 'code',
    ...numberOptions,
  }).formatToParts(0);
  const numericPartTypes = new Set(['integer', 'group', 'decimal', 'fraction']);
  const firstNumericPart = currencyParts.findIndex((part) => numericPartTypes.has(part.type));
  const lastNumericPart = currencyParts.reduce(
    (last, part, index) => numericPartTypes.has(part.type) ? index : last,
    -1,
  );
  const prefix = currencyParts.slice(0, firstNumericPart).map((part) => part.value).join('');
  const suffix = currencyParts.slice(lastNumericPart + 1).map((part) => part.value).join('');
  return `${prefix}${numberFormat.format(Number(value))}${suffix}`;
}

export function formatBuildTimestamp(value, locale) {
  if (!value) return value;

  const dateOnly = /^\d{4}-\d{2}-\d{2}$/.test(value);
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;

  const options = dateOnly
    ? { dateStyle: 'medium', timeZone: 'UTC' }
    : { dateStyle: 'medium', timeStyle: 'medium', timeZone: 'UTC' };
  const formatted = new Intl.DateTimeFormat(normalizeLocale(locale), options).format(parsed);
  return dateOnly ? formatted : `${formatted} UTC`;
}

export const DEFAULT_TOP_HOLDINGS_MAXIMUM = 0;
export const TOP_HOLDINGS_MAXIMUM_STORAGE_KEY = 'etf-lens.top-holdings-maximum.v1';

export function validateTopHoldingsMaximum(value) {
  const maximum = typeof value === 'number'
    ? value
    : typeof value === 'string' && value.trim()
      ? Number(value)
      : Number.NaN;
  return Number.isFinite(maximum) && Number.isInteger(maximum) && maximum >= 0
    ? maximum
    : null;
}

export function getTopHoldingsDisplayLimit(availableCount, maximum) {
  const validMaximum = validateTopHoldingsMaximum(maximum);
  if (!Number.isInteger(availableCount) || availableCount < 0 || validMaximum === null) {
    return 0;
  }
  return validMaximum === 0 ? availableCount : Math.min(availableCount, validMaximum);
}

export function loadTopHoldingsMaximum(storage) {
  try {
    const stored = storage.getItem(TOP_HOLDINGS_MAXIMUM_STORAGE_KEY);
    if (stored === null) return DEFAULT_TOP_HOLDINGS_MAXIMUM;
    return validateTopHoldingsMaximum(JSON.parse(stored))
      ?? DEFAULT_TOP_HOLDINGS_MAXIMUM;
  } catch {
    return DEFAULT_TOP_HOLDINGS_MAXIMUM;
  }
}

export function saveTopHoldingsMaximum(maximum, storage) {
  const validated = validateTopHoldingsMaximum(maximum);
  if (validated === null) return false;

  try {
    storage.setItem(TOP_HOLDINGS_MAXIMUM_STORAGE_KEY, JSON.stringify(validated));
    return true;
  } catch {
    return false;
  }
}

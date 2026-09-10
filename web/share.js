const LEGACY_SHARE_PAYLOAD_VERSION = 1;
const SHARE_PAYLOAD_VERSION = 2;
const PRIVATE_SHARE_PAYLOAD_VERSION = 2;

function encodeBase64Url(value) {
  const bytes = new TextEncoder().encode(value);
  let binary = '';
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function decodeBase64Url(value) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
  const padded = normalized.padEnd(normalized.length + ((4 - (normalized.length % 4)) % 4), '=');
  const binary = atob(padded);
  const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
  return new TextDecoder('utf-8', { fatal: true }).decode(bytes);
}

function normalizeSharedPortfolio(portfolio) {
  if (!Array.isArray(portfolio)) {
    return null;
  }

  const normalized = [];
  const seenIsins = new Set();
  for (const position of portfolio) {
    if (
      !position ||
      typeof position.isin !== 'string' ||
      !position.isin.trim() ||
      typeof position.shares !== 'number' ||
      !Number.isFinite(position.shares) ||
      position.shares < 0
    ) {
      return null;
    }
    const isin = position.isin.trim().toUpperCase();
    if (seenIsins.has(isin)) {
      return null;
    }
    seenIsins.add(isin);
    const normalizedPosition = { isin, shares: position.shares };
    if (position.valuationMode === 'imported' || position.valuationMode === 'latest') normalizedPosition.valuationMode = position.valuationMode;
    if (Number.isFinite(Number(position.price)) && Number(position.price) >= 0) normalizedPosition.price = Number(position.price);
    if (typeof position.currency === 'string' && ['CHF', 'EUR', 'USD'].includes(position.currency.toUpperCase())) normalizedPosition.currency = position.currency.toUpperCase();
    if (Number.isFinite(Number(position.value)) && Number(position.value) >= 0) normalizedPosition.value = Number(position.value);
    if (Number.isFinite(Number(position.valueChf)) && Number(position.valueChf) >= 0) normalizedPosition.valueChf = Number(position.valueChf);
    normalized.push(normalizedPosition);
  }
  return normalized;
}

function normalizePrivatePortfolio(portfolio) {
  if (!Array.isArray(portfolio)) {
    return null;
  }

  const normalized = [];
  const seenIsins = new Set();
  for (const position of portfolio) {
    if (
      !position ||
      typeof position.isin !== 'string' ||
      !position.isin.trim() ||
      typeof position.shares !== 'number' ||
      !Number.isFinite(position.shares) ||
      position.shares < 0 ||
      position.price !== undefined ||
      position.currency !== undefined ||
      position.value !== undefined ||
      position.valueChf !== undefined
    ) {
      return null;
    }
    const isin = position.isin.trim().toUpperCase();
    if (seenIsins.has(isin)) {
      return null;
    }
    seenIsins.add(isin);
    normalized.push({ isin, shares: position.shares });
  }
  return normalized.some((position) => position.shares > 0) ? normalized : null;
}

export function encodePortfolioShare(portfolio) {
  const normalizedPortfolio = normalizeSharedPortfolio(portfolio);
  if (!normalizedPortfolio?.length) {
    return null;
  }
  return encodeBase64Url(
    JSON.stringify({ version: SHARE_PAYLOAD_VERSION, portfolio: normalizedPortfolio })
  );
}

export function encodePrivatePortfolioShare(positions, getTotalShareUnits, getPositionWeight) {
  const totalShareUnits = getTotalShareUnits(positions);
  if (!totalShareUnits) {
    return null;
  }
  const normalizedPortfolio = normalizePrivatePortfolio(
    positions.map((position) => ({
      isin: position.isin,
      shares: getPositionWeight(position, totalShareUnits),
    }))
  );
  if (!normalizedPortfolio) {
    return null;
  }
  return encodeBase64Url(
    JSON.stringify({ version: PRIVATE_SHARE_PAYLOAD_VERSION, mode: 'percentage', portfolio: normalizedPortfolio })
  );
}

export function decodePortfolioShare(value) {
  if (!value) {
    return { status: 'missing', mode: 'full', portfolio: null };
  }
  try {
    const parsed = JSON.parse(decodeBase64Url(value));
    if (parsed?.version === PRIVATE_SHARE_PAYLOAD_VERSION && parsed?.mode === 'percentage') {
      const portfolio = normalizePrivatePortfolio(parsed.portfolio);
      return portfolio
        ? { status: 'valid', mode: 'percentage', portfolio }
        : { status: 'invalid', mode: 'full', portfolio: null };
    }
    if (parsed?.version !== LEGACY_SHARE_PAYLOAD_VERSION && parsed?.version !== SHARE_PAYLOAD_VERSION) {
      return { status: 'invalid', mode: 'full', portfolio: null };
    }
    const portfolio = normalizeSharedPortfolio(parsed.portfolio);
    return portfolio
      ? { status: 'valid', mode: 'full', portfolio }
      : { status: 'invalid', mode: 'full', portfolio: null };
  } catch {
    return { status: 'invalid', mode: 'full', portfolio: null };
  }
}

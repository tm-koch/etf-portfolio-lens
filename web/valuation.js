const SUPPORTED_CURRENCIES = new Set(['CHF', 'EUR', 'USD']);

export function normalizeLivePrices(artifact) {
  if (!artifact || artifact.schema_version !== 1 || typeof artifact.generated_at !== 'string') return null;
  if (!artifact.quotes || typeof artifact.quotes !== 'object' || !artifact.fx || typeof artifact.fx !== 'object') return null;
  return artifact;
}

function getConversion(artifact, currency) {
  if (currency === 'CHF') return { rate: 1, quotedAt: null };
  if (!SUPPORTED_CURRENCIES.has(currency)) return null;
  const rate = artifact?.fx?.[`${currency}/CHF`];
  if (!rate || rate.status !== 'available' || !Number.isFinite(Number(rate.rate))) return null;
  return { rate: Number(rate.rate), quotedAt: rate.quoted_at || null };
}

export function getEffectiveValuation(position, livePrices, valuationMode = position?.valuationMode) {
  const hasExplicitMode = arguments.length >= 3;
  const importedValueChf = Number(position?.valueChf);
  const quote = livePrices?.quotes?.[position?.isin];
  const currency = String(quote?.currency || position?.currency || 'CHF').toUpperCase();
  const importedValue = Number(position?.value);
  const importedConversion = getConversion(livePrices, String(position?.currency || 'CHF').toUpperCase());
  const derivedImportedValueChf = Number.isFinite(importedValue) && importedValue >= 0 && importedConversion
    ? importedValue * importedConversion.rate
    : null;
  const resolvedImportedValueChf = Number.isFinite(importedValueChf) && importedValueChf >= 0
    ? importedValueChf
    : derivedImportedValueChf;
  const shares = Number(position?.shares);
  const price = Number(quote?.price);
  const conversion = getConversion(livePrices, currency);
  if (valuationMode !== 'imported' && quote?.status === 'available' && Number.isFinite(price) && price >= 0 && Number.isFinite(shares) && shares >= 0 && conversion) {
    return {
      status: 'live',
      price,
      currency,
      valueChf: shares * price * conversion.rate,
      quoteAt: quote.quoted_at || null,
      fxAt: conversion.quotedAt,
    };
  }
  if (Number.isFinite(resolvedImportedValueChf) && resolvedImportedValueChf >= 0) {
    return {
      status: hasExplicitMode && valuationMode === 'imported' ? 'imported' : 'fallback',
      price: Number.isFinite(Number(position?.price)) ? Number(position.price) : null,
      currency: String(position?.currency || 'CHF').toUpperCase(),
      valueChf: resolvedImportedValueChf,
      quoteAt: null,
      fxAt: null,
    };
  }
  return { status: 'unavailable', price: null, currency, valueChf: null, quoteAt: null, fxAt: null };
}

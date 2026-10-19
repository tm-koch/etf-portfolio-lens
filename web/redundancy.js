export const DEFAULT_REDUNDANCY_THRESHOLDS = Object.freeze({
  lowModerate: 10,
  moderateHigh: 25,
});
export const REDUNDANCY_THRESHOLDS_STORAGE_KEY = 'etf-lens.redundancy-thresholds.v1';
export const DEFAULT_NEAR_IDENTICAL_THRESHOLD = 90;
export const NEAR_IDENTICAL_THRESHOLD_STORAGE_KEY = 'etf-lens.near-identical-threshold.v1';
export const DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES = 20;
export const PAIRWISE_HOLDINGS_MAX_COMPANIES_STORAGE_KEY = 'etf-lens.pairwise-holdings-max-companies.v1';

export function validatePairwiseHoldingsMaxCompanies(value) {
  const maximum = typeof value === 'number'
    ? value
    : typeof value === 'string' && value.trim()
      ? Number(value)
      : Number.NaN;
  return Number.isFinite(maximum) && Number.isInteger(maximum) && maximum > 0
    ? maximum
    : null;
}

export function loadPairwiseHoldingsMaxCompanies(storage) {
  try {
    const stored = storage.getItem(PAIRWISE_HOLDINGS_MAX_COMPANIES_STORAGE_KEY);
    if (stored === null) return DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES;
    return validatePairwiseHoldingsMaxCompanies(JSON.parse(stored))
      ?? DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES;
  } catch {
    return DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES;
  }
}

export function savePairwiseHoldingsMaxCompanies(maximum, storage) {
  const validated = validatePairwiseHoldingsMaxCompanies(maximum);
  if (validated === null) return false;

  try {
    storage.setItem(PAIRWISE_HOLDINGS_MAX_COMPANIES_STORAGE_KEY, JSON.stringify(validated));
    return true;
  } catch {
    return false;
  }
}

export function validateNearIdenticalThreshold(value) {
  const threshold = typeof value === 'number'
    ? value
    : typeof value === 'string' && value.trim()
      ? Number(value)
      : Number.NaN;
  return Number.isFinite(threshold) && threshold >= 0 && threshold <= 100
    ? threshold
    : null;
}

export function loadNearIdenticalThreshold(storage) {
  try {
    const stored = storage.getItem(NEAR_IDENTICAL_THRESHOLD_STORAGE_KEY);
    if (stored === null) return DEFAULT_NEAR_IDENTICAL_THRESHOLD;
    return validateNearIdenticalThreshold(JSON.parse(stored))
      ?? DEFAULT_NEAR_IDENTICAL_THRESHOLD;
  } catch {
    return DEFAULT_NEAR_IDENTICAL_THRESHOLD;
  }
}

export function saveNearIdenticalThreshold(threshold, storage) {
  const validated = validateNearIdenticalThreshold(threshold);
  if (validated === null) return false;

  try {
    storage.setItem(NEAR_IDENTICAL_THRESHOLD_STORAGE_KEY, JSON.stringify(validated));
    return true;
  } catch {
    return false;
  }
}

export function validateRedundancyThresholds(lowModerate, moderateHigh) {
  const lowValue = typeof lowModerate === 'string' && !lowModerate.trim()
    ? Number.NaN
    : Number(lowModerate);
  const highValue = typeof moderateHigh === 'string' && !moderateHigh.trim()
    ? Number.NaN
    : Number(moderateHigh);

  if (
    !Number.isFinite(lowValue)
    || !Number.isFinite(highValue)
    || lowValue < 0
    || lowValue > 100
    || highValue < 0
    || highValue > 100
    || lowValue >= highValue
  ) {
    return null;
  }

  return { lowModerate: lowValue, moderateHigh: highValue };
}

export function loadRedundancyThresholds(storage) {
  try {
    const stored = storage.getItem(REDUNDANCY_THRESHOLDS_STORAGE_KEY);
    if (!stored) return { ...DEFAULT_REDUNDANCY_THRESHOLDS };
    const parsed = JSON.parse(stored);
    return validateRedundancyThresholds(parsed?.lowModerate, parsed?.moderateHigh)
      || { ...DEFAULT_REDUNDANCY_THRESHOLDS };
  } catch {
    return { ...DEFAULT_REDUNDANCY_THRESHOLDS };
  }
}

export function saveRedundancyThresholds(thresholds, storage) {
  const validated = validateRedundancyThresholds(
    thresholds?.lowModerate,
    thresholds?.moderateHigh,
  );
  if (!validated) return false;

  try {
    storage.setItem(REDUNDANCY_THRESHOLDS_STORAGE_KEY, JSON.stringify(validated));
    return true;
  } catch {
    return false;
  }
}

export function calculateRedundancyScore(holdings, positions) {
  const positivePositions = positions.filter((position) =>
    Number.isFinite(Number(position.weight)) && Number(position.weight) > 0
  );
  const maximum = positivePositions.length
    ? 100 * (1 - 1 / positivePositions.length)
    : 0;

  if (
    !positivePositions.length
    || positivePositions.some((position) => !position.hasUsableHoldings)
  ) {
    return { available: false, score: null, maximum, etfCount: positivePositions.length };
  }

  const overlap = holdings.reduce((total, holding) => {
    const contributionWeights = holding.contributors
      .map((contributor) => Number(contributor.weight))
      .filter(Number.isFinite);
    const largestContribution = Math.max(0, ...contributionWeights);
    return total + Math.max(0, Number(holding.weight) - largestContribution);
  }, 0);

  return {
    available: true,
    score: Math.min(Math.max(overlap, 0), maximum),
    maximum,
    etfCount: positivePositions.length,
  };
}

export function classifyRedundancyScore(score, lowModerate, moderateHigh) {
  if (score < lowModerate) return 'low';
  if (score < moderateHigh) return 'moderate';
  return 'high';
}

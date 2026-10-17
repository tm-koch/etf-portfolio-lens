export const DEFAULT_REDUNDANCY_THRESHOLDS = Object.freeze({
  lowModerate: 10,
  moderateHigh: 25,
});
export const REDUNDANCY_THRESHOLDS_STORAGE_KEY = 'etf-lens.redundancy-thresholds.v1';

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

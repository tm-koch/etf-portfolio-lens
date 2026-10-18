const MINIMUM_SCALE_MAXIMUM = 40;
const COVERAGE_COMPLETION_TOLERANCE = 0.005;

export function classifyDiversificationScore(score) {
  if (score < 5) return 'highlyConcentrated';
  if (score < 10) return 'concentrated';
  if (score < 20) return 'moderatelyDiversified';
  if (score < 40) return 'wellDiversified';
  return 'highlyDiversified';
}

export function calculateDiversificationScore(companyWeights, positions) {
  const weights = companyWeights
    .map(Number)
    .filter((weight) => Number.isFinite(weight) && weight > 0);
  const totalExposure = weights.reduce((total, weight) => total + weight, 0);
  const positivePositions = positions.filter((position) =>
    Number.isFinite(Number(position.weight)) && Number(position.weight) > 0
  );
  const totalPositionWeight = positivePositions.reduce(
    (total, position) => total + Number(position.weight),
    0,
  );
  const coveragePct = totalPositionWeight
    ? Math.min(positivePositions.reduce((total, position) => {
      const coverage = Number(position.coveragePct);
      const normalizedCoverage = Number.isFinite(coverage)
        ? Math.min(Math.max(coverage, 0), 100)
        : 0;
      return total + (Number(position.weight) / totalPositionWeight) * normalizedCoverage;
    }, 0), 100)
    : 0;
  const coverageIncomplete = coveragePct < 100 - COVERAGE_COMPLETION_TOLERANCE;

  if (!totalExposure) {
    return {
      available: false,
      score: null,
      rating: null,
      maximum: MINIMUM_SCALE_MAXIMUM,
      coveragePct,
      coverageIncomplete,
    };
  }

  const hhi = weights.reduce((total, weight) => {
    const normalizedWeight = weight / totalExposure;
    return total + normalizedWeight ** 2;
  }, 0);
  const score = 1 / hhi;

  return {
    available: true,
    score,
    rating: classifyDiversificationScore(score),
    maximum: Math.max(MINIMUM_SCALE_MAXIMUM, score),
    coveragePct,
    coverageIncomplete,
  };
}

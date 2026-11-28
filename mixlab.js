export const COUNTRY_BUCKET_VERSION = 'mixlab-country-buckets-v1';
export const MINIMUM_COUNTRY_COVERAGE_PCT = 95;

const COUNTRY_CODE_BY_LABEL = new Map([
  ['australia', 'AU'], ['austria', 'AT'], ['belgium', 'BE'], ['bermuda', 'BM'],
  ['brazil', 'BR'], ['canada', 'CA'], ['cayman islands', 'KY'], ['chile', 'CL'],
  ['china', 'CN'], ['colombia', 'CO'], ['czech republic', 'CZ'], ['denmark', 'DK'],
  ['egypt', 'EG'], ['finland', 'FI'], ['france', 'FR'], ['germany', 'DE'],
  ['greece', 'GR'], ['hong kong', 'HK'], ['hungary', 'HU'], ['india', 'IN'],
  ['indonesia', 'ID'], ['ireland', 'IE'], ['israel', 'IL'], ['italy', 'IT'],
  ['japan', 'JP'], ['jersey', 'JE'], ['korea (south)', 'KR'], ['kuwait', 'KW'],
  ['liechtenstein', 'LI'], ['luxembourg', 'LU'], ['malaysia', 'MY'], ['mexico', 'MX'],
  ['netherlands', 'NL'], ['new zealand', 'NZ'], ['norway', 'NO'], ['peru', 'PE'],
  ['philippines', 'PH'], ['poland', 'PL'], ['portugal', 'PT'], ['qatar', 'QA'],
  ['republic of korea', 'KR'], ['russia', 'RU'], ['russian federation', 'RU'],
  ['saudi arabia', 'SA'], ['singapore', 'SG'], ['south africa', 'ZA'],
  ['south korea', 'KR'], ['spain', 'ES'], ['sweden', 'SE'], ['switzerland', 'CH'],
  ['taiwan', 'TW'], ['thailand', 'TH'], ['turkey', 'TR'],
  ['united arab emirates', 'AE'], ['united kingdom', 'GB'], ['united states', 'US'],
  ['usa', 'US'],
]);

const COUNTRY_BUCKET_BY_CODE = new Map();
const assignBucket = (bucket, codes) => {
  for (const code of codes) COUNTRY_BUCKET_BY_CODE.set(code, bucket);
};

assignBucket('switzerland', ['CH']);
assignBucket('northAmerica', ['CA', 'US']);
assignBucket('developedEurope', [
  'AT', 'BE', 'DK', 'FI', 'FR', 'DE', 'IE', 'IT', 'LI', 'LU', 'NL', 'NO', 'PT',
  'ES', 'SE', 'GB',
]);
assignBucket('developedAsiaPacific', ['AU', 'HK', 'JP', 'NZ', 'SG']);
assignBucket('emergingMarkets', [
  'BR', 'CL', 'CN', 'CO', 'CZ', 'EG', 'GR', 'HU', 'ID', 'IN', 'KR', 'MY', 'MX',
  'PE', 'PH', 'PL', 'QA', 'RU', 'SA', 'TH', 'TR', 'TW', 'ZA', 'AE',
]);
assignBucket('otherClassified', ['BM', 'KY', 'IL', 'JE', 'KW']);

export function normalizeCountryCode(classification = {}) {
  const code = String(classification.country_code ?? '').trim().toUpperCase();
  if (code) return COUNTRY_BUCKET_BY_CODE.has(code) ? code : null;
  const label = String(classification.country ?? '').trim().toLowerCase();
  return COUNTRY_CODE_BY_LABEL.get(label) ?? null;
}

export function countryBucketFor(countryCode) {
  return COUNTRY_BUCKET_BY_CODE.get(String(countryCode ?? '').trim().toUpperCase()) ?? null;
}

export function aggregateCountryExposure(holdings = []) {
  const buckets = {
    switzerland: 0,
    developedEurope: 0,
    northAmerica: 0,
    developedAsiaPacific: 0,
    emergingMarkets: 0,
    otherClassified: 0,
    unclassified: 0,
  };
  let disclosedWeight = 0;
  let classifiedWeight = 0;

  for (const holding of holdings) {
    const weight = Number(holding?.exposure?.weight_pct ?? holding?.weight_pct);
    if (!Number.isFinite(weight) || weight <= 0) continue;
    disclosedWeight += weight;

    const countryCode = normalizeCountryCode(holding?.classification ?? holding);
    const bucket = countryBucketFor(countryCode);
    if (bucket) {
      buckets[bucket] += weight;
      classifiedWeight += weight;
    } else {
      buckets.unclassified += weight;
    }
  }

  const denominator = Math.max(disclosedWeight, 100);
  if (disclosedWeight < 100) buckets.unclassified += 100 - disclosedWeight;
  const scale = denominator ? 100 / denominator : 0;
  for (const bucket of Object.keys(buckets)) buckets[bucket] *= scale;

  return {
    buckets,
    coveragePct: denominator ? (classifiedWeight / denominator) * 100 : 0,
    unclassifiedPct: buckets.unclassified,
    disclosedWeightPct: disclosedWeight,
  };
}

function normalizedClassifiedBuckets(exposure) {
  const entries = Object.entries(exposure?.buckets ?? {})
    .filter(([bucket, weight]) => bucket !== 'unclassified' && Number(weight) > 0);
  const total = entries.reduce((sum, [, weight]) => sum + Number(weight), 0);
  return total ? new Map(entries.map(([bucket, weight]) => [bucket, Number(weight) / total])) : null;
}

export function calculateProportionalOverlap(target, candidate) {
  const targetCoveragePct = Number(target?.coveragePct) || 0;
  const candidateCoveragePct = Number(candidate?.coveragePct) || 0;
  const targetBuckets = normalizedClassifiedBuckets(target);
  const candidateBuckets = normalizedClassifiedBuckets(candidate);
  const coverageSufficient = targetCoveragePct >= MINIMUM_COUNTRY_COVERAGE_PCT
    && candidateCoveragePct >= MINIMUM_COUNTRY_COVERAGE_PCT;

  if (!coverageSufficient || !targetBuckets || !candidateBuckets) {
    return {
      available: false,
      coverageSufficient,
      overlapPct: null,
      targetCoveragePct,
      candidateCoveragePct,
    };
  }

  const buckets = new Set([...targetBuckets.keys(), ...candidateBuckets.keys()]);
  const overlap = [...buckets].reduce(
    (total, bucket) => total + Math.min(targetBuckets.get(bucket) ?? 0, candidateBuckets.get(bucket) ?? 0),
    0,
  );
  return {
    available: true,
    coverageSufficient: true,
    overlapPct: overlap * 100,
    targetCoveragePct,
    candidateCoveragePct,
  };
}

const VALID_INVESTMENT_UNIVERSES = new Set([
  'developed_world',
  'all_country_world',
  'emerging_markets',
  'developed_europe',
  'switzerland',
]);

function holdingCompanyIdentity(holding) {
  const security = holding?.security ?? {};
  const identity = security.company_id
    || security.canonical_name
    || security.isin
    || security.ticker
    || security.name;
  return typeof identity === 'string' && identity.trim()
    ? identity.trim().toLowerCase()
    : null;
}

export function calculateEffectiveCompanies(companyWeights) {
  const weights = [...(companyWeights instanceof Map ? companyWeights.values() : companyWeights)]
    .map(Number)
    .filter((weight) => Number.isFinite(weight) && weight > 0);
  const total = weights.reduce((sum, weight) => sum + weight, 0);
  if (!total) return null;
  const hhi = weights.reduce((sum, weight) => sum + (weight / total) ** 2, 0);
  return hhi > 0 ? 1 / hhi : null;
}

export function prepareMixLabFund(entry, snapshot) {
  const issues = new Set(entry?.optimizerMetadataIssues ?? []);
  const rawTerPct = entry?.terPct;
  const terPct = rawTerPct === null || rawTerPct === undefined ? NaN : Number(rawTerPct);
  const distributionPolicy = entry?.distributionPolicy;
  const investmentUniverse = entry?.investmentUniverse;
  if (!Number.isFinite(terPct) || terPct < 0 || !entry?.terSource) issues.add('ter_metadata');
  if (!['accumulating', 'distributing'].includes(distributionPolicy)) issues.add('distribution_policy');
  if (!VALID_INVESTMENT_UNIVERSES.has(investmentUniverse)) issues.add('investment_universe');
  if (!Array.isArray(snapshot?.holdings) || !snapshot.holdings.length) issues.add('holdings');

  const companyWeights = new Map();
  for (const holding of snapshot?.holdings ?? []) {
    const rawWeight = Number(holding?.exposure?.weight_pct);
    const company = holdingCompanyIdentity(holding);
    if (!company || !Number.isFinite(rawWeight) || rawWeight <= 0) continue;
    companyWeights.set(company, (companyWeights.get(company) ?? 0) + rawWeight);
  }

  return {
    ...entry,
    terPct: Number.isFinite(terPct) ? terPct : null,
    distributionPolicy,
    investmentUniverse,
    snapshotDate: snapshot?.snapshot?.as_of ?? null,
    exposure: aggregateCountryExposure(snapshot?.holdings ?? []),
    companyWeights,
    companyWeightTotal: [...companyWeights.values()].reduce((sum, weight) => sum + weight, 0),
    effectiveCompanies: calculateEffectiveCompanies(companyWeights),
    eligibilityIssues: [...issues],
    eligible: issues.size === 0,
  };
}

export function combineMixAllocations(allocations) {
  const normalized = (allocations ?? []).map(({ fund, weightPct }) => ({
    fund,
    weightPct: Number(weightPct),
  }));
  const valid = normalized.every(({ fund, weightPct }) => fund && Number.isFinite(weightPct) && weightPct >= 0);
  const totalWeightPct = normalized.reduce((sum, allocation) => sum + allocation.weightPct, 0);
  if (!valid || Math.abs(totalWeightPct - 100) > 1e-6) {
    return { available: false, reason: 'allocations_must_total_100', totalWeightPct };
  }

  const buckets = {
    switzerland: 0,
    developedEurope: 0,
    northAmerica: 0,
    developedAsiaPacific: 0,
    emergingMarkets: 0,
    otherClassified: 0,
    unclassified: 0,
  };
  const companyWeights = new Map();
  let coveragePct = 0;
  let weightedTerPct = 0;
  for (const { fund, weightPct } of normalized) {
    const share = weightPct / 100;
    for (const [bucket, weight] of Object.entries(fund.exposure?.buckets ?? {})) {
      if (bucket in buckets) buckets[bucket] += Number(weight) * share;
    }
    coveragePct += (Number(fund.exposure?.coveragePct) || 0) * share;
    if (Number.isFinite(Number(fund.terPct))) weightedTerPct += Number(fund.terPct) * share;
    for (const [company, weight] of fund.companyWeights ?? []) {
      companyWeights.set(company, (companyWeights.get(company) ?? 0) + Number(weight) * share);
    }
  }
  return {
    available: true,
    totalWeightPct,
    exposure: {
      buckets,
      coveragePct,
      unclassifiedPct: buckets.unclassified,
      disclosedWeightPct: 100,
    },
    companyWeights,
    effectiveCompanies: calculateEffectiveCompanies(companyWeights),
    weightedTerPct,
  };
}

function companyDotProduct(fundA, fundB) {
  const [smaller, larger] = fundA.companyWeights.size <= fundB.companyWeights.size
    ? [fundA.companyWeights, fundB.companyWeights]
    : [fundB.companyWeights, fundA.companyWeights];
  let dotProduct = 0;
  for (const [company, weight] of smaller) {
    dotProduct += weight * (larger.get(company) ?? 0);
  }
  return dotProduct;
}

function compareMixResults(left, right) {
  if (Math.abs(left.score - right.score) > 1e-12) return left.score - right.score;
  if (left.fundCount !== right.fundCount) return left.fundCount - right.fundCount;
  if (Math.abs(left.weightedTerPct - right.weightedTerPct) > 1e-12) {
    return left.weightedTerPct - right.weightedTerPct;
  }
  return left.signature.localeCompare(right.signature);
}

function limitStatus(weightedTerPct, effectiveCompanies, options) {
  const maximumEnabled = options.maximumTerEnabled === true;
  const minimumEnabled = options.minimumEffectiveCompaniesEnabled === true;
  const maximumRaw = options.maximumTerPct;
  const minimumRaw = options.minimumEffectiveCompanies;
  const maximumValue = maximumRaw === null || maximumRaw === undefined || maximumRaw === ''
    ? NaN
    : Number(maximumRaw);
  const minimumValue = minimumRaw === null || minimumRaw === undefined || minimumRaw === ''
    ? NaN
    : Number(minimumRaw);
  const maximumValid = Number.isFinite(maximumValue) && maximumValue >= 0;
  const minimumValid = Number.isFinite(minimumValue) && minimumValue >= 0;
  return {
    maximumTer: !maximumEnabled || (maximumValid && weightedTerPct <= maximumValue + 1e-12),
    minimumEffectiveCompanies: !minimumEnabled
      || (minimumValid && effectiveCompanies + 1e-12 >= minimumValue),
    validationErrors: [
      ...(maximumEnabled && !maximumValid ? ['invalid_maximum_ter'] : []),
      ...(minimumEnabled && !minimumValid ? ['invalid_minimum_effective_companies'] : []),
    ],
  };
}

function insertRankedResult(results, result, limit, compare) {
  const duplicateIndex = results.findIndex((previous) => previous.signature === result.signature);
  if (duplicateIndex >= 0) {
    if (compare(result, results[duplicateIndex]) >= 0) return;
    results.splice(duplicateIndex, 1);
  }
  const insertionIndex = results.findIndex((previous) => compare(result, previous) < 0);
  if (insertionIndex < 0) {
    if (results.length < limit) results.push(result);
  } else {
    results.splice(insertionIndex, 0, result);
    if (results.length > limit) results.pop();
  }
}

function compareClosestAlternatives(left, right) {
  if (left.failedConstraints.length !== right.failedConstraints.length) {
    return left.failedConstraints.length - right.failedConstraints.length;
  }
  if (Math.abs(left.exposureDistance - right.exposureDistance) > 1e-12) {
    return left.exposureDistance - right.exposureDistance;
  }
  return compareMixResults(left, right);
}

function annualTerCost(portfolioValueChf, weightedTerPct) {
  return portfolioValueChf !== null
    && portfolioValueChf !== undefined
    && portfolioValueChf !== ''
    && Number.isFinite(Number(portfolioValueChf))
    ? Number(portfolioValueChf) * weightedTerPct / 100
    : null;
}

function combinationCount(n, k) {
  if (k < 0 || k > n) return 0;
  let result = 1;
  for (let index = 1; index <= Math.min(k, n - k); index += 1) {
    result = result * (n - index + 1) / index;
  }
  return result;
}

function estimateGridEvaluations(fundCount, maximumFunds, allocationStepPct) {
  const units = 100 / allocationStepPct;
  let total = 0;
  for (let count = 1; count <= Math.min(fundCount, maximumFunds); count += 1) {
    total += combinationCount(fundCount, count) * combinationCount(units + count - 1, count - 1);
  }
  return total;
}

function boundedAllocationStep(requestedStep, fundCount, maximumFunds) {
  const evaluationBudget = 500000;
  const supportedSteps = [1, 2, 4, 5, 10, 20, 25, 50, 100];
  for (const step of supportedSteps) {
    if (step < requestedStep) continue;
    if (estimateGridEvaluations(fundCount, maximumFunds, step) <= evaluationBudget) return step;
  }
  return 100;
}

export function searchConsolidation({
  funds = [],
  target,
  overlapThresholdPct = 97,
  diversificationPriority = 0,
  maximumFunds = 5,
  allocationStepPct = 5,
  portfolioValueChf = null,
  distributionPolicyFilter = 'both',
  maximumTerEnabled = false,
  maximumTerPct = null,
  minimumEffectiveCompaniesEnabled = false,
  minimumEffectiveCompanies = null,
  maximumResults = 10,
} = {}) {
  const metadataEligibleFunds = funds
    .filter((fund) => fund?.eligible && Number.isFinite(fund.terPct));
  const validDistributionFilter = ['both', 'accumulating', 'distributing']
    .includes(distributionPolicyFilter);
  const eligibleFunds = metadataEligibleFunds
    .filter((fund) => validDistributionFilter
      && (distributionPolicyFilter === 'both' || fund.distributionPolicy === distributionPolicyFilter))
    .sort((left, right) => left.isin.localeCompare(right.isin));
  const highestCandidateTerPct = Math.max(0, ...eligibleFunds.map((fund) => fund.terPct));
  const priority = Math.min(1, Math.max(0, Number(diversificationPriority) || 0));
  const requestedStep = Number(allocationStepPct);
  const unitsPerHundred = Math.round(100 / requestedStep);
  const controlErrors = validDistributionFilter ? [] : ['invalid_distribution_filter'];
  const controlOptions = {
    maximumTerEnabled,
    maximumTerPct,
    minimumEffectiveCompaniesEnabled,
    minimumEffectiveCompanies,
  };
  controlErrors.push(...limitStatus(0, 0, controlOptions).validationErrors);
  if (!target || requestedStep <= 0 || Math.abs(unitsPerHundred * requestedStep - 100) > 1e-8) {
    return {
      eligibleFundCount: eligibleFunds.length,
      filteredByDistributionCount: metadataEligibleFunds.length - eligibleFunds.length,
      evaluatedMixCount: 0,
      validationErrors: controlErrors,
      distributionPolicyFilter,
      results: [],
      closestAlternatives: [],
    };
  }

  const maxFunds = Math.min(5, Math.max(1, Math.floor(Number(maximumFunds) || 5)));
  const step = boundedAllocationStep(requestedStep, eligibleFunds.length, maxFunds);
  const actualUnitsPerHundred = Math.round(100 / step);
  const resultLimit = Math.max(1, Math.floor(Number(maximumResults) || 10));
  const alternativeLimit = Math.min(3, resultLimit);
  const topResults = [];
  const closestAlternatives = [];
  const companyDots = eligibleFunds.map((fundA) =>
    eligibleFunds.map((fundB) => companyDotProduct(fundA, fundB))
  );
  let evaluatedMixCount = 0;

  const evaluate = (subset, units) => {
    evaluatedMixCount += 1;
    const allocations = [];
    const buckets = {
      switzerland: 0,
      developedEurope: 0,
      northAmerica: 0,
      developedAsiaPacific: 0,
      emergingMarkets: 0,
      otherClassified: 0,
      unclassified: 0,
    };
    let coveragePct = 0;
    let weightedTerPct = 0;
    let companyWeightTotal = 0;

    for (let index = 0; index < subset.length; index += 1) {
      const fund = subset[index];
      const weightPct = units[index] * step;
      if (!weightPct) continue;
      const share = weightPct / 100;
      allocations.push({ fund, weightPct });
      for (const [bucket, weight] of Object.entries(fund.exposure.buckets)) {
        buckets[bucket] += Number(weight) * share;
      }
      coveragePct += fund.exposure.coveragePct * share;
      weightedTerPct += fund.terPct * share;
      companyWeightTotal += fund.companyWeightTotal * share;
    }
    if (!companyWeightTotal) return;

    let companySquaredWeight = 0;
    for (let left = 0; left < subset.length; left += 1) {
      const leftShare = units[left] * step / 100;
      if (!leftShare) continue;
      const leftIndex = eligibleFunds.indexOf(subset[left]);
      for (let right = 0; right < subset.length; right += 1) {
        const rightShare = units[right] * step / 100;
        if (!rightShare) continue;
        const rightIndex = eligibleFunds.indexOf(subset[right]);
        companySquaredWeight += leftShare * rightShare * companyDots[leftIndex][rightIndex];
      }
    }
    if (!companySquaredWeight) return;
    const effectiveCompanies = (companyWeightTotal ** 2) / companySquaredWeight;
    const exposure = {
      buckets,
      coveragePct,
      unclassifiedPct: buckets.unclassified,
      disclosedWeightPct: 100,
    };
    const overlap = calculateProportionalOverlap(target, exposure);
    const terObjective = highestCandidateTerPct > 0 ? weightedTerPct / highestCandidateTerPct : 0;
    const hhiPenalty = 1 / effectiveCompanies;
    const score = ((1 - priority) * terObjective) + (priority * hhiPenalty);
    const limits = limitStatus(weightedTerPct, effectiveCompanies, controlOptions);
    const exposurePassed = overlap.available && overlap.overlapPct + 1e-12 >= overlapThresholdPct;
    const constraintStatus = {
      exposure: exposurePassed,
      distribution: validDistributionFilter,
      maximumTer: limits.maximumTer,
      minimumEffectiveCompanies: limits.minimumEffectiveCompanies,
    };
    const failedConstraints = Object.entries(constraintStatus)
      .filter(([, passed]) => !passed)
      .map(([constraint]) => constraint);
    const minimumCoveragePct = Math.min(overlap.targetCoveragePct, overlap.candidateCoveragePct);
    const exposureDistance = overlap.available
      ? Math.max(0, overlapThresholdPct - overlap.overlapPct)
      : 100 + Math.max(0, MINIMUM_COUNTRY_COVERAGE_PCT - minimumCoveragePct);
    const signature = allocations
      .map(({ fund, weightPct }) => `${fund.isin}:${weightPct.toFixed(2)}`)
      .join('|');
    const result = {
      allocations: allocations.map(({ fund, weightPct }) => ({
        isin: fund.isin,
        ticker: fund.ticker,
        weightPct,
      })),
      fundCount: allocations.length,
      weightedTerPct,
      effectiveCompanies,
      exposure,
      overlapPct: overlap.overlapPct,
      targetCoveragePct: overlap.targetCoveragePct,
      candidateCoveragePct: overlap.candidateCoveragePct,
      annualTerCostChf: annualTerCost(portfolioValueChf, weightedTerPct),
      snapshotDates: [...new Set(allocations.map(({ fund }) => fund.snapshotDate).filter(Boolean))],
      score,
      constraintStatus,
      failedConstraints,
      exposureDistance,
      qualifying: failedConstraints.length === 0,
      distributionPolicyFilter,
      signature,
    };
    if (result.qualifying) {
      insertRankedResult(topResults, result, resultLimit, compareMixResults);
    } else {
      insertRankedResult(closestAlternatives, result, alternativeLimit, compareClosestAlternatives);
    }
  };

  const visitAllocations = (subset, index, remaining, units) => {
    if (index === subset.length - 1) {
      units[index] = remaining;
      evaluate(subset, units);
      return;
    }
    for (let assigned = 0; assigned <= remaining; assigned += 1) {
      units[index] = assigned;
      visitAllocations(subset, index + 1, remaining - assigned, units);
    }
  };

  const visitSubsets = (startIndex, selected) => {
    if (selected.length) {
      visitAllocations(selected, 0, actualUnitsPerHundred, Array(selected.length).fill(0));
    }
    if (selected.length >= maxFunds) return;
    for (let index = startIndex; index < eligibleFunds.length; index += 1) {
      visitSubsets(index + 1, [...selected, eligibleFunds[index]]);
    }
  };
  visitSubsets(0, []);

  const rankedResults = topResults
    .map(({ signature, ...result }) => result);
  const rankedAlternatives = closestAlternatives
    .map(({ signature, exposureDistance, ...result }) => result);
  return {
    eligibleFundCount: eligibleFunds.length,
    filteredByDistributionCount: metadataEligibleFunds.length - eligibleFunds.length,
    evaluatedMixCount,
    validationErrors: controlErrors,
    distributionPolicyFilter,
    requestedAllocationStepPct: requestedStep,
    allocationStepPct: step,
    results: rankedResults,
    closestAlternatives: rankedResults.length ? [] : rankedAlternatives,
  };
}

export function searchCustomSleeves({
  funds = [],
  sleeveAllocations = {},
  diversificationPriority = 0,
  portfolioValueChf = null,
  distributionPolicyFilter = 'both',
  maximumTerEnabled = false,
  maximumTerPct = null,
  minimumEffectiveCompaniesEnabled = false,
  minimumEffectiveCompanies = null,
  maximumResults = 10,
} = {}) {
  const entries = Object.entries(sleeveAllocations ?? {});
  const validDistributionFilter = ['both', 'accumulating', 'distributing']
    .includes(distributionPolicyFilter);
  const controlOptions = {
    maximumTerEnabled,
    maximumTerPct,
    minimumEffectiveCompaniesEnabled,
    minimumEffectiveCompanies,
  };
  const controlErrors = [
    ...(!validDistributionFilter ? ['invalid_distribution_filter'] : []),
    ...limitStatus(0, 0, controlOptions).validationErrors,
  ];
  const normalizedSleeves = [];
  const validationErrors = [...controlErrors];
  for (const [sleeve, rawWeight] of entries) {
    const weightPct = rawWeight === null || rawWeight === undefined || rawWeight === ''
      ? NaN
      : Number(rawWeight);
    if (!VALID_INVESTMENT_UNIVERSES.has(sleeve)) validationErrors.push('unknown_sleeve');
    if (!Number.isFinite(weightPct) || weightPct < 0) validationErrors.push('invalid_sleeve_weight');
    else normalizedSleeves.push({ sleeve, weightPct });
  }
  const totalWeightPct = normalizedSleeves.reduce((sum, sleeve) => sum + sleeve.weightPct, 0);
  if (!entries.length || validationErrors.length || Math.abs(totalWeightPct - 100) > 1e-6) {
    if (Math.abs(totalWeightPct - 100) > 1e-6) validationErrors.push('sleeve_total_must_equal_100');
    return {
      valid: false,
      totalWeightPct,
      validationErrors: [...new Set(validationErrors)],
      missingSleeves: [],
      evaluatedMixCount: 0,
      results: [],
    };
  }

  const activeSleeves = normalizedSleeves.filter(({ weightPct }) => weightPct > 0);
  const metadataEligibleFunds = funds
    .filter((fund) => fund?.eligible && Number.isFinite(fund.terPct));
  const eligibleFunds = metadataEligibleFunds
    .filter((fund) => validDistributionFilter
      && (distributionPolicyFilter === 'both' || fund.distributionPolicy === distributionPolicyFilter))
    .sort((left, right) => left.isin.localeCompare(right.isin));
  const fundsBySleeve = new Map(activeSleeves.map(({ sleeve }) => [
    sleeve,
    eligibleFunds.filter((fund) => fund.investmentUniverse === sleeve),
  ]));
  const missingSleeves = activeSleeves
    .filter(({ sleeve }) => fundsBySleeve.get(sleeve).length === 0)
    .map(({ sleeve }) => sleeve);
  if (missingSleeves.length) {
    return {
      valid: true,
      totalWeightPct,
      validationErrors: controlErrors,
      missingSleeves,
      evaluatedMixCount: 0,
      eligibleFundCount: eligibleFunds.length,
      filteredByDistributionCount: metadataEligibleFunds.length - eligibleFunds.length,
      results: [],
      closestAlternatives: [],
    };
  }

  const highestCandidateTerPct = Math.max(0, ...eligibleFunds.map((fund) => fund.terPct));
  const priority = Math.min(1, Math.max(0, Number(diversificationPriority) || 0));
  const resultLimit = Math.max(1, Math.floor(Number(maximumResults) || 10));
  const alternativeLimit = Math.min(3, resultLimit);
  const results = [];
  const closestAlternatives = [];
  let evaluatedMixCount = 0;

  const evaluate = (allocations) => {
    evaluatedMixCount += 1;
    const mixed = combineMixAllocations(allocations);
    if (!mixed.available || mixed.effectiveCompanies === null) return;
    const score = ((1 - priority) * (highestCandidateTerPct > 0 ? mixed.weightedTerPct / highestCandidateTerPct : 0))
      + (priority / mixed.effectiveCompanies);
    const signature = allocations
      .map(({ fund, weightPct }) => `${fund.isin}:${weightPct.toFixed(2)}`)
      .sort()
      .join('|');
    const limits = limitStatus(mixed.weightedTerPct, mixed.effectiveCompanies, controlOptions);
    const constraintStatus = {
      exposure: true,
      distribution: validDistributionFilter,
      maximumTer: limits.maximumTer,
      minimumEffectiveCompanies: limits.minimumEffectiveCompanies,
    };
    const failedConstraints = Object.entries(constraintStatus)
      .filter(([, passed]) => !passed)
      .map(([constraint]) => constraint);
    const candidate = {
      allocations: allocations.map(({ fund, weightPct }) => ({
        isin: fund.isin,
        ticker: fund.ticker,
        weightPct,
      })),
      fundCount: allocations.length,
      sleeveAllocations: Object.fromEntries(activeSleeves.map(({ sleeve, weightPct }) => [sleeve, weightPct])),
      weightedTerPct: mixed.weightedTerPct,
      effectiveCompanies: mixed.effectiveCompanies,
      exposure: mixed.exposure,
      sleeveFitPct: 100,
      annualTerCostChf: annualTerCost(portfolioValueChf, mixed.weightedTerPct),
      snapshotDates: [...new Set(allocations.map(({ fund }) => fund.snapshotDate).filter(Boolean))],
      score,
      constraintStatus,
      failedConstraints,
      exposureDistance: 0,
      qualifying: failedConstraints.length === 0,
      distributionPolicyFilter,
      signature,
    };
    if (candidate.qualifying) {
      insertRankedResult(results, candidate, resultLimit, compareMixResults);
    } else {
      insertRankedResult(closestAlternatives, candidate, alternativeLimit, compareClosestAlternatives);
    }
  };

  const chooseSleeveFunds = (index, allocations) => {
    if (index >= activeSleeves.length) {
      evaluate(allocations);
      return;
    }
    const { sleeve, weightPct } = activeSleeves[index];
    for (const fund of fundsBySleeve.get(sleeve)) {
      chooseSleeveFunds(index + 1, [...allocations, { fund, weightPct }]);
    }
  };
  chooseSleeveFunds(0, []);

  const rankedResults = results
    .map(({ signature, ...result }) => result);
  const rankedAlternatives = closestAlternatives
    .map(({ signature, exposureDistance, ...result }) => result);
  return {
    valid: true,
    totalWeightPct,
    validationErrors: controlErrors,
    missingSleeves: [],
    evaluatedMixCount,
    eligibleFundCount: eligibleFunds.length,
    filteredByDistributionCount: metadataEligibleFunds.length - eligibleFunds.length,
    distributionPolicyFilter,
    results: rankedResults,
    closestAlternatives: rankedResults.length ? [] : rankedAlternatives,
  };
}

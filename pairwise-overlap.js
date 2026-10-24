function pairKey(isinA, isinB) {
  return [isinA, isinB].sort().join('\u0000');
}

export function buildPairwiseOverlapIndex(pairwiseOverlap) {
  const index = new Map();
  if (pairwiseOverlap?.version !== 1 || !Array.isArray(pairwiseOverlap.pairs)) {
    return index;
  }

  for (const pair of pairwiseOverlap.pairs) {
    if (
      typeof pair?.isinA !== 'string'
      || !pair.isinA
      || typeof pair.isinB !== 'string'
      || !pair.isinB
      || pair.isinA === pair.isinB
      || typeof pair.available !== 'boolean'
    ) {
      continue;
    }
    if (
      pair.available
      && (!Number.isFinite(pair.overlapPct) || pair.overlapPct < 0 || pair.overlapPct > 100)
    ) {
      continue;
    }
    index.set(pairKey(pair.isinA, pair.isinB), pair);
  }
  return index;
}

export function getPairwiseOverlap(index, isinA, isinB) {
  if (!index || !isinA || !isinB || isinA === isinB) return null;
  return index.get(pairKey(isinA, isinB)) || null;
}

export function reconcilePairwiseSelection(positions, selectedIsins = []) {
  const available = positions.map((position) => position.isin).filter(Boolean);
  if (available.length < 2) return [];

  const retained = [...new Set(selectedIsins)].filter((isin) => available.includes(isin));
  const first = retained[0] || available[0];
  const second = retained.find((isin) => isin !== first)
    || available.find((isin) => isin !== first);
  return second ? [first, second] : [];
}

function normalizeHoldingCompanyIdentity(holding) {
  const security = holding?.security || {};
  const company = security.company_id || security.canonical_name;
  if (typeof company !== 'string' || !company.trim()) return null;
  return company.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || null;
}

function summarizeHoldings(holdings) {
  const isinWeights = new Map();
  const companies = new Map();
  const companyIsinWeights = new Map();
  const companyNames = new Map();

  for (const holding of holdings || []) {
    const rawWeight = holding?.exposure?.weight_pct;
    const weight = Number(rawWeight);
    if (rawWeight === null || rawWeight === undefined || !Number.isFinite(weight) || weight < 0) continue;

    const security = holding?.security || {};
    const isin = typeof security.isin === 'string' ? security.isin.trim().toLowerCase() : '';
    const company = normalizeHoldingCompanyIdentity(holding);
    if (isin) isinWeights.set(isin, (isinWeights.get(isin) || 0) + weight);
    if (!company) continue;

    companies.set(company, (companies.get(company) || 0) + weight);
    if (!companyNames.has(company)) {
      companyNames.set(company, security.canonical_name || security.name || security.ticker || company);
    }
    if (!companyIsinWeights.has(company)) companyIsinWeights.set(company, new Map());
    if (isin) {
      const weightsByIsin = companyIsinWeights.get(company);
      weightsByIsin.set(isin, (weightsByIsin.get(isin) || 0) + weight);
    }
  }

  return { isinWeights, companies, companyIsinWeights, companyNames };
}

export function buildPairwiseHoldingsBreakdown(holdingsA, holdingsB, maximumCompanies = 20) {
  const summaryA = summarizeHoldings(holdingsA);
  const summaryB = summarizeHoldings(holdingsB);
  const exactIsinWeights = new Map();
  let exactOverlap = 0;

  for (const [isin, weightA] of summaryA.isinWeights) {
    const weightB = summaryB.isinWeights.get(isin);
    if (weightB === undefined) continue;
    const contribution = Math.min(weightA, weightB);
    exactIsinWeights.set(isin, contribution);
    exactOverlap += contribution;
  }

  const companies = [];
  let exactCompanyOverlap = 0;
  for (const [company, weightA] of summaryA.companies) {
    const weightB = summaryB.companies.get(company);
    if (weightB === undefined) continue;

    const companyIsinsA = summaryA.companyIsinWeights.get(company) || new Map();
    const companyIsinsB = summaryB.companyIsinWeights.get(company) || new Map();
    let exactOverlapForCompany = 0;
    for (const [isin, isinWeightA] of companyIsinsA) {
      const isinWeightB = companyIsinsB.get(isin);
      if (isinWeightB !== undefined) exactOverlapForCompany += Math.min(isinWeightA, isinWeightB);
    }
    exactCompanyOverlap += exactOverlapForCompany;

    companies.push({
      key: company,
      name: summaryA.companyNames.get(company) || summaryB.companyNames.get(company) || company,
      weightA,
      weightB,
      contribution: Math.max(exactOverlapForCompany, Math.min(weightA, weightB)),
    });
  }

  for (const [isin, contribution] of exactIsinWeights) {
    const companyA = [...summaryA.companyIsinWeights]
      .find(([, weightsByIsin]) => weightsByIsin.has(isin))?.[0];
    const companyB = [...summaryB.companyIsinWeights]
      .find(([, weightsByIsin]) => weightsByIsin.has(isin))?.[0];
    if (companyA && companyA === companyB) continue;

    const holdingA = (holdingsA || []).find((holding) => holding?.security?.isin?.trim?.().toLowerCase() === isin);
    const holdingB = (holdingsB || []).find((holding) => holding?.security?.isin?.trim?.().toLowerCase() === isin);
    companies.push({
      key: `isin:${isin}`,
      name: holdingA?.security?.canonical_name
        || holdingA?.security?.name
        || holdingB?.security?.canonical_name
        || holdingB?.security?.name
        || holdingA?.security?.ticker
        || holdingB?.security?.ticker
        || isin,
      weightA: summaryA.isinWeights.get(isin),
      weightB: summaryB.isinWeights.get(isin),
      contribution,
    });
  }

  const unassignedExactOverlap = Math.max(0, exactOverlap - exactCompanyOverlap);
  if (unassignedExactOverlap > 0 && !companies.some((company) => company.key.startsWith('isin:'))) {
    companies.push({
      key: 'shared:isin',
      name: 'Shared security',
      weightA: unassignedExactOverlap,
      weightB: unassignedExactOverlap,
      contribution: unassignedExactOverlap,
    });
  }

  companies.sort((companyA, companyB) =>
    companyB.contribution - companyA.contribution
    || (companyB.weightA + companyB.weightB) - (companyA.weightA + companyA.weightB)
    || companyA.name.localeCompare(companyB.name)
  );

  const limit = Number.isFinite(maximumCompanies) && Number.isInteger(maximumCompanies) && maximumCompanies > 0
    ? maximumCompanies
    : 20;
  const displayed = companies.slice(0, limit);
  const remainingCompanies = companies.slice(limit);
  const remainingWeights = remainingCompanies.reduce((totals, company) => ({
    weightA: totals.weightA + company.weightA,
    weightB: totals.weightB + company.weightB,
  }), { weightA: 0, weightB: 0 });
  return {
    companies,
    displayed,
    remainingContribution: remainingCompanies.reduce((total, company) => total + company.contribution, 0),
    remainingWeights,
  };
}

export function buildPairwiseMatrix(positions, index, threshold) {
  return positions.map((position, rowIndex) => ({
    product: {
      isin: position.isin,
      ticker: position.entry.ticker,
      name: position.entry.name,
    },
    cells: positions.map((other, columnIndex) => {
      if (columnIndex === rowIndex) return { type: 'diagonal' };
      if (columnIndex > rowIndex) return { type: 'empty' };

      const pair = getPairwiseOverlap(index, position.isin, other.isin);
      if (!pair || !pair.available || !Number.isFinite(pair.overlapPct)) {
        return { type: 'unavailable', pair };
      }
      return {
        type: 'overlap',
        overlapPct: pair.overlapPct,
        coveragePctA: pair.coveragePctA,
        coveragePctB: pair.coveragePctB,
        nearIdentical: pair.overlapPct >= threshold,
      };
    }),
  }));
}

export function findNearIdenticalPairs(positions, index, threshold) {
  return buildPairwiseMatrix(positions, index, threshold).flatMap((row, rowIndex) =>
    row.cells.flatMap((cell, columnIndex) => {
      if (cell.type !== 'overlap' || !cell.nearIdentical) return [];
      const other = positions[columnIndex];
      return [{
        productA: row.product,
        productB: {
          isin: other.isin,
          ticker: other.entry.ticker,
          name: other.entry.name,
        },
        overlapPct: cell.overlapPct,
      }];
    })
  );
}

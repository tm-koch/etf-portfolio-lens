function cloneValue(value) {
  return value == null ? value : JSON.parse(JSON.stringify(value));
}

export function buildReportSnapshot({
  scope = 'portfolio',
  portfolioPositions = [],
  catalogEtfs = [],
  catalogTimestamp = null,
  portfolioMode = 'full',
  valuationMode = 'latest',
  locale = 'en-CH',
  buildInfo = null,
  livePrices = null,
  generatedAt = new Date().toISOString(),
} = {}) {
  if (!['portfolio', 'catalog'].includes(scope)) {
    throw new RangeError(`Unsupported report scope: ${scope}`);
  }

  const reportPositions = cloneValue(portfolioPositions);
  const positionsByIsin = new Map(reportPositions.map((position) => [position.isin, position]));
  const reportCatalog = scope === 'catalog' ? cloneValue(catalogEtfs) : [];
  const etfs = scope === 'catalog'
    ? reportCatalog.map((entry) => ({
      entry,
      portfolioPosition: positionsByIsin.get(entry.isin) || null,
    }))
    : reportPositions.map((position) => ({
      entry: position.entry,
      portfolioPosition: position,
    }));
  const sourceCommit = buildInfo?.source?.commit;

  return {
    scope,
    generatedAt,
    locale,
    portfolioMode,
    valuationMode,
    portfolioPositions: reportPositions,
    etfs,
    provenance: {
      buildId: typeof sourceCommit === 'string' ? sourceCommit.slice(0, 7) : null,
      snapshotTimestamp: buildInfo?.data?.timestamp || catalogTimestamp || null,
      livePricesTimestamp: livePrices?.generated_at || null,
    },
  };
}

export function buildReportAnalytics({
  snapshot,
  rankedCompanies = [],
  summary = {},
  rollups = {},
  redundancy = null,
  diversification = null,
  charts = {},
  pairwiseHeatmap = [],
} = {}) {
  const etfColumns = (snapshot?.portfolioPositions || []).map((position) => ({
    isin: position.isin,
    ticker: position.entry?.ticker || position.isin,
    name: position.entry?.name || position.isin,
  }));
  const ranked = [...rankedCompanies].sort((first, second) =>
    Number(second.weight || 0) - Number(first.weight || 0)
      || String(first.key || first.name).localeCompare(String(second.key || second.name))
  );
  const companies = ranked.slice(0, 20).map((company, index) => {
    const contributors = new Map(
      (company.contributors || []).map((contributor) => [contributor.ticker, contributor])
    );
    return {
      rank: index + 1,
      key: company.key,
      name: company.name,
      totalContribution: Number(company.weight) || 0,
      contributions: etfColumns.map((column) => {
        const contributor = contributors.get(column.ticker);
        return {
          ticker: column.ticker,
          value: contributor ? Number(contributor.weight) || 0 : null,
        };
      }),
    };
  });

  return {
    summary: cloneValue(summary),
    rollups: cloneValue(rollups),
    redundancy: cloneValue(redundancy),
    diversification: cloneValue(diversification),
    charts: cloneValue(charts),
    pairwiseHeatmap: cloneValue(pairwiseHeatmap),
    etfColumns,
    companies,
  };
}
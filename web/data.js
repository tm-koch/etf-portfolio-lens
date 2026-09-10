const CATALOG_URL = './data/catalog.json';
const BUILD_INFO_URL = './build-info.json';
const LIVE_PRICES_URL = './data/live_prices.json';

/** @typedef {{ isin: string, ticker: string, name: string, provider: string, snapshotPath: string }} CatalogEntry */
/** @typedef {{ generatedAt: string, basis: string, etfs: CatalogEntry[] }} PublishedCatalog */
/** @typedef {{ schemaVersion: number, repositoryUrl?: string, source?: { commit?: string, commitTimestamp?: string }, publishedAt?: string, data?: { timestamp?: string, live?: { generatedAt?: string, status?: string } }, details?: Record<string, unknown> }} BuildInfo */
/** @typedef {{ schema_version: number, generated_at: string, status: string, quotes: Record<string, { price?: number, currency?: string, quoted_at?: string, status?: string }>, fx: Record<string, { rate?: number, quoted_at?: string, status?: string }> }} LivePrices */

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to load ${url}: ${response.status}`);
  }
  return response.json();
}

async function fetchJsonWithFallbacks(urls) {
  let lastError = null;

  for (const url of urls) {
    try {
      return await fetchJson(url);
    } catch (error) {
      lastError = error;
    }
  }

  throw lastError || new Error('Failed to load snapshot');
}

export async function loadPublishedCatalog() {
  /** @type {PublishedCatalog} */
  const catalog = await fetchJson(CATALOG_URL);
  return {
    ...catalog,
    etfs: catalog.etfs.map((entry) => ({
      ...entry,
      searchText: [entry.name, entry.ticker, entry.isin, entry.provider]
        .filter(Boolean)
        .join(' ')
        .toLowerCase(),
    })),
  };
}

export async function loadBuildInfo() {
  try {
    /** @type {BuildInfo} */
    const buildInfo = await fetchJson(BUILD_INFO_URL);
    if (!buildInfo || buildInfo.schemaVersion !== 1 || typeof buildInfo !== 'object') {
      return null;
    }
    return buildInfo;
  } catch {
    return null;
  }
}

export async function loadLivePrices() {
  try {
    /** @type {LivePrices} */
    const artifact = await fetchJsonWithFallbacks([
      LIVE_PRICES_URL,
      '../data/live_prices.json',
    ]);
    if (!artifact || artifact.schema_version !== 1 || typeof artifact.generated_at !== 'string') {
      return null;
    }
    if (!artifact.quotes || typeof artifact.quotes !== 'object' || !artifact.fx || typeof artifact.fx !== 'object') {
      return null;
    }
    return artifact;
  } catch {
    return null;
  }
}

export async function loadSnapshot(entry) {
  const normalizedPath = entry.snapshotPath.replace(/^\/+/, '');
  const candidateUrls = [
    entry.snapshotPath,
    `./${normalizedPath}`,
    `../${normalizedPath}`,
  ];

  return fetchJsonWithFallbacks(candidateUrls);
}

export function buildCatalogMaps(catalog) {
  const byIsin = new Map();
  const byTicker = new Map();
  for (const entry of catalog.etfs) {
    byIsin.set(entry.isin, entry);
    byTicker.set(entry.ticker.toLowerCase(), entry);
  }
  return { byIsin, byTicker };
}

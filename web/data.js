const CATALOG_URL = './data/catalog.json';

/** @typedef {{ isin: string, ticker: string, name: string, provider: string, snapshotPath: string }} CatalogEntry */
/** @typedef {{ generatedAt: string, basis: string, etfs: CatalogEntry[] }} PublishedCatalog */

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to load ${url}: ${response.status}`);
  }
  return response.json();
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

export async function loadSnapshot(entry) {
  return fetchJson(entry.snapshotPath);
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

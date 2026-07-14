import { buildCatalogMaps, loadPublishedCatalog, loadSnapshot } from './data.js';
import { destroyComparisonCharts, renderComparisonChart } from './charts.js';

const STORAGE_KEY = 'etf-lens.portfolio.v1';
const defaultState = {
  activeTab: 'portfolio',
  searchTerm: '',
  portfolio: [],
};

const chartRefs = {
  sector: { current: null },
  region: { current: null },
  currency: { current: null },
};

const PORTFOLIO_REFERENCE_LABEL = 'Portfolio reference (share-weighted)';
const COMPANY_BATCH_SIZE = 20;

const ETF_SEGMENT_COLORS = [
  '#67d3ff',
  '#f7b955',
  '#9dffcb',
  '#b79bff',
  '#ff8b8b',
  '#f2dd72',
  '#63f0a6',
  '#7ec8ff',
];

const state = {
  ...defaultState,
  catalog: null,
  catalogMaps: null,
  snapshots: new Map(),
  companyRanked: [],
  companyVisibleCount: 0,
  companyObserver: null,
};

const elements = {};

function loadPortfolioState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return [];
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function savePortfolioState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.portfolio));
}

function formatPercent(value) {
  return `${value.toFixed(1)}%`;
}

function formatCount(value) {
  return new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(value);
}

function getHoldingName(holding) {
  return holding?.security?.name || holding?.security?.ticker || 'Unknown holding';
}

function getHoldingKey(holding) {
  return holding?.security?.isin || holding?.security?.ticker || getHoldingName(holding);
}

function getSnapshotForPosition(position) {
  return state.snapshots.get(position.isin) || null;
}

function enrichPositions() {
  return state.portfolio
    .map((position) => {
      const entry = state.catalogMaps.byIsin.get(position.isin);
      const snapshot = entry ? state.snapshots.get(position.isin) : null;
      return {
        ...position,
        entry,
        snapshot,
        shares: Number(position.shares) || 0,
      };
    })
    .filter((position) => position.entry);
}

function getSelectedPositions() {
  return enrichPositions();
}

function getTotalShareUnits(positions) {
  return positions.reduce((sum, position) => sum + Math.max(position.shares, 0), 0);
}

function getPositionWeight(position, totalShareUnits) {
  if (!totalShareUnits) {
    return 0;
  }
  return (Math.max(position.shares, 0) / totalShareUnits) * 100;
}

function roundExposurePercent(value) {
  return Math.round(value * 10) / 10;
}

function disconnectCompanyObserver() {
  if (state.companyObserver) {
    state.companyObserver.disconnect();
    state.companyObserver = null;
  }
}

function getMetricData(positions, metricKey) {
  const labels = new Set();
  const series = [];

  for (const position of positions) {
    const snapshot = position.snapshot;
    const aggregates = snapshot?.aggregates || {};
    const items = aggregates[metricKey] || [];
    const values = new Map();

    for (const item of items) {
      if (!item?.name) {
        continue;
      }
      labels.add(item.name);
      values.set(item.name, Number(item.weight_pct || 0));
    }

    series.push({ label: position.entry.ticker, values });
  }

  return { labels: [...labels], series };
}

function normalizeCurrencyItems(items) {
  const normalized = [];
  let otherWeight = 0;
  let otherIncluded = false;

  for (const item of items || []) {
    if (!item?.name) {
      continue;
    }

    const weight = Number(item.weight_pct || 0);
    const name = item.name;
    if (name === 'Unknown' || weight < 1) {
      otherWeight += weight;
      otherIncluded = true;
      continue;
    }

    normalized.push({ name, weight_pct: weight });
  }

  if (otherIncluded) {
    normalized.push({ name: 'Other', weight_pct: otherWeight });
  }

  return normalized;
}

function getCurrencyMetricData(positions) {
  const labels = new Set();
  const series = [];
  let otherGrouped = false;

  for (const position of positions) {
    const snapshot = position.snapshot;
    const aggregates = snapshot?.aggregates || {};
    const items = normalizeCurrencyItems(aggregates.currency_weights);
    const values = new Map();

    for (const item of items) {
      labels.add(item.name);
      values.set(item.name, Number(item.weight_pct || 0));
      if (item.name === 'Other') {
        otherGrouped = true;
      }
    }

    series.push({ label: position.entry.ticker, values });
  }

  return {
    labels: [...labels],
    series,
    legendLabelOverrides: otherGrouped ? new Map([['Other', 'Other (<1% / Unknown)']]) : new Map(),
  };
}

function getComparisonSelection() {
  return getSelectedPositions();
}

function aggregateCompanyExposure(positions) {
  const totalShareUnits = getTotalShareUnits(positions);
  const exposure = new Map();
  const warnings = [];

  for (const [positionIndex, position] of positions.entries()) {
    const snapshot = position.snapshot;
    if (!snapshot) {
      warnings.push(`${position.entry.ticker}: snapshot not loaded`);
      continue;
    }

    const contributionColor = ETF_SEGMENT_COLORS[positionIndex % ETF_SEGMENT_COLORS.length];

    const positionWeight = getPositionWeight(position, totalShareUnits);
    const holdings = snapshot.holdings || [];
    for (const holding of holdings) {
      const holdingWeight = Number(holding?.exposure?.weight_pct || 0);
      const contribution = (positionWeight * holdingWeight) / 100;
      const key = getHoldingKey(holding);
      const name = getHoldingName(holding);
      const existing = exposure.get(key) || {
        key,
        name,
        weight: 0,
        etfs: new Set(),
        contributors: new Map(),
      };
      existing.weight += contribution;
      existing.etfs.add(position.entry.ticker);
      const contributor = existing.contributors.get(position.entry.ticker) || {
        ticker: position.entry.ticker,
        name: position.entry.name,
        weight: 0,
        color: contributionColor,
      };
      contributor.weight += contribution;
      contributor.color = contributionColor;
      existing.contributors.set(position.entry.ticker, contributor);
      exposure.set(key, existing);
    }

    const unmatchedCount = (holdings || []).filter(
      (holding) => holding?.provenance?.match?.status !== 'matched'
    ).length;
    if (unmatchedCount) {
      warnings.push(`${position.entry.ticker}: ${unmatchedCount} holdings are unmatched or partially matched`);
    }
  }

  const ranked = [...exposure.values()]
    .sort((a, b) => b.weight - a.weight)
    .map((company) => {
      const contributors = [...company.contributors.values()]
        .map((contributor) => ({
          ...contributor,
          shareOfCompany: company.weight ? (contributor.weight / company.weight) * 100 : 0,
        }))
        .sort((a, b) => b.weight - a.weight);

      return {
        ...company,
        contributors,
      };
    });
  const normalizedWeights = ranked.map((company) => roundExposurePercent(company.weight));
  const maxWeight = normalizedWeights[0] || 0;

  const scaled = ranked.map((company, index) => ({
    ...company,
    displayWeight: normalizedWeights[index],
    shareOfMax: maxWeight ? (normalizedWeights[index] / maxWeight) * 100 : 0,
  }));
  return {
    totalShareUnits,
    ranked: scaled,
    warnings,
  };
}

function buildCompanyRow(company, index) {
  const barSegments = company.contributors.map((contributor) => {
    const tooltip = `${contributor.ticker}: ${formatPercent(contributor.shareOfCompany)} of ${company.name} (${formatPercent(contributor.weight)} of portfolio)`;
    const showInlineLabel = contributor.shareOfCompany >= 16;
    return `
      <div
        class="company-bar-segment"
        style="flex: ${Math.max(contributor.shareOfCompany, 0.01)} 1 0; background: ${contributor.color};"
        title="${tooltip}"
        aria-label="${tooltip}"
      >
        ${showInlineLabel ? `<span class="company-segment-label">${contributor.ticker} ${formatPercent(contributor.shareOfCompany)}</span>` : ''}
      </div>
    `;
  }).join('');

  const detailChips = company.contributors.map((contributor) => `
    <div class="company-chip" title="${contributor.ticker}: ${formatPercent(contributor.shareOfCompany)} of company exposure, ${formatPercent(contributor.weight)} of portfolio">
      <span class="chip-swatch" style="background: ${contributor.color};"></span>
      <span class="chip-ticker">${contributor.ticker}</span>
      <strong>${formatPercent(contributor.shareOfCompany)}</strong>
      <span class="chip-meta">${formatPercent(contributor.weight)} portfolio</span>
    </div>
  `).join('');

  return `
    <article class="company-row">
      <div class="company-row-head">
        <div class="company-row-title">
          <div class="company-name">${index + 1}. ${company.name}</div>
          <div class="company-meta">${company.etfs.size} ETF(s) contributing · ${formatPercent(company.weight)} of portfolio</div>
        </div>
        <div class="company-total">${formatPercent(company.weight)}</div>
      </div>
      <div class="company-bar-track" style="width: ${Math.max(company.shareOfMax, 0.01)}%;" role="img" aria-label="${company.name} exposure split across ETFs: ${company.contributors.map((contributor) => `${contributor.ticker} ${formatPercent(contributor.shareOfCompany)}`).join(', ')}">
        <div class="company-bar-fill">
          ${barSegments}
        </div>
      </div>
      <div class="company-chip-list">
        ${detailChips}
      </div>
    </article>
  `;
}

function appendCompanyBatch() {
  const ranked = state.companyRanked;
  const start = state.companyVisibleCount;
  const end = Math.min(start + COMPANY_BATCH_SIZE, ranked.length);

  if (end <= start) {
    disconnectCompanyObserver();
    return;
  }

  const fragment = document.createRange().createContextualFragment(
    ranked.slice(start, end).map((company, index) => buildCompanyRow(company, start + index)).join('')
  );
  const sentinel = elements.companyList.querySelector('.company-scroll-sentinel');

  if (sentinel) {
    elements.companyList.insertBefore(fragment, sentinel);
  } else {
    elements.companyList.appendChild(fragment);
  }

  state.companyVisibleCount = end;

  if (state.companyVisibleCount >= ranked.length) {
    const existingSentinel = elements.companyList.querySelector('.company-scroll-sentinel');
    if (existingSentinel) {
      existingSentinel.remove();
    }
    disconnectCompanyObserver();
    return;
  }

  const nextSentinel = elements.companyList.querySelector('.company-scroll-sentinel');
  if (state.companyObserver && nextSentinel) {
    state.companyObserver.observe(nextSentinel);
  }
}

function ensureCompanyObserver() {
  disconnectCompanyObserver();
  state.companyObserver = new IntersectionObserver(
    (entries) => {
      if (state.activeTab !== 'aggregated') {
        return;
      }
      if (entries.some((entry) => entry.isIntersecting)) {
        const sentinel = elements.companyList.querySelector('.company-scroll-sentinel');
        if (sentinel) {
          state.companyObserver?.unobserve(sentinel);
        }
        appendCompanyBatch();
      }
    },
    { root: null, rootMargin: '0px 0px 240px 0px', threshold: 0 }
  );

  const sentinel = elements.companyList.querySelector('.company-scroll-sentinel');
  if (sentinel) {
    state.companyObserver.observe(sentinel);
  }
}

function aggregatePortfolioRollups(positions) {
  const totals = {
    sector: new Map(),
    region: new Map(),
    currency: new Map(),
  };
  const totalShareUnits = getTotalShareUnits(positions);

  for (const position of positions) {
    const snapshot = position.snapshot;
    if (!snapshot || !totalShareUnits) {
      continue;
    }
    const positionWeight = getPositionWeight(position, totalShareUnits);
    const aggregates = snapshot.aggregates || {};
    const add = (bucket, items) => {
      for (const item of items || []) {
        if (!item?.name) {
          continue;
        }
        const current = bucket.get(item.name) || 0;
        bucket.set(item.name, current + (positionWeight * Number(item.weight_pct || 0)) / 100);
      }
    };
    add(totals.sector, aggregates.sector_weights);
    add(totals.region, aggregates.region_weights);
    add(totals.currency, aggregates.currency_weights);
  }

  return totals;
}

function mergeLabels(...labelGroups) {
  const labels = [];
  const seen = new Set();

  for (const group of labelGroups) {
    for (const label of group || []) {
      if (seen.has(label)) {
        continue;
      }
      seen.add(label);
      labels.push(label);
    }
  }

  return labels;
}

function buildReferenceSeries(labels, values, label = PORTFOLIO_REFERENCE_LABEL) {
  return {
    label,
    values: new Map(labels.map((entry) => [entry, values.get(entry) || 0])),
  };
}

function updateSummary() {
  const positions = getSelectedPositions();
  const totalShareUnits = getTotalShareUnits(positions);
  const uniqueEtfs = positions.length;
  const totalHoldings = positions.reduce((sum, position) => sum + (position.snapshot?.holdings?.length || 0), 0);
  const overlapCount = aggregateCompanyExposure(positions).ranked.filter((item) => item.etfs.size > 1).length;

  const cards = [
    { label: 'Positions', value: formatCount(uniqueEtfs) },
    { label: 'Share units', value: formatCount(totalShareUnits) },
    { label: 'Underlying holdings', value: formatCount(totalHoldings) },
    { label: 'Shared companies', value: formatCount(overlapCount) },
  ];

  elements.summaryGrid.innerHTML = cards
    .map(
      (card) => `
        <article class="summary-card">
          <div class="label">${card.label}</div>
          <div class="value">${card.value}</div>
        </article>
      `
    )
    .join('');
}

function renderCatalog() {
  const term = state.searchTerm.trim().toLowerCase();
  const entries = state.catalog.etfs.filter((entry) => !term || entry.searchText.includes(term));

  if (!entries.length) {
    elements.catalogList.innerHTML = '<div class="empty-state">No ETFs match the current search.</div>';
    return;
  }

  elements.catalogList.innerHTML = entries
    .map((entry) => {
      const selected = state.portfolio.some((position) => position.isin === entry.isin);
      return `
        <article class="catalog-item">
          <div class="catalog-head">
            <div class="catalog-title">
              <strong>${entry.name}</strong>
              <span>${entry.ticker} · ${entry.isin} · ${entry.provider}</span>
            </div>
            <button type="button" data-add-etf="${entry.isin}" ${selected ? 'disabled' : ''}>
              ${selected ? 'Added' : 'Add'}
            </button>
          </div>
          <div class="position-meta">Snapshot: ${entry.snapshotPath}</div>
        </article>
      `;
    })
    .join('');
}

function renderPositions() {
  const positions = getSelectedPositions();
  if (!positions.length) {
    elements.positionsBody.innerHTML = '<tr><td colspan="4"><div class="empty-state">No positions yet. Search the catalog and add an ETF.</div></td></tr>';
    elements.portfolioHint.textContent = 'The portfolio is empty.';
    return;
  }

  const totalShareUnits = getTotalShareUnits(positions);
  elements.portfolioHint.textContent = 'Share counts act as the portfolio weighting proxy until ETF unit prices are published.';

  elements.positionsBody.innerHTML = positions
    .map((position) => {
      const weight = getPositionWeight(position, totalShareUnits);
      const snapshot = position.snapshot;
      const warnings = snapshot?.holdings?.filter((holding) => holding?.provenance?.match?.status !== 'matched').length || 0;
      return `
        <tr class="position-row">
          <td>
            <div class="position-name">
              <strong>${position.entry.ticker}</strong>
              <span>${position.entry.name}</span>
            </div>
          </td>
          <td>
            <input class="position-input" type="number" min="0" step="1" value="${position.shares}" data-shares-input="${position.isin}" />
          </td>
          <td>${formatPercent(weight)}${warnings ? ` · ${warnings} warnings` : ''}</td>
          <td><button type="button" class="remove-button" data-remove-position="${position.isin}">Remove</button></td>
        </tr>
      `;
    })
    .join('');
}

function renderComparisonToolbar(positions) {
  if (!positions.length) {
    elements.comparisonToolbar.innerHTML = '<div class="empty-state">Add positions to compare ETFs.</div>';
    return;
  }

  elements.comparisonToolbar.innerHTML = positions
    .map(
      (position) => `
        <label class="tool-pill" title="${position.entry.name}">
          <input type="checkbox" checked data-compare-toggle="${position.isin}" title="${position.entry.name}" />
          ${position.entry.ticker}
        </label>
      `
    )
    .join('');
}

function getComparisonPositions() {
  const selected = getSelectedPositions();
  const checked = new Set(
    [...document.querySelectorAll('[data-compare-toggle]')]
      .filter((input) => input.checked)
      .map((input) => input.dataset.compareToggle)
  );
  return selected.filter((position) => checked.has(position.isin));
}

function renderComparisonCharts() {
  const comparisonPositions = getComparisonPositions();
  const portfolioPositions = getSelectedPositions();

  const sectorData = getMetricData(comparisonPositions, 'sector_weights');
  const regionData = getMetricData(comparisonPositions, 'region_weights');
  const currencyData = getCurrencyMetricData(comparisonPositions);

  const portfolioSectorData = getMetricData(portfolioPositions, 'sector_weights');
  const portfolioRegionData = getMetricData(portfolioPositions, 'region_weights');
  const portfolioCurrencyData = getCurrencyMetricData(portfolioPositions);

  const rollups = aggregatePortfolioRollups(portfolioPositions);
  const hasPortfolioReference = getTotalShareUnits(portfolioPositions) > 0;

  const sectorLabels = mergeLabels(portfolioSectorData.labels, sectorData.labels);
  const regionLabels = mergeLabels(portfolioRegionData.labels, regionData.labels);
  const currencyLabels = mergeLabels(portfolioCurrencyData.labels, currencyData.labels);

  const sectorSeries = hasPortfolioReference
    ? [buildReferenceSeries(sectorLabels, rollups.sector), ...sectorData.series]
    : sectorData.series;
  const regionSeries = hasPortfolioReference
    ? [buildReferenceSeries(regionLabels, rollups.region), ...regionData.series]
    : regionData.series;
  const currencySeries = hasPortfolioReference
    ? [buildReferenceSeries(currencyLabels, rollups.currency), ...currencyData.series]
    : currencyData.series;

  renderComparisonChart(chartRefs.sector, elements.sectorCanvas, 'Sectors', sectorSeries, sectorLabels, {
    legendMode: 'labels',
  });
  renderComparisonChart(chartRefs.region, elements.regionCanvas, 'Regions', regionSeries, regionLabels, {
    legendMode: 'labels',
  });
  renderComparisonChart(
    chartRefs.currency,
    elements.currencyCanvas,
    'Currencies',
    currencySeries,
    currencyLabels,
    {
      legendMode: 'labels',
      legendLabelOverrides: currencyData.legendLabelOverrides,
      labelColorOverrides: new Map([['Other', '#4b5563']]),
    }
  );
}

function renderRollups() {
  const positions = getSelectedPositions();
  const rollups = aggregatePortfolioRollups(positions);
  const cards = [
    { label: 'Sector exposure', values: rollups.sector },
    { label: 'Region exposure', values: rollups.region },
    { label: 'Currency exposure', values: rollups.currency },
  ];

  elements.rollupGrid.innerHTML = cards
    .map((card) => {
      const sorted = [...card.values.entries()].sort((a, b) => b[1] - a[1]);
      const top = sorted[0];
      return `
        <article class="rollup-card">
          <strong>${card.label}</strong>
          <div class="value">${top ? formatPercent(top[1]) : '0.0%'}</div>
          <div class="subtext">${top ? top[0] : 'No data yet'}</div>
        </article>
      `;
    })
    .join('');
}

function renderCompanyList() {
  const positions = getSelectedPositions();
  const { ranked } = aggregateCompanyExposure(positions);
  state.companyRanked = ranked;
  state.companyVisibleCount = 0;
  disconnectCompanyObserver();

  if (!ranked.length) {
    elements.companyList.innerHTML = '<div class="empty-state">Add positions to calculate company exposure.</div>';
    elements.companyHint.textContent = 'No look-through exposure is available yet.';
    return;
  }

  elements.companyHint.textContent = 'Showing the top 20 holdings. Scroll down to load more.';
  elements.companyList.innerHTML = '';
  appendCompanyBatch();

  if (state.companyVisibleCount < ranked.length) {
    const sentinel = document.createElement('div');
    sentinel.className = 'company-scroll-sentinel';
    sentinel.setAttribute('aria-hidden', 'true');
    elements.companyList.appendChild(sentinel);
    ensureCompanyObserver();
  }
}

function renderWarnings() {
  const positions = getSelectedPositions();
  const { warnings } = aggregateCompanyExposure(positions);
  const items = [];

  for (const position of positions) {
    const snapshot = position.snapshot;
    if (!snapshot) {
      items.push(`${position.entry.ticker}: snapshot unavailable`);
      continue;
    }
    if (!snapshot.holdings?.length) {
      items.push(`${position.entry.ticker}: snapshot has no holdings`);
    }
  }

  items.push(...warnings);

  if (!items.length) {
    elements.warningList.innerHTML = '<div class="empty-state">No warnings detected in the current selection.</div>';
    return;
  }

  elements.warningList.innerHTML = items.map((item) => `
    <article class="warning-item">
      <div class="left">${item}</div>
    </article>
  `).join('');
}

function renderAll() {
  renderCatalog();
  renderPositions();
  renderComparisonToolbar(getSelectedPositions());
  renderComparisonCharts();
  renderRollups();
  renderCompanyList();
  renderWarnings();
  updateSummary();
}

function setTab(tabName) {
  state.activeTab = tabName;
  for (const button of elements.tabButtons) {
    button.classList.toggle('active', button.dataset.tab === tabName);
  }
  for (const panel of elements.tabPanels) {
    panel.classList.toggle('active', panel.dataset.panel === tabName);
  }
  if (tabName === 'comparison') {
    renderComparisonCharts();
  }
  if (tabName === 'aggregated') {
    renderCompanyList();
  }
}

function addPosition(isin) {
  if (state.portfolio.some((position) => position.isin === isin)) {
    return;
  }
  state.portfolio = [...state.portfolio, { isin, shares: 1 }];
  savePortfolioState();
  renderAll();
}

function updatePositionShares(isin, shares) {
  state.portfolio = state.portfolio.map((position) =>
    position.isin === isin ? { ...position, shares } : position
  );
  savePortfolioState();
  renderAll();
}

function removePosition(isin) {
  state.portfolio = state.portfolio.filter((position) => position.isin !== isin);
  savePortfolioState();
  renderAll();
}

async function bootstrap() {
  elements.summaryGrid = document.getElementById('summary-grid');
  elements.tabButtons = [...document.querySelectorAll('.tab-button')];
  elements.tabPanels = [...document.querySelectorAll('.tab-panel')];
  elements.catalogSearch = document.getElementById('catalog-search');
  elements.catalogList = document.getElementById('catalog-list');
  elements.positionsBody = document.getElementById('positions-tbody');
  elements.portfolioHint = document.getElementById('portfolio-hint');
  elements.comparisonToolbar = document.getElementById('comparison-toolbar');
  elements.sectorCanvas = document.getElementById('sector-chart');
  elements.regionCanvas = document.getElementById('region-chart');
  elements.currencyCanvas = document.getElementById('currency-chart');
  elements.rollupGrid = document.getElementById('rollup-grid');
  elements.companyList = document.getElementById('company-list');
  elements.companyHint = document.getElementById('company-hint');
  elements.warningList = document.getElementById('warning-list');

  state.catalog = await loadPublishedCatalog();
  state.catalogMaps = buildCatalogMaps(state.catalog);
  state.portfolio = loadPortfolioState();

  const snapshotResults = await Promise.allSettled(
    state.catalog.etfs.map(async (entry) => [entry.isin, await loadSnapshot(entry)])
  );
  const snapshots = [];
  for (const result of snapshotResults) {
    if (result.status === 'fulfilled') {
      snapshots.push(result.value);
    } else {
      console.warn('Skipping ETF snapshot that failed to load:', result.reason);
    }
  }
  state.snapshots = new Map(snapshots);

  for (const position of state.portfolio) {
    if (!state.catalogMaps.byIsin.has(position.isin)) {
      state.catalogMaps.byIsin.set(position.isin, { ...position, ticker: position.isin, name: position.isin, provider: 'Unknown', snapshotPath: '' });
    }
  }

  elements.catalogSearch.addEventListener('input', (event) => {
    state.searchTerm = event.target.value;
    renderCatalog();
  });

  document.addEventListener('click', (event) => {
    const addButton = event.target.closest('[data-add-etf]');
    if (addButton) {
      addPosition(addButton.dataset.addEtf);
      return;
    }

    const removeButton = event.target.closest('[data-remove-position]');
    if (removeButton) {
      removePosition(removeButton.dataset.removePosition);
      return;
    }

    const tabButton = event.target.closest('[data-tab]');
    if (tabButton) {
      setTab(tabButton.dataset.tab);
      return;
    }
  });

  document.addEventListener('change', (event) => {
    const sharesInput = event.target.closest('[data-shares-input]');
    if (sharesInput) {
      updatePositionShares(sharesInput.dataset.sharesInput, Number(sharesInput.value || 0));
      return;
    }

    const compareToggle = event.target.closest('[data-compare-toggle]');
    if (compareToggle) {
      renderComparisonCharts();
    }
  });

  renderAll();
  setTab('portfolio');
}

window.addEventListener('DOMContentLoaded', () => {
  bootstrap().catch((error) => {
    document.body.innerHTML = `<pre style="white-space: pre-wrap; padding: 24px; color: #fff;">Failed to start ETF Portfolio Lens: ${error.message}</pre>`;
    console.error(error);
  });
});

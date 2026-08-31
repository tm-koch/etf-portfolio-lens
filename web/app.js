import { buildCatalogMaps, loadBuildInfo, loadPublishedCatalog, loadSnapshot } from './data.js?v=20260816-3';
import { destroyComparisonCharts, renderComparisonChart } from './charts.js?v=20260812-3';
import { calculateImportedPosition, extractPdfPages, matchImportedRows, parseSaxoPages } from './portfolio-import.js';

const STORAGE_KEY = 'etf-lens.portfolio.v1';
const ACTIVE_TAB_STORAGE_KEY = 'etf-lens.active-tab.v1';
const COMPACT_EXPLORE_STORAGE_KEY = 'etf-lens.compact-explore-preview.v1';
const PORTFOLIO_IMPORT_DEBUG_STORAGE_KEY = 'etf-lens.portfolio-import-debug.v1';
const COLOR_MODE_STORAGE_KEY = 'etf-lens.color-mode.v1';
const SHARE_FRAGMENT_KEY = 'portfolio';
const SHARE_PAYLOAD_VERSION = 1;
const COLOR_MODES = ['bright', 'automatic', 'dark'];
const DARK_MODE_MEDIA_QUERY = '(prefers-color-scheme: dark)';
const defaultState = {
  activeTab: 'home',
  searchTerm: '',
  companySearchTerm: '',
  portfolio: [],
  importReviewRows: [],
  compactExplorePreview: false,
  colorMode: 'automatic',
  effectiveColorMode: 'bright',
  shareFeedback: '',
  shareFallbackUrl: '',
};

const chartRefs = {
  sector: { current: null },
  region: { current: null },
  currency: { current: null },
};

const PORTFOLIO_REFERENCE_LABEL = 'Portfolio reference (share-weighted)';
const COMPANY_BATCH_SIZE = 20;
const CHART_FRAME_HEIGHT_DESKTOP = '680px';
const CHART_FRAME_HEIGHT_MOBILE_TABLET = '420px';
const INCOMPLETE_MATCH_STATUSES = new Set(['ambiguous', 'unmatched']);

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
  buildInfo: null,
  buildDialogReturnFocus: null,
  companyRanked: [],
  companyVisibleCount: 0,
  companyObserver: null,
  colorModeMediaQuery: null,
};

const elements = {};

const NAVIGATION_DESTINATIONS = [
  { key: 'home', label: 'Home', icon: 'house' },
  { key: 'portfolio', label: 'Portfolio', icon: 'briefcase-business' },
  { key: 'comparison', label: 'Compare', icon: 'scale' },
  { key: 'aggregated', label: 'Explore', icon: 'layers-3' },
];

function getNavigationDestination(key) {
  return NAVIGATION_DESTINATIONS.find((destination) => destination.key === key) || null;
}

function isColorMode(value) {
  return COLOR_MODES.includes(value);
}

function loadColorMode() {
  try {
    const storedMode = localStorage.getItem(COLOR_MODE_STORAGE_KEY);
    return isColorMode(storedMode) ? storedMode : defaultState.colorMode;
  } catch {
    return defaultState.colorMode;
  }
}

function saveColorMode() {
  try {
    localStorage.setItem(COLOR_MODE_STORAGE_KEY, state.colorMode);
  } catch {
    // Browser storage may be unavailable in private or restricted contexts.
  }
}

function prefersDarkMode() {
  return window.matchMedia?.(DARK_MODE_MEDIA_QUERY).matches ?? false;
}

function resolveColorMode(colorMode) {
  return colorMode === 'automatic' ? (prefersDarkMode() ? 'dark' : 'bright') : colorMode;
}

function applyColorMode() {
  state.effectiveColorMode = resolveColorMode(state.colorMode);
  document.documentElement.dataset.colorMode = state.effectiveColorMode;
  document.documentElement.dataset.colorModePreference = state.colorMode;
}

function handleSystemColorModeChange() {
  if (state.colorMode === 'automatic') {
    applyColorMode();
    renderComparisonCharts();
  }
}

function setupColorModeMediaQuery() {
  state.colorModeMediaQuery = window.matchMedia?.(DARK_MODE_MEDIA_QUERY) || null;
  state.colorModeMediaQuery?.addEventListener('change', handleSystemColorModeChange);
}

function setColorMode(colorMode) {
  if (!isColorMode(colorMode)) {
    return;
  }
  state.colorMode = colorMode;
  saveColorMode();
  applyColorMode();
  renderColorModeControl();
  renderComparisonCharts();
}

function renderColorModeControl() {
  if (!elements.colorModeButton || !elements.colorModeMenu) {
    return;
  }

  const modes = [
    { key: 'bright', label: 'Bright', icon: 'sun' },
    { key: 'automatic', label: 'Automatic', icon: 'monitor' },
    { key: 'dark', label: 'Dark', icon: 'moon' },
  ];
  const selectedMode = modes.find((mode) => mode.key === state.colorMode) || modes[1];
  elements.colorModeButton.innerHTML = `
    <i data-lucide="${selectedMode.icon}" aria-hidden="true"></i>
    <span>${selectedMode.label}</span>
  `;
  elements.colorModeButton.setAttribute('aria-label', `Color mode: ${selectedMode.label}`);
  elements.colorModeMenu.innerHTML = modes
    .map(
      (mode) => `
        <button class="color-mode-option" type="button" role="menuitemradio" aria-checked="${mode.key === state.colorMode}" data-color-mode-option="${mode.key}">
          <i data-lucide="${mode.icon}" aria-hidden="true"></i>
          <span>${mode.label}</span>
        </button>
      `
    )
    .join('');
  window.lucide?.createIcons();
}

function positionColorModeControl() {
  if (!elements.colorModeUtility) {
    return;
  }

  const activePanel = document.querySelector(`.tab-panel[data-panel="${state.activeTab}"]`);
  const title = activePanel?.querySelector('.eyebrow, .panel-heading .section-label');
  const titleContainer = title?.closest('.hero, .panel-heading');
  if (!title || !titleContainer || !title.getBoundingClientRect().width) {
    elements.colorModeUtility.style.top = '';
    elements.colorModeUtility.style.right = '';
    return;
  }

  const titleRect = title.getBoundingClientRect();
  const containerRect = titleContainer.getBoundingClientRect();
  elements.colorModeUtility.style.top = `${titleRect.top + window.scrollY}px`;
  elements.colorModeUtility.style.right = `${document.documentElement.clientWidth - containerRect.right - window.scrollX}px`;
}

function toggleColorModeMenu(forceOpen) {
  const isOpen = !elements.colorModeMenu.hidden;
  const shouldOpen = forceOpen ?? !isOpen;
  elements.colorModeMenu.hidden = !shouldOpen;
  elements.colorModeButton.setAttribute('aria-expanded', String(shouldOpen));
  if (shouldOpen) {
    elements.colorModeMenu.querySelector('[aria-checked="true"]')?.focus();
  }
}

function loadActiveTab() {
  const storedTab = localStorage.getItem(ACTIVE_TAB_STORAGE_KEY);
  return getNavigationDestination(storedTab)?.key || defaultState.activeTab;
}

function saveActiveTab() {
  localStorage.setItem(ACTIVE_TAB_STORAGE_KEY, state.activeTab);
}

function loadCompactExplorePreview() {
  try {
    return localStorage.getItem(COMPACT_EXPLORE_STORAGE_KEY) === 'true';
  } catch {
    return false;
  }
}

function saveCompactExplorePreview() {
  try {
    localStorage.setItem(COMPACT_EXPLORE_STORAGE_KEY, String(state.compactExplorePreview));
  } catch {
    // Browser storage may be unavailable in private or restricted contexts.
  }
}

function loadPortfolioImportDebug() {
  try {
    return localStorage.getItem(PORTFOLIO_IMPORT_DEBUG_STORAGE_KEY) === 'true';
  } catch {
    return false;
  }
}

function savePortfolioImportDebug() {
  try {
    localStorage.setItem(PORTFOLIO_IMPORT_DEBUG_STORAGE_KEY, String(state.portfolioImportDebug));
  } catch {
    // Browser storage may be unavailable in private or restricted contexts.
  }
}

function updateImportDebugVisibility() {
  if (!elements.importDebug) {
    return;
  }
  elements.importDebug.hidden = !(state.portfolioImportDebug && window.__etfLensPdfImportPages?.length);
}

function renderNavigation() {
  elements.navigationItems.innerHTML = NAVIGATION_DESTINATIONS
    .map(
      (destination) => `
        <button class="tab-button" data-tab="${destination.key}" type="button">
          <i class="navigation-icon" data-lucide="${destination.icon}" aria-hidden="true"></i>
          <span>${destination.label}</span>
        </button>
      `
    )
    .join('');

  window.lucide?.createIcons();
}

function loadPortfolioState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return [];
    }
    const parsed = JSON.parse(raw);
    return normalizePortfolioPositions(parsed);
  } catch {
    return [];
  }
}

function savePortfolioState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.portfolio));
}

function normalizePortfolioPositions(portfolio) {
  if (!Array.isArray(portfolio)) {
    return [];
  }
  const seenIsins = new Set();
  return portfolio.flatMap((position) => {
    const isin = typeof position?.isin === 'string' ? position.isin.trim().toUpperCase() : '';
    const shares = Number(position?.shares);
    if (!isin || seenIsins.has(isin) || !Number.isFinite(shares) || shares < 0) {
      return [];
    }
    seenIsins.add(isin);
    const normalized = { isin, shares };
    if (Number.isFinite(Number(position.price)) && Number(position.price) >= 0) normalized.price = Number(position.price);
    if (typeof position.currency === 'string' && ['CHF', 'EUR'].includes(position.currency.toUpperCase())) normalized.currency = position.currency.toUpperCase();
    if (Number.isFinite(Number(position.value)) && Number(position.value) >= 0) normalized.value = Number(position.value);
    if (Number.isFinite(Number(position.valueChf)) && Number(position.valueChf) >= 0) normalized.valueChf = Number(position.valueChf);
    return [normalized];
  });
}

function encodeBase64Url(value) {
  const bytes = new TextEncoder().encode(value);
  let binary = '';
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function decodeBase64Url(value) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
  const padded = normalized.padEnd(normalized.length + ((4 - (normalized.length % 4)) % 4), '=');
  const binary = atob(padded);
  const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
  return new TextDecoder('utf-8', { fatal: true }).decode(bytes);
}

function normalizeSharedPortfolio(portfolio) {
  if (!Array.isArray(portfolio)) {
    return null;
  }

  const normalized = [];
  const seenIsins = new Set();
  for (const position of portfolio) {
    if (
      !position ||
      typeof position.isin !== 'string' ||
      !position.isin.trim() ||
      typeof position.shares !== 'number' ||
      !Number.isFinite(position.shares) ||
      position.shares < 0
    ) {
      return null;
    }
    const isin = position.isin.trim().toUpperCase();
    if (seenIsins.has(isin)) {
      return null;
    }
    seenIsins.add(isin);
    const normalizedPosition = { isin, shares: position.shares };
    if (Number.isFinite(Number(position.price)) && Number(position.price) >= 0) normalizedPosition.price = Number(position.price);
    if (typeof position.currency === 'string' && ['CHF', 'EUR'].includes(position.currency.toUpperCase())) normalizedPosition.currency = position.currency.toUpperCase();
    if (Number.isFinite(Number(position.value)) && Number(position.value) >= 0) normalizedPosition.value = Number(position.value);
    if (Number.isFinite(Number(position.valueChf)) && Number(position.valueChf) >= 0) normalizedPosition.valueChf = Number(position.valueChf);
    normalized.push(normalizedPosition);
  }
  return normalized;
}

function encodePortfolioShare(portfolio) {
  const normalizedPortfolio = normalizeSharedPortfolio(portfolio);
  if (!normalizedPortfolio?.length) {
    return null;
  }
  return encodeBase64Url(
    JSON.stringify({ version: SHARE_PAYLOAD_VERSION, portfolio: normalizedPortfolio })
  );
}

function decodePortfolioShare(value) {
  if (!value) {
    return { status: 'missing', portfolio: null };
  }
  try {
    const parsed = JSON.parse(decodeBase64Url(value));
    if (parsed?.version !== SHARE_PAYLOAD_VERSION) {
      return { status: 'invalid', portfolio: null };
    }
    const portfolio = normalizeSharedPortfolio(parsed.portfolio);
    return portfolio ? { status: 'valid', portfolio } : { status: 'invalid', portfolio: null };
  } catch {
    return { status: 'invalid', portfolio: null };
  }
}

function readPortfolioShareFromUrl() {
  const params = new URLSearchParams(window.location.hash.replace(/^#/, ''));
  return decodePortfolioShare(params.get(SHARE_FRAGMENT_KEY));
}

function buildPortfolioShareUrl(portfolio) {
  const encoded = encodePortfolioShare(portfolio);
  if (!encoded) {
    return null;
  }
  const url = new URL(window.location.href);
  url.hash = `${SHARE_FRAGMENT_KEY}=${encoded}`;
  return url.toString();
}

function renderShareFeedback() {
  if (!elements.shareStatus || !elements.shareFallbackUrl) {
    return;
  }
  elements.shareStatus.textContent = state.shareFeedback;
  elements.shareFallbackUrl.value = state.shareFallbackUrl;
  elements.shareFallbackUrl.hidden = !state.shareFallbackUrl;
}

async function sharePortfolio() {
  const url = buildPortfolioShareUrl(state.portfolio);
  if (!url) {
    state.shareFeedback = 'Add at least one position before creating a share link.';
    state.shareFallbackUrl = '';
    renderShareFeedback();
    return;
  }

  state.shareFallbackUrl = url;
  try {
    if (!navigator.clipboard?.writeText) {
      throw new Error('Clipboard unavailable');
    }
    await navigator.clipboard.writeText(url);
    state.shareFeedback = 'Share link copied. It uses the latest published ETF data when opened.';
  } catch {
    state.shareFeedback = 'Automatic copying is unavailable. Copy the link from the field below.';
  }
  renderShareFeedback();
}

function formatPercent(value) {
  return `${value.toFixed(1)}%`;
}

function formatCount(value) {
  return new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(value);
}

function formatChfValue(value) {
  return `CHF ${Number(value).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).replace(/,/g, "'")}`;
}

function formatBuildTimestamp(value) {
  if (!value) {
    return 'Unavailable (local development)';
  }
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    return value;
  }
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }
  return `${new Intl.DateTimeFormat('en', {
    dateStyle: 'medium',
    timeStyle: 'medium',
    timeZone: 'UTC',
  }).format(parsed)} UTC`;
}

function getCommitUrl(repositoryUrl, commit) {
  if (!repositoryUrl || !commit) {
    return null;
  }
  try {
    const url = new URL(repositoryUrl);
    if (!['http:', 'https:'].includes(url.protocol)) {
      return null;
    }
    return `${url.toString().replace(/\/$/, '')}/commit/${encodeURIComponent(commit)}`;
  } catch {
    return null;
  }
}

function appendBuildMetadataRow(container, label, valueNode) {
  const term = document.createElement('dt');
  term.textContent = label;
  const description = document.createElement('dd');
  description.append(valueNode);
  container.append(term, description);
}

function renderBuildData() {
  if (!elements.buildData) {
    return;
  }
  elements.buildData.replaceChildren();
  appendBuildMetadataRow(
    elements.buildData,
    'ETF data timestamp',
    document.createTextNode(formatBuildTimestamp(state.buildInfo?.data?.timestamp))
  );
  const positions = state.portfolio
    .map((position) => state.catalogMaps?.byIsin.get(position.isin))
    .filter(Boolean);
  if (!positions.length) {
    const status = document.createElement('p');
    status.className = 'build-metadata-status';
    status.textContent = 'No ETFs selected.';
    elements.buildData.append(status);
    return;
  }
  for (const entry of positions) {
    appendBuildMetadataRow(
      elements.buildData,
      `${entry.ticker} snapshot`,
      document.createTextNode(entry.snapshotPath || 'Unavailable')
    );
  }
}

function renderBuildInfo() {
  if (!elements.buildMetadata) {
    return;
  }

  elements.buildMetadata.replaceChildren();
  renderBuildData();
  elements.buildDetailsExtra.replaceChildren();
  elements.buildDetailsExtra.hidden = true;
  renderBuildWarnings();

  if (!state.buildInfo) {
    const status = document.createElement('p');
    status.className = 'build-metadata-status';
    status.textContent = 'Build metadata is unavailable in local development or could not be loaded.';
    elements.buildMetadata.append(status);
    return;
  }

  const source = state.buildInfo.source || {};
  const sourceValue = document.createElement('span');
  const commitUrl = getCommitUrl(state.buildInfo.repositoryUrl, source.commit);
  if (commitUrl) {
    const commitLink = document.createElement('a');
    commitLink.href = commitUrl;
    commitLink.target = '_blank';
    commitLink.rel = 'noreferrer';
    commitLink.textContent = source.commit;
    sourceValue.append(commitLink);
  } else {
    sourceValue.textContent = source.commit || 'Unavailable (local development)';
  }

  appendBuildMetadataRow(elements.buildMetadata, 'Source commit', sourceValue);
  appendBuildMetadataRow(
    elements.buildMetadata,
    'Commit timestamp',
    document.createTextNode(formatBuildTimestamp(source.commitTimestamp))
  );
  appendBuildMetadataRow(
    elements.buildMetadata,
    'Publish timestamp',
    document.createTextNode(formatBuildTimestamp(state.buildInfo.publishedAt))
  );
  const details = state.buildInfo.details;
  if (details && typeof details === 'object' && !Array.isArray(details) && Object.keys(details).length > 0) {
    const heading = document.createElement('h3');
    heading.textContent = 'Additional details';
    const detailsList = document.createElement('dl');
    detailsList.className = 'build-metadata';
    for (const [key, value] of Object.entries(details)) {
      const displayValue = typeof value === 'string' ? value : JSON.stringify(value);
      appendBuildMetadataRow(detailsList, key, document.createTextNode(displayValue));
    }
    elements.buildDetailsExtra.append(heading, detailsList);
    elements.buildDetailsExtra.hidden = false;
  }
}

function openBuildDialog() {
  state.buildDialogReturnFocus = document.activeElement;
  if (typeof elements.buildDialog.showModal === 'function') {
    elements.buildDialog.showModal();
  } else {
    elements.buildDialog.setAttribute('open', '');
  }
}

function closeBuildDialog() {
  if (typeof elements.buildDialog.close === 'function') {
    elements.buildDialog.close();
  } else {
    elements.buildDialog.removeAttribute('open');
  }
}

function getHoldingName(holding) {
  return holding?.security?.canonical_name || holding?.security?.name || holding?.security?.ticker || 'Unknown holding';
}

function getHoldingKey(holding) {
  return holding?.security?.company_id || holding?.security?.isin || holding?.security?.ticker || getHoldingName(holding);
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
  return positions.reduce((sum, position) => sum + getPositionWeightBase(position), 0);
}

function getPositionWeightBase(position) {
  const valueChf = Number(position.valueChf);
  return Number.isFinite(valueChf) && valueChf > 0 ? valueChf : Math.max(Number(position.shares) || 0, 0);
}

function getPositionWeight(position, totalShareUnits) {
  if (!totalShareUnits) {
    return 0;
  }
  return (getPositionWeightBase(position) / totalShareUnits) * 100;
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

    const unmatchedCount = (holdings || []).filter((holding) =>
      INCOMPLETE_MATCH_STATUSES.has(holding?.provenance?.match?.status)
    ).length;
    if (unmatchedCount) {
      warnings.push(`${position.entry.ticker}: ${unmatchedCount} holdings are unmatched or partially matched`);
    }
  }

  const ranked = [...exposure.values()]
    .sort((a, b) => b.weight - a.weight || a.key.localeCompare(b.key))
    .map((company) => {
      const contributors = [...company.contributors.values()]
        .map((contributor) => ({
          ...contributor,
          shareOfCompany: company.weight ? (contributor.weight / company.weight) * 100 : 0,
        }))
        .sort((a, b) => b.weight - a.weight || a.ticker.localeCompare(b.ticker));

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

function getCurrentSelectionWarnings(positions = getSelectedPositions()) {
  const { warnings } = aggregateCompanyExposure(positions);
  const snapshotWarnings = [];

  for (const position of positions) {
    const snapshot = position.snapshot;
    if (!snapshot) {
      snapshotWarnings.push(`${position.entry.ticker}: snapshot unavailable`);
      continue;
    }
    if (!snapshot.holdings?.length) {
      snapshotWarnings.push(`${position.entry.ticker}: snapshot has no holdings`);
    }
  }

  return [...snapshotWarnings, ...warnings];
}

function renderWarningItems(container, items, emptyText) {
  if (!items.length) {
    container.innerHTML = `<div class="empty-state">${emptyText}</div>`;
    return;
  }

  container.innerHTML = items.map((item) => `
    <article class="warning-item">
      <div class="left">${item}</div>
    </article>
  `).join('');
}

function renderBuildWarnings() {
  if (!elements.buildWarningList) {
    return;
  }
  const items = state.catalogMaps ? getCurrentSelectionWarnings() : [];
  renderWarningItems(elements.buildWarningList, items, 'No warnings detected in the current selection.');
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

function buildCompactExploreRow(positions, company, rank) {
  const contributionByTicker = new Map(
    company.contributors.map((contributor) => [contributor.ticker, contributor])
  );
  const etfCells = positions.map((position) => {
    const contributor = contributionByTicker.get(position.entry.ticker);
    return `<td class="compact-explore-number">${contributor ? formatPercent(contributor.shareOfCompany) : '—'}</td>`;
  }).join('');

  return `
    <tr>
      <th scope="row" class="compact-explore-holding" title="${company.name}">
        <span class="compact-explore-holding-content">
          <span class="compact-explore-rank" aria-label="Rank ${rank}">${rank}</span>
          <span class="compact-explore-holding-name">${company.name}</span>
        </span>
      </th>
      <td class="compact-explore-number compact-explore-total">${formatPercent(company.displayWeight)}</td>
      ${etfCells}
    </tr>
  `;
}

function buildCompactExploreTable(positions) {
  const etfHeaders = positions.map((position) => `
    <th scope="col" class="compact-explore-etf-column" title="${position.entry.name}">
      ${position.entry.ticker}
    </th>
  `).join('');

  return `
    <div class="compact-explore-table-wrap">
      <table class="compact-explore-table">
        <thead>
          <tr>
            <th scope="col" class="compact-explore-holding">Holding</th>
            <th scope="col" class="compact-explore-number compact-explore-total">Portfolio</th>
            ${etfHeaders}
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
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

  const positions = getSelectedPositions();
  const sentinel = elements.companyList.querySelector('.company-scroll-sentinel');

  if (state.compactExplorePreview) {
    const template = document.createElement('template');
    template.innerHTML = ranked
      .slice(start, end)
      .map((company, index) => buildCompactExploreRow(positions, company, start + index + 1))
      .join('');
    elements.companyList.querySelector('.compact-explore-table tbody').appendChild(template.content);
  } else {
    const fragment = document.createRange().createContextualFragment(
      ranked
        .slice(start, end)
        .map((company, index) => buildCompanyRow(company, start + index))
        .join('')
    );
    if (sentinel) {
      elements.companyList.insertBefore(fragment, sentinel);
    } else {
      elements.companyList.appendChild(fragment);
    }
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

function applyChartFrameSizing() {
  const width = window.innerWidth;
  for (const frame of document.querySelectorAll('.chart-frame')) {
    if (width <= 480) {
      const frameWidth = frame.getBoundingClientRect().width;
      const height = Math.max(Math.round(frameWidth), 1);
      frame.style.setProperty('height', `${height}px`, 'important');
      frame.style.setProperty('min-height', `${height}px`, 'important');
      continue;
    }

    const height = width <= 760 ? CHART_FRAME_HEIGHT_MOBILE_TABLET : CHART_FRAME_HEIGHT_DESKTOP;
    frame.style.setProperty('height', height, 'important');
    frame.style.setProperty('min-height', height, 'important');
  }
}

function updateSummary() {
  const positions = getSelectedPositions();
  const shareCountTotal = positions.reduce((sum, position) => sum + Math.max(Number(position.shares) || 0, 0), 0);
  const importedValues = positions
    .map((position) => Number(position.valueChf))
    .filter((value) => Number.isFinite(value) && value >= 0);
  const totalValueChf = importedValues.length
    ? formatChfValue(importedValues.reduce((sum, value) => sum + value, 0))
    : 'Unavailable';
  const uniqueEtfs = positions.length;
  const totalHoldings = positions.reduce((sum, position) => sum + (position.snapshot?.holdings?.length || 0), 0);
  const overlapCount = aggregateCompanyExposure(positions).ranked.filter((item) => item.etfs.size > 1).length;

  const cards = [
    { label: 'Positions', value: formatCount(uniqueEtfs) },
    { label: 'Share units', value: formatCount(shareCountTotal) },
    { label: 'Total value', value: totalValueChf },
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
        </article>
      `;
    })
    .join('');
}

function renderPositions() {
  const positions = getSelectedPositions();
  if (!positions.length) {
      elements.positionsBody.innerHTML = '<tr><td colspan="6"><div class="empty-state">No positions yet. Search the catalog and add an ETF.</div></td></tr>';
    elements.portfolioHint.textContent = 'The portfolio is empty.';
    return;
  }

  const totalShareUnits = getTotalShareUnits(positions);
  elements.portfolioHint.textContent = positions.some((position) => Number.isFinite(position.valueChf))
    ? 'Weights use imported CHF values; positions without a value use their share count.'
    : 'Share counts act as the portfolio weighting proxy until ETF unit prices are imported.';

  elements.positionsBody.innerHTML = positions
    .map((position) => {
      const weight = getPositionWeight(position, totalShareUnits);
      return `
        <tr class="position-row">
          <td class="position-identity" data-label="ETF">
            <div class="position-name">
              <strong>${position.entry.ticker}</strong>
              <span>· ${position.entry.name}</span>
            </div>
          </td>
          <td class="position-shares" data-label="Shares">
            <input class="position-input" aria-label="Shares for ${position.entry.ticker}" type="number" min="0" step="1" value="${position.shares}" data-shares-input="${position.isin}" />
          </td>
          <td class="position-price" data-label="Price">${position.price !== undefined ? `${position.currency || 'CHF'} ${Number(position.price).toFixed(2)}` : 'Not imported'}</td>
          <td class="position-value" data-label="Value CHF">${position.valueChf !== undefined ? `CHF ${Number(position.valueChf).toFixed(2)}` : 'Not imported'}</td>
          <td class="position-weight" data-label="Weight" aria-label="Weight ${formatPercent(weight)}">${formatPercent(weight)}</td>
          <td class="position-remove" data-label="Remove"><button type="button" class="remove-button" aria-label="Remove ${position.entry.ticker}" title="Remove ${position.entry.ticker}" data-remove-position="${position.isin}"><i data-lucide="trash-2" aria-hidden="true"></i><span class="remove-button-label">Remove</span></button></td>
        </tr>
      `;
    })
    .join('');
  window.lucide?.createIcons();
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
    legendContainer: elements.sectorLegend,
  });
  renderComparisonChart(chartRefs.region, elements.regionCanvas, 'Regions', regionSeries, regionLabels, {
    legendMode: 'labels',
    legendContainer: elements.regionLegend,
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
      legendContainer: elements.currencyLegend,
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
  elements.compactExploreSearch.hidden = !state.compactExplorePreview;

  if (state.compactExplorePreview) {
    if (!ranked.length) {
      elements.companyList.innerHTML = '<div class="empty-state">Add positions to calculate company exposure.</div>';
      elements.companyHint.textContent = 'No look-through exposure is available yet.';
      return;
    }

    const searchTerm = state.companySearchTerm.trim().toLowerCase();
    elements.companyList.innerHTML = buildCompactExploreTable(positions);

    if (searchTerm) {
      const matches = ranked
        .map((company, index) => ({ company, rank: index + 1 }))
        .filter(({ company }) => company.name.toLowerCase().includes(searchTerm));
      elements.companyHint.textContent = matches.length
        ? `${matches.length} matching compan${matches.length === 1 ? 'y' : 'ies'}.`
        : 'No companies match the current search.';
      elements.companyList.querySelector('.compact-explore-table tbody').innerHTML = matches
        .map(({ company, rank }) => buildCompactExploreRow(positions, company, rank))
        .join('');
      state.companyVisibleCount = matches.length;
      return;
    }

    elements.companyHint.textContent = 'Holdings ranked by total portfolio exposure.';
    appendCompanyBatch();
    if (state.companyVisibleCount < ranked.length) {
      const sentinel = document.createElement('div');
      sentinel.className = 'company-scroll-sentinel';
      sentinel.setAttribute('aria-hidden', 'true');
      elements.companyList.appendChild(sentinel);
      ensureCompanyObserver();
    }
    return;
  }

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
  renderBuildWarnings();
}

function updateCompanySearchClearButton() {
  elements.companySearchClear.hidden = !elements.companySearch.value;
}

function formatImportedMoney(value, currency = 'CHF') {
  if (!Number.isFinite(Number(value))) {
    return 'Invalid';
  }
  return `${currency} ${Number(value).toFixed(2)}`;
}

function renderImportReview() {
  const validRows = state.importReviewRows.filter((row) => row.included && !row.warnings.length && row.matchStatus === 'matched');
  elements.importSummary.textContent = `${state.importReviewRows.length} rows found. ${validRows.length} will replace the existing portfolio.`;
  elements.importTbody.innerHTML = state.importReviewRows
    .map((row, index) => {
      const warning = row.warnings.length ? ` ${row.warnings.join('; ')}` : row.matchStatus === 'unmatched' ? ' ISIN is not in the catalog.' : '';
      const label = row.entry ? `${row.entry.ticker} · ${row.entry.name}` : row.isin;
      return `
        <tr class="import-row ${warning ? 'import-row-warning' : ''}">
          <td><input type="checkbox" aria-label="Include ${label}" data-import-include="${index}" ${row.included ? 'checked' : ''} ${row.matchStatus !== 'matched' ? 'disabled' : ''} /></td>
          <td><strong>${label}</strong><span class="import-row-meta">${row.isin} · Page ${row.pageNumber}${warning ? ` · ${warning}` : ''}</span></td>
          <td><input class="import-input" type="number" min="0" step="1" value="${row.shares ?? ''}" data-import-shares="${index}" /></td>
          <td><input class="import-input" type="number" min="0" step="0.0001" value="${row.price ?? ''}" data-import-price="${index}" /></td>
          <td><select class="import-currency" data-import-currency="${index}"><option value="CHF" ${row.currency === 'CHF' ? 'selected' : ''}>CHF</option><option value="EUR" ${row.currency === 'EUR' ? 'selected' : ''}>EUR</option></select></td>
          <td data-import-value="${index}">${formatImportedMoney(row.value, row.currency)}</td>
          <td data-import-value-chf="${index}">${formatImportedMoney(row.valueChf)}</td>
        </tr>
      `;
    })
    .join('');
  elements.importConfirm.disabled = !validRows.length;
}

function updateImportRow(index, field, value) {
  const row = state.importReviewRows[index];
  if (!row) return;
  if (field === 'currency') row.currency = value;
  else row[field] = Number(value);
  const calculated = calculateImportedPosition(Number(row.shares), Number(row.price), row.currency);
  row.value = calculated.value;
  row.valueChf = calculated.valueChf;
  row.warnings = [];
  if (!Number.isFinite(row.shares) || row.shares < 0) row.warnings.push('Shares are missing or invalid');
  if (!Number.isFinite(row.price) || row.price < 0) row.warnings.push('Price is missing or invalid');
  refreshImportReviewTotals();
}

function refreshImportReviewTotals() {
  const validRows = state.importReviewRows.filter((row) => row.included && !row.warnings.length && row.matchStatus === 'matched');
  elements.importSummary.textContent = `${state.importReviewRows.length} rows found. ${validRows.length} will replace the existing portfolio.`;
  for (const [index, row] of state.importReviewRows.entries()) {
    const value = elements.importTbody.querySelector(`[data-import-value="${index}"]`);
    const valueChf = elements.importTbody.querySelector(`[data-import-value-chf="${index}"]`);
    if (value) value.textContent = formatImportedMoney(row.value, row.currency);
    if (valueChf) valueChf.textContent = formatImportedMoney(row.valueChf);
  }
  elements.importConfirm.disabled = !validRows.length;
}

function showImportDialog(rows) {
  state.importReviewRows = rows;
  renderImportReview();
  if (typeof elements.importDialog.showModal === 'function') elements.importDialog.showModal();
  else elements.importDialog.setAttribute('open', '');
}

function closeImportDialog() {
  if (typeof elements.importDialog.close === 'function') elements.importDialog.close();
  else elements.importDialog.removeAttribute('open');
  state.importReviewRows = [];
}

function downloadExtractedPdfText() {
  const pages = window.__etfLensPdfImportPages || [];
  const text = pages.map((page) => `--- Page ${page.pageNumber} ---\n${page.text}`).join('\n\n');
  const url = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'etf-lens-pdfjs-text.txt';
  link.click();
  URL.revokeObjectURL(url);
}

async function importPortfolioFile(file) {
  if (!file) return;
  if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    elements.importStatus.textContent = 'Select a PDF holdings report.';
    return;
  }
  elements.importStatus.textContent = `Reading ${file.name} locally...`;
  window.__etfLensPdfImportPages = null;
  updateImportDebugVisibility();
  try {
    const pages = await extractPdfPages(file);
    window.__etfLensPdfImportPages = pages;
    updateImportDebugVisibility();
    const rows = matchImportedRows(parseSaxoPages(pages), state.catalogMaps);
    if (!rows.length) throw new Error('No ETF holdings were found in the supported Saxo sections.');
    showImportDialog(rows);
    elements.importStatus.textContent = 'Review the proposed positions before replacing the portfolio.';
  } catch (error) {
    elements.importStatus.textContent = error.message;
    updateImportDebugVisibility();
  }
}

function confirmImport() {
  const positions = state.importReviewRows
    .filter((row) => row.included && row.matchStatus === 'matched' && !row.warnings.length && row.entry)
    .map((row) => ({
      isin: row.isin,
      shares: row.shares,
      price: row.price,
      currency: row.currency,
      value: row.value,
      valueChf: row.valueChf,
    }));
  if (!positions.length) {
    elements.importStatus.textContent = 'No valid catalog positions are selected for import.';
    return;
  }
  state.portfolio = positions;
  savePortfolioState();
  closeImportDialog();
  elements.importStatus.textContent = `Imported ${positions.length} ETF position${positions.length === 1 ? '' : 's'} and replaced the portfolio.`;
  renderAll();
}

function renderAll() {
  renderCatalog();
  renderPositions();
  renderBuildData();
  renderComparisonToolbar(getSelectedPositions());
  renderComparisonCharts();
  if (state.activeTab === 'comparison') {
    applyChartFrameSizing();
  }
  renderRollups();
  renderCompanyList();
  renderWarnings();
  updateSummary();
  renderShareFeedback();
}

function setTab(tabName) {
  state.activeTab = getNavigationDestination(tabName)?.key || defaultState.activeTab;
  saveActiveTab();
  for (const button of elements.tabButtons) {
    const isActive = button.dataset.tab === state.activeTab;
    button.classList.toggle('active', isActive);
    if (isActive) {
      button.setAttribute('aria-current', 'page');
    } else {
      button.removeAttribute('aria-current');
    }
  }
  for (const panel of elements.tabPanels) {
    panel.classList.toggle('active', panel.dataset.panel === state.activeTab);
  }
  positionColorModeControl();
  if (state.activeTab === 'comparison') {
    applyChartFrameSizing();
    renderComparisonCharts();
  }
  if (state.activeTab === 'aggregated') {
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
  elements.navigationItems = document.getElementById('primary-navigation-items');
  renderNavigation();
  window.lucide?.createIcons();
  elements.tabButtons = [...document.querySelectorAll('.tab-button')];
  elements.tabPanels = [...document.querySelectorAll('.tab-panel')];
  elements.catalogSearch = document.getElementById('catalog-search');
  elements.catalogList = document.getElementById('catalog-list');
  elements.positionsBody = document.getElementById('positions-tbody');
  elements.portfolioHint = document.getElementById('portfolio-hint');
  elements.shareButton = document.getElementById('share-portfolio-button');
  elements.shareStatus = document.getElementById('share-portfolio-status');
  elements.shareFallbackUrl = document.getElementById('share-portfolio-url');
  elements.comparisonToolbar = document.getElementById('comparison-toolbar');
  elements.sectorCanvas = document.getElementById('sector-chart');
  elements.sectorLegend = document.getElementById('sector-legend');
  elements.regionCanvas = document.getElementById('region-chart');
  elements.regionLegend = document.getElementById('region-legend');
  elements.currencyCanvas = document.getElementById('currency-chart');
  elements.currencyLegend = document.getElementById('currency-legend');
  elements.rollupGrid = document.getElementById('rollup-grid');
  elements.companyList = document.getElementById('company-list');
  elements.companyHint = document.getElementById('company-hint');
  elements.aboutBuildButton = document.getElementById('about-build-button');
  elements.buildDialog = document.getElementById('build-dialog');
  elements.buildDialogClose = document.getElementById('build-dialog-close');
  elements.buildMetadata = document.getElementById('build-metadata');
  elements.buildData = document.getElementById('build-data');
  elements.buildDetailsExtra = document.getElementById('build-details-extra');
  elements.buildWarningList = document.getElementById('build-warning-list');
  elements.compactExplorePreview = document.getElementById('compact-explore-preview');
  elements.portfolioImportDebugEnabled = document.getElementById('portfolio-import-debug-enabled');
  elements.importDialog = document.getElementById('portfolio-import-dialog');
  elements.importDialogClose = document.getElementById('portfolio-import-close');
  elements.importDialogCancel = document.getElementById('portfolio-import-cancel');
  elements.importConfirm = document.getElementById('portfolio-import-confirm');
  elements.importTbody = document.getElementById('portfolio-import-tbody');
  elements.importSummary = document.getElementById('portfolio-import-summary');
  elements.importStatus = document.getElementById('portfolio-import-status');
  elements.importDebug = document.getElementById('portfolio-import-debug');
  elements.importFile = document.getElementById('portfolio-import-file');
  elements.importControl = document.querySelector('.portfolio-import-control');
  elements.colorModeButton = document.getElementById('color-mode-button');
  elements.colorModeMenu = document.getElementById('color-mode-menu');
  elements.colorModeUtility = document.querySelector('.app-utility-bar');

  state.colorMode = loadColorMode();
  state.portfolioImportDebug = loadPortfolioImportDebug();
  applyColorMode();
  renderColorModeControl();
  elements.portfolioImportDebugEnabled.checked = state.portfolioImportDebug;
  renderBuildInfo();
  elements.aboutBuildButton.addEventListener('click', openBuildDialog);
  elements.buildDialogClose.addEventListener('click', closeBuildDialog);
  elements.buildDialog.addEventListener('close', () => {
    state.buildDialogReturnFocus?.focus();
    state.buildDialogReturnFocus = null;
  });
  elements.buildDialog.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeBuildDialog();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && elements.buildDialog.open) {
      event.preventDefault();
      closeBuildDialog();
    }
  });
  void loadBuildInfo().then((buildInfo) => {
    state.buildInfo = buildInfo;
    renderBuildInfo();
  });

  applyChartFrameSizing();
  positionColorModeControl();
  window.addEventListener('resize', applyChartFrameSizing);
  window.addEventListener('resize', positionColorModeControl);
  setupColorModeMediaQuery();

  state.catalog = await loadPublishedCatalog();
  state.catalogMaps = buildCatalogMaps(state.catalog);
  renderBuildData();
  const sharedPortfolio = readPortfolioShareFromUrl();
  if (sharedPortfolio.status === 'valid') {
    state.portfolio = sharedPortfolio.portfolio;
    state.activeTab = 'portfolio';
    state.shareFeedback = 'Shared portfolio loaded using the latest published ETF data.';
    savePortfolioState();
  } else {
    state.portfolio = loadPortfolioState();
    state.activeTab = loadActiveTab();
    if (sharedPortfolio.status === 'invalid') {
      state.shareFeedback = 'This share link could not be loaded. Your local portfolio was kept.';
    }
  }
  positionColorModeControl();
  state.compactExplorePreview = loadCompactExplorePreview();
  elements.compactExplorePreview.checked = state.compactExplorePreview;

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

  elements.companySearch = document.getElementById('company-search');
  elements.companySearchClear = document.getElementById('company-search-clear');
  elements.compactExploreSearch = document.getElementById('compact-explore-search');
  elements.companySearch.addEventListener('input', (event) => {
    state.companySearchTerm = event.target.value;
    updateCompanySearchClearButton();
    if (state.activeTab === 'aggregated' && state.compactExplorePreview) {
      renderCompanyList();
    }
  });
  elements.companySearchClear.addEventListener('click', (event) => {
    event.preventDefault();
    elements.companySearch.value = '';
    state.companySearchTerm = '';
    updateCompanySearchClearButton();
    if (state.activeTab === 'aggregated' && state.compactExplorePreview) {
      renderCompanyList();
    }
    elements.companySearch.focus();
  });
  updateCompanySearchClearButton();

  elements.importFile.addEventListener('change', (event) => {
    void importPortfolioFile(event.target.files?.[0]);
    event.target.value = '';
  });
  elements.portfolioImportDebugEnabled.addEventListener('change', (event) => {
    state.portfolioImportDebug = event.target.checked;
    savePortfolioImportDebug();
    updateImportDebugVisibility();
  });
  elements.importDebug.addEventListener('click', downloadExtractedPdfText);
  elements.importControl.addEventListener('dragover', (event) => {
    event.preventDefault();
    elements.importControl.classList.add('is-dragging');
  });
  elements.importControl.addEventListener('dragleave', () => elements.importControl.classList.remove('is-dragging'));
  elements.importControl.addEventListener('drop', (event) => {
    event.preventDefault();
    elements.importControl.classList.remove('is-dragging');
    void importPortfolioFile(event.dataTransfer.files?.[0]);
  });
  elements.importDialogClose.addEventListener('click', closeImportDialog);
  elements.importDialogCancel.addEventListener('click', closeImportDialog);
  elements.importConfirm.addEventListener('click', confirmImport);
  elements.importDialog.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeImportDialog();
  });
  elements.importTbody.addEventListener('input', (event) => {
    const input = event.target.closest('[data-import-shares], [data-import-price]');
    if (!input) return;
    const field = input.dataset.importShares !== undefined ? 'shares' : 'price';
    updateImportRow(Number(input.dataset.importShares ?? input.dataset.importPrice), field, input.value);
  });
  elements.importTbody.addEventListener('change', (event) => {
    const include = event.target.closest('[data-import-include]');
    if (include) {
      state.importReviewRows[Number(include.dataset.importInclude)].included = include.checked;
      renderImportReview();
      return;
    }
    const currency = event.target.closest('[data-import-currency]');
    if (currency) updateImportRow(Number(currency.dataset.importCurrency), 'currency', currency.value);
  });

  document.addEventListener('click', (event) => {
    const colorModeOption = event.target.closest('[data-color-mode-option]');
    if (colorModeOption) {
      setColorMode(colorModeOption.dataset.colorModeOption);
      toggleColorModeMenu(false);
      return;
    }

    if (event.target.closest('[data-color-mode-control]')) {
      if (event.target.closest('#color-mode-button')) {
        toggleColorModeMenu();
      }
      return;
    }
    toggleColorModeMenu(false);

    const addButton = event.target.closest('[data-add-etf]');
    if (addButton) {
      addPosition(addButton.dataset.addEtf);
      return;
    }

    const shareButton = event.target.closest('[data-share-portfolio]');
    if (shareButton) {
      void sharePortfolio();
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
      return;
    }

    const compactExplorePreview = event.target.closest('[data-compact-explore-preview]');
    if (compactExplorePreview) {
      state.compactExplorePreview = compactExplorePreview.checked;
      saveCompactExplorePreview();
      if (state.activeTab === 'aggregated') {
        renderCompanyList();
      }
    }
  });

  renderAll();
  setTab(state.activeTab);
}

window.addEventListener('DOMContentLoaded', () => {
  bootstrap().catch((error) => {
    document.body.innerHTML = `<pre style="white-space: pre-wrap; padding: 24px; color: #fff;">Failed to start ETF Portfolio Lens: ${error.message}</pre>`;
    console.error(error);
  });
});

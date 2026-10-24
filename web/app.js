import { buildCatalogMaps, loadBuildInfo, loadLivePrices, loadPublishedCatalog, loadSnapshot } from './data.js?v=20261017-1';
import { destroyComparisonCharts, renderComparisonChart } from './charts.js?v=20261015-1';
import { translateTaxonomyLabel } from './taxonomy.js';
import {
  formatBuildTimestamp as formatLocaleTimestamp,
  formatCount as formatLocaleCount,
  formatCurrencyValue as formatLocaleCurrency,
  formatPercent as formatLocalePercent,
  formatPercentNumber as formatLocalePercentNumber,
} from './formatting.js?v=20261019-2';
import { calculateImportedPosition, extractPdfPages, matchImportedRows, parseSaxoPages } from './portfolio-import.js?v=20260910-2';
import { getEffectiveValuation, hasCompleteImportedValuations } from './valuation.js?v=20261016-1';
import {
  buildPairwiseHoldingsBreakdown,
  buildPairwiseMatrix,
  getPairwiseOverlap,
  reconcilePairwiseSelection,
  buildPairwiseOverlapIndex,
  findNearIdenticalPairs,
} from './pairwise-overlap.js';
import { calculateDiversificationScore } from './diversification.js';
import {
  DEFAULT_TOP_HOLDINGS_MAXIMUM,
  getTopHoldingsDisplayLimit,
  loadTopHoldingsMaximum,
  saveTopHoldingsMaximum,
  validateTopHoldingsMaximum,
} from './explore-settings.js';
import {
  calculateRedundancyScore,
  classifyRedundancyScore,
  DEFAULT_REDUNDANCY_THRESHOLDS,
  DEFAULT_NEAR_IDENTICAL_THRESHOLD,
  DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES,
  loadPairwiseHoldingsMaxCompanies,
  loadNearIdenticalThreshold,
  loadRedundancyThresholds,
  savePairwiseHoldingsMaxCompanies,
  saveNearIdenticalThreshold,
  saveRedundancyThresholds,
  validatePairwiseHoldingsMaxCompanies,
  validateNearIdenticalThreshold,
  validateRedundancyThresholds,
} from './redundancy.js?v=20261019-1';
import { decodePortfolioShare, encodePortfolioShare, encodePrivatePortfolioShare } from './share.js';
import { initializeLocalization, selectLocale } from './localization.js';
import { buildReportAnalytics, buildReportSnapshot } from './report-data.js';
import { openReportDialog } from './export-view.js';
import { generateReportPdf } from './pdf-export.js';

const STORAGE_KEY = 'etf-lens.portfolio.v1';
const ACTIVE_TAB_STORAGE_KEY = 'etf-lens.active-tab.v1';
const COMPACT_EXPLORE_STORAGE_KEY = 'etf-lens.compact-explore-preview.v1';
const PORTFOLIO_IMPORT_DEBUG_STORAGE_KEY = 'etf-lens.portfolio-import-debug.v1';
const COLOR_MODE_STORAGE_KEY = 'etf-lens.color-mode.v1';
const SHARE_FRAGMENT_KEY = 'portfolio';
const PORTFOLIO_MODES = ['full', 'percentage'];
const COLOR_MODES = ['bright', 'automatic', 'dark'];
const DARK_MODE_MEDIA_QUERY = '(prefers-color-scheme: dark)';
const defaultState = {
  activeTab: 'home',
  searchTerm: '',
  companySearchTerm: '',
  portfolio: [],
  portfolioMode: 'full',
  importReviewRows: [],
  compactExplorePreview: false,
  redundancyThresholds: { ...DEFAULT_REDUNDANCY_THRESHOLDS },
  nearIdenticalThreshold: DEFAULT_NEAR_IDENTICAL_THRESHOLD,
  pairwiseHoldingsMaxCompanies: DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES,
  topHoldingsMaximum: DEFAULT_TOP_HOLDINGS_MAXIMUM,
  pairwiseSelection: [],
  colorMode: 'automatic',
  effectiveColorMode: 'bright',
  shareFeedback: '',
  shareFallbackUrl: '',
  importValuationMode: 'latest',
  valuationMode: 'latest',
};

const chartRefs = {
  sector: { current: null },
  region: { current: null },
  currency: { current: null },
};

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
  pairwiseOverlapIndex: new Map(),
  buildInfo: null,
  livePrices: null,
  buildDialogReturnFocus: null,
  dataDialogReturnFocus: null,
  exportDialogReturnFocus: null,
  companyRanked: [],
  companyVisibleCount: 0,
  companyObserver: null,
  companyTableResizeObserver: null,
  colorModeMediaQuery: null,
};

const elements = {};
let deferredInstallPrompt = null;

const NAVIGATION_DESTINATIONS = [
  { key: 'home', labelKey: 'nav.home', icon: 'house' },
  { key: 'portfolio', labelKey: 'nav.portfolio', icon: 'briefcase-business' },
  { key: 'comparison', labelKey: 'nav.compare', icon: 'scale' },
  { key: 'aggregated', labelKey: 'nav.explore', icon: 'layers-3' },
];

function t(key, options) {
  return window.i18next.t(key, options);
}

function hideScoreBandTouchTooltips(except = null) {
  document.querySelectorAll('[data-score-band-touch-tooltip]').forEach((tooltip) => {
    if (tooltip !== except) tooltip.hidden = true;
  });
}

function showScoreBandTouchTooltip(meter, segments, event) {
  const track = meter.querySelector('.redundancy-meter-track');
  const scoreBox = meter.closest('.redundancy-score-box');
  const tooltip = scoreBox.querySelector('[data-score-band-touch-tooltip]');
  const trackRect = track.getBoundingClientRect();
  if (
    event.clientX < trackRect.left
    || event.clientX > trackRect.right
    || event.clientY < trackRect.top - 12
    || event.clientY > trackRect.bottom + 12
  ) {
    return;
  }

  const segment = segments.find((candidate) => {
    const rect = candidate.getBoundingClientRect();
    return rect.width > 0 && event.clientX >= rect.left && event.clientX <= rect.right;
  });
  const translationKey = segment?.getAttribute('data-i18n-attr-title');
  if (!translationKey) return;

  hideScoreBandTouchTooltips(tooltip);
  tooltip.textContent = t(translationKey);
  tooltip.hidden = false;

  const tooltipRect = tooltip.getBoundingClientRect();
  const scoreBoxRect = scoreBox.getBoundingClientRect();
  const horizontalInset = 8;
  const meterRect = meter.getBoundingClientRect();
  const minCenter = meterRect.left + tooltipRect.width / 2 + horizontalInset;
  const maxCenter = Math.max(minCenter, meterRect.right - tooltipRect.width / 2 - horizontalInset);
  const targetCenter = Math.min(Math.max(event.clientX, minCenter), maxCenter);

  tooltip.style.left = `${targetCenter - scoreBoxRect.left}px`;
  tooltip.style.top = `${Math.max(event.clientY - scoreBoxRect.top + 10, meterRect.bottom - scoreBoxRect.top + 6)}px`;
}

function bindScoreBandTouchTooltip(meter, segments) {
  const track = meter.querySelector('.redundancy-meter-track');
  let touchStart = null;

  meter.addEventListener('pointerdown', (event) => {
    if (event.pointerType !== 'touch') return;
    const rect = track.getBoundingClientRect();
    if (
      event.clientX < rect.left
      || event.clientX > rect.right
      || event.clientY < rect.top - 12
      || event.clientY > rect.bottom + 12
    ) {
      touchStart = null;
      return;
    }
    touchStart = { pointerId: event.pointerId, x: event.clientX, y: event.clientY };
  }, { passive: true });

  meter.addEventListener('pointerup', (event) => {
    if (!touchStart || event.pointerId !== touchStart.pointerId) return;
    const start = touchStart;
    touchStart = null;
    if (Math.hypot(event.clientX - start.x, event.clientY - start.y) > 10) return;
    showScoreBandTouchTooltip(meter, segments, event);
  });

  meter.addEventListener('pointercancel', () => {
    touchStart = null;
  });
}

function getNavigationDestination(key) {
  return NAVIGATION_DESTINATIONS.find((destination) => destination.key === key) || null;
}

function applyStaticTranslations() {
  for (const element of document.querySelectorAll('[data-i18n]')) {
    element.textContent = window.i18next.t(element.dataset.i18n);
  }
  for (const element of document.querySelectorAll('*')) {
    for (const attribute of element.getAttributeNames()) {
      if (!attribute.startsWith('data-i18n-attr-')) continue;
      const name = attribute.slice('data-i18n-attr-'.length);
      element.setAttribute(name, window.i18next.t(element.getAttribute(attribute)));
    }
  }
}

function renderLanguageControl() {
  const currentLocale = window.i18next.resolvedLanguage || window.i18next.language;
  const languages = [
    { locale: 'en-CH', code: 'EN', labelKey: 'language.english' },
    { locale: 'de-CH', code: 'DE', labelKey: 'language.german' },
    { locale: 'pl-PL', code: 'PL', labelKey: 'language.polish' },
  ];
  const selectedLanguage = languages.find((language) => language.locale === currentLocale) || languages[0];
  if (!elements.languageButton || !elements.languageMenu) return;

  elements.languageButton.innerHTML = `
    <span class="language-name">${t(selectedLanguage.labelKey)}</span>
    <span class="language-code">${selectedLanguage.code}</span>
  `;
  elements.languageButton.setAttribute(
    'aria-label',
    t('language.current', { language: t(selectedLanguage.labelKey) })
  );
  elements.languageMenu.innerHTML = languages
    .map((language) => `
      <button class="color-mode-option language-option" type="button" role="menuitemradio" aria-checked="${language.locale === currentLocale}" data-locale="${language.locale}" aria-label="${t(language.labelKey)}">
        <span>${t(language.labelKey)}</span>
      </button>
    `)
    .join('');
  window.lucide?.createIcons();
}

function isStandaloneDisplayMode() {
  return window.matchMedia?.('(display-mode: standalone)').matches || window.navigator.standalone === true;
}

function isMobileViewport() {
  return window.matchMedia?.('(max-width: 760px)').matches ?? false;
}

function updateInstallAction() {
  if (!elements.installAppButton) {
    return;
  }
  elements.installAppButton.hidden = !deferredInstallPrompt
    || isStandaloneDisplayMode()
    || !isMobileViewport()
    || state.activeTab !== 'home';
}

function handleBeforeInstallPrompt(event) {
  event.preventDefault();
  deferredInstallPrompt = event;
  updateInstallAction();
}

async function promptToInstall() {
  const installPrompt = deferredInstallPrompt;
  if (!installPrompt) {
    return;
  }
  deferredInstallPrompt = null;
  updateInstallAction();
  try {
    await installPrompt.prompt();
    await installPrompt.userChoice;
  } catch (error) {
    console.warn('ETF Portfolio Lens install prompt failed.', error);
  }
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
    { key: 'bright', labelKey: 'colorMode.bright', icon: 'sun' },
    { key: 'automatic', labelKey: 'colorMode.automatic', icon: 'monitor' },
    { key: 'dark', labelKey: 'colorMode.dark', icon: 'moon' },
  ];
  const selectedMode = modes.find((mode) => mode.key === state.colorMode) || modes[1];
  const selectedLabel = t(selectedMode.labelKey);
  elements.colorModeButton.innerHTML = `
    <i data-lucide="${selectedMode.icon}" aria-hidden="true"></i>
    <span>${selectedLabel}</span>
  `;
  elements.colorModeButton.setAttribute('aria-label', t('colorMode.current', { mode: selectedLabel }));
  elements.colorModeMenu.innerHTML = modes
    .map(
      (mode) => `
        <button class="color-mode-option" type="button" role="menuitemradio" aria-checked="${mode.key === state.colorMode}" data-color-mode-option="${mode.key}">
          <i data-lucide="${mode.icon}" aria-hidden="true"></i>
          <span>${t(mode.labelKey)}</span>
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

function closePairwiseSelectorMenus() {
  document.querySelectorAll('[data-pairwise-selector-button]').forEach((button) => {
    button.setAttribute('aria-expanded', 'false');
  });
  document.querySelectorAll('[data-pairwise-selector-menu]').forEach((menu) => {
    menu.hidden = true;
  });
}

function togglePairwiseSelectorMenu(button) {
  const menu = document.querySelector(`[data-pairwise-selector-menu="${button.dataset.pairwiseSelectorButton}"]`);
  if (!menu) return;
  const shouldOpen = menu.hidden;
  closePairwiseSelectorMenus();
  if (!shouldOpen) return;

  menu.hidden = false;
  button.setAttribute('aria-expanded', 'true');
  menu.querySelector('[aria-checked="true"]')?.focus();
}

function toggleLanguageMenu(forceOpen) {
  const isOpen = !elements.languageMenu.hidden;
  const shouldOpen = forceOpen ?? !isOpen;
  elements.languageMenu.hidden = !shouldOpen;
  elements.languageButton.setAttribute('aria-expanded', String(shouldOpen));
  if (shouldOpen) {
    elements.languageMenu.querySelector('[aria-checked="true"]')?.focus();
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

function loadRedundancyThresholdPreferences() {
  try {
    return loadRedundancyThresholds(localStorage);
  } catch {
    return { ...DEFAULT_REDUNDANCY_THRESHOLDS };
  }
}

function saveRedundancyThresholdPreferences(thresholds) {
  try {
    return saveRedundancyThresholds(thresholds, localStorage);
  } catch {
    return false;
  }
}

function loadNearIdenticalThresholdPreference() {
  try {
    return loadNearIdenticalThreshold(localStorage);
  } catch {
    return DEFAULT_NEAR_IDENTICAL_THRESHOLD;
  }
}

function saveNearIdenticalThresholdPreference(threshold) {
  try {
    return saveNearIdenticalThreshold(threshold, localStorage);
  } catch {
    return false;
  }
}

function loadPairwiseHoldingsMaxCompaniesPreference() {
  try {
    return loadPairwiseHoldingsMaxCompanies(localStorage);
  } catch {
    return DEFAULT_PAIRWISE_HOLDINGS_MAX_COMPANIES;
  }
}

function savePairwiseHoldingsMaxCompaniesPreference(maximum) {
  try {
    return savePairwiseHoldingsMaxCompanies(maximum, localStorage);
  } catch {
    return false;
  }
}

function loadTopHoldingsMaximumPreference() {
  try {
    return loadTopHoldingsMaximum(localStorage);
  } catch {
    return DEFAULT_TOP_HOLDINGS_MAXIMUM;
  }
}

function saveTopHoldingsMaximumPreference(maximum) {
  try {
    return saveTopHoldingsMaximum(maximum, localStorage);
  } catch {
    return false;
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
          <span>${t(destination.labelKey)}</span>
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
      return { mode: 'full', valuationMode: 'latest', portfolio: [] };
    }
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      return { mode: 'full', valuationMode: 'latest', portfolio: normalizePortfolioPositions(parsed) };
    }
    const mode = PORTFOLIO_MODES.includes(parsed?.mode) ? parsed.mode : 'full';
    const valuationMode = parsed?.valuationMode === 'imported' ? 'imported' : 'latest';
    return { mode, valuationMode, portfolio: normalizePortfolioPositions(parsed?.portfolio) };
  } catch {
    return { mode: 'full', valuationMode: 'latest', portfolio: [] };
  }
}

function savePortfolioState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ mode: state.portfolioMode, valuationMode: state.valuationMode, portfolio: state.portfolio }));
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
    if (position.valuationMode === 'imported' || position.valuationMode === 'latest') normalized.valuationMode = position.valuationMode;
    if (position.price != null && Number.isFinite(Number(position.price)) && Number(position.price) >= 0) normalized.price = Number(position.price);
    if (typeof position.currency === 'string' && ['CHF', 'EUR', 'USD'].includes(position.currency.toUpperCase())) normalized.currency = position.currency.toUpperCase();
    if (position.value != null && Number.isFinite(Number(position.value)) && Number(position.value) >= 0) normalized.value = Number(position.value);
    if (position.valueChf != null && Number.isFinite(Number(position.valueChf)) && Number(position.valueChf) >= 0) normalized.valueChf = Number(position.valueChf);
    return [normalized];
  });
}

function readPortfolioShareFromUrl() {
  const params = new URLSearchParams(window.location.hash.replace(/^#/, ''));
  return decodePortfolioShare(params.get(SHARE_FRAGMENT_KEY));
}

function buildPortfolioShareUrl(portfolio, mode = 'full') {
  const encoded = mode === 'percentage'
    ? encodePrivatePortfolioShare(portfolio, getTotalShareUnits, getPositionWeight)
    : encodePortfolioShare(portfolio, state.valuationMode);
  if (!encoded) {
    return null;
  }
  const url = new URL(window.location.href);
  url.hash = `${SHARE_FRAGMENT_KEY}=${encoded}`;
  return url.toString();
}

function renderShareFeedback() {
  if (!elements.shareStatus || !elements.shareFallbackUrl || !elements.shareFallbackLabel) {
    return;
  }
  const hasFallbackUrl = Boolean(state.shareFallbackUrl);
  elements.shareStatus.textContent = state.shareFeedback ? t(state.shareFeedback) : '';
  elements.shareFallbackUrl.value = state.shareFallbackUrl;
  elements.shareFallbackLabel.hidden = !hasFallbackUrl;
  elements.shareFallbackUrl.hidden = !hasFallbackUrl;
}

function clearShareFeedback() {
  state.shareFeedback = '';
  state.shareFallbackUrl = '';
  renderShareFeedback();
}

async function sharePortfolio(mode = 'full') {
  if (state.portfolioMode === 'percentage') {
    mode = 'percentage';
  }
  const url = buildPortfolioShareUrl(getSelectedPositions(), mode);
  if (!url) {
    state.shareFeedback = 'share.addPositionFirst';
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
    state.shareFeedback = mode === 'percentage'
      ? 'share.privateCopied'
      : 'share.copied';
  } catch {
    state.shareFeedback = 'share.copyUnavailable';
  }
  renderShareFeedback();
}

function formatPercent(value) {
  return formatLocalePercent(value, window.i18next.language);
}

function formatPercentNumber(value) {
  return formatLocalePercentNumber(value, window.i18next.language);
}

function formatCount(value) {
  return formatLocaleCount(value, window.i18next.language);
}

function formatCurrencyValue(value, currency = 'CHF') {
  return formatLocaleCurrency(value, currency, window.i18next.language);
}

function formatChfValue(value) {
  return formatCurrencyValue(value, 'CHF');
}

function formatBuildTimestamp(value) {
  if (!value) {
    return t('common.unavailableLocalDev');
  }
  return formatLocaleTimestamp(value, window.i18next.language);
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
  if (!elements.dataDialogMetadata) {
    return;
  }
  elements.dataDialogMetadata.replaceChildren();
  appendBuildMetadataRow(
    elements.dataDialogMetadata,
    t('build.etfDataTimestamp'),
    document.createTextNode(formatBuildTimestamp(state.buildInfo?.data?.timestamp))
  );
  appendBuildMetadataRow(
    elements.dataDialogMetadata,
    t('build.liveData'),
    document.createTextNode(state.livePrices ? `${formatBuildTimestamp(state.livePrices.generated_at)} (${state.livePrices.status})` : t('common.unavailable'))
  );
  const positions = state.portfolio
    .map((position) => state.catalogMaps?.byIsin.get(position.isin))
    .filter(Boolean);
  if (!positions.length) {
    const status = document.createElement('p');
    status.className = 'build-metadata-status';
    status.textContent = t('portfolio.noEtfsSelected');
    elements.dataDialogMetadata.append(status);
    return;
  }
  for (const entry of positions) {
    appendBuildMetadataRow(
      elements.dataDialogMetadata,
      `${entry.ticker} snapshot`,
      document.createTextNode(entry.snapshotPath || t('common.unavailable'))
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
    status.textContent = t('build.metadataUnavailable');
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
    sourceValue.textContent = source.commit || t('common.unavailableLocalDev');
  }

  appendBuildMetadataRow(elements.buildMetadata, t('build.sourceCommit'), sourceValue);
  appendBuildMetadataRow(
    elements.buildMetadata,
    t('build.commitTimestamp'),
    document.createTextNode(formatBuildTimestamp(source.commitTimestamp))
  );
  appendBuildMetadataRow(
    elements.buildMetadata,
    t('build.publishTimestamp'),
    document.createTextNode(formatBuildTimestamp(state.buildInfo.publishedAt))
  );
  const details = state.buildInfo.details;
  if (details && typeof details === 'object' && !Array.isArray(details) && Object.keys(details).length > 0) {
    const heading = document.createElement('h3');
    heading.textContent = t('build.additionalDetails');
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

function openDataDialog() {
  state.dataDialogReturnFocus = document.activeElement;
  if (typeof elements.dataDialog.showModal === 'function') {
    elements.dataDialog.showModal();
  } else {
    elements.dataDialog.setAttribute('open', '');
  }
}

function closeBuildDialog() {
  if (typeof elements.buildDialog.close === 'function') {
    elements.buildDialog.close();
  } else {
    elements.buildDialog.removeAttribute('open');
  }
}

function closeDataDialog() {
  if (typeof elements.dataDialog.close === 'function') {
    elements.dataDialog.close();
  } else {
    elements.dataDialog.removeAttribute('open');
  }
}

function openExportDialog() {
  state.exportDialogReturnFocus = document.activeElement;
  elements.exportGenerateButton.disabled = false;
  openReportDialog({
    dialog: elements.exportDialog,
    scopeControls: elements.exportScope,
    allocationOnlyControl: elements.exportAllocationOnly,
    generationStatus: elements.exportGenerationStatus,
  });
}

async function generateExportReport() {
  elements.exportGenerateButton.disabled = true;
  elements.exportGenerationStatus.hidden = false;
  elements.exportGenerationStatus.textContent = t('export.generating');
  try {
    const scope = elements.exportScope.find((control) => control.checked)?.value || 'portfolio';
    const snapshot = createReportSnapshot(scope);
    const analytics = createReportAnalytics(snapshot);
    await generateReportPdf({
      snapshot,
      analytics,
      allocationOnly: elements.exportAllocationOnly.checked,
      t,
      formatCount,
      formatDecimal: formatPercentNumber,
      formatPercent,
      formatCurrency: formatCurrencyValue,
      translateTaxonomy: (label) => translateTaxonomyLabel(label, t),
      formatTimestamp: (value) => value ? formatBuildTimestamp(value) : t('common.unavailable'),
    });
    elements.exportGenerationStatus.textContent = t('export.pdfReady');
    closeExportDialog();
  } catch (error) {
    console.error('Could not build the PDF report:', error);
    elements.exportGenerationStatus.textContent = t('export.generationFailed');
  } finally {
    elements.exportGenerateButton.disabled = false;
  }
}

function closeExportDialog() {
  if (typeof elements.exportDialog.close === 'function') {
    elements.exportDialog.close();
  } else {
    elements.exportDialog.removeAttribute('open');
    state.exportDialogReturnFocus?.focus();
    state.exportDialogReturnFocus = null;
  }
}

function openScoreInfoDialog(event) {
  const opener = event.currentTarget;
  const panelId = opener.dataset.scoreInfo;
  const panel = elements.scoreInfoPanels.find((candidate) => candidate.dataset.scoreInfoPanel === panelId);
  if (!panel) return;

  state.scoreInfoReturnFocus = opener;
  elements.scoreInfoTitle.textContent = t(opener.dataset.scoreInfoTitle);
  for (const candidate of elements.scoreInfoPanels) {
    candidate.hidden = candidate !== panel;
  }
  if (typeof elements.scoreInfoDialog.showModal === 'function') {
    elements.scoreInfoDialog.showModal();
  } else {
    elements.scoreInfoDialog.setAttribute('open', '');
  }
}

function closeScoreInfoDialog() {
  if (typeof elements.scoreInfoDialog.close === 'function') {
    elements.scoreInfoDialog.close();
  } else {
    elements.scoreInfoDialog.removeAttribute('open');
  }
}

function openPairwiseInfoDialog(event) {
  const opener = event.currentTarget;
  const dialog = opener.dataset.pairwiseInfo === 'heatmap'
    ? elements.pairwiseHeatmapInfoDialog
    : elements.pairwiseHoldingsInfoDialog;
  if (!dialog) return;

  state.pairwiseInfoReturnFocus = opener;
  if (typeof dialog.showModal === 'function') {
    dialog.showModal();
  } else {
    dialog.setAttribute('open', '');
  }
}

function restorePairwiseInfoFocus() {
  state.pairwiseInfoReturnFocus?.focus();
  state.pairwiseInfoReturnFocus = null;
}

function closePairwiseInfoDialog(dialog) {
  if (typeof dialog.close === 'function') {
    dialog.close();
  } else {
    dialog.removeAttribute('open');
  }
  restorePairwiseInfoFocus();
}

function getHoldingName(holding) {
  return holding?.security?.canonical_name || holding?.security?.name || holding?.security?.ticker || t('explore.unknownHolding');
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

function createReportSnapshot(scope = 'portfolio') {
  const positions = getSelectedPositions();
  const totalShareUnits = getTotalShareUnits(positions);
  const portfolioPositions = positions.map((position) => ({
    ...position,
    valuation: getPositionValuation(position),
    weightPct: getPositionWeight(position, totalShareUnits),
  }));

  return buildReportSnapshot({
    scope,
    portfolioPositions,
    catalogEtfs: state.catalog?.etfs || [],
    catalogTimestamp: state.catalog?.generatedAt || null,
    portfolioMode: state.portfolioMode,
    valuationMode: state.valuationMode,
    locale: window.i18next.resolvedLanguage || window.i18next.language,
    buildInfo: state.buildInfo,
    livePrices: state.livePrices,
  });
}

function createReportAnalytics(snapshot) {
  const positions = snapshot.portfolioPositions;
  const companyExposure = aggregateCompanyExposure(positions);
  const { ranked } = companyExposure;
  const rollupMaps = aggregatePortfolioRollups(positions);
  const positionWeights = positions.map((position) => ({
    weight: position.weightPct,
    hasUsableHoldings: Boolean(position.snapshot?.holdings?.length),
  }));
  const redundancy = calculateRedundancyScore(ranked, positionWeights);
  const coveragePositions = positions.map((position) => ({
    weight: position.weightPct,
    coveragePct: (position.snapshot?.holdings || []).reduce((total, holding) => {
      const weight = Number(holding?.exposure?.weight_pct);
      return total + (Number.isFinite(weight) && weight > 0 ? weight : 0);
    }, 0),
  }));
  const diversification = calculateDiversificationScore(
    ranked.map((company) => company.weight),
    coveragePositions,
  );
  const rollups = Object.fromEntries(
    Object.entries(rollupMaps).map(([key, values]) => [key, Object.fromEntries(values)])
  );
  const hasPortfolioReference = positionWeights.some((position) => position.weight > 0);
  const chartData = (metricKey) => {
    const data = metricKey === 'currency_weights'
      ? getCurrencyMetricData(positions)
      : getMetricData(positions, metricKey);
    const rollupKey = metricKey.replace('_weights', '');
    const labels = mergeLabels(data.labels, Object.keys(rollups[rollupKey] || {}));
    const series = data.series.map((entry) => ({
      label: entry.label,
      values: Object.fromEntries(entry.values),
    }));
    if (hasPortfolioReference) {
      series.unshift({
        label: t('chart.portfolioReference'),
        values: Object.fromEntries(labels.map((label) => [label, rollups[rollupKey]?.[label] || 0])),
      });
    }
    return { labels, series };
  };
  const values = positions
    .map((position) => Number(position.valuation?.valueChf))
    .filter((value) => Number.isFinite(value) && value >= 0);
  const summary = {
    positions: positions.length,
    shareUnits: snapshot.portfolioMode === 'percentage'
      ? null
      : positions.reduce((total, position) => total + Math.max(Number(position.shares) || 0, 0), 0),
    totalValueChf: snapshot.portfolioMode === 'percentage' || !values.length
      ? null
      : values.reduce((total, value) => total + value, 0),
    underlyingHoldings: positions.reduce((total, position) => total + (position.snapshot?.holdings?.length || 0), 0),
    sharedCompanies: companyExposure.ranked.filter((company) => company.etfs.size > 1).length,
  };
  const pairwiseHeatmap = buildPairwiseMatrix(
    positions,
    state.pairwiseOverlapIndex,
    state.nearIdenticalThreshold,
  );

  return buildReportAnalytics({
    snapshot,
    rankedCompanies: companyExposure.ranked,
    summary,
    rollups,
    redundancy: {
      ...redundancy,
      level: redundancy.available
        ? classifyRedundancyScore(
          redundancy.score,
          state.redundancyThresholds.lowModerate,
          state.redundancyThresholds.moderateHigh,
        )
        : null,
    },
    diversification,
    charts: {
      sector: chartData('sector_weights'),
      region: chartData('region_weights'),
      currency: chartData('currency_weights'),
    },
    pairwiseHeatmap,
  });
}

function getPositionValuation(position) {
  return getEffectiveValuation(position, state.livePrices, state.valuationMode);
}

function renderValuationModeControl() {
  if (!elements.portfolioValuationControl || !elements.portfolioValuation || !elements.portfolioValuationStatus) {
    return;
  }
  const isPercentagePortfolio = state.portfolioMode === 'percentage';
  const hasImportedValuations = !isPercentagePortfolio && hasCompleteImportedValuations(state.portfolio, state.livePrices);
  const importedOption = elements.portfolioValuation.querySelector('option[value="imported"]');
  if (importedOption) {
    importedOption.hidden = !hasImportedValuations;
    importedOption.disabled = !hasImportedValuations;
  }
  if (!isPercentagePortfolio && !hasImportedValuations && state.valuationMode === 'imported') {
    state.valuationMode = 'latest';
    savePortfolioState();
  }
  elements.portfolioValuationControl.hidden = isPercentagePortfolio;
  elements.portfolioValuation.disabled = isPercentagePortfolio;
  elements.portfolioValuation.value = state.valuationMode;
  elements.portfolioValuationStatus.hidden = isPercentagePortfolio;
  elements.portfolioValuationStatus.querySelector('[data-valuation-status-label]').textContent = state.valuationMode === 'imported' ? t('valuation.imported') : t('valuation.live');
  elements.portfolioValuationStatus.querySelector('.dot').hidden = state.valuationMode !== 'latest';
}

function renderPortfolioModeControl() {
  elements.portfolioModeControl?.querySelectorAll('[data-portfolio-mode]').forEach((input) => {
    input.checked = input.value === state.portfolioMode;
  });
}

function updatePortfolioMode(mode) {
  if (mode === state.portfolioMode) {
    return;
  }

  if (mode === 'percentage') {
    const positions = state.portfolio.map((position) => ({ ...position }));
    const totalShareUnits = getTotalShareUnits(positions);
    state.portfolio = positions.map((position) => ({
      isin: position.isin,
      shares: getPositionWeight(position, totalShareUnits),
    }));
    state.portfolioMode = 'percentage';
  } else {
    state.portfolio = state.portfolio.map((position) => ({ ...position, shares: 0 }));
    state.portfolioMode = 'full';
  }

  clearShareFeedback();
  savePortfolioState();
  renderAll();
}

function getTotalShareUnits(positions) {
  return positions.reduce((sum, position) => sum + getPositionWeightBase(position), 0);
}

function getPositionWeightBase(position) {
  if (state.portfolioMode === 'percentage') {
    return Math.max(Number(position.shares) || 0, 0);
  }
  const valueChf = Number(getPositionValuation(position).valueChf);
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
    legendLabelOverrides: otherGrouped ? new Map([['Other', t('chart.otherGrouped')]]) : new Map(),
  };
}

function getComparisonSelection() {
  return getSelectedPositions();
}

function aggregateCompanyExposure(positions) {
  const hasCapturedWeights = positions.every((position) => Number.isFinite(position.weightPct));
  const totalShareUnits = hasCapturedWeights ? 0 : getTotalShareUnits(positions);
  const exposure = new Map();
  const warnings = [];

  for (const [positionIndex, position] of positions.entries()) {
    const snapshot = position.snapshot;
    if (!snapshot) {
      continue;
    }

    const contributionColor = ETF_SEGMENT_COLORS[positionIndex % ETF_SEGMENT_COLORS.length];

    const positionWeight = hasCapturedWeights
      ? position.weightPct
      : getPositionWeight(position, totalShareUnits);
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
      warnings.push(t('warnings.unmatchedHoldings', {
        ticker: position.entry.ticker,
        count: unmatchedCount,
        countDisplay: formatCount(unmatchedCount),
      }));
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
      snapshotWarnings.push(t('warnings.snapshotUnavailable', { ticker: position.entry.ticker }));
      continue;
    }
    if (!snapshot.holdings?.length) {
      snapshotWarnings.push(t('warnings.snapshotNoHoldings', { ticker: position.entry.ticker }));
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
  if (!elements.dataDialogWarningList) {
    return;
  }
  const items = state.catalogMaps ? getCurrentSelectionWarnings() : [];
  renderWarningItems(elements.dataDialogWarningList, items, t('warnings.noneDetected'));
}

function buildCompanyRow(company, index) {
  const barSegments = company.contributors.map((contributor) => {
    const tooltip = t('explore.contributorTooltip', {
      ticker: contributor.ticker,
      share: formatPercent(contributor.shareOfCompany),
      company: company.name,
      portfolio: formatPercent(contributor.weight),
    });
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
    <div class="company-chip" title="${t('explore.companyChipTooltip', {
      ticker: contributor.ticker,
      share: formatPercent(contributor.shareOfCompany),
      portfolio: formatPercent(contributor.weight),
    })}">
      <span class="chip-swatch" style="background: ${contributor.color};"></span>
      <span class="chip-ticker">${contributor.ticker}</span>
      <strong>${formatPercent(contributor.shareOfCompany)}</strong>
      <span class="chip-meta">${t('explore.portfolioShare', { value: formatPercent(contributor.weight) })}</span>
    </div>
  `).join('');

  return `
    <article class="company-row">
      <div class="company-row-head">
        <div class="company-row-title">
          <div class="company-name">${index + 1}. ${company.name}</div>
          <div class="company-meta">${t('explore.etfContributionCount', {
      count: company.etfs.size,
      countDisplay: formatCount(company.etfs.size),
      value: formatPercent(company.weight),
    })}</div>
        </div>
        <div class="company-total">${formatPercent(company.weight)}</div>
      </div>
      <div class="company-bar-track" style="width: ${Math.max(company.shareOfMax, 0.01)}%;" role="img" aria-label="${t('explore.companyExposureLabel', {
    company: company.name,
    contributors: company.contributors.map((contributor) => `${contributor.ticker} ${formatPercent(contributor.shareOfCompany)}`).join(', '),
  })}">
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
          <span class="compact-explore-rank" aria-label="${t('explore.rank', { rank })}">${rank}</span>
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
  const headerRow = `
    <tr>
      <th scope="col" class="compact-explore-holding">${t('explore.holding')}</th>
      <th scope="col" class="compact-explore-number compact-explore-total">${t('explore.portfolio')}</th>
      ${etfHeaders}
    </tr>
  `;
  const columns = `
    <colgroup>
      <col class="compact-explore-holding-column" />
      <col class="compact-explore-number-column compact-explore-total-column" />
      ${positions.map(() => '<col class="compact-explore-number-column" />').join('')}
    </colgroup>
  `;

  return `
    <div class="compact-explore-table-wrap">
      <div class="compact-explore-sticky-header" aria-hidden="true">
        <div class="compact-explore-sticky-header-clip">
          <table class="compact-explore-table compact-explore-sticky-header-table">
            ${columns}
            <thead>${headerRow}</thead>
          </table>
        </div>
      </div>
      <div class="compact-explore-table-scroll">
        <table class="compact-explore-table compact-explore-table-body">
          ${columns}
          <thead class="compact-explore-table-semantic-header">${headerRow}</thead>
          <tbody></tbody>
        </table>
      </div>
    </div>
  `;
}

function syncCompactExploreHeader(scrollContainer) {
  const tableWrap = scrollContainer.closest('.compact-explore-table-wrap');
  const headerTable = tableWrap?.querySelector('.compact-explore-sticky-header-table');
  const bodyTable = tableWrap?.querySelector('.compact-explore-table-body');
  if (!headerTable || !bodyTable) return;

  const bodyCells = bodyTable.querySelector('tbody tr')?.cells;
  const headerColumns = headerTable.querySelectorAll('col');
  if (bodyCells?.length === headerColumns.length) {
    [...headerColumns].forEach((column, index) => {
      column.style.width = `${bodyCells[index].getBoundingClientRect().width}px`;
    });
  }
  headerTable.style.width = `${bodyTable.getBoundingClientRect().width}px`;
  headerTable.style.minWidth = '0';
  headerTable.style.transform = `translateX(-${scrollContainer.scrollLeft}px)`;
  const holdingHeader = headerTable.querySelector('.compact-explore-holding');
  if (holdingHeader) {
    holdingHeader.style.transform = `translateX(${scrollContainer.scrollLeft}px)`;
  }
}

function appendCompanyBatch() {
  const ranked = state.companyRanked;
  const start = state.companyVisibleCount;
  const displayLimit = getTopHoldingsDisplayLimit(ranked.length, state.topHoldingsMaximum);
  const end = Math.min(start + COMPANY_BATCH_SIZE, displayLimit);

  if (end <= start) {
    elements.companyList.querySelector('.company-scroll-sentinel')?.remove();
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
    elements.companyList.querySelector('.compact-explore-table-body tbody').appendChild(template.content);
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

  if (state.companyVisibleCount >= displayLimit) {
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
  const hasCapturedWeights = positions.every((position) => Number.isFinite(position.weightPct));
  const totalShareUnits = hasCapturedWeights ? 0 : getTotalShareUnits(positions);

  for (const position of positions) {
    const snapshot = position.snapshot;
    if (!snapshot || !totalShareUnits) {
      continue;
    }
    const positionWeight = hasCapturedWeights
      ? position.weightPct
      : getPositionWeight(position, totalShareUnits);
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

function buildReferenceSeries(labels, values, label = t('chart.portfolioReference')) {
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
  const effectiveValues = positions
    .map((position) => Number(getPositionValuation(position).valueChf))
    .filter((value) => Number.isFinite(value) && value >= 0);
  const totalValueChf = state.portfolioMode === 'percentage'
    ? t('common.notAvailable')
    : effectiveValues.length
    ? formatChfValue(effectiveValues.reduce((sum, value) => sum + value, 0))
    : formatChfValue(0);
  const uniqueEtfs = positions.length;
  const totalHoldings = positions.reduce((sum, position) => sum + (position.snapshot?.holdings?.length || 0), 0);
  const overlapCount = aggregateCompanyExposure(positions).ranked.filter((item) => item.etfs.size > 1).length;

  const cards = [
    { label: t('summary.positions'), value: formatCount(uniqueEtfs) },
    { label: t('summary.shareUnits'), value: formatCount(shareCountTotal) },
    { label: t('summary.totalValue'), value: totalValueChf },
    { label: t('summary.underlyingHoldings'), value: formatCount(totalHoldings) },
    { label: t('summary.sharedCompanies'), value: formatCount(overlapCount) },
  ];
  if (state.portfolioMode === 'percentage') {
    cards[1].value = t('common.notAvailable');
  }

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
    elements.catalogList.innerHTML = `<div class="empty-state">${t('catalog.noMatches')}</div>`;
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
            <button type="button" data-add-etf="${entry.isin}"${selected ? ' data-state="added" disabled' : ''}>
              ${selected ? t('catalog.added') : t('catalog.add')}
            </button>
          </div>
        </article>
      `;
    })
    .join('');
}

function renderPositions() {
  const positions = getSelectedPositions();
  const isPercentagePortfolio = state.portfolioMode === 'percentage';
  elements.positionInputHeading.textContent = isPercentagePortfolio ? t('ui.allocationPercent') : t('ui.shares');
  document.querySelectorAll('.positions-table thead [data-private-hidden]').forEach((header) => {
    header.hidden = isPercentagePortfolio;
  });
  if (!positions.length) {
    elements.positionsBody.innerHTML = `<tr><td colspan="${isPercentagePortfolio ? 4 : 6}"><div class="empty-state">${t('portfolio.noPositions')}</div></td></tr>`;
    elements.portfolioHint.textContent = t('portfolio.empty');
    return;
  }

  const totalShareUnits = getTotalShareUnits(positions);
  elements.portfolioHint.textContent = isPercentagePortfolio
    ? t('portfolio.percentageHint')
    : positions.some((position) => Number.isFinite(getPositionValuation(position).valueChf))
    ? state.valuationMode === 'imported'
      ? t('portfolio.importedWeightsHint')
      : t('portfolio.liveWeightsHint')
    : t('portfolio.shareCountWeightsHint');

  elements.positionsBody.innerHTML = positions
    .map((position) => {
      const weight = getPositionWeight(position, totalShareUnits);
      const valuation = isPercentagePortfolio ? null : getPositionValuation(position);
      const shareInputStep = isPercentagePortfolio ? '0.1' : '1';
      const shareInputValue = isPercentagePortfolio ? Number(position.shares).toFixed(1) : position.shares;
      const shareInputLabel = isPercentagePortfolio ? t('ui.allocationPercent') : t('ui.shares');
      const valuationCells = isPercentagePortfolio
        ? ''
        : `
          <td class="position-price" data-label="${t('ui.price')}"><span class="position-metric-value">${valuation.price !== null ? formatCurrencyValue(valuation.price, valuation.currency) : t('common.unavailable')}</span></td>
          <td class="position-value" data-label="${t('ui.valueChf')}"><span class="position-metric-value">${valuation.valueChf !== null ? formatCurrencyValue(valuation.valueChf) : t('common.unavailable')}</span></td>`;
      const allocationCells = isPercentagePortfolio
        ? `
          <td class="position-weight" data-label="${t('ui.weight')}" aria-label="${t('portfolio.weightLabel', { value: formatPercent(weight) })}"><span class="position-metric-value">${formatPercent(weight)}</span></td>
          <td class="position-remove" data-label="${t('ui.remove')}"><button type="button" class="remove-button" aria-label="${t('portfolio.removeTicker', { ticker: position.entry.ticker })}" title="${t('portfolio.removeTicker', { ticker: position.entry.ticker })}" data-remove-position="${position.isin}"><i data-lucide="trash-2" aria-hidden="true"></i><span class="remove-button-label">${t('ui.remove')}</span></button></td>`
        : `
          <td class="position-weight" data-label="${t('ui.weight')}" aria-label="${t('portfolio.weightLabel', { value: formatPercent(weight) })}"><span class="position-metric-value">${formatPercent(weight)}</span></td>
          <td class="position-remove" data-label="${t('ui.remove')}"><button type="button" class="remove-button" aria-label="${t('portfolio.removeTicker', { ticker: position.entry.ticker })}" title="${t('portfolio.removeTicker', { ticker: position.entry.ticker })}" data-remove-position="${position.isin}"><i data-lucide="trash-2" aria-hidden="true"></i><span class="remove-button-label">${t('ui.remove')}</span></button></td>`;
      return `
        <tr class="position-row${isPercentagePortfolio ? ' position-row--percentage' : ''}">
          <td class="position-identity" data-label="${t('ui.etf')}">
            <div class="position-name">
              <strong>${position.entry.ticker}</strong>
              <span>· ${position.entry.name}</span>
            </div>
          </td>
          <td class="position-shares" data-label="${shareInputLabel}">
            <input class="position-input" aria-label="${t('portfolio.inputForTicker', { field: shareInputLabel, ticker: position.entry.ticker })}" type="number" min="0" step="${shareInputStep}" value="${shareInputValue}" data-shares-input="${position.isin}" />
          </td>
          ${valuationCells}
          ${allocationCells}
        </tr>
      `;
    })
    .join('');
  window.lucide?.createIcons();
}

function renderComparisonToolbar(positions) {
  if (!positions.length) {
    elements.comparisonToolbar.innerHTML = `<div class="empty-state">${t('comparison.addPositions')}</div>`;
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

  const chartOptions = (labels) => ({
    legendMode: 'labels',
    labelDisplayOverrides: new Map(labels.map((label) => [label, translateTaxonomyLabel(label, t)])),
    translate: t,
    formatPercent,
  });
  renderComparisonChart(chartRefs.sector, elements.sectorCanvas, t('chart.titleSectors'), sectorSeries, sectorLabels, {
    ...chartOptions(sectorLabels),
    legendContainer: elements.sectorLegend,
  });
  renderComparisonChart(chartRefs.region, elements.regionCanvas, t('chart.titleRegions'), regionSeries, regionLabels, {
    ...chartOptions(regionLabels),
    legendContainer: elements.regionLegend,
  });
  renderComparisonChart(
    chartRefs.currency,
    elements.currencyCanvas,
    t('chart.titleCurrencies'),
    currencySeries,
    currencyLabels,
    {
      ...chartOptions(currencyLabels),
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
    { label: t('rollup.sectorExposure'), values: rollups.sector },
    { label: t('rollup.regionExposure'), values: rollups.region },
    { label: t('rollup.currencyExposure'), values: rollups.currency },
  ];

  elements.rollupGrid.innerHTML = cards
    .map((card) => {
      const sorted = [...card.values.entries()].sort((a, b) => b[1] - a[1]);
      const top = sorted[0];
      return `
        <article class="rollup-card">
          <strong>${card.label}</strong>
          <div class="value">${top ? formatPercent(top[1]) : formatPercent(0)}</div>
          <div class="subtext">${top ? translateTaxonomyLabel(top[0], t) : t('common.noDataYet')}</div>
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
  state.companyTableResizeObserver?.disconnect();
  state.companyTableResizeObserver = null;
  const unfilteredDisplayLimit = getTopHoldingsDisplayLimit(
    ranked.length,
    state.topHoldingsMaximum,
  );
  elements.compactExploreSearch.hidden = !state.compactExplorePreview;
  const searchTerm = state.companySearchTerm.trim().toLowerCase();

  if (state.compactExplorePreview) {
    if (!ranked.length) {
      elements.companyList.innerHTML = `<div class="empty-state">${t('explore.addPositions')}</div>`;
      elements.companyHint.textContent = t('explore.noExposureYet');
      return;
    }

    elements.companyList.innerHTML = buildCompactExploreTable(positions);
    const tableScroll = elements.companyList.querySelector('.compact-explore-table-scroll');
    tableScroll.addEventListener('scroll', () => syncCompactExploreHeader(tableScroll), { passive: true });
    state.companyTableResizeObserver = new ResizeObserver(() => syncCompactExploreHeader(tableScroll));
    state.companyTableResizeObserver.observe(tableScroll);
    state.companyTableResizeObserver.observe(
      elements.companyList.querySelector('.compact-explore-table-body'),
    );

    if (searchTerm) {
      const matches = ranked
        .map((company, index) => ({ company, rank: index + 1 }))
        .filter(({ company }) => company.name.toLowerCase().includes(searchTerm));
      elements.companyHint.textContent = matches.length
        ? t('explore.matchCount', { count: matches.length, countDisplay: formatCount(matches.length) })
        : t('explore.noCompanyMatches');
      elements.companyList.querySelector('.compact-explore-table-body tbody').innerHTML = matches
        .map(({ company, rank }) => buildCompactExploreRow(positions, company, rank))
        .join('');
      state.companyVisibleCount = matches.length;
      syncCompactExploreHeader(tableScroll);
      return;
    }

    elements.companyHint.textContent = t('explore.holdingsRanked');
    appendCompanyBatch();
    if (state.companyVisibleCount < unfilteredDisplayLimit) {
      const sentinel = document.createElement('div');
      sentinel.className = 'company-scroll-sentinel';
      sentinel.setAttribute('aria-hidden', 'true');
      elements.companyList.appendChild(sentinel);
      ensureCompanyObserver();
    }
    return;
  }

  if (!ranked.length) {
    elements.companyList.innerHTML = `<div class="empty-state">${t('explore.addPositions')}</div>`;
    elements.companyHint.textContent = t('explore.noExposureYet');
    return;
  }

  if (searchTerm) {
    const matches = ranked
      .map((company, index) => ({ company, rank: index + 1 }))
      .filter(({ company }) => company.name.toLowerCase().includes(searchTerm));
    elements.companyHint.textContent = matches.length
      ? t('explore.matchCount', { count: matches.length, countDisplay: formatCount(matches.length) })
      : t('explore.noCompanyMatches');
    elements.companyList.innerHTML = matches
      .map(({ company, rank }) => buildCompanyRow(company, rank - 1))
      .join('');
    state.companyVisibleCount = matches.length;
    return;
  }

  elements.companyHint.textContent = t('explore.showingTopHoldings');
  elements.companyList.innerHTML = '';
  appendCompanyBatch();

  if (state.companyVisibleCount < unfilteredDisplayLimit) {
    const sentinel = document.createElement('div');
    sentinel.className = 'company-scroll-sentinel';
    sentinel.setAttribute('aria-hidden', 'true');
    elements.companyList.appendChild(sentinel);
    ensureCompanyObserver();
  }
}

function renderRedundancyScore() {
  renderNearIdenticalPairWarning();
  const positions = getSelectedPositions();
  const totalShareUnits = getTotalShareUnits(positions);
  const positionWeights = positions.map((position) => ({
    weight: getPositionWeight(position, totalShareUnits),
    hasUsableHoldings: Boolean(position.snapshot?.holdings?.length),
  }));
  const { ranked } = aggregateCompanyExposure(positions);
  const result = calculateRedundancyScore(ranked, positionWeights);
  elements.redundancyMaximum.textContent = result.available
    ? formatPercent(result.maximum)
    : t('common.notAvailable');

  if (!result.available) {
    elements.redundancyScoreValue.textContent = t('common.notAvailable');
    elements.redundancyScoreLevel.hidden = true;
    elements.redundancyDescription.textContent = t('explore.redundancyUnavailable');
    elements.redundancyMeter.setAttribute('aria-label', t('explore.redundancyUnavailable'));
    elements.redundancyMarker.hidden = true;
    elements.redundancyMarker.removeAttribute('title');
    for (const segment of elements.redundancySegments) segment.style.width = '0%';
    return;
  }

  const scoreText = formatPercent(result.score);
  const level = classifyRedundancyScore(
    result.score,
    state.redundancyThresholds.lowModerate,
    state.redundancyThresholds.moderateHigh,
  );
  const scalePosition = (value) => result.maximum > 0
    ? Math.min(Math.max((value / result.maximum) * 100, 0), 100)
    : 0;
  const lowBoundary = scalePosition(state.redundancyThresholds.lowModerate);
  const moderateBoundary = scalePosition(state.redundancyThresholds.moderateHigh);
  const scorePosition = scalePosition(result.score);

  elements.redundancyScoreValue.textContent = scoreText;
  elements.redundancyScoreLevel.hidden = false;
  elements.redundancyScoreLevel.className = `redundancy-score-level is-${level}`;
  elements.redundancyScoreLevel.textContent = t(`explore.redundancy.${level}`);
  elements.redundancyDescription.textContent = t('explore.redundancyDescription', { value: scoreText });
  elements.redundancyMeter.setAttribute('aria-label', t('explore.redundancyBarLabel', {
    score: scoreText,
    level: t(`explore.redundancy.${level}`),
    maximum: formatPercent(result.maximum),
  }));
  elements.redundancyMarker.title = t(`explore.redundancy.${level}`);
  elements.redundancySegments[0].style.width = `${result.maximum > 0 ? lowBoundary : 0}%`;
  elements.redundancySegments[1].style.left = `${lowBoundary}%`;
  elements.redundancySegments[1].style.width = `${result.maximum > 0 ? Math.max(moderateBoundary - lowBoundary, 0) : 0}%`;
  elements.redundancySegments[2].style.width = `${result.maximum > 0 ? Math.max(100 - moderateBoundary, 0) : 0}%`;
  elements.redundancyMarker.style.left = `${scorePosition}%`;
  elements.redundancyMarker.hidden = false;
}

function formatDiversificationNumber(value) {
  return new Intl.NumberFormat(window.i18next.language, {
    maximumFractionDigits: 1,
  }).format(value);
}

function formatDiversificationCoverage(value) {
  return new Intl.NumberFormat(window.i18next.language, {
    style: 'percent',
    maximumFractionDigits: 2,
  }).format(value / 100);
}

function renderDiversificationScore() {
  const positions = getSelectedPositions();
  const totalShareUnits = getTotalShareUnits(positions);
  const { ranked } = aggregateCompanyExposure(positions);
  const coveragePositions = positions.map((position) => {
    const disclosedWeight = (position.snapshot?.holdings || []).reduce((total, holding) => {
      const weight = Number(holding?.exposure?.weight_pct);
      return total + (Number.isFinite(weight) && weight > 0 ? weight : 0);
    }, 0);
    return {
      weight: getPositionWeight(position, totalShareUnits),
      coveragePct: disclosedWeight,
    };
  });
  const result = calculateDiversificationScore(
    ranked.map((company) => company.weight),
    coveragePositions,
  );
  const boundaries = [0, 5, 10, 20, 40, result.maximum];
  const segmentWidths = boundaries.slice(1).map((boundary, index) =>
    Math.max(boundary - boundaries[index], 0) / result.maximum * 100
  );

  elements.diversificationScoreValue.textContent = result.available
    ? formatDiversificationNumber(result.score)
    : t('common.notAvailable');
  elements.diversificationDescription.textContent = result.available
    ? t('explore.diversificationDescription')
    : t('explore.diversificationUnavailable');
  elements.diversificationScoreLevel.hidden = !result.available;
  elements.diversificationMaximum.textContent = result.available
    ? formatDiversificationNumber(result.maximum)
    : t('common.notAvailable');
  elements.diversificationCoverageWarning.hidden = !result.available || !result.coverageIncomplete;
  if (result.available) {
    const level = t(`explore.diversification.${result.rating}`);
    const ratingClass = result.rating.replace(/[A-Z]/g, (character) => `-${character.toLowerCase()}`);
    elements.diversificationScoreLevel.className = `redundancy-score-level is-${ratingClass}`;
    elements.diversificationScoreLevel.textContent = level;
    elements.diversificationCoverageWarning.textContent = t('explore.diversificationCoverageWarning', {
      coverage: formatDiversificationCoverage(result.coveragePct),
    });
    elements.diversificationMeter.setAttribute('aria-label', t('explore.diversificationBarLabel', {
      score: formatDiversificationNumber(result.score),
      level,
      maximum: formatDiversificationNumber(result.maximum),
    }));
  } else {
    elements.diversificationScoreLevel.className = 'redundancy-score-level';
    elements.diversificationMeter.setAttribute('aria-label', t('explore.diversificationUnavailable'));
    elements.diversificationMarker.removeAttribute('title');
  }

  for (const [index, segment] of elements.diversificationSegments.entries()) {
    segment.style.left = `${boundaries[index] / result.maximum * 100}%`;
    segment.style.width = `${result.available ? segmentWidths[index] : 0}%`;
  }
  elements.diversificationMarker.style.left = result.available
    ? `${Math.min((result.score / result.maximum) * 100, 100)}%`
    : '0%';
  if (result.available) elements.diversificationMarker.title = t(`explore.diversification.${result.rating}`);
  elements.diversificationMarker.hidden = !result.available;
}

function escapeMarkup(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[character]);
}

function renderNearIdenticalPairWarning() {
  const pairs = findNearIdenticalPairs(
    getSelectedPositions(),
    state.pairwiseOverlapIndex,
    state.nearIdenticalThreshold,
  );
  if (!pairs.length) {
    elements.nearIdenticalPairWarning.hidden = true;
    elements.nearIdenticalPairWarning.innerHTML = '';
    return;
  }

  const items = pairs.map((pair) => `
    <li>${escapeMarkup(t('explore.nearIdenticalPair', {
      a: pair.productA.name,
      b: pair.productB.name,
      overlap: formatPercent(pair.overlapPct),
    }))}</li>
  `).join('');
  elements.nearIdenticalPairWarning.innerHTML = `
    <i data-lucide="triangle-alert" aria-hidden="true"></i>
    <div>
      <strong>${escapeMarkup(t('explore.nearIdenticalWarning', {
        threshold: formatPercent(state.nearIdenticalThreshold),
      }))}</strong>
      <ul>${items}</ul>
    </div>
  `;
  elements.nearIdenticalPairWarning.hidden = false;
  window.lucide?.createIcons();
}

function renderPairwiseSelector(positions, slot, selectedIsin, otherIsin) {
  const selected = positions.find((position) => position.isin === selectedIsin);
  const labelKey = slot === 'a' ? 'explore.pairwiseFirstETF' : 'explore.pairwiseSecondETF';
  const options = positions
    .filter((position) => position.isin !== otherIsin)
    .map((position) => `
      <button class="color-mode-option pairwise-selector-option" type="button" role="menuitemradio" aria-checked="${position.isin === selectedIsin}" data-pairwise-etf-option data-pairwise-selector-slot="${slot}" data-pairwise-etf-isin="${escapeMarkup(position.isin)}">
        <span><strong>${escapeMarkup(position.entry.ticker)}</strong><small>${escapeMarkup(position.entry.name)}</small></span>
      </button>
    `).join('');

  return `
    <div class="color-mode-control pairwise-selector-control">
      <span class="pairwise-selector-label" id="pairwise-selector-label-${slot}">${escapeMarkup(t(labelKey))}</span>
      <button class="color-mode-button pairwise-selector-button" type="button" aria-haspopup="menu" aria-expanded="false" aria-labelledby="pairwise-selector-label-${slot} pairwise-selector-value-${slot}" data-pairwise-selector-button="${slot}">
        <span id="pairwise-selector-value-${slot}">${escapeMarkup(selected?.entry.ticker || '')}</span>
        <i data-lucide="chevron-down" aria-hidden="true"></i>
      </button>
      <div class="color-mode-menu pairwise-selector-menu" role="menu" aria-labelledby="pairwise-selector-label-${slot}" data-pairwise-selector-menu="${slot}" hidden>
        ${options}
      </div>
    </div>
  `;
}

function renderPairwiseHoldingsDetail(positions) {
  const [isinA, isinB] = state.pairwiseSelection;
  const positionA = positions.find((position) => position.isin === isinA);
  const positionB = positions.find((position) => position.isin === isinB);
  const pair = getPairwiseOverlap(state.pairwiseOverlapIndex, isinA, isinB);
  if (!positionA || !positionB || !pair?.available || !Number.isFinite(pair.overlapPct)) {
    return `<p class="pairwise-overlap-status">${escapeMarkup(t('explore.pairwiseHoldingsUnavailable'))}</p>`;
  }

  const holdingsA = positionA.snapshot?.holdings;
  const holdingsB = positionB.snapshot?.holdings;
  if (!Array.isArray(holdingsA) || !Array.isArray(holdingsB)) {
    return `<p class="pairwise-overlap-status">${escapeMarkup(t('explore.pairwiseHoldingsUnavailable'))}</p>`;
  }

  const breakdown = buildPairwiseHoldingsBreakdown(
    holdingsA,
    holdingsB,
    state.pairwiseHoldingsMaxCompanies,
  );
  const displayedContribution = breakdown.displayed.reduce(
    (total, company) => total + company.contribution,
    0,
  );
  const hasRemaining = breakdown.companies.length > breakdown.displayed.length;
  const remainingContribution = hasRemaining
    ? Math.max(0, pair.overlapPct - displayedContribution)
    : 0;
  const scale = Math.max(0, ...breakdown.displayed.flatMap((company) => [company.weightA, company.weightB])) || 1;
  const barGridStyle = (weight) => {
    const fillRatio = Math.min(1, Math.max(0, weight / scale));
    return `--pairwise-fill: ${fillRatio}fr; --pairwise-empty: ${1 - fillRatio}fr`;
  };
  const rows = breakdown.displayed.map((company) => `
    <li class="pairwise-butterfly-company">
      <strong>${escapeMarkup(company.name)}</strong>
      <div class="pairwise-butterfly-chart" role="img" aria-label="${escapeMarkup(t('explore.pairwiseCompanyWeights', {
        company: company.name,
        tickerA: positionA.entry.ticker,
        weightA: formatPercent(company.weightA),
        tickerB: positionB.entry.ticker,
        weightB: formatPercent(company.weightB),
      }))}">
        <span class="pairwise-butterfly-side is-a" style="${barGridStyle(company.weightA)}" aria-hidden="true">
          <span class="pairwise-butterfly-side-spacer"></span>
          <span class="pairwise-butterfly-value">${escapeMarkup(formatPercentNumber(company.weightA))}</span>
          <span class="pairwise-butterfly-side-gap"></span>
          <span class="pairwise-butterfly-side-track"><i class="is-a"></i></span>
        </span>
        <span class="pairwise-butterfly-side is-b" style="${barGridStyle(company.weightB)}" aria-hidden="true">
          <span class="pairwise-butterfly-side-track"><i class="is-b"></i></span>
          <span class="pairwise-butterfly-side-gap"></span>
          <span class="pairwise-butterfly-value">${escapeMarkup(formatPercentNumber(company.weightB))}</span>
          <span class="pairwise-butterfly-side-spacer"></span>
        </span>
      </div>
    </li>
  `).join('');
  return `
    <section class="pairwise-holdings-detail" aria-labelledby="pairwise-holdings-heading">
      <div class="pairwise-holdings-heading">
        <h4 id="pairwise-holdings-heading">${escapeMarkup(positionA.entry.ticker)} <span aria-hidden="true">↔</span> ${escapeMarkup(positionB.entry.ticker)}</h4>
        <div class="pairwise-holdings-meta">
          <div class="pairwise-holdings-total" aria-label="${escapeMarkup(t('explore.pairwiseOverlapTotal'))}">
            <strong>${escapeMarkup(formatPercent(pair.overlapPct))}</strong>
            <span>${escapeMarkup(t('explore.pairwiseOverlapSuffix'))}</span>
          </div>
        </div>
      </div>
      <div class="pairwise-butterfly-legend" role="group" aria-label="${escapeMarkup(t('explore.pairwiseLegendLabel'))}">
        <span><i class="is-a" aria-hidden="true"></i>${escapeMarkup(positionA.entry.ticker)}</span>
        <span><i class="is-b" aria-hidden="true"></i>${escapeMarkup(positionB.entry.ticker)}</span>
      </div>
      ${rows
    ? `<ol class="pairwise-holdings-list" aria-label="${escapeMarkup(t('explore.pairwiseHoldingsHeading'))}">${rows}</ol>`
    : `<p class="pairwise-no-shared-holdings">${escapeMarkup(t('explore.pairwiseNoSharedHoldings'))}</p>`}
      <p class="pairwise-holdings-footer">
        <span class="pairwise-weight-unit" role="note">${escapeMarkup(t('explore.pairwiseWeightsUnit'))}</span>${hasRemaining ? `<span class="pairwise-remaining-contribution"> ${escapeMarkup(t('explore.pairwiseRemainingContribution', { weight: formatPercent(remainingContribution) }))}</span>` : ''}
      </p>
    </section>
  `;
}

function renderPairwiseOverlap() {
  const positions = getSelectedPositions();
  state.pairwiseSelection = reconcilePairwiseSelection(positions, state.pairwiseSelection);
  if (!positions.length) {
    elements.pairwiseOverlapContent.innerHTML = `<p class="empty-state">${escapeMarkup(t('explore.pairwiseNoSelection'))}</p>`;
    elements.pairwiseHoldingsContent.innerHTML = `<p class="empty-state">${escapeMarkup(t('explore.pairwiseNoSelection'))}</p>`;
    return;
  }

  const pairwiseControls = positions.length < 2
    ? `<p class="pairwise-overlap-status">${escapeMarkup(t('explore.pairwiseNeedTwo'))}</p>`
    : `
      <div class="pairwise-holdings-controls" data-pairwise-selector-group role="group" aria-label="${escapeMarkup(t('explore.pairwiseSelectionLabel'))}">
        ${renderPairwiseSelector(positions, 'a', state.pairwiseSelection[0], state.pairwiseSelection[1])}
        ${renderPairwiseSelector(positions, 'b', state.pairwiseSelection[1], state.pairwiseSelection[0])}
      </div>
    `;
  const holdingsDetail = positions.length < 2 ? '' : renderPairwiseHoldingsDetail(positions);
  elements.pairwiseHoldingsContent.innerHTML = `${pairwiseControls}${holdingsDetail}`;

  const headers = positions.map((position) => `
    <th scope="col" title="${escapeMarkup(position.entry.name)}">
      <span>${escapeMarkup(position.entry.ticker)}</span>
    </th>
  `).join('');
  const matrix = buildPairwiseMatrix(
    positions,
    state.pairwiseOverlapIndex,
    state.nearIdenticalThreshold,
  );
  const coverageValues = matrix.flatMap((row) => row.cells.flatMap((cell) => {
    if (cell.type === 'overlap') return [cell.coveragePctA, cell.coveragePctB];
    if (cell.type === 'unavailable' && cell.pair) {
      return [cell.pair.coveragePctA, cell.pair.coveragePctB];
    }
    return [];
  })).filter(Number.isFinite);
  const coverageRange = coverageValues.length
    ? `${formatPercent(Math.min(...coverageValues))}–${formatPercent(Math.max(...coverageValues))}`
    : t('explore.pairwiseCoverageUnavailable');
  const rows = matrix.map((row) => {
    const cells = row.cells.map((cell, columnIndex) => {
      if (cell.type === 'diagonal') {
        return `<td class="pairwise-diagonal" aria-label="${escapeMarkup(t('explore.pairwiseDiagonal'))}">&mdash;</td>`;
      }
      if (cell.type === 'empty') {
        return '<td class="pairwise-empty" aria-hidden="true"></td>';
      }

      if (cell.type === 'unavailable') {
        const coverage = cell.pair
          ? t('explore.pairwiseCoverage', {
            a: formatPercent(cell.pair.coveragePctA),
            b: formatPercent(cell.pair.coveragePctB),
          })
          : t('explore.pairwiseCoverageUnavailable');
        const label = t('explore.pairwiseCellLabel', {
          a: row.product.name,
          b: positions[columnIndex].entry.name,
          overlap: t('explore.pairwiseUnavailable'),
          coverage,
        });
        return `
          <td class="pairwise-overlap-cell is-unavailable" aria-label="${escapeMarkup(label)}">
            <span class="pairwise-overlap-value">${escapeMarkup(t('explore.pairwiseUnavailable'))}</span>
            <span class="pairwise-overlap-coverage">${escapeMarkup(coverage)}</span>
          </td>
        `;
      }

      const overlap = cell.overlapPct;
      const level = overlap >= 75 ? 'high' : overlap >= 35 ? 'moderate' : 'low';
      const nearIdentical = cell.nearIdentical;
      const coverage = t('explore.pairwiseCoverage', {
        a: formatPercent(cell.coveragePctA),
        b: formatPercent(cell.coveragePctB),
      });
      const label = t('explore.pairwiseCellLabel', {
        a: row.product.name,
        b: positions[columnIndex].entry.name,
        overlap: formatPercent(overlap),
        coverage,
      });
      const overlapLabel = new Intl.NumberFormat(window.i18next.language, {
        maximumFractionDigits: 1,
      }).format(overlap);
      return `
        <td class="pairwise-overlap-cell is-${level}${nearIdentical ? ' is-near-identical' : ''}" style="--pairwise-overlap: ${Math.min(Math.max(overlap, 0), 100)}" aria-label="${escapeMarkup(label)}">
          <span class="pairwise-overlap-value">${nearIdentical ? '≈' : ''}${escapeMarkup(overlapLabel)}</span>
          <span class="pairwise-overlap-coverage">${escapeMarkup(coverage)}</span>
        </td>
      `;
    }).join('');
    return `
      <tr>
        <th scope="row" class="pairwise-row-label" title="${escapeMarkup(row.product.name)}">
          <span>${escapeMarkup(row.product.ticker)}</span>
          <small>${escapeMarkup(row.product.name)}</small>
        </th>
        ${cells}
      </tr>
    `;
  }).join('');

  const missingCatalogData = !state.catalog?.pairwiseOverlap?.pairs;
  elements.pairwiseOverlapContent.innerHTML = `
    ${missingCatalogData ? `<p class="pairwise-overlap-status">${escapeMarkup(t('explore.pairwiseCatalogUnavailable'))}</p>` : ''}
    <div class="pairwise-overlap-viewport" role="region" tabindex="0" aria-label="${escapeMarkup(t('explore.pairwiseTitle'))}">
      <table class="pairwise-overlap-table">
        <thead><tr><th class="pairwise-corner" scope="col">${escapeMarkup(t('explore.pairwiseProduct'))}</th>${headers}</tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
    <div class="pairwise-overlap-legend" role="group" aria-label="${escapeMarkup(t('explore.pairwiseLegendLabel'))}">
      <div class="pairwise-overlap-legend-scale">
        <span>${escapeMarkup(formatPercent(0))}</span>
        <span class="pairwise-overlap-legend-swatches" aria-hidden="true">${[0, 25, 50, 75, 100].map((value) => `<i style="--pairwise-overlap: ${value}"></i>`).join('')}</span>
        <span>${escapeMarkup(formatPercent(100))}</span>
        <span class="pairwise-near-identical-swatch" aria-hidden="true"></span>
        <span>${escapeMarkup(t('explore.pairwiseLegendNearIdentical', { threshold: formatPercent(state.nearIdenticalThreshold) }))}</span>
      </div>
      <p>${escapeMarkup(t('explore.pairwiseLegendDescription', { coverage: coverageRange }))}</p>
    </div>
  `;
  window.lucide?.createIcons();
}

function renderWarnings() {
  renderBuildWarnings();
}

function updateSearchClearButton(input, button) {
  button.hidden = !input.value;
}

function updateCompanySearchClearButton() {
  updateSearchClearButton(elements.companySearch, elements.companySearchClear);
}

function formatImportedMoney(value, currency = 'CHF') {
  if (!Number.isFinite(Number(value))) {
    return t('common.invalid');
  }
  return formatCurrencyValue(value, currency);
}

function getImportReviewValuation(row) {
  return getEffectiveValuation(row, state.livePrices, state.importValuationMode);
}

function formatImportReviewValuation(row) {
  const valuation = getImportReviewValuation(row);
  const source = t(valuation.status === 'fallback' ? 'import.sourceImportedFallback' : `import.source.${valuation.status}`);
  const value = valuation.status === 'unavailable'
    ? formatImportedMoney(row.valueChf)
    : formatImportedMoney(valuation.valueChf);
  return t('import.valueWithSource', { value, source });
}

function translateImportWarning(warning) {
  const keys = {
    'Invalid ISIN': 'import.warningInvalidIsin',
    'Shares are missing or invalid': 'import.warningInvalidShares',
    'Price is missing or invalid': 'import.warningInvalidPrice',
    'Currency is missing or unsupported': 'import.warningInvalidCurrency',
  };
  return keys[warning] ? t(keys[warning]) : t('import.warningUnsupported', { warning });
}

function translateImportError(error) {
  const keys = {
    'This PDF is not a supported Saxo Bank report.': 'import.errorUnsupportedPdf',
    'No Saxo holdings pages were found in this PDF.': 'import.errorNoHoldingsPages',
    'PDF.js is unavailable. Reload the page and try again.': 'import.errorPdfJsUnavailable',
    'No ETF holdings were found in the supported Saxo sections.': 'import.errorNoEtfHoldings',
  };
  return keys[error.message] ? t(keys[error.message]) : error.message;
}

function getImportReviewPrice(row) {
  const valuation = getImportReviewValuation(row);
  return {
    value: valuation.price === null ? '' : valuation.price,
    editable: valuation.status !== 'live',
  };
}

function renderImportReview() {
  const validRows = state.importReviewRows.filter((row) => row.included && !row.warnings.length && row.matchStatus === 'matched');
  elements.importSummary.textContent = t('import.reviewSummary', {
    count: state.importReviewRows.length,
    countDisplay: formatCount(state.importReviewRows.length),
    validDisplay: formatCount(validRows.length),
  });
  elements.importTbody.innerHTML = state.importReviewRows
    .map((row, index) => {
      const warning = row.warnings.length
        ? ` ${row.warnings.map(translateImportWarning).join('; ')}`
        : row.matchStatus === 'unmatched' ? ` ${t('import.warningIsinNotInCatalog')}` : '';
      const label = row.entry ? `${row.entry.ticker} · ${row.entry.name}` : row.isin;
      const price = getImportReviewPrice(row);
      return `
        <tr class="import-row ${warning ? 'import-row-warning' : ''}">
          <td><input type="checkbox" aria-label="${t('import.includeLabel', { label })}" data-import-include="${index}" ${row.included ? 'checked' : ''} ${row.matchStatus !== 'matched' ? 'disabled' : ''} /></td>
          <td><strong>${label}</strong><span class="import-row-meta">${row.isin} · ${t('import.page', { page: row.pageNumber })}${warning ? ` · ${warning}` : ''}</span></td>
          <td><input class="import-input" type="number" min="0" step="1" value="${row.shares ?? ''}" data-import-shares="${index}" /></td>
          <td><input class="import-input" type="number" min="0" step="0.0001" value="${price.value}" data-import-price="${index}" ${price.editable ? '' : 'readonly'} /></td>
          <td><select class="import-currency" data-import-currency="${index}"><option value="CHF" ${row.currency === 'CHF' ? 'selected' : ''}>CHF</option><option value="EUR" ${row.currency === 'EUR' ? 'selected' : ''}>EUR</option><option value="USD" ${row.currency === 'USD' ? 'selected' : ''}>USD</option></select></td>
          <td data-import-value="${index}">${formatImportedMoney(row.value, row.currency)}</td>
          <td data-import-value-chf="${index}">${formatImportReviewValuation(row)}</td>
        </tr>
      `;
    })
    .join('');
  elements.importConfirm.disabled = !validRows.length;
  elements.importValuation.value = state.importValuationMode;
}

function updateImportRow(index, field, value) {
  const row = state.importReviewRows[index];
  if (!row) return;
  if (field === 'currency') row.currency = value;
  else row[field] = Number(value);
  const calculated = calculateImportedPosition(Number(row.shares), Number(row.price), row.currency, state.livePrices?.fx);
  row.value = calculated.value;
  row.valueChf = calculated.valueChf;
  row.warnings = [];
  if (!Number.isFinite(row.shares) || row.shares < 0) row.warnings.push('Shares are missing or invalid');
  if (!Number.isFinite(row.price) || row.price < 0) row.warnings.push('Price is missing or invalid');
  refreshImportReviewTotals();
}

function refreshImportReviewTotals() {
  const validRows = state.importReviewRows.filter((row) => row.included && !row.warnings.length && row.matchStatus === 'matched');
  elements.importSummary.textContent = t('import.reviewSummary', {
    count: state.importReviewRows.length,
    countDisplay: formatCount(state.importReviewRows.length),
    validDisplay: formatCount(validRows.length),
  });
  for (const [index, row] of state.importReviewRows.entries()) {
    const value = elements.importTbody.querySelector(`[data-import-value="${index}"]`);
    const price = elements.importTbody.querySelector(`[data-import-price="${index}"]`);
    const valueChf = elements.importTbody.querySelector(`[data-import-value-chf="${index}"]`);
    if (value) value.textContent = formatImportedMoney(row.value, row.currency);
    if (price) {
      const reviewPrice = getImportReviewPrice(row);
      price.value = reviewPrice.value;
      price.readOnly = !reviewPrice.editable;
    }
    if (valueChf) valueChf.textContent = formatImportReviewValuation(row);
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
    elements.importStatus.textContent = t('import.selectPdf');
    return;
  }
  elements.importStatus.textContent = t('import.readingLocally', { name: file.name });
  window.__etfLensPdfImportPages = null;
  updateImportDebugVisibility();
  try {
    const pages = await extractPdfPages(file);
    window.__etfLensPdfImportPages = pages;
    updateImportDebugVisibility();
    const rows = matchImportedRows(parseSaxoPages(pages, state.livePrices?.fx), state.catalogMaps);
    if (!rows.length) throw new Error('No ETF holdings were found in the supported Saxo sections.');
    showImportDialog(rows);
    elements.importStatus.textContent = t('import.reviewBeforeReplace');
  } catch (error) {
    elements.importStatus.textContent = translateImportError(error);
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
      valuationMode: state.importValuationMode,
    }));
  if (!positions.length) {
    elements.importStatus.textContent = t('import.noValidSelection');
    return;
  }
  state.portfolio = positions;
  state.portfolioMode = 'full';
  state.valuationMode = state.importValuationMode;
  clearShareFeedback();
  savePortfolioState();
  closeImportDialog();
  elements.importStatus.textContent = t('import.importedPositions', {
    count: positions.length,
    countDisplay: formatCount(positions.length),
  });
  renderAll();
}

function renderAll() {
  renderPortfolioModeControl();
  renderValuationModeControl();
  renderCatalog();
  renderPositions();
  renderBuildData();
  renderComparisonToolbar(getSelectedPositions());
  renderComparisonCharts();
  if (state.activeTab === 'comparison') {
    applyChartFrameSizing();
  }
  renderRollups();
  renderRedundancyScore();
  renderPairwiseOverlap();
  renderDiversificationScore();
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
  updateInstallAction();
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
  clearShareFeedback();
  savePortfolioState();
  renderAll();
}

function updatePositionShares(isin, shares) {
  state.portfolio = state.portfolio.map((position) =>
    position.isin === isin ? { ...position, shares: Number.isFinite(shares) ? Math.max(shares, 0) : 0 } : position
  );
  clearShareFeedback();
  savePortfolioState();
  renderAll();
}

function removePosition(isin) {
  state.portfolio = state.portfolio.filter((position) => position.isin !== isin);
  clearShareFeedback();
  savePortfolioState();
  renderAll();
}

async function bootstrap() {
  elements.summaryGrid = document.getElementById('summary-grid');
  elements.navigationItems = document.getElementById('primary-navigation-items');
  elements.languageButton = document.getElementById('language-button');
  elements.languageMenu = document.getElementById('language-menu');
  applyStaticTranslations();
  renderLanguageControl();
  renderNavigation();
  window.lucide?.createIcons();
  elements.tabButtons = [...document.querySelectorAll('.tab-button')];
  elements.tabPanels = [...document.querySelectorAll('.tab-panel')];
  elements.catalogSearch = document.getElementById('catalog-search');
  elements.catalogSearchClear = document.getElementById('catalog-search-clear');
  elements.catalogList = document.getElementById('catalog-list');
  elements.positionsBody = document.getElementById('positions-tbody');
  elements.portfolioModeControl = document.getElementById('portfolio-mode-control');
  elements.positionInputHeading = document.querySelector('[data-position-input-heading]');
  elements.portfolioValuationControl = document.getElementById('portfolio-valuation-control');
  elements.portfolioValuation = document.getElementById('portfolio-valuation');
  elements.portfolioValuationStatus = document.getElementById('portfolio-valuation-status');
  elements.portfolioHint = document.getElementById('portfolio-hint');
  elements.shareButton = document.getElementById('share-portfolio-button');
  elements.shareStatus = document.getElementById('share-portfolio-status');
  elements.shareFallbackLabel = document.querySelector('.share-portfolio-url-label');
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
  elements.redundancyScoreValue = document.getElementById('redundancy-score-value');
  elements.redundancyScoreLevel = document.getElementById('redundancy-score-level');
  elements.redundancyDescription = document.getElementById('redundancy-description');
  elements.redundancyMeter = document.getElementById('redundancy-meter');
  elements.redundancyMaximum = document.getElementById('redundancy-maximum');
  elements.redundancySegments = [...document.querySelectorAll('[data-redundancy-segment]')];
  elements.redundancyMarker = document.getElementById('redundancy-meter-marker');
  elements.redundancyLowThreshold = document.getElementById('redundancy-low-threshold');
  elements.redundancyHighThreshold = document.getElementById('redundancy-high-threshold');
  elements.redundancyThresholdError = document.getElementById('redundancy-threshold-error');
  elements.nearIdenticalPairWarning = document.getElementById('near-identical-pair-warning');
  elements.pairwiseOverlapContent = document.getElementById('pairwise-overlap-content');
  elements.pairwiseHoldingsContent = document.getElementById('pairwise-holdings-content');
  elements.diversificationScoreValue = document.getElementById('diversification-score-value');
  elements.diversificationScoreLevel = document.getElementById('diversification-score-level');
  elements.diversificationDescription = document.getElementById('diversification-description');
  elements.diversificationMeter = document.getElementById('diversification-meter');
  elements.diversificationMaximum = document.getElementById('diversification-maximum');
  elements.diversificationSegments = [...document.querySelectorAll('[data-diversification-segment]')];
  elements.diversificationMarker = document.getElementById('diversification-meter-marker');
  elements.diversificationCoverageWarning = document.getElementById('diversification-coverage-warning');
  elements.nearIdenticalThreshold = document.getElementById('near-identical-threshold');
  elements.nearIdenticalThresholdError = document.getElementById('near-identical-threshold-error');
  elements.pairwiseHoldingsMaxCompanies = document.getElementById('pairwise-holdings-max-companies');
  elements.pairwiseHoldingsMaxCompaniesError = document.getElementById('pairwise-holdings-max-companies-error');
  elements.topHoldingsMaximum = document.getElementById('top-holdings-maximum');
  elements.topHoldingsMaximumError = document.getElementById('top-holdings-maximum-error');
  elements.buildDialogButton = document.getElementById('build-dialog-button');
  elements.dataDialogButton = document.getElementById('data-dialog-button');
  elements.exportButton = document.getElementById('export-report-button');
  elements.exportDialog = document.getElementById('export-report-dialog');
  elements.exportDialogClose = document.getElementById('export-report-close');
  elements.exportScope = [...document.querySelectorAll('input[name="export-report-scope"]')];
  elements.exportAllocationOnly = document.getElementById('export-allocation-only');
  elements.exportGenerateButton = document.getElementById('export-report-generate');
  elements.exportGenerationStatus = document.getElementById('export-generation-status');
  elements.buildDialog = document.getElementById('build-dialog');
  elements.buildDialogClose = document.getElementById('build-dialog-close');
  elements.buildMetadata = document.getElementById('build-metadata');
  elements.buildDetailsExtra = document.getElementById('build-details-extra');
  elements.dataDialog = document.getElementById('data-dialog');
  elements.dataDialogClose = document.getElementById('data-dialog-close');
  elements.dataDialogMetadata = document.getElementById('data-dialog-metadata');
  elements.dataDialogWarningList = document.getElementById('data-dialog-warning-list');
  elements.scoreInfoDialog = document.getElementById('score-info-dialog');
  elements.scoreInfoTitle = document.getElementById('score-info-dialog-title');
  elements.scoreInfoDialogClose = document.getElementById('score-info-dialog-close');
  elements.scoreInfoPanels = [...document.querySelectorAll('[data-score-info-panel]')];
  elements.pairwiseHeatmapInfoDialog = document.getElementById('pairwise-heatmap-info-dialog');
  elements.pairwiseHoldingsInfoDialog = document.getElementById('pairwise-holdings-info-dialog');
  elements.pairwiseInfoDialogs = [elements.pairwiseHeatmapInfoDialog, elements.pairwiseHoldingsInfoDialog];
  elements.compactExplorePreview = document.getElementById('compact-explore-preview');
  elements.portfolioImportDebugEnabled = document.getElementById('portfolio-import-debug-enabled');
  elements.importDialog = document.getElementById('portfolio-import-dialog');
  elements.importDialogClose = document.getElementById('portfolio-import-close');
  elements.importDialogCancel = document.getElementById('portfolio-import-cancel');
  elements.importConfirm = document.getElementById('portfolio-import-confirm');
  elements.importValuation = document.getElementById('portfolio-import-valuation');
  elements.importTbody = document.getElementById('portfolio-import-tbody');
  elements.importSummary = document.getElementById('portfolio-import-summary');
  elements.importStatus = document.getElementById('portfolio-import-status');
  elements.importDebug = document.getElementById('portfolio-import-debug');
  elements.importFile = document.getElementById('portfolio-import-file');
  elements.importControl = document.querySelector('.portfolio-import-control');
  elements.colorModeButton = document.getElementById('color-mode-button');
  elements.colorModeMenu = document.getElementById('color-mode-menu');
  elements.installAppButton = document.getElementById('install-app-button');
  elements.colorModeUtility = document.querySelector('.app-utility-bar');
  bindScoreBandTouchTooltip(elements.redundancyMeter, elements.redundancySegments);
  bindScoreBandTouchTooltip(elements.diversificationMeter, elements.diversificationSegments);
  document.addEventListener('pointerdown', (event) => {
    if (!event.target.closest?.('.redundancy-meter-track')) hideScoreBandTouchTooltips();
  }, true);
  window.addEventListener('scroll', () => hideScoreBandTouchTooltips(), { capture: true, passive: true });
  window.addEventListener('resize', () => hideScoreBandTouchTooltips());
  window.matchMedia?.('(max-width: 760px)').addEventListener('change', updateInstallAction);

  state.colorMode = loadColorMode();
  state.portfolioImportDebug = loadPortfolioImportDebug();
  applyColorMode();
  renderColorModeControl();
  updateInstallAction();
  elements.portfolioImportDebugEnabled.checked = state.portfolioImportDebug;
  renderBuildInfo();
  elements.buildDialogButton.addEventListener('click', openBuildDialog);
  elements.dataDialogButton.addEventListener('click', openDataDialog);
  elements.exportButton.addEventListener('click', openExportDialog);
  elements.exportDialogClose.addEventListener('click', closeExportDialog);
  elements.exportGenerateButton.addEventListener('click', generateExportReport);
  elements.buildDialogClose.addEventListener('click', closeBuildDialog);
  elements.dataDialogClose.addEventListener('click', closeDataDialog);
  document.querySelectorAll('[data-score-info]').forEach((button) => {
    button.addEventListener('click', openScoreInfoDialog);
  });
  document.querySelectorAll('[data-pairwise-info]').forEach((button) => {
    button.addEventListener('click', openPairwiseInfoDialog);
  });
  document.querySelectorAll('[data-pairwise-info-close]').forEach((button) => {
    button.addEventListener('click', (event) => {
      closePairwiseInfoDialog(event.currentTarget.closest('dialog'));
    });
  });
  elements.pairwiseInfoDialogs.forEach((dialog) => {
    dialog.addEventListener('close', restorePairwiseInfoFocus);
    dialog.addEventListener('cancel', (event) => {
      event.preventDefault();
      closePairwiseInfoDialog(dialog);
    });
  });
  elements.scoreInfoDialogClose.addEventListener('click', closeScoreInfoDialog);
  elements.scoreInfoDialog.addEventListener('close', () => {
    state.scoreInfoReturnFocus?.focus();
    state.scoreInfoReturnFocus = null;
  });
  elements.buildDialog.addEventListener('close', () => {
    state.buildDialogReturnFocus?.focus();
    state.buildDialogReturnFocus = null;
  });
  elements.buildDialog.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeBuildDialog();
  });
  elements.dataDialog.addEventListener('close', () => {
    state.dataDialogReturnFocus?.focus();
    state.dataDialogReturnFocus = null;
  });
  elements.dataDialog.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeDataDialog();
  });
  elements.exportDialog.addEventListener('close', () => {
    state.exportDialogReturnFocus?.focus();
    state.exportDialogReturnFocus = null;
  });
  elements.exportDialog.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeExportDialog();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') hideScoreBandTouchTooltips();
    if (event.key === 'Escape') {
      const openPairwiseSelector = document.querySelector('[data-pairwise-selector-button][aria-expanded="true"]');
      if (openPairwiseSelector) {
        closePairwiseSelectorMenus();
        openPairwiseSelector.focus();
      }
    }
    if (event.key === 'Escape' && elements.buildDialog.open) {
      event.preventDefault();
      closeBuildDialog();
    }
    if (event.key === 'Escape' && elements.dataDialog.open) {
      event.preventDefault();
      closeDataDialog();
    }
    if (event.key === 'Escape' && elements.exportDialog.open) {
      event.preventDefault();
      closeExportDialog();
    }
    if (event.key === 'Escape' && elements.scoreInfoDialog.open) {
      event.preventDefault();
      closeScoreInfoDialog();
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
  state.pairwiseOverlapIndex = buildPairwiseOverlapIndex(state.catalog.pairwiseOverlap);
  state.livePrices = await loadLivePrices();
  renderBuildData();
  const sharedPortfolio = readPortfolioShareFromUrl();
  if (sharedPortfolio.status === 'valid') {
    state.portfolio = sharedPortfolio.portfolio;
    state.portfolioMode = sharedPortfolio.mode;
    state.valuationMode = sharedPortfolio.valuationMode;
    state.activeTab = 'portfolio';
    state.shareFeedback = sharedPortfolio.mode === 'percentage'
      ? 'share.privateLoaded'
      : 'share.loaded';
    savePortfolioState();
  } else {
    const savedPortfolio = loadPortfolioState();
    state.portfolio = savedPortfolio.portfolio;
    state.portfolioMode = savedPortfolio.mode;
    state.valuationMode = savedPortfolio.valuationMode;
    state.activeTab = loadActiveTab();
    if (sharedPortfolio.status === 'invalid') {
      state.shareFeedback = 'share.invalidKeptLocal';
    }
  }
  renderValuationModeControl();
  positionColorModeControl();
  updateInstallAction();
  state.compactExplorePreview = loadCompactExplorePreview();
  elements.compactExplorePreview.checked = state.compactExplorePreview;
  state.redundancyThresholds = loadRedundancyThresholdPreferences();
  elements.redundancyLowThreshold.value = state.redundancyThresholds.lowModerate;
  elements.redundancyHighThreshold.value = state.redundancyThresholds.moderateHigh;
  state.nearIdenticalThreshold = loadNearIdenticalThresholdPreference();
  elements.nearIdenticalThreshold.value = state.nearIdenticalThreshold;
  state.pairwiseHoldingsMaxCompanies = loadPairwiseHoldingsMaxCompaniesPreference();
  elements.pairwiseHoldingsMaxCompanies.value = state.pairwiseHoldingsMaxCompanies;
  state.topHoldingsMaximum = loadTopHoldingsMaximumPreference();
  elements.topHoldingsMaximum.value = state.topHoldingsMaximum;

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

  elements.companySearch = document.getElementById('company-search');
  elements.companySearchClear = document.getElementById('company-search-clear');
  elements.compactExploreSearch = document.getElementById('compact-explore-search');
  elements.companySearch.addEventListener('input', (event) => {
    state.companySearchTerm = event.target.value;
    updateCompanySearchClearButton();
    if (state.activeTab === 'aggregated') {
      renderCompanyList();
    }
  });
  elements.companySearchClear.addEventListener('click', (event) => {
    event.preventDefault();
    elements.companySearch.value = '';
    state.companySearchTerm = '';
    updateCompanySearchClearButton();
    if (state.activeTab === 'aggregated') {
      renderCompanyList();
    }
    elements.companySearch.focus();
  });
  updateCompanySearchClearButton();

  elements.catalogSearch.addEventListener('input', (event) => {
    state.searchTerm = event.target.value;
    updateSearchClearButton(elements.catalogSearch, elements.catalogSearchClear);
    renderCatalog();
  });
  elements.catalogSearchClear.addEventListener('click', (event) => {
    event.preventDefault();
    elements.catalogSearch.value = '';
    state.searchTerm = '';
    updateSearchClearButton(elements.catalogSearch, elements.catalogSearchClear);
    renderCatalog();
    elements.catalogSearch.focus();
  });

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
  elements.importValuation.addEventListener('change', () => {
    state.importValuationMode = elements.importValuation.value === 'imported' ? 'imported' : 'latest';
    refreshImportReviewTotals();
  });
  elements.portfolioValuation.addEventListener('change', () => {
    state.valuationMode = elements.portfolioValuation.value === 'imported'
      && hasCompleteImportedValuations(state.portfolio, state.livePrices)
      ? 'imported'
      : 'latest';
    savePortfolioState();
    renderAll();
  });
  elements.portfolioModeControl.addEventListener('change', (event) => {
    const modeInput = event.target.closest('[data-portfolio-mode]');
    if (modeInput) {
      updatePortfolioMode(modeInput.value);
    }
  });
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

  document.addEventListener('click', async (event) => {
    if (!event.target.closest('[data-pairwise-selector-group]')) closePairwiseSelectorMenus();

    const languageOption = event.target.closest('[data-locale]');
    if (languageOption) {
      toggleLanguageMenu(false);
      toggleColorModeMenu(false);
      if (languageOption.getAttribute('aria-checked') !== 'true') {
        await selectLocale(languageOption.dataset.locale);
        applyStaticTranslations();
        renderLanguageControl();
        renderNavigation();
        renderColorModeControl();
        renderAll();
        if (elements.importDialog.open) renderImportReview();
        setTab(state.activeTab);
      }
      return;
    }

    if (event.target.closest('[data-language-control]')) {
      if (event.target.closest('#language-button')) {
        toggleLanguageMenu();
        toggleColorModeMenu(false);
      }
      return;
    }

    const colorModeOption = event.target.closest('[data-color-mode-option]');
    if (colorModeOption) {
      setColorMode(colorModeOption.dataset.colorModeOption);
      toggleColorModeMenu(false);
      return;
    }

    if (event.target.closest('[data-color-mode-control]')) {
      if (event.target.closest('#color-mode-button')) {
        toggleColorModeMenu();
        toggleLanguageMenu(false);
      }
      return;
    }
    const pairwiseEtfOption = event.target.closest('[data-pairwise-etf-option]');
    if (pairwiseEtfOption) {
      const slotIndex = pairwiseEtfOption.dataset.pairwiseSelectorSlot === 'a' ? 0 : 1;
      state.pairwiseSelection[slotIndex] = pairwiseEtfOption.dataset.pairwiseEtfIsin;
      const slot = pairwiseEtfOption.dataset.pairwiseSelectorSlot;
      closePairwiseSelectorMenus();
      renderPairwiseOverlap();
      document.querySelector(`[data-pairwise-selector-button="${slot}"]`)?.focus();
      return;
    }
    const pairwiseSelectorButton = event.target.closest('[data-pairwise-selector-button]');
    if (pairwiseSelectorButton) {
      togglePairwiseSelectorMenu(pairwiseSelectorButton);
      toggleColorModeMenu(false);
      toggleLanguageMenu(false);
      return;
    }
    if (event.target.closest('#install-app-button')) {
      void promptToInstall();
      return;
    }
    toggleColorModeMenu(false);
    toggleLanguageMenu(false);

    const addButton = event.target.closest('[data-add-etf]');
    if (addButton) {
      addPosition(addButton.dataset.addEtf);
      return;
    }

    const shareButton = event.target.closest('[data-share-portfolio]');
    if (shareButton) {
      void sharePortfolio(shareButton.dataset.shareMode || 'full');
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
    const redundancyThreshold = event.target.closest('[data-redundancy-threshold]');
    if (redundancyThreshold) {
      const thresholds = validateRedundancyThresholds(
        elements.redundancyLowThreshold.value,
        elements.redundancyHighThreshold.value,
      );
      if (!thresholds) {
        elements.redundancyLowThreshold.value = state.redundancyThresholds.lowModerate;
        elements.redundancyHighThreshold.value = state.redundancyThresholds.moderateHigh;
        elements.redundancyThresholdError.hidden = false;
        elements.redundancyThresholdError.textContent = t('developer.invalidRedundancyThresholds');
        return;
      }

      state.redundancyThresholds = thresholds;
      saveRedundancyThresholdPreferences(thresholds);
      elements.redundancyThresholdError.hidden = true;
      renderRedundancyScore();
      return;
    }

    const nearIdenticalThreshold = event.target.closest('[data-near-identical-threshold]');
    if (nearIdenticalThreshold) {
      const threshold = validateNearIdenticalThreshold(elements.nearIdenticalThreshold.value);
      if (threshold === null) {
        elements.nearIdenticalThreshold.value = state.nearIdenticalThreshold;
        elements.nearIdenticalThresholdError.hidden = false;
        elements.nearIdenticalThresholdError.textContent = t('developer.invalidNearIdenticalThreshold');
        return;
      }

      state.nearIdenticalThreshold = threshold;
      saveNearIdenticalThresholdPreference(threshold);
      elements.nearIdenticalThresholdError.hidden = true;
      renderAll();
      return;
    }

    const pairwiseHoldingsMaximum = event.target.closest('[data-pairwise-holdings-max-companies]');
    if (pairwiseHoldingsMaximum) {
      const maximum = validatePairwiseHoldingsMaxCompanies(elements.pairwiseHoldingsMaxCompanies.value);
      if (maximum === null) {
        elements.pairwiseHoldingsMaxCompanies.value = state.pairwiseHoldingsMaxCompanies;
        elements.pairwiseHoldingsMaxCompaniesError.hidden = false;
        elements.pairwiseHoldingsMaxCompaniesError.textContent = t('developer.invalidPairwiseHoldingsMaximum');
        return;
      }

      state.pairwiseHoldingsMaxCompanies = maximum;
      savePairwiseHoldingsMaxCompaniesPreference(maximum);
      elements.pairwiseHoldingsMaxCompaniesError.hidden = true;
      renderPairwiseOverlap();
      return;
    }

    const topHoldingsMaximum = event.target.closest('[data-top-holdings-maximum]');
    if (topHoldingsMaximum) {
      const maximum = validateTopHoldingsMaximum(elements.topHoldingsMaximum.value);
      if (maximum === null) {
        elements.topHoldingsMaximum.value = state.topHoldingsMaximum;
        elements.topHoldingsMaximumError.hidden = false;
        elements.topHoldingsMaximumError.textContent = t('developer.invalidTopHoldingsMaximum');
        return;
      }

      state.topHoldingsMaximum = maximum;
      saveTopHoldingsMaximumPreference(maximum);
      elements.topHoldingsMaximumError.hidden = true;
      if (state.activeTab === 'aggregated') {
        renderCompanyList();
      }
      return;
    }

    const sharesInput = event.target.closest('[data-shares-input]');
    if (sharesInput) {
      const shares = Number(sharesInput.value || 0);
      if (
        state.portfolioMode !== 'percentage'
        && (!Number.isFinite(shares) || shares < 0 || !Number.isInteger(shares))
      ) {
        renderPositions();
        return;
      }
      updatePositionShares(sharesInput.dataset.sharesInput, shares);
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

window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
window.addEventListener('appinstalled', () => {
  deferredInstallPrompt = null;
  updateInstallAction();
});
window.addEventListener('DOMContentLoaded', () => {
  const isLocalDevelopment = ['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname);
  if ('serviceWorker' in navigator && !isLocalDevelopment) {
    navigator.serviceWorker.register('./sw.js').catch((error) => {
      console.warn('ETF Portfolio Lens service worker registration failed.', error);
    });
  } else if ('serviceWorker' in navigator && isLocalDevelopment) {
    void navigator.serviceWorker.getRegistrations().then((registrations) => {
      for (const registration of registrations) {
        void registration.unregister();
      }
    });
  }
  initializeLocalization().then(bootstrap).catch((error) => {
    document.body.innerHTML = `<pre style="white-space: pre-wrap; padding: 24px; color: #fff;">Failed to start ETF Portfolio Lens: ${error.message}</pre>`;
    console.error(error);
  });
});

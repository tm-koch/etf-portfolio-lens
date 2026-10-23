import json
import subprocess
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class WebRuntimeTests(unittest.TestCase):
    def test_top_holdings_maximum_preference_defaults_validates_and_persists(self) -> None:
        script = """
import {
  DEFAULT_TOP_HOLDINGS_MAXIMUM,
  TOP_HOLDINGS_MAXIMUM_STORAGE_KEY,
    getTopHoldingsDisplayLimit,
  loadTopHoldingsMaximum,
  saveTopHoldingsMaximum,
  validateTopHoldingsMaximum,
} from './web/explore-settings.js';

const values = new Map();
const storage = {
  getItem: (key) => values.get(key) ?? null,
  setItem: (key, value) => values.set(key, value),
};
const missing = loadTopHoldingsMaximum(storage);
const saved = saveTopHoldingsMaximum(35, storage);
const loaded = loadTopHoldingsMaximum(storage);
values.set(TOP_HOLDINGS_MAXIMUM_STORAGE_KEY, '"Infinity"');
const malformed = loadTopHoldingsMaximum(storage);
const unlimitedSaved = saveTopHoldingsMaximum(0, storage);
console.log(JSON.stringify({
  defaultValue: DEFAULT_TOP_HOLDINGS_MAXIMUM,
  missing,
  saved,
  loaded,
  malformed,
  unlimitedSaved,
  acceptsIntegerString: validateTopHoldingsMaximum('3'),
  acceptsUnlimited: validateTopHoldingsMaximum(0),
  rejects: [-1, 1.5, ' ', 'NaN'].map(validateTopHoldingsMaximum),
    limits: [
        getTopHoldingsDisplayLimit(5, 3),
        getTopHoldingsDisplayLimit(5, 5),
        getTopHoldingsDisplayLimit(5, 8),
        getTopHoldingsDisplayLimit(5, 0),
    ],
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["defaultValue"], 0)
        self.assertEqual(values["missing"], 0)
        self.assertTrue(values["saved"])
        self.assertEqual(values["loaded"], 35)
        self.assertEqual(values["malformed"], 0)
        self.assertTrue(values["unlimitedSaved"])
        self.assertEqual(values["acceptsIntegerString"], 3)
        self.assertEqual(values["acceptsUnlimited"], 0)
        self.assertEqual(values["rejects"], [None, None, None, None])
        self.assertEqual(values["limits"], [3, 5, 5, 5])

    def test_localization_resolves_locale_and_persists_runtime_switch(self) -> None:
        script = """
import { LOCALE_STORAGE_KEY, resolveLocale, selectLocale } from './web/localization.js';

const saved = new Map();
globalThis.document = { documentElement: { lang: 'en' } };
const i18n = {
  language: 'en-CH',
  async changeLanguage(locale) { this.language = locale; },
};
const results = {
  savedGerman: resolveLocale('de-CH', ['en-US']),
    savedPolish: resolveLocale('pl-PL', ['en-US']),
  browserGerman: resolveLocale(null, ['fr-FR', 'de-DE']),
  browserEnglish: resolveLocale(null, ['en-US']),
    browserPolish: resolveLocale(null, ['pl-PL']),
    browserPolishAfterUnsupported: resolveLocale(null, ['fr-FR', 'pl-PL']),
  unsupported: resolveLocale(null, ['fr-FR']),
};
await selectLocale('de-CH', {
  i18n,
  storage: { setItem: (key, value) => saved.set(key, value) },
});
await selectLocale('pl-PL', {
    i18n,
    storage: { setItem: (key, value) => saved.set(key, value) },
});
console.log(JSON.stringify({ ...results, language: document.documentElement.lang, saved: saved.get(LOCALE_STORAGE_KEY) }));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["savedGerman"], "de-CH")
        self.assertEqual(values["savedPolish"], "pl-PL")
        self.assertEqual(values["browserGerman"], "de-CH")
        self.assertEqual(values["browserEnglish"], "en-CH")
        self.assertEqual(values["browserPolish"], "pl-PL")
        self.assertEqual(values["browserPolishAfterUnsupported"], "pl-PL")
        self.assertEqual(values["unsupported"], "en-CH")
        self.assertEqual(values["language"], "pl-PL")
        self.assertEqual(values["saved"], "pl-PL")

    def test_language_selector_uses_supported_locales_and_local_runtime(
        self,
    ) -> None:
        index = (REPOSITORY_ROOT / "web" / "index.html").read_text(encoding="utf-8")
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")
        language_control = app[
            app.index("function renderLanguageControl()") : app.index(
                "function isStandaloneDisplayMode()"
            )
        ]
        styles = (REPOSITORY_ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        mobile_styles = styles[styles.rfind("@media (max-width: 760px)") :]

        self.assertIn('id="language-control"', index)
        self.assertIn('id="language-button"', index)
        self.assertIn('id="language-menu"', index)
        self.assertIn('aria-haspopup="menu"', index)
        self.assertIn('role="menuitemradio"', app)
        self.assertNotIn('data-lucide="chevron-down"', language_control)
        self.assertIn('data-locale="${language.locale}"', app)
        self.assertIn("locale: 'en-CH', code: 'EN', labelKey: 'language.english'", app)
        self.assertIn("locale: 'de-CH', code: 'DE', labelKey: 'language.german'", app)
        self.assertIn("locale: 'pl-PL', code: 'PL', labelKey: 'language.polish'", app)
        self.assertIn(
            '<span class="language-name">${t(selectedLanguage.labelKey)}</span>', app
        )
        self.assertIn(
            '<span class="language-code">${selectedLanguage.code}</span>', app
        )
        self.assertIn("<span>${t(language.labelKey)}</span>", app)
        self.assertIn("language: t(selectedLanguage.labelKey)", app)
        self.assertIn(
            ".language-button > .language-code {\n  display: none;\n}", styles
        )
        self.assertIn(".language-button > .language-name {", mobile_styles)
        self.assertIn(".language-button > .language-code {", mobile_styles)
        self.assertIn("display: inline;", mobile_styles)
        self.assertIn(
            ".language-button,\n  .color-mode-button {\n"
            "    box-sizing: border-box;\n"
            "    width: 43px;\n"
            "    height: 37px;\n"
            "    padding: 0;\n"
            "    justify-content: center;\n"
            "  }",
            mobile_styles,
        )
        self.assertNotIn('<select id="language-select"', index)
        self.assertIn("./vendor/i18next.min.js", index)
        self.assertIn("initializeLocalization().then(bootstrap)", app)
        self.assertIn("await selectLocale(languageOption.dataset.locale)", app)
        self.assertIn("renderLanguageControl();", app)

    def test_compare_rollup_and_portfolio_headings_match_redundancy_score_inset(
        self,
    ) -> None:
        styles = (REPOSITORY_ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        index = (REPOSITORY_ROOT / "web" / "index.html").read_text(encoding="utf-8")
        base_styles = styles[: styles.index("@media (max-width: 760px)")]

        self.assertIn(
            ".chart-card-head h3,\n.rollups-box > .subcard-heading h3,\n"
            "#portfolio-panel .portfolio-column > .subcard > .subcard-heading "
            'h3[data-i18n="ui.selectedPositions"] {\n'
            "  margin: 2px 0 0;\n}",
            base_styles,
        )
        self.assertIn('<div class="subcard stack rollups-box">', index)
        self.assertIn(
            '<h3 data-i18n="ui.selectedPositions">Selected positions</h3>',
            index,
        )
        self.assertIn(
            "  .aggregation-layout > .subcard > .subcard-heading h3 {\n"
            "    margin: 0;",
            styles,
        )

    def test_local_resources_initialize_and_switch_without_network_access(self) -> None:
        script = """
import fs from 'node:fs';
import './web/vendor/i18next.min.js';
import { initializeLocalization, selectLocale } from './web/localization.js';
const i18next = globalThis.i18next;

globalThis.document = { documentElement: { lang: 'en' } };
globalThis.fetch = async (url) => {
  const locale = new URL(url).pathname.split('/').at(-1).replace('.json', '');
  const body = fs.readFileSync(`web/locales/${locale}.json`, 'utf8');
  return { ok: true, json: async () => JSON.parse(body) };
};
const stored = new Map();
await initializeLocalization({
  i18n: i18next,
  storage: { getItem: () => null },
  browserLanguages: ['de-DE'],
});
const german = i18next.t('nav.home');
await selectLocale('en-CH', {
  i18n: i18next,
  storage: { setItem: (key, value) => stored.set(key, value) },
});
console.log(JSON.stringify({
  german,
  english: i18next.t('nav.home'),
  lang: document.documentElement.lang,
  selected: stored.get('etf-lens.locale.v1'),
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["german"], "Start")
        self.assertEqual(values["english"], "Home")
        self.assertEqual(values["lang"], "en-CH")
        self.assertEqual(values["selected"], "en-CH")

    def test_polish_plural_categories_use_raw_counts_and_formatted_display(
        self,
    ) -> None:
        script = """
import fs from 'node:fs';
import './web/vendor/i18next.min.js';
import { initializeLocalization } from './web/localization.js';

globalThis.document = { documentElement: { lang: 'en' } };
globalThis.fetch = async (url) => {
  const locale = new URL(url).pathname.split('/').at(-1).replace('.json', '');
  return { ok: true, json: async () => JSON.parse(fs.readFileSync(`web/locales/${locale}.json`, 'utf8')) };
};
const i18next = globalThis.i18next;
await initializeLocalization({ i18n: i18next, storage: { getItem: () => null }, browserLanguages: ['pl-PL'] });
const values = [1, 2, 5, 12, 22, 1.5].map((count) => ({
  count,
  message: i18next.t('explore.matchCount', {
    count,
    countDisplay: new Intl.NumberFormat('pl-PL').format(count),
  }),
}));
console.log(JSON.stringify(values));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        values = json.loads(result.stdout)

        self.assertEqual(
            [item["message"] for item in values],
            [
                "1 pasująca spółka.",
                "2 pasujące spółki.",
                "5 pasujących spółek.",
                "12 pasujących spółek.",
                "22 pasujące spółki.",
                "1,5 pasującej spółki.",
            ],
        )

    def test_chart_taxonomy_translation_is_display_only_and_has_fallbacks(self) -> None:
        script = r"""
import fs from 'node:fs';
import { translateTaxonomyLabel } from './web/taxonomy.js';
import { renderComparisonChart } from './web/charts.js';

const english = JSON.parse(fs.readFileSync('web/locales/en-CH.json', 'utf8')).translation;
const german = JSON.parse(fs.readFileSync('web/locales/de-CH.json', 'utf8')).translation;
const translate = (resources) => (key, values = {}) => String(resources[key] || key)
    .replace(/\{\{(\w+)\}\}/g, (_, name) => values[name] ?? '');
globalThis.Chart = class {
  static defaults = { plugins: { legend: { labels: { generateLabels: () => [] } } } };
    constructor(canvas, config) { this.data = config.data; this.config = config; }
  destroy() {}
};
const chartRef = { current: null };
const legendContainer = { innerHTML: '' };
const canonicalValues = new Map([['Health Care', 12.5]]);
renderComparisonChart(chartRef, {}, german['chart.titleSectors'], [{ label: 'CHSPI', values: canonicalValues }], ['Health Care'], {
  labelDisplayOverrides: new Map([['Health Care', translateTaxonomyLabel('Health Care', translate(german))]]),
  legendMode: 'labels',
    legendContainer,
    translate: translate(german),
    formatPercent: (value) => `${value.toFixed(1)}%`,
});
const tooltipCallbacks = chartRef.current.config.options.plugins.tooltip.callbacks;
console.log(JSON.stringify({
  germanSector: translateTaxonomyLabel('Health Care', translate(german)),
  germanRegion: translateTaxonomyLabel('North America', translate(german)),
  englishSector: translateTaxonomyLabel('Health Care', translate(english)),
  unknown: translateTaxonomyLabel('  New Category  ', translate(german)),
  displayedChartLabels: chartRef.current.data.labels,
    legend: legendContainer.innerHTML,
    tooltipTitle: tooltipCallbacks.title([{ dataset: { label: 'CHSPI' }, label: 'Gesundheitswesen' }]),
    tooltipShare: tooltipCallbacks.label({ raw: 12.5 }),
  chartValues: chartRef.current.data.datasets[0].data,
  canonicalLabels: [...canonicalValues.keys()],
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["germanSector"], "Gesundheitswesen")
        self.assertEqual(values["germanRegion"], "Nordamerika")
        self.assertEqual(values["englishSector"], "Health Care")
        self.assertEqual(values["unknown"], "  New Category  ")
        self.assertEqual(values["displayedChartLabels"], ["Gesundheitswesen"])
        self.assertIn("Gesundheitswesen", values["legend"])
        self.assertEqual(
            values["tooltipTitle"], ["ETF: CHSPI", "Sektoren: Gesundheitswesen"]
        )
        self.assertEqual(values["tooltipShare"], "Anteil: 12.5%")
        self.assertEqual(values["chartValues"], [12.5])
        self.assertEqual(values["canonicalLabels"], ["Health Care"])

    def test_locale_formatters_cover_counts_percentages_dates_and_currency_codes(
        self,
    ) -> None:
        script = """
import { formatBuildTimestamp, formatCount, formatCurrencyValue, formatPercent } from './web/formatting.js';
const values = {};
for (const locale of ['en-CH', 'de-CH', 'pl-PL']) {
  values[locale] = {
    count: formatCount(1234567, locale),
    percent: formatPercent(12.5, locale),
    currencies: Object.fromEntries(['CHF', 'EUR', 'USD'].map((currency) => [
      currency,
      formatCurrencyValue(1234.5, currency, locale),
    ])),
    timestamp: formatBuildTimestamp('2026-09-20T14:05:06Z', locale),
    date: formatBuildTimestamp('2026-09-20', locale),
  };
}
console.log(JSON.stringify(values));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["en-CH"]["count"], "1’234’567")
        self.assertEqual(values["de-CH"]["count"], "1’234’567")
        self.assertEqual(values["pl-PL"]["count"], "1\u00a0234\u00a0567")
        self.assertEqual(values["en-CH"]["percent"], "12.5%")
        self.assertEqual(values["de-CH"]["percent"], "12.5%")
        self.assertEqual(values["pl-PL"]["percent"], "12,5%")
        for locale in ("en-CH", "de-CH"):
            for currency in ("CHF", "EUR", "USD"):
                self.assertEqual(
                    values[locale]["currencies"][currency],
                    f"{currency}\u00a01’234.50",
                )
        for currency in ("CHF", "EUR", "USD"):
            self.assertEqual(
                values["pl-PL"]["currencies"][currency],
                f"1234,50\u00a0{currency}",
            )
        self.assertEqual(values["en-CH"]["date"], "20 Sept 2026")
        self.assertEqual(values["de-CH"]["date"], "20.09.2026")
        self.assertEqual(values["pl-PL"]["date"], "20 wrz 2026")
        self.assertIn("14:05:06 UTC", values["en-CH"]["timestamp"])
        self.assertIn("14:05:06 UTC", values["de-CH"]["timestamp"])
        self.assertIn("14:05:06 UTC", values["pl-PL"]["timestamp"])

    def test_share_input_handler_rejects_fractional_shares_only_in_shares_mode(
        self,
    ) -> None:
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")

        change_start = app.index("document.addEventListener('change', (event) => {")
        compare_start = app.index(
            "const compareToggle = event.target.closest('[data-compare-toggle]');",
            change_start,
        )
        handler = app[change_start:compare_start]

        self.assertIn("const shares = Number(sharesInput.value || 0);", handler)
        self.assertIn("state.portfolioMode !== 'percentage'", handler)
        self.assertIn("!Number.isInteger(shares)", handler)
        self.assertIn("renderPositions();\n        return;", handler)
        self.assertLess(
            handler.index("renderPositions();"), handler.index("updatePositionShares(")
        )
        self.assertIn(
            "updatePositionShares(sharesInput.dataset.sharesInput, shares);",
            handler,
        )

        render_start = app.index("function renderPositions()")
        render_end = app.index("function renderComparisonToolbar", render_start)
        render_positions = app[render_start:render_end]
        self.assertIn(
            "const shareInputValue = isPercentagePortfolio ? Number(position.shares).toFixed(1) : position.shares;",
            render_positions,
        )

    def test_allocation_mode_converts_weights_and_zeros_shares_without_prompt(
        self,
    ) -> None:
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")
        index = (REPOSITORY_ROOT / "web" / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="portfolio-mode-control"', index)
        self.assertIn('value="percentage" data-portfolio-mode', index)
        self.assertIn(
            'data-position-input-heading data-i18n="ui.shares">Shares</th>', index
        )

        mode_start = app.index("function updatePortfolioMode(mode)")
        mode_end = app.index("function getTotalShareUnits", mode_start)
        update_mode = app[mode_start:mode_end]
        self.assertIn(
            "const totalShareUnits = getTotalShareUnits(positions);", update_mode
        )
        self.assertIn(
            "shares: getPositionWeight(position, totalShareUnits)", update_mode
        )
        self.assertIn("state.portfolioMode = 'percentage';", update_mode)
        self.assertIn(
            "state.portfolio = state.portfolio.map((position) => ({ ...position, shares: 0 }));",
            update_mode,
        )
        self.assertNotIn("window.confirm(", update_mode)
        self.assertNotIn("state.portfolio = [];", update_mode)
        self.assertIn("state.portfolioMode = 'full';", update_mode)
        self.assertIn("savePortfolioState();", update_mode)

        self.assertIn(
            "elements.positionInputHeading.textContent = isPercentagePortfolio ? t('ui.allocationPercent') : t('ui.shares');",
            app,
        )
        self.assertIn(
            "? t('portfolio.percentageHint')",
            app,
        )
        self.assertIn("Number.isFinite(shares) ? Math.max(shares, 0) : 0", app)

    def test_percentage_position_rendering_skips_valuation_resolution(self) -> None:
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")

        render_start = app.index("function renderPositions()")
        render_end = app.index("function renderComparisonToolbar", render_start)
        render_positions = app[render_start:render_end]

        self.assertIn(
            "const valuation = isPercentagePortfolio ? null : getPositionValuation(position);",
            render_positions,
        )
        self.assertIn(
            "const valuationCells = isPercentagePortfolio\n        ? ''",
            render_positions,
        )
        self.assertIn(
            "const weight = getPositionWeight(position, totalShareUnits);",
            render_positions,
        )
        self.assertIn(
            "const totalShareUnits = getTotalShareUnits(positions);", render_positions
        )
        self.assertIn(
            "const valueChf = Number(getPositionValuation(position).valueChf);", app
        )
        self.assertIn(
            "if (state.portfolioMode === 'percentage') {\n    return Math.max(Number(position.shares) || 0, 0);",
            app,
        )

    def test_private_portfolio_hides_valuation_status_after_rerenders(self) -> None:
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")

        render_control_start = app.index("function renderValuationModeControl()")
        render_control_end = app.index(
            "function getTotalShareUnits", render_control_start
        )
        render_control = app[render_control_start:render_control_end]

        self.assertIn(
            "const isPercentagePortfolio = state.portfolioMode === 'percentage';",
            render_control,
        )
        self.assertIn(
            "elements.portfolioValuationStatus.hidden = isPercentagePortfolio;",
            render_control,
        )
        self.assertIn("renderValuationModeControl();\n  renderCatalog();", app)
        self.assertIn("state.portfolioMode = sharedPortfolio.mode;", app)

    def test_full_portfolio_status_preserves_live_and_imported_behavior(self) -> None:
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (REPOSITORY_ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            "state.valuationMode === 'imported' ? t('valuation.imported') : t('valuation.live')",
            app,
        )
        self.assertIn(
            "elements.portfolioValuationStatus.querySelector('.dot').hidden = state.valuationMode !== 'latest';",
            app,
        )
        self.assertIn("importedOption.hidden = !hasImportedValuations;", app)
        self.assertIn("importedOption.disabled = !hasImportedValuations;", app)
        self.assertIn("state.valuationMode = 'latest';\n    savePortfolioState();", app)
        self.assertIn("animation: live-status-pulse 2.8s ease-in-out infinite;", styles)

    def test_imported_valuation_requires_complete_position_coverage(self) -> None:
        script = """
import { hasCompleteImportedValuations } from './web/valuation.js';

const livePrices = {
  fx: { 'EUR/CHF': { rate: 0.96, status: 'available' } },
};
const cases = [
  hasCompleteImportedValuations([], livePrices),
  hasCompleteImportedValuations([{ isin: 'CHF_ETF', shares: 1, valueChf: 0 }], livePrices),
  hasCompleteImportedValuations([
    { isin: 'CHF_ETF', shares: 1, valueChf: 100 },
    { isin: 'MISSING', shares: 1 },
  ], livePrices),
  hasCompleteImportedValuations([{ isin: 'CHF_ETF', shares: 1, value: null, valueChf: null }], livePrices),
  hasCompleteImportedValuations([
    { isin: 'EUR_ETF', shares: 1, currency: 'EUR', value: 100 },
    { isin: 'CHF_ETF', shares: 1, valueChf: 0 },
  ], livePrices),
  hasCompleteImportedValuations([{ isin: 'EUR_ETF', shares: 1, currency: 'EUR', value: 100 }], { fx: {} }),
];
console.log(JSON.stringify(cases));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            json.loads(result.stdout), [False, True, False, False, True, False]
        )

    def test_redundancy_score_uses_lookthrough_contributions_and_etf_scale(
        self,
    ) -> None:
        script = """
import { calculateRedundancyScore } from './web/redundancy.js';

const calculate = (weights, hasUsableHoldings = weights.map(() => true)) =>
  calculateRedundancyScore(
    [{
      weight: 100,
      contributors: weights.map((weight, index) => ({ ticker: `ETF${index + 1}`, weight })),
    }],
    weights.map((weight, index) => ({ weight, hasUsableHoldings: hasUsableHoldings[index] })),
  );
const values = {
  one: calculate([100]),
  two: calculate([50, 50]),
  three: calculate([100 / 3, 100 / 3, 100 / 3]),
  four: calculate([25, 25, 25, 25]),
  unequal: calculate([70, 30]),
  missing: calculate([50, 50], [true, false]),
  zeroWeightMissing: calculate([100, 0], [true, false]),
  unique: calculateRedundancyScore(
    [{ weight: 100, contributors: [{ ticker: 'ETF1', weight: 100 }] }],
    [{ weight: 100, hasUsableHoldings: true }, { weight: 0, hasUsableHoldings: true }],
  ),
};
console.log(JSON.stringify(values));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual((values["one"]["score"], values["one"]["maximum"]), (0, 0))
        self.assertEqual((values["two"]["score"], values["two"]["maximum"]), (50, 50))
        self.assertAlmostEqual(values["three"]["score"], 200 / 3)
        self.assertAlmostEqual(values["three"]["maximum"], 200 / 3)
        self.assertEqual((values["four"]["score"], values["four"]["maximum"]), (75, 75))
        self.assertEqual(values["unequal"]["score"], 30)
        self.assertFalse(values["missing"]["available"])
        self.assertEqual(values["zeroWeightMissing"]["score"], 0)
        self.assertEqual(values["unique"]["score"], 0)

    def test_redundancy_threshold_boundaries_and_localized_percent_formatting(
        self,
    ) -> None:
        script = """
import { classifyRedundancyScore } from './web/redundancy.js';
import { formatPercent } from './web/formatting.js';

const locales = ['en-CH', 'de-CH', 'pl-PL'];
const formatted = Object.fromEntries(locales.map((locale) => [
  locale,
  {
    actual: formatPercent(12.5, locale),
    expected: new Intl.NumberFormat(locale, { style: 'percent', maximumFractionDigits: 1 }).format(0.125),
  },
]));
console.log(JSON.stringify({
  bands: [
    classifyRedundancyScore(9.9, 10, 25),
    classifyRedundancyScore(10, 10, 25),
    classifyRedundancyScore(24.9, 10, 25),
    classifyRedundancyScore(25, 10, 25),
  ],
  formatted,
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["bands"], ["low", "moderate", "moderate", "high"])
        for localized in values["formatted"].values():
            self.assertEqual(localized["actual"], localized["expected"])
            self.assertTrue(localized["actual"])

    def test_redundancy_threshold_validation(self) -> None:
        script = """
import { DEFAULT_REDUNDANCY_THRESHOLDS, validateRedundancyThresholds } from './web/redundancy.js';

console.log(JSON.stringify({
  defaults: DEFAULT_REDUNDANCY_THRESHOLDS,
  valid: validateRedundancyThresholds('10.5', '25'),
  minimum: validateRedundancyThresholds(0, 100),
  equal: validateRedundancyThresholds(10, 10),
  reversed: validateRedundancyThresholds(26, 25),
  empty: validateRedundancyThresholds('', 25),
  outOfRange: validateRedundancyThresholds(10, 100.1),
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["defaults"], {"lowModerate": 10, "moderateHigh": 25})
        self.assertEqual(values["valid"], {"lowModerate": 10.5, "moderateHigh": 25})
        self.assertEqual(values["minimum"], {"lowModerate": 0, "moderateHigh": 100})
        self.assertIsNone(values["equal"])
        self.assertIsNone(values["reversed"])
        self.assertIsNone(values["empty"])
        self.assertIsNone(values["outOfRange"])

    def test_redundancy_threshold_preferences_persist_and_fall_back_safely(
        self,
    ) -> None:
        script = """
import {
  REDUNDANCY_THRESHOLDS_STORAGE_KEY,
  loadRedundancyThresholds,
  saveRedundancyThresholds,
} from './web/redundancy.js';

const values = new Map();
const storage = {
  getItem: (key) => values.get(key) ?? null,
  setItem: (key, value) => values.set(key, value),
};
const defaults = loadRedundancyThresholds(storage);
const saved = saveRedundancyThresholds({ lowModerate: 12, moderateHigh: 30 }, storage);
const restored = loadRedundancyThresholds(storage);
const rejected = saveRedundancyThresholds({ lowModerate: 30, moderateHigh: 12 }, storage);
values.set(REDUNDANCY_THRESHOLDS_STORAGE_KEY, '{');
const corrupt = loadRedundancyThresholds(storage);
const unavailable = loadRedundancyThresholds({ getItem() { throw new Error('blocked'); } });
console.log(JSON.stringify({ defaults, saved, restored, rejected, corrupt, unavailable }));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["defaults"], {"lowModerate": 10, "moderateHigh": 25})
        self.assertTrue(values["saved"])
        self.assertEqual(values["restored"], {"lowModerate": 12, "moderateHigh": 30})
        self.assertFalse(values["rejected"])
        self.assertEqual(values["corrupt"], {"lowModerate": 10, "moderateHigh": 25})
        self.assertEqual(values["unavailable"], {"lowModerate": 10, "moderateHigh": 25})

    def test_near_identical_threshold_defaults_validates_and_persists(self) -> None:
        script = """
import {
    DEFAULT_NEAR_IDENTICAL_THRESHOLD,
    NEAR_IDENTICAL_THRESHOLD_STORAGE_KEY,
    loadNearIdenticalThreshold,
    saveNearIdenticalThreshold,
    validateNearIdenticalThreshold,
} from './web/redundancy.js';

const values = new Map();
const storage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
};
const initial = loadNearIdenticalThreshold(storage);
const saved = saveNearIdenticalThreshold('92.5', storage);
const restored = loadNearIdenticalThreshold(storage);
const rejected = saveNearIdenticalThreshold(101, storage);
values.set(NEAR_IDENTICAL_THRESHOLD_STORAGE_KEY, 'null');
const corrupt = loadNearIdenticalThreshold(storage);
const invalid = [validateNearIdenticalThreshold(''), validateNearIdenticalThreshold(-1), validateNearIdenticalThreshold(Infinity)];
console.log(JSON.stringify({ default: DEFAULT_NEAR_IDENTICAL_THRESHOLD, initial, saved, restored, rejected, corrupt, invalid }));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["default"], 90)
        self.assertEqual(values["initial"], 90)
        self.assertTrue(values["saved"])
        self.assertEqual(values["restored"], 92.5)
        self.assertFalse(values["rejected"])
        self.assertEqual(values["corrupt"], 90)
        self.assertEqual(values["invalid"], [None, None, None])

    def test_pairwise_overlap_index_supports_unordered_pairs_and_legacy_catalogs(
        self,
    ) -> None:
        script = """
import { buildPairwiseOverlapIndex, getPairwiseOverlap } from './web/pairwise-overlap.js';

const index = buildPairwiseOverlapIndex({
    version: 1,
    pairs: [
        { isinA: 'AAA', isinB: 'BBB', overlapPct: 91, available: true },
        { isinA: 'CCC', isinB: 'DDD', overlapPct: null, available: false },
        { isinA: 'BAD', isinB: 'PAIR', overlapPct: 101, available: true },
    ],
});
console.log(JSON.stringify({
    reversed: getPairwiseOverlap(index, 'BBB', 'AAA'),
    unavailable: getPairwiseOverlap(index, 'DDD', 'CCC'),
    bad: getPairwiseOverlap(index, 'BAD', 'PAIR'),
    same: getPairwiseOverlap(index, 'AAA', 'AAA'),
    legacySize: buildPairwiseOverlapIndex(undefined).size,
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["reversed"]["overlapPct"], 91)
        self.assertFalse(values["unavailable"]["available"])
        self.assertIsNone(values["bad"])
        self.assertIsNone(values["same"])
        self.assertEqual(values["legacySize"], 0)

    def test_pairwise_matrix_uses_selection_order_and_inclusive_threshold(self) -> None:
        script = """
import { buildPairwiseMatrix, buildPairwiseOverlapIndex } from './web/pairwise-overlap.js';

const index = buildPairwiseOverlapIndex({
    version: 1,
    pairs: [{ isinA: 'A', isinB: 'B', overlapPct: 90, coveragePctA: 95, coveragePctB: 92, available: true }],
});
const positions = ['B', 'A', 'C'].map((isin) => ({
    isin,
    entry: { ticker: isin, name: `Fund ${isin}` },
}));
const atThreshold = buildPairwiseMatrix(positions, index, 90);
const aboveThreshold = buildPairwiseMatrix(positions, index, 90.1);
console.log(JSON.stringify({
    order: atThreshold.map((row) => row.product.isin),
    diagonal: atThreshold[0].cells[0].type,
    upper: atThreshold[0].cells[2].type,
    near: atThreshold[1].cells[0].nearIdentical,
    below: aboveThreshold[1].cells[0].nearIdentical,
    missing: atThreshold[2].cells[0].type,
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["order"], ["B", "A", "C"])
        self.assertEqual(values["diagonal"], "diagonal")
        self.assertEqual(values["upper"], "empty")
        self.assertTrue(values["near"])
        self.assertFalse(values["below"])
        self.assertEqual(values["missing"], "unavailable")

    def test_restored_portfolio_reconciles_valuation_before_render(self) -> None:
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")
        bootstrap_start = app.index("async function bootstrap()")
        restore_start = app.index(
            "const sharedPortfolio = readPortfolioShareFromUrl();", bootstrap_start
        )
        control_render = app.index("renderValuationModeControl();", restore_start)
        portfolio_render = app.index("renderAll();", control_render)

        self.assertIn(
            "state.valuationMode = sharedPortfolio.valuationMode;",
            app[restore_start:control_render],
        )
        self.assertIn(
            "state.valuationMode = savedPortfolio.valuationMode;",
            app[restore_start:control_render],
        )
        self.assertLess(control_render, portfolio_render)

    def test_share_links_preserve_compatibility_and_private_payload_boundaries(
        self,
    ) -> None:
        script = """
import { decodePortfolioShare, encodePortfolioShare, encodePrivatePortfolioShare } from './web/share.js';

const encodePayload = (payload) => Buffer.from(JSON.stringify(payload)).toString('base64url');
const legacy = decodePortfolioShare(encodePayload({
  version: 1,
  portfolio: [{ isin: 'ch0237935652', shares: 2 }],
}));
const current = decodePortfolioShare(encodePortfolioShare([{
  isin: 'IE00B44Z5B48',
  shares: 1,
  valuationMode: 'latest',
  price: 265.35,
  currency: 'CHF',
  value: 265.35,
  valueChf: 265.35,
}]));
const nullValues = decodePortfolioShare(encodePayload({
    version: 2,
    valuationMode: 'imported',
    portfolio: [{ isin: 'IE00B44Z5B48', shares: 1, price: null, currency: 'CHF', value: null, valueChf: null }],
}));
const privateToken = encodePrivatePortfolioShare(
  [{ isin: 'CH0237935652', shares: 2 }, { isin: 'IE00B44Z5B48', shares: 1 }],
  (positions) => positions.reduce((sum, position) => sum + position.shares, 0),
  (position, total) => (position.shares / total) * 100,
);
const privatePayload = JSON.parse(Buffer.from(privateToken, 'base64url').toString('utf8'));
console.log(JSON.stringify({ legacy, current, nullValues, privatePayload, decodedPrivate: decodePortfolioShare(privateToken) }));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)

        self.assertEqual(
            values["legacy"],
            {
                "status": "valid",
                "mode": "full",
                "portfolio": [{"isin": "CH0237935652", "shares": 2}],
            },
        )
        self.assertEqual(values["current"]["status"], "valid")
        self.assertEqual(values["current"]["portfolio"][0]["valuationMode"], "latest")
        self.assertEqual(
            set(values["nullValues"]["portfolio"][0]),
            {"isin", "shares", "currency"},
        )
        self.assertEqual(values["privatePayload"]["version"], 2)
        self.assertEqual(values["privatePayload"]["mode"], "percentage")
        self.assertEqual(
            set(values["privatePayload"]["portfolio"][0]),
            {"isin", "shares"},
        )
        private_shares = [
            position["shares"] for position in values["decodedPrivate"]["portfolio"]
        ]
        self.assertAlmostEqual(private_shares[0], 200 / 3)
        self.assertAlmostEqual(private_shares[1], 100 / 3)

    def test_effective_valuation_covers_live_fallback_and_unavailable_states(
        self,
    ) -> None:
        script = """
import { getEffectiveValuation } from './web/valuation.js';

const livePrices = {
  schema_version: 1,
  generated_at: '2026-08-29T21:00:00Z',
  quotes: {
    CHF_ETF: { price: 101.25, currency: 'CHF', status: 'available', quoted_at: '2026-08-29T17:00:00Z' },
    EUR_ETF: { price: 50, currency: 'EUR', status: 'available', quoted_at: '2026-08-29T17:00:00Z' },
  },
  fx: { 'EUR/CHF': { rate: 0.96, status: 'available', quoted_at: '2026-08-29' } },
};

const cases = [
  getEffectiveValuation({ isin: 'CHF_ETF', shares: 2 }, livePrices),
  getEffectiveValuation({ isin: 'EUR_ETF', shares: 3 }, livePrices),
  getEffectiveValuation({ isin: 'CHF_ETF', shares: 2, price: 90, valueChf: 180, valuationMode: 'imported' }, livePrices),
  getEffectiveValuation({ isin: 'CHF_ETF', shares: 2, price: 90, valueChf: 180 }, livePrices, 'imported'),
  getEffectiveValuation({ isin: 'EUR_ETF', shares: 3, price: 50, currency: 'EUR', value: 150 }, livePrices, 'imported'),
  getEffectiveValuation({ isin: 'EUR_ETF', shares: 3, valueChf: 140 }, { ...livePrices, fx: {} }),
  getEffectiveValuation({ isin: 'MISSING', shares: 1 }, livePrices),
];
console.log(JSON.stringify(cases));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        values = json.loads(result.stdout)
        self.assertEqual(
            [value["status"] for value in values],
            [
                "live",
                "live",
                "fallback",
                "imported",
                "imported",
                "fallback",
                "unavailable",
            ],
        )
        self.assertAlmostEqual(values[0]["valueChf"], 202.5)
        self.assertAlmostEqual(values[1]["valueChf"], 144)
        self.assertEqual(values[2]["valueChf"], 180)
        self.assertEqual(values[3]["valueChf"], 180)
        self.assertEqual(values[4]["valueChf"], 144)
        self.assertEqual(values[5]["valueChf"], 140)
        self.assertIsNone(values[6]["valueChf"])


if __name__ == "__main__":
    unittest.main()

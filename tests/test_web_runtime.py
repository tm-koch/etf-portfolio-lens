import json
import subprocess
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class WebRuntimeTests(unittest.TestCase):
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
  browserGerman: resolveLocale(null, ['fr-FR', 'de-DE']),
  browserEnglish: resolveLocale(null, ['en-US']),
  unsupported: resolveLocale(null, ['fr-FR']),
};
await selectLocale('de-CH', {
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
        )
        values = json.loads(result.stdout)

        self.assertEqual(values["savedGerman"], "de-CH")
        self.assertEqual(values["browserGerman"], "de-CH")
        self.assertEqual(values["browserEnglish"], "en-CH")
        self.assertEqual(values["unsupported"], "en-CH")
        self.assertEqual(values["language"], "de-CH")
        self.assertEqual(values["saved"], "de-CH")

    def test_language_selector_uses_supported_swiss_locales_and_local_runtime(
        self,
    ) -> None:
        index = (REPOSITORY_ROOT / "web" / "index.html").read_text(encoding="utf-8")
        app = (REPOSITORY_ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn('id="language-control"', index)
        self.assertIn('id="language-button"', index)
        self.assertIn('id="language-menu"', index)
        self.assertIn('aria-haspopup="menu"', index)
        self.assertIn('role="menuitemradio"', app)
        self.assertNotIn('data-lucide="chevron-down"', app)
        self.assertIn('data-locale="${language.locale}"', app)
        self.assertIn("locale: 'en-CH'", app)
        self.assertIn("locale: 'de-CH'", app)
        self.assertNotIn('<select id="language-select"', index)
        self.assertIn("./vendor/i18next.min.js", index)
        self.assertIn("initializeLocalization().then(bootstrap)", app)
        self.assertIn("await selectLocale(languageOption.dataset.locale)", app)
        self.assertIn("renderLanguageControl();", app)

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
for (const locale of ['en-CH', 'de-CH']) {
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
        self.assertEqual(values["en-CH"]["percent"], "12.5%")
        self.assertEqual(values["de-CH"]["percent"], "12.5%")
        for locale in ("en-CH", "de-CH"):
            for currency in ("CHF", "EUR", "USD"):
                self.assertEqual(
                    values[locale]["currencies"][currency],
                    f"{currency}\u00a01’234.50",
                )
        self.assertEqual(values["en-CH"]["date"], "20 Sept 2026")
        self.assertEqual(values["de-CH"]["date"], "20.09.2026")
        self.assertIn("14:05:06 UTC", values["en-CH"]["timestamp"])
        self.assertIn("14:05:06 UTC", values["de-CH"]["timestamp"])

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
        self.assertIn("animation: live-status-pulse 2.8s ease-in-out infinite;", styles)

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
const privateToken = encodePrivatePortfolioShare(
  [{ isin: 'CH0237935652', shares: 2 }, { isin: 'IE00B44Z5B48', shares: 1 }],
  (positions) => positions.reduce((sum, position) => sum + position.shares, 0),
  (position, total) => (position.shares / total) * 100,
);
const privatePayload = JSON.parse(Buffer.from(privateToken, 'base64url').toString('utf8'));
console.log(JSON.stringify({ legacy, current, privatePayload, decodedPrivate: decodePortfolioShare(privateToken) }));
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

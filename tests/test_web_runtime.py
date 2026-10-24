import json
import subprocess
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class WebRuntimeTests(unittest.TestCase):
    def test_report_matrix_columns_are_partitioned_for_readable_continuation(
        self,
    ) -> None:
        script = """
import { partitionReportColumns } from './web/pdf-report-renderer.js';

const columns = Array.from({ length: 19 }, (_, index) => ({ ticker: `ETF${index + 1}` }));
const panels = partitionReportColumns(columns);
console.log(JSON.stringify({
  sizes: panels.map((panel) => panel.columns.length),
  ranges: panels.map((panel) => [panel.start, panel.end]),
  preservesOrder: panels.flatMap((panel) => panel.columns).every((column, index) => column === columns[index]),
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

        self.assertEqual(values["sizes"], [8, 8, 3])
        self.assertEqual(values["ranges"], [[0, 8], [8, 16], [16, 19]])
        self.assertTrue(values["preservesOrder"])

    def test_opening_export_dialog_resets_only_export_session_controls(self) -> None:
        script = """
import { openReportDialog } from './web/export-view.js';

const appState = {
  portfolio: [{ isin: 'IE0001', shares: 8 }],
  valuationMode: 'imported',
  colorMode: 'dark',
};
const initialAppState = structuredClone(appState);
const dialog = {
  open: false,
  showModal() { this.open = true; },
};
const scopeControls = [
    { value: 'portfolio', checked: false },
    { value: 'catalog', checked: true },
];
const allocationOnlyControl = { checked: true };
const generationStatus = { textContent: 'Previous status', hidden: false };
openReportDialog({ dialog, scopeControls, allocationOnlyControl, generationStatus });
console.log(JSON.stringify({
  opened: dialog.open,
    selectedScope: scopeControls.find((control) => control.checked)?.value,
  allocationOnly: allocationOnlyControl.checked,
  statusText: generationStatus.textContent,
  statusHidden: generationStatus.hidden,
  appStateUnchanged: JSON.stringify(appState) === JSON.stringify(initialAppState),
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

        self.assertTrue(values["opened"])
        self.assertEqual(values["selectedScope"], "portfolio")
        self.assertFalse(values["allocationOnly"])
        self.assertEqual(values["statusText"], "")
        self.assertTrue(values["statusHidden"])
        self.assertTrue(values["appStateUnchanged"])

    def test_top_holdings_maximum_preference_defaults_validates_and_persists(
        self,
    ) -> None:
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

    def test_report_rollups_use_captured_weights_without_share_totals(self) -> None:
        script = """
import { aggregatePortfolioRollups } from './web/report-data.js';

const positions = [
    {
        weightPct: 60,
        snapshot: { aggregates: {
            sector_weights: [{ name: 'Technology', weight_pct: 50 }],
            region_weights: [{ name: 'North America', weight_pct: 100 }],
            currency_weights: [{ name: 'USD', weight_pct: 80 }, { name: 'CHF', weight_pct: 20 }],
        } },
    },
    {
        weightPct: 40,
        snapshot: { aggregates: {
            sector_weights: [{ name: 'Healthcare', weight_pct: 100 }],
            region_weights: [{ name: 'Europe', weight_pct: 100 }],
            currency_weights: [{ name: 'CHF', weight_pct: 100 }],
        } },
    },
];
const rollups = aggregatePortfolioRollups(positions, {
    getTotalShareUnits: () => { throw new Error('Captured weights must not require share totals'); },
    getPositionWeight: () => { throw new Error('Captured weights must be used directly'); },
});
console.log(JSON.stringify(Object.fromEntries(
    Object.entries(rollups).map(([key, values]) => [key, Object.fromEntries(values)])
)));
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

        self.assertEqual(values["sector"], {"Technology": 30, "Healthcare": 40})
        self.assertEqual(values["region"], {"North America": 60, "Europe": 40})
        self.assertEqual(values["currency"], {"USD": 48, "CHF": 52})

    def test_report_snapshot_separates_catalog_listing_from_portfolio(self) -> None:
        script = """
import { buildReportSnapshot } from './web/report-data.js';

const heldPosition = {
    isin: 'IE0001',
    shares: 12,
    entry: { isin: 'IE0001', ticker: 'HELD' },
    snapshot: { holdings: [{ security: { name: 'Example Co' } }] },
    valuation: { valueChf: 240 },
};
const portfolioPositions = [heldPosition];
const catalogEtfs = [heldPosition.entry, { isin: 'IE0002', ticker: 'UNHELD' }];
const common = {
    portfolioPositions,
    catalogEtfs,
    catalogTimestamp: '2026-10-20',
    portfolioMode: 'full',
    valuationMode: 'latest',
    locale: 'pl-PL',
    buildInfo: { source: { commit: 'abcdef1234567890' }, data: { timestamp: '2026-10-19' } },
    livePrices: { generated_at: '2026-10-20T18:21:37Z' },
    generatedAt: '2026-10-23T12:00:00Z',
};
const portfolio = buildReportSnapshot(common);
const catalog = buildReportSnapshot({ ...common, scope: 'catalog' });
heldPosition.shares = 99;
console.log(JSON.stringify({
    portfolioCount: portfolio.etfs.length,
    catalogCount: catalog.etfs.length,
    analyticsPositionCount: catalog.portfolioPositions.length,
    heldTicker: catalog.etfs[0].portfolioPosition.entry.ticker,
    unheldPosition: catalog.etfs[1].portfolioPosition,
    capturedShares: catalog.portfolioPositions[0].shares,
    locale: catalog.locale,
    provenance: catalog.provenance,
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

        self.assertEqual(values["portfolioCount"], 1)
        self.assertEqual(values["catalogCount"], 2)
        self.assertEqual(values["analyticsPositionCount"], 1)
        self.assertEqual(values["heldTicker"], "HELD")
        self.assertIsNone(values["unheldPosition"])
        self.assertEqual(values["capturedShares"], 12)
        self.assertEqual(values["locale"], "pl-PL")
        self.assertEqual(
            values["provenance"],
            {
                "buildId": "abcdef1",
                "snapshotTimestamp": "2026-10-19",
                "livePricesTimestamp": "2026-10-20T18:21:37Z",
            },
        )

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
            "    height: var(--utility-control-height);\n"
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

    def test_wide_position_metric_columns_use_shared_tracks(self) -> None:
        styles = (REPOSITORY_ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        wide_styles = styles[
            styles.index("@media (min-width: 761px)") : styles.index(
                ".positions-table {"
            )
        ]
        mobile_styles = styles[styles.index("@media (max-width: 760px)") :]

        self.assertIn(
            ".positions-table .position-row {\n"
            "    display: grid;\n"
            "    grid-template-columns: minmax(0, 1fr) 7rem 7rem 4rem auto;",
            wide_styles,
        )
        self.assertIn(
            ".positions-table .position-row--percentage {\n"
            "    grid-template-columns: minmax(0, 1fr) auto auto;",
            wide_styles,
        )
        self.assertIn(
            "  .position-row {\n"
            "    display: grid;\n"
            "    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto;",
            mobile_styles,
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

    def test_pdf_portfolio_link_preserves_share_modes_and_omits_empty_portfolios(
        self,
    ) -> None:
        script = """
import { buildPortfolioShareUrl, decodePortfolioShare } from './web/share.js';
import { renderReportDocument } from './web/pdf-report-renderer.js';

const positions = [{ isin: 'IE0001', shares: 2 }, { isin: 'CH0002', shares: 1 }];
const currentUrl = 'https://app.test/web/?language=en#old';
const totalShares = (items) => items.reduce((sum, item) => sum + item.shares, 0);
const positionWeight = (item, total) => (item.shares / total) * 100;
const fullUrl = buildPortfolioShareUrl(positions, 'full', { currentUrl, valuationMode: 'imported' });
const privateUrl = buildPortfolioShareUrl(positions, 'percentage', {
    currentUrl,
    getTotalShareUnits: totalShares,
    getPositionWeight: positionWeight,
});
const emptyUrl = buildPortfolioShareUrl([], 'full', { currentUrl });
const annotations = [];
const labels = [];
function render(url) {
    const pdf = {
        text: (value) => labels.push(value),
        link: (...args) => annotations.push(args),
        getTextWidth: (value) => value.length * 0.5,
        splitTextToSize: (value) => [value],
        lastAutoTable: null,
    };
    for (const method of ['addPage', 'setFont', 'setFontSize', 'setTextColor', 'setDrawColor', 'setLineWidth', 'line', 'setFillColor', 'roundedRect']) {
        pdf[method] = () => {};
    }
    renderReportDocument({
        pdf,
        autoTable: (document, options) => { document.lastAutoTable = { finalY: options.startY + 8 }; },
            snapshot: { generatedAt: '2026-10-23T12:00:00Z', provenance: {}, portfolioMode: 'full', etfs: [] },
        analytics: {
            summary: {}, rollups: {}, redundancy: {}, diversification: {}, charts: {},
            etfColumns: [], companies: [], pairwiseHeatmap: [],
        },
        portfolioShareUrl: url,
        t: (key) => key === 'export.openPortfolio' ? 'Open this portfolio online' : key,
        formatCount: String,
        formatDecimal: String,
        formatPercent: (value) => `${value}%`,
        formatCurrency: String,
        translateTaxonomy: (value) => value,
    });
}
render(fullUrl);
render(privateUrl);
render(emptyUrl);
console.log(JSON.stringify({
    fullUrl,
    privateUrl,
    full: decodePortfolioShare(new URL(fullUrl).hash.slice('#portfolio='.length)),
    private: decodePortfolioShare(new URL(privateUrl).hash.slice('#portfolio='.length)),
    emptyUrl,
    annotations: annotations.map(([, , , , options]) => options.url),
    linkLabels: labels.filter((value) => value === 'Open this portfolio online'),
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

        self.assertEqual(values["full"]["mode"], "full")
        self.assertEqual(
            [item["shares"] for item in values["full"]["portfolio"]], [2, 1]
        )
        self.assertEqual(values["private"]["mode"], "percentage")
        self.assertAlmostEqual(values["private"]["portfolio"][0]["shares"], 200 / 3)
        self.assertAlmostEqual(values["private"]["portfolio"][1]["shares"], 100 / 3)
        self.assertIsNone(values["emptyUrl"])
        self.assertEqual(
            values["annotations"], [values["fullUrl"], values["privateUrl"]]
        )
        self.assertEqual(values["linkLabels"], ["Open this portfolio online"] * 2)

    def test_report_analytics_limits_ranked_matrix_to_top_twenty_portfolio_etfs(
        self,
    ) -> None:
        script = """
import { buildReportAnalytics, buildReportSnapshot } from './web/report-data.js';

const snapshot = buildReportSnapshot({
  scope: 'catalog',
    portfolioPositions: [
        { isin: 'IE0001', entry: { ticker: 'HELD', name: 'Held ETF' } },
        { isin: 'IE0002', entry: { ticker: 'SECOND', name: 'Second ETF' } },
        { isin: 'IE0003', entry: { ticker: 'THIRD', name: 'Third ETF' } },
        { isin: 'IE0004', entry: { ticker: 'FOURTH', name: 'Fourth ETF' } },
    ],
  catalogEtfs: [
    { isin: 'IE0001', ticker: 'HELD', name: 'Held ETF' },
        { isin: 'IE0005', ticker: 'UNHELD', name: 'Unheld ETF' },
  ],
});
const rankedCompanies = Array.from({ length: 25 }, (_, index) => ({
  key: `company-${index}`,
  name: `Company ${index}`,
  weight: 25 - index,
    contributors: index === 0 ? [
        { ticker: 'HELD', weight: 12.5 },
        { ticker: 'SECOND', weight: 7.5 },
        { ticker: 'THIRD', weight: 5 },
    ] : [],
}));
const analytics = buildReportAnalytics({
  snapshot,
  rankedCompanies,
  summary: { positions: 1 },
  rollups: { sector: { Technology: 25 } },
  redundancy: { available: false },
  charts: { sector: { labels: ['Technology'], series: [] } },
  pairwiseHeatmap: [{ product: { ticker: 'HELD' }, cells: [{ type: 'diagonal' }] }],
});
const zeroTotal = buildReportAnalytics({
    snapshot,
    rankedCompanies: [{
        key: 'zero',
        name: 'Zero company',
        weight: 0,
        contributors: [{ ticker: 'HELD', weight: 0 }],
    }],
}).companies[0];
console.log(JSON.stringify({
  columnTickers: analytics.etfColumns.map((column) => column.ticker),
  count: analytics.companies.length,
  first: analytics.companies[0],
  lastRank: analytics.companies.at(-1).rank,
  preservedSummary: analytics.summary,
  empty: buildReportAnalytics({ snapshot }).companies,
    zeroTotal,
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

        self.assertEqual(values["columnTickers"], ["HELD", "SECOND", "THIRD", "FOURTH"])
        self.assertEqual(values["count"], 20)
        self.assertEqual(values["first"]["rank"], 1)
        self.assertEqual(values["first"]["name"], "Company 0")
        self.assertEqual(values["first"]["totalContribution"], 25)
        self.assertEqual(
            values["first"]["contributions"],
            [
                {"ticker": "HELD", "value": 50},
                {"ticker": "SECOND", "value": 30},
                {"ticker": "THIRD", "value": 20},
                {"ticker": "FOURTH", "value": None},
            ],
        )
        self.assertEqual(
            sum(item["value"] for item in values["first"]["contributions"] if item["value"] is not None),
            100,
        )
        self.assertEqual(values["zeroTotal"]["contributions"][0]["value"], 0)
        self.assertEqual(values["lastRank"], 20)
        self.assertEqual(values["preservedSummary"], {"positions": 1})
        self.assertEqual(values["empty"], [])

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

    def test_pdf_options_are_landscape_and_stamp_localized_generated_line_on_every_page(
        self,
    ) -> None:
        script = """
import { createReportPdfOptions, stampReportPdf } from './web/pdf-export.js';

const calls = [];
const pdf = {
    internal: { getNumberOfPages: () => 2, pageSize: { getWidth: () => 297, getHeight: () => 210 } },
  setProperties: (value) => calls.push(['properties', value]),
  setPage: (value) => calls.push(['page', value]),
  setFont: () => {},
  setFontSize: () => {},
  setTextColor: () => {},
  setDrawColor: () => {},
  line: (...value) => calls.push(['line', ...value]),
  splitTextToSize: (value) => [value],
    text: (value, x, y, options) => calls.push(['text', Array.isArray(value) ? value.join(' ') : value, x, y, options]),
  getTextWidth: (value) => value.length * 0.5,
  link: (...value) => calls.push(['link', ...value]),
};
const snapshot = {
  generatedAt: '2026-10-23T12:00:00Z',
  provenance: { buildId: 'abcdef1', snapshotTimestamp: '2026-10-22', livePricesTimestamp: null },
};
const labels = {
  'export.generatedAt': 'Generated',
  'export.buildIdentifier': 'Build',
  'export.etfSnapshot': 'Snapshot',
  'export.livePrices': 'Live prices',
  'common.unavailable': 'Unavailable',
};
const t = (key, values = {}) => key === 'export.page'
    ? `Page ${values.page} of ${values.total}`
    : labels[key];
for (const generatedLabel of ['Generated', 'Erstellt', 'Wygenerowano']) {
    labels['export.generatedAt'] = generatedLabel;
    stampReportPdf(pdf, { snapshot, t, formatTimestamp: () => '24 Oct 2026, 11:24:30 UTC' });
}
const options = createReportPdfOptions(snapshot);
console.log(JSON.stringify({
  pageFormat: options.jsPDF,
  filename: options.filename,
  pages: calls.filter(([type]) => type === 'page').map(([, page]) => page),
        text: calls.filter(([type, text]) => type === 'text' && text.startsWith('ETF Portfolio Lens | ')).map(([, text]) => text),
    pageNumbers: calls.filter(([type, text]) => type === 'text' && text.startsWith('Page ')).map(([, text, x, y, options]) => ({ text, x, y, align: options.align })),
        links: calls.filter(([type]) => type === 'link').map(([, x, y, width, height, options]) => ({
            x, y, width, height, url: options.url,
        })),
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

        self.assertEqual(values["pageFormat"]["format"], "a4")
        self.assertEqual(values["pageFormat"]["orientation"], "landscape")
        self.assertEqual(values["filename"], "etf-portfolio-lens-report-2026-10-23.pdf")
        self.assertEqual(values["pages"], [1, 2] * 3)
        self.assertEqual(
            values["pageNumbers"],
            [
                {"text": "Page 1 of 2", "x": 289, "y": 202, "align": "right"},
                {"text": "Page 2 of 2", "x": 289, "y": 202, "align": "right"},
            ] * 3,
        )
        self.assertEqual(len(values["links"]), 6)
        self.assertTrue(
            all(
                link["url"] == "https://tm-koch.github.io/etf-portfolio-lens/"
                for link in values["links"]
            )
        )
        self.assertTrue(
            all(
                link["x"] == 8 and link["width"] == len("ETF Portfolio Lens") * 0.5
                for link in values["links"]
            )
        )
        self.assertTrue(all(link["height"] == 4 for link in values["links"]))
        self.assertEqual(
            values["text"],
            [
                f"ETF Portfolio Lens | {label}: 24 Oct 2026, 11:24:30 UTC"
                for label in ("Generated", "Erstellt", "Wygenerowano")
                for _ in range(2)
            ],
        )

    def test_offline_pwa_uses_cached_report_resources_without_uploads(self) -> None:
        script = """
import { generateReportPdf } from './web/pdf-export.js';

const listeners = new Map();
const cacheStore = new Map();
const networkRequests = [];
let offline = false;
let savedFilename = null;
let capturedOptions = null;
const shellCacheName = 'etf-lens-shell-test';
const runtimeCacheName = 'etf-lens-runtime-test';
const shellCache = {
    addAll: async (urls) => urls.forEach((url) => cacheStore.set(url, {
        asset: url,
        ok: true,
        arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer,
    })),
    match: async (request, options = {}) => {
        const url = typeof request === 'string' ? request : request.url;
        if (cacheStore.has(url)) return cacheStore.get(url);
        if (options.ignoreSearch) {
            const path = new URL(url).pathname;
            return [...cacheStore.entries()].find(([key]) => new URL(key).pathname === path)?.[1] || null;
        }
        return null;
    },
    put: async (request, response) => cacheStore.set(request.url, response),
    keys: async () => [...cacheStore.keys()].map((url) => ({ url })),
    delete: async (request) => cacheStore.delete(request.url),
};
const caches = {
    open: async () => shellCache,
    keys: async () => [shellCacheName, runtimeCacheName],
    delete: async () => true,
};
const self = {
    registration: { scope: 'https://app.test/web/' },
    clients: { claim: async () => {} },
    skipWaiting: async () => {},
    addEventListener: (name, listener) => listeners.set(name, listener),
};
async function fetch(request) {
    networkRequests.push({ url: request.url, method: request.method });
    if (offline) throw new Error('offline');
    return { ok: true, value: request.url, clone() { return { ...this }; } };
}
const workerSource = await (await import('node:fs/promises')).readFile('./web/sw.js', 'utf8');
const vm = await import('node:vm');
vm.runInNewContext(workerSource, { self, caches, fetch, URL, Promise, Error });

let installPromise;
listeners.get('install')({ waitUntil: (promise) => { installPromise = promise; } });
await installPromise;
async function requestThroughWorker(request) {
    let responsePromise;
    listeners.get('fetch')({ request, respondWith: (promise) => { responsePromise = promise; } });
    return responsePromise;
}
const cachedRequests = [
    { url: 'https://app.test/web/data/catalog.json', method: 'GET', mode: 'cors' },
    { url: 'https://app.test/data/raw/snapshots/CHSPI.json', method: 'GET', mode: 'cors' },
];
for (const request of cachedRequests) await requestThroughWorker(request);
offline = true;
const offlineData = await Promise.all(cachedRequests.map(requestThroughWorker));
const pdfAssetPaths = [
    'pdf-report-renderer.js',
    'pdf-vendor.js',
    'chart-palette.js',
    'icons/launchericon-512x512.png',
    'fonts/space-grotesk-400.ttf',
    'fonts/space-grotesk-500.ttf',
    'fonts/space-grotesk-700.ttf',
    'vendor/jspdf.umd.min.js',
    'vendor/jspdf.plugin.autotable.min.js',
];
const pdfAssetsListed = pdfAssetPaths.every((path) => workerSource.includes(`'${path}'`));

globalThis.document = { fonts: { ready: Promise.resolve() } };
let pageCount = 1;
let activePage = 1;
let coverImage = null;
const renderedText = [];
const roundedRects = [];
const pdf = {
    internal: { getNumberOfPages: () => pageCount, pageSize: { getWidth: () => 297, getHeight: () => 210 } },
    setProperties: () => {},
    setPage: (page) => { activePage = page; },
    setFont: () => {},
    setFontSize: () => {},
    setTextColor: () => {},
    setDrawColor: () => {},
    setFillColor: () => {},
    setLineWidth: () => {},
    roundedRect: (...args) => roundedRects.push({ page: activePage, args }),
    rect: () => {},
    line: () => {},
    splitTextToSize: (value) => [value],
    text: (value, x, y) => renderedText.push({ page: activePage, value: Array.isArray(value) ? value.join(' ') : value, x, y }),
    getTextWidth: (value) => value.length * 0.5,
    addImage: (data, format, x, y, width, height) => { coverImage = { data, format, page: activePage, x, y, width, height }; },
    addPage: () => { pageCount += 1; activePage = pageCount; },
    link: () => {},
    addFileToVFS: () => {},
    addFont: () => {},
    save: (filename) => { savedFilename = filename; },
};
class PdfConstructor {
    constructor(options) { capturedOptions = options; return pdf; }
}
const autoTable = (document, options) => {
    document.lastAutoTable = { finalY: (options.startY || 12) + 8 };
};
await generateReportPdf({
    snapshot: { generatedAt: '2026-10-23T12:00:00Z', provenance: {}, etfs: [] },
    analytics: {
        summary: {},
        rollups: {},
        redundancy: {},
        diversification: {},
        etfColumns: [],
        companies: [],
        pairwiseHeatmap: [],
    },
    t: (key, values = {}) => key === 'export.page' ? `Page ${values.page} of ${values.total}` : key,
    formatTimestamp: (value) => value || 'Unavailable',
    formatCount: (value) => String(value),
    formatDecimal: (value) => String(value),
    formatPercent: (value) => `${value}%`,
    formatCurrency: (value) => String(value),
    translateTaxonomy: (value) => value,
    jsPDFConstructor: PdfConstructor,
    autoTable,
    fetchImpl: async (url) => {
        const filename = new URL(url).pathname.split('/').at(-1);
        const assetSuffix = filename === 'launchericon-512x512.png' ? `/icons/${filename}` : `/fonts/${filename}`;
        if (offline && ![...cacheStore.keys()].some((path) => path.endsWith(assetSuffix))) {
            throw new Error(`Offline report asset unavailable: ${filename}`);
        }
        return { ok: true, arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer };
    },
});
console.log(JSON.stringify({
    offlineData: offlineData.map((response) => response.value),
    pdfAssetsListed,
    filename: savedFilename,
    orientation: capturedOptions.orientation,
    coverImage,
    pageCount,
    renderedText,
    roundedRects,
    networkRequests,
    cacheContainsPdfFonts: ['400', '500', '700'].every((weight) => [...cacheStore.keys()].some((url) => url.endsWith(`/fonts/space-grotesk-${weight}.ttf`))),
}));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout)

        self.assertEqual(
            values["offlineData"],
            [
                "https://app.test/web/data/catalog.json",
                "https://app.test/data/raw/snapshots/CHSPI.json",
            ],
        )
        self.assertTrue(values["pdfAssetsListed"])
        self.assertEqual(values["filename"], "etf-portfolio-lens-report-2026-10-23.pdf")
        self.assertEqual(values["orientation"], "landscape")
        self.assertTrue(values["cacheContainsPdfFonts"])
        self.assertTrue(
            values["coverImage"]["data"].startswith("data:image/png;base64,")
        )
        self.assertEqual(values["coverImage"]["page"], 1)
        self.assertFalse(any(item["page"] == 1 for item in values["roundedRects"]))
        rendered_values = [item["value"] for item in values["renderedText"]]
        self.assertIn("ETF Portfolio Lens", rendered_values)
        self.assertIn("export.generatedAt", rendered_values)
        self.assertIn("export.buildIdentifier", rendered_values)
        self.assertIn("export.etfSnapshot", rendered_values)
        self.assertIn("export.livePrices", rendered_values)
        footer_values = [
            value
            for value in rendered_values
            if value.startswith("ETF Portfolio Lens | ")
        ]
        self.assertEqual(len(footer_values), values["pageCount"])
        self.assertIn("export.sectionPortfolio", rendered_values)
        self.assertNotIn(
            "https://tm-koch.github.io/etf-portfolio-lens/", rendered_values
        )
        self.assertTrue(
            all(request["method"] == "GET" for request in values["networkRequests"])
        )
        self.assertTrue(
            all(
                request["url"].startswith("https://app.test/")
                for request in values["networkRequests"]
            )
        )

    def test_report_score_cards_show_verdict_badges_without_coverage(self) -> None:
        script = """
import { renderReportDocument } from './web/pdf-report-renderer.js';

globalThis.document = {
    documentElement: { dataset: { colorMode: 'light' } },
    createElement: () => ({ getContext: () => ({}) }),
};
globalThis.Chart = class { destroy() {} };
const translations = {
    'export.portfolioScores': 'Portfolio scores',
    'export.redundancy': 'Redundancy',
    'export.diversification': 'Diversification',
    'export.coverage': 'Holdings coverage',
    'explore.redundancy.low': 'Low',
    'explore.redundancy.moderate': 'Moderate',
    'explore.redundancy.high': 'High',
    'explore.diversification.highlyConcentrated': 'Highly Concentrated',
    'explore.diversification.concentrated': 'Concentrated',
    'explore.diversification.moderatelyDiversified': 'Moderately Diversified',
    'explore.diversification.wellDiversified': 'Well Diversified',
    'explore.diversification.highlyDiversified': 'Highly Diversified',
};
const cases = [
    { type: 'redundancy', verdict: 'low', label: 'Low', color: [201, 232, 200] },
    { type: 'redundancy', verdict: 'moderate', label: 'Moderate', color: [248, 221, 162] },
    { type: 'redundancy', verdict: 'high', label: 'High', color: [245, 208, 209] },
    { type: 'diversification', verdict: 'highlyConcentrated', label: 'Highly Concentrated', color: [245, 208, 209] },
    { type: 'diversification', verdict: 'concentrated', label: 'Concentrated', color: [246, 214, 188] },
    { type: 'diversification', verdict: 'moderatelyDiversified', label: 'Moderately Diversified', color: [248, 221, 162] },
    { type: 'diversification', verdict: 'wellDiversified', label: 'Well Diversified', color: [220, 228, 185] },
    { type: 'diversification', verdict: 'highlyDiversified', label: 'Highly Diversified', color: [201, 232, 200] },
];
const results = [];
for (const colorMode of ['light', 'dark']) {
    document.documentElement.dataset.colorMode = colorMode;
    for (const testCase of cases) {
        const textCalls = [];
        const fillColors = [];
        const pdf = {
            text: (value) => textCalls.push(Array.isArray(value) ? value.join(' ') : value),
            splitTextToSize: (value) => [value],
            setFillColor: (...value) => fillColors.push(value),
            lastAutoTable: null,
        };
        for (const method of ['addPage', 'setFont', 'setFontSize', 'setTextColor', 'setDrawColor', 'setLineWidth', 'roundedRect', 'rect', 'line', 'link']) {
            pdf[method] = () => {};
        }
        renderReportDocument({
            pdf,
            autoTable: (document, options) => { document.lastAutoTable = { finalY: options.startY + 8 }; },
            snapshot: { generatedAt: '2026-10-23T12:00:00Z', provenance: {}, portfolioMode: 'full', etfs: [] },
            analytics: {
                summary: {},
                rollups: {},
                redundancy: {
                    available: true,
                    score: 8,
                    level: testCase.type === 'redundancy' ? testCase.verdict : 'low',
                },
                diversification: {
                    available: true,
                    score: 12.5,
                    rating: testCase.type === 'diversification' ? testCase.verdict : 'moderatelyDiversified',
                    coveragePct: 42,
                },
                charts: {},
                etfColumns: [],
                companies: [],
                pairwiseHeatmap: [],
            },
            t: (key) => translations[key] || key,
            formatCount: String,
            formatDecimal: String,
            formatPercent: (value) => `${value}%`,
            formatCurrency: String,
            translateTaxonomy: (value) => value,
        });
        results.push({ colorMode, testCase, textCalls, fillColors });
    }
}
console.log(JSON.stringify(results));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        results = json.loads(result.stdout)

        self.assertEqual(len(results), 16)
        for result in results:
            test_case = result["testCase"]
            self.assertIn("Portfolio scores", result["textCalls"])
            self.assertIn(test_case["label"], result["textCalls"])
            self.assertNotIn("Holdings coverage", result["textCalls"])
            self.assertIn(test_case["color"], result["fillColors"])

    def test_report_portfolio_table_uses_dashes_only_for_missing_values(self) -> None:
        script = """
import { renderReportDocument } from './web/pdf-report-renderer.js';

let portfolioTable = null;
const textCalls = [];
const pdf = {
    text: (value) => textCalls.push(Array.isArray(value) ? value.join(' ') : value),
    splitTextToSize: (value) => [value],
    lastAutoTable: null,
};
for (const method of ['addPage', 'setFont', 'setFontSize', 'setTextColor', 'setDrawColor', 'setLineWidth', 'setFillColor', 'roundedRect', 'rect', 'line', 'link']) {
    pdf[method] = () => {};
}
globalThis.document = { createElement: () => ({ getContext: () => ({}) }) };
globalThis.Chart = class { destroy() {} };
const translations = {
    'export.noData': 'Unavailable',
    'export.sectionPortfolio': '1 · Portfolio',
    'export.sectionAnalytics': '2 · Portfolio Analytics',
    'export.sectionExposure': '3 · Exposure Analysis',
    'export.inPortfolio': 'In portfolio',
    'export.catalogOnly': 'Catalog only',
};
renderReportDocument({
    pdf,
    autoTable: (document, options) => {
        if (options.head?.[0]?.[0] === 'ui.etf') portfolioTable = options;
        document.lastAutoTable = { finalY: options.startY + 8 };
    },
    snapshot: {
        generatedAt: '2026-10-23T12:00:00Z',
        provenance: {},
        portfolioMode: 'full',
        etfs: [
            {
                entry: { ticker: 'AAA', name: 'Missing Values' },
                portfolioPosition: {
                    shares: null,
                    weightPct: null,
                    valuation: { price: null, valueChf: null },
                },
            },
            { entry: { ticker: 'BBB', name: 'Catalog Only' }, portfolioPosition: null },
            {
                entry: { ticker: 'CCC', name: 'Zero Values' },
                portfolioPosition: {
                    shares: 0,
                    weightPct: 0,
                    valuation: { price: 0, valueChf: 0, currency: 'CHF' },
                },
            },
        ],
    },
    analytics: {
        summary: {}, rollups: {}, redundancy: {}, diversification: {}, charts: {},
        etfColumns: [], companies: [], pairwiseHeatmap: [],
    },
    t: (key) => translations[key] || key,
    formatCount: (value) => `${value} shares`,
    formatDecimal: String,
    formatPercent: (value) => `${value}%`,
    formatCurrency: (value) => `CHF ${value}`,
    translateTaxonomy: (value) => value,
});
console.log(JSON.stringify({ body: portfolioTable.body, textCalls }));
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
            values["body"],
            [
                ["AAA · Missing Values", "In portfolio", "—", "—", "—", "—"],
                ["BBB · Catalog Only", "Catalog only", "—", "—", "—", "—"],
                [
                    "CCC · Zero Values",
                    "In portfolio",
                    "0 shares",
                    "CHF 0",
                    "CHF 0",
                    "0%",
                ],
            ],
        )
        self.assertIn("Unavailable", values["textCalls"])

    def test_report_cover_centers_separator_and_keeps_provenance_clear_of_footer(
        self,
    ) -> None:
        script = """
import { renderReportDocument } from './web/pdf-report-renderer.js';

const textCalls = [];
const lines = [];
let coverImage = null;
const pdf = {
    text: (value, x, y) => textCalls.push({ value: Array.isArray(value) ? value.join(' ') : value, x, y }),
    splitTextToSize: (value) => [value],
    line: (...value) => lines.push(value),
    addImage: (...value) => { coverImage = value; },
    lastAutoTable: null,
};
for (const method of ['addPage', 'setFont', 'setFontSize', 'setTextColor', 'setDrawColor', 'setLineWidth', 'setFillColor', 'roundedRect', 'rect', 'link']) {
    pdf[method] = () => {};
}
globalThis.document = { createElement: () => ({ getContext: () => ({}) }) };
globalThis.Chart = class { destroy() {} };
renderReportDocument({
    pdf,
    autoTable: (document, options) => { document.lastAutoTable = { finalY: options.startY + 8 }; },
    snapshot: {
        generatedAt: '2026-10-23T12:00:00Z',
        provenance: { buildId: 'abcdef1', snapshotTimestamp: '2026-10-22', livePricesTimestamp: '2026-10-23' },
        portfolioMode: 'full',
        etfs: [],
    },
    analytics: {
        summary: {}, rollups: {}, redundancy: {}, diversification: {}, charts: {},
        etfColumns: [], companies: [], pairwiseHeatmap: [],
    },
    coverIcon: 'icon',
    t: (key) => key,
    formatCount: String,
    formatDecimal: String,
    formatPercent: String,
    formatCurrency: String,
    formatTimestamp: (value) => value,
    translateTaxonomy: (value) => value,
});
console.log(JSON.stringify({ textCalls, lines, coverImage }));
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
        text_calls = values["textCalls"]
        cover_title = next(
            item for item in text_calls if item["value"] == "ETF Portfolio Lens"
        )
        provenance_values = {
            "export.generatedAt",
            "export.buildIdentifier",
            "export.etfSnapshot",
            "export.livePrices",
            "2026-10-23T12:00:00Z",
            "abcdef1",
            "2026-10-22",
            "2026-10-23",
        }
        provenance = [item for item in text_calls if item["value"] in provenance_values]

        self.assertEqual(values["coverImage"][2:6], [8, 59, 32, 32])
        self.assertEqual(cover_title["y"], 76)
        self.assertEqual(values["lines"][0], [8, 105, 289, 105])
        self.assertEqual(len(provenance), len(provenance_values))
        self.assertGreater(105, cover_title["y"])
        self.assertLess(105, min(item["y"] for item in provenance))
        self.assertLessEqual(max(item["y"] for item in provenance), 182)

    def test_report_rollups_limit_entries_and_group_the_remainder(self) -> None:
        script = """
import { renderReportDocument } from './web/pdf-report-renderer.js';

const textCalls = [];
const pdf = {
    text: (value) => textCalls.push(Array.isArray(value) ? value.join(' ') : value),
    splitTextToSize: (value) => [value],
    lastAutoTable: null,
};
for (const method of ['addPage', 'setFont', 'setFontSize', 'setTextColor', 'setDrawColor', 'setLineWidth', 'setFillColor', 'roundedRect', 'rect', 'line', 'link']) {
    pdf[method] = () => {};
}
const sector = Object.fromEntries(Array.from({ length: 25 }, (_, index) => [`Sector ${index + 1}`, 25 - index]));
const region = Object.fromEntries(Array.from({ length: 20 }, (_, index) => [`Region ${index + 1}`, 20 - index]));
const translations = {
    'export.otherRollup': 'Other categories',
    'rollup.sectorExposure': 'Sector exposure',
    'rollup.regionExposure': 'Region exposure',
    'rollup.currencyExposure': 'Currency exposure',
};
renderReportDocument({
    pdf,
    autoTable: (document, options) => { document.lastAutoTable = { finalY: (options.startY || 12) + 8 }; },
    snapshot: { generatedAt: '2026-10-23T12:00:00Z', provenance: {}, portfolioMode: 'full', etfs: [] },
    analytics: {
        summary: {}, rollups: { sector, region, currency: {} }, redundancy: {}, diversification: {}, charts: {},
        etfColumns: [], companies: [], pairwiseHeatmap: [],
    },
    t: (key) => translations[key] || key,
    formatCount: String,
    formatDecimal: String,
    formatPercent: (value) => `${value}%`,
    formatCurrency: String,
    translateTaxonomy: (value) => value,
});
console.log(JSON.stringify(textCalls));
"""
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        text_calls = json.loads(result.stdout)
        sector_labels = [
            value
            for value in text_calls
            if value.startswith("Sector ") and value != "Sector exposure"
        ]
        self.assertEqual(sector_labels, [f"Sector {index}" for index in range(1, 21)])
        self.assertNotIn("Sector 21", text_calls)
        self.assertIn("Other categories", text_calls)
        self.assertIn("15%", text_calls)
        self.assertEqual(text_calls.count("Other categories"), 1)
        self.assertEqual(
            [
                value
                for value in text_calls
                if value.startswith("Region ") and value != "Region exposure"
            ],
            [f"Region {index}" for index in range(1, 21)],
        )

    def test_report_category_headers_repeat_and_exposure_bars_span_columns(
        self,
    ) -> None:
        script = """
import { renderReportDocument } from './web/pdf-report-renderer.js';

let fontSize = 0;
const textCalls = [];
const lines = [];
const tableOptions = [];
let drawColor = null;
let lineWidth = 0;
const pdf = {
    text: (value, x, y) => textCalls.push({ value: Array.isArray(value) ? value.join(' ') : value, x, y, fontSize }),
    setFontSize: (value) => { fontSize = value; },
    setDrawColor: (...values) => { drawColor = values; },
    setLineWidth: (value) => { lineWidth = value; },
    line: (...values) => lines.push({ values, drawColor, lineWidth }),
    splitTextToSize: (value) => [value],
    lastAutoTable: null,
};
for (const method of ['addPage', 'setFont', 'setTextColor', 'setFillColor', 'roundedRect', 'rect', 'link', 'addImage']) {
    pdf[method] = () => {};
}
globalThis.document = {
    createElement: () => ({ getContext: () => ({}), toDataURL: () => 'data:image/png;base64,chart' }),
};
globalThis.Chart = class { destroy() {} };
const columns = Array.from({ length: 9 }, (_, index) => ({ ticker: `ETF${index + 1}`, name: `ETF ${index + 1}` }));
const currencies = ['USD', 'EUR', 'CHF', 'GBP', 'CAD', 'JPY', 'AUD', 'SEK'];
const analytics = {
    summary: {}, rollups: {}, redundancy: {}, diversification: {},
    charts: { currency: { labels: currencies, series: [{ label: 'Portfolio', values: Object.fromEntries(currencies.map((currency) => [currency, 12.5])) }] } },
    etfColumns: columns,
    companies: [{
        rank: 1,
        name: 'Example Company',
        totalContribution: 20,
        contributions: columns.map((column, index) => ({
            ticker: column.ticker,
            value: index === 0 ? 50 : index === 1 ? 30 : index === 2 ? 20 : null,
        })),
    }],
    pairwiseHeatmap: columns.map((product) => ({ product, cells: columns.map(() => ({ type: 'diagonal' })) })),
};
const translations = {
    'export.sectionAnalytics': '2 · Portfolio Analytics',
    'export.sectionExposure': '3 · Exposure Analysis',
    'export.topCompanies': 'Top companies',
    'export.rank': 'Rank',
    'export.company': 'Company',
    'export.totalContribution': 'Total contribution',
    'export.pairwiseOverlap': 'Pairwise ETF overlap',
    'chart.titleSectors': 'Sector chart',
    'chart.titleRegions': 'Region chart',
    'chart.titleCurrencies': 'Currency chart',
};
renderReportDocument({
    pdf,
    autoTable: (document, options) => {
        tableOptions.push(options);
        document.lastAutoTable = { finalY: options.startY + 8 };
        options.willDrawPage?.({ pageNumber: 2 });
    },
    snapshot: { generatedAt: '2026-10-23T12:00:00Z', provenance: {}, portfolioMode: 'full', etfs: [] },
    analytics,
    t: (key, values = {}) => translations[key]
        || (key === 'export.contributionPanel' ? `ETF columns ${values.start}-${values.end}` : key)
        || (key === 'export.overlapPanel' ? `Compared ETFs ${values.start}-${values.end}` : key),
    formatCount: String,
    formatDecimal: String,
    formatPercent: (value) => `${value}%`,
    formatCurrency: String,
    translateTaxonomy: (value) => value,
});
const bars = lines.filter(({ values: [, y1, , y2] }) => y1 === 34 && y2 === 34);
const currencyLegend = textCalls.filter(({ value }) => currencies.includes(value));
const topCompanyTable = tableOptions.find((options) => options.head?.[0]?.[1] === 'Company');
console.log(JSON.stringify({
    textCalls,
    topCompanyRows: topCompanyTable?.body,
    bars: bars.map(({ values: [x1, , x2], drawColor, lineWidth }) => ({ x: x1, width: x2 - x1, drawColor, lineWidth })),
    currencyLegend,
    topAutoContinuation: tableOptions.some((options) => typeof options.willDrawPage === 'function'),
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
        text_calls = values["textCalls"]
        top_titles = [item for item in text_calls if item["value"] == "Top companies"]
        pairwise_titles = [
            item for item in text_calls if item["value"] == "Pairwise ETF overlap"
        ]
        self.assertGreaterEqual(len(top_titles), 4)
        self.assertGreaterEqual(len(pairwise_titles), 4)
        self.assertTrue(
            all(item["fontSize"] == 11 for item in top_titles + pairwise_titles)
        )
        self.assertTrue(values["topAutoContinuation"])
        top_company_row = values["topCompanyRows"][0]
        self.assertEqual(
            top_company_row[:7],
            ["1", "Example Company", "20%", "50%", "30%", "20%", "—"],
        )
        self.assertEqual(top_company_row[7:], ["—"] * 4)
        self.assertEqual(
            values["bars"],
            [
                {"x": 8, "width": 87, "drawColor": [213, 220, 227], "lineWidth": 0.35},
                {
                    "x": 105,
                    "width": 87,
                    "drawColor": [213, 220, 227],
                    "lineWidth": 0.35,
                },
                {
                    "x": 202,
                    "width": 87,
                    "drawColor": [213, 220, 227],
                    "lineWidth": 0.35,
                },
            ],
        )
        currency_legend = values["currencyLegend"]
        self.assertEqual(len(currency_legend), 8)
        self.assertEqual(len({item["x"] for item in currency_legend[:4]}), 4)
        self.assertEqual(len({item["y"] for item in currency_legend[:4]}), 1)


if __name__ == "__main__":
    unittest.main()

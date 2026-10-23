from pathlib import Path
from html.parser import HTMLParser
import json
import re
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPOSITORY_ROOT / "web"


class LocalizationKeyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.keys: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value and (name == "data-i18n" or name.startswith("data-i18n-attr-")):
                self.keys.add(value)


class WebContractTests(unittest.TestCase):
    def test_web_readme_documents_shipped_locales_and_offline_language_switching(
        self,
    ) -> None:
        readme = (WEB_ROOT / "README.md").read_text(encoding="utf-8")
        locales = {path.stem for path in (WEB_ROOT / "locales").glob("*.json")}

        self.assertEqual(locales, {"en-CH", "de-CH", "pl-PL"})
        for locale in locales:
            self.assertIn(locale, readme)
        self.assertIn("unsupported browser languages default to `en-CH`", readme)
        self.assertIn("available for switching while offline", readme)

    def test_static_translation_keys_exist_in_all_locales(self) -> None:
        parser = LocalizationKeyParser()
        parser.feed((WEB_ROOT / "index.html").read_text(encoding="utf-8"))

        for locale in ("en-CH", "de-CH", "pl-PL"):
            resources = json.loads(
                (WEB_ROOT / "locales" / f"{locale}.json").read_text(encoding="utf-8")
            )["translation"]
            self.assertEqual(parser.keys - resources.keys(), set(), locale)

    def test_home_headline_is_localized_in_all_supported_languages(self) -> None:
        expected = {
            "en-CH": "Privacy-first ETF portfolio exposure, clear on any screen.",
            "de-CH": "Datenschutz zuerst. Klare ETF-Portfolio-Exponierung auf jedem Bildschirm.",
            "pl-PL": "Prywatność przede wszystkim. Ekspozycja portfela ETF czytelna na każdym ekranie.",
        }

        for locale, headline in expected.items():
            resources = json.loads(
                (WEB_ROOT / "locales" / f"{locale}.json").read_text(encoding="utf-8")
            )["translation"]
            self.assertEqual(resources["ui.heroTitle"], headline, locale)

    def test_comparison_header_to_chart_gap_is_compact_at_all_widths(self) -> None:
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        base_styles = styles[: styles.index("@media (max-width: 760px)")]
        mobile_styles = styles[styles.rfind("@media (max-width: 760px)") :]

        self.assertIn(
            ".chart-card {\n"
            "  padding: 18px;\n"
            "  border-radius: var(--radius);\n"
            "  display: grid;\n"
            "  gap: 14px;\n"
            "}",
            base_styles,
        )
        self.assertIn(".chart-card-head {\n  margin-bottom: -6px;\n}", base_styles)
        self.assertIn("--comparison-donut-mobile-spacing: 16px;", styles)
        self.assertIn("gap: var(--comparison-donut-mobile-spacing);", mobile_styles)
        self.assertIn(
            ".chart-card-head {\n    margin-bottom: -8px;\n  }", mobile_styles
        )
        self.assertEqual(index.count('<article class="chart-card">'), 3)
        self.assertEqual(index.count('class="chart-card-head"'), 3)
        self.assertEqual(index.count('class="chart-frame"'), 3)
        self.assertEqual(index.count('class="chart-legend-shell"'), 3)

    def test_export_labels_exist_in_all_locales_and_keep_required_section_titles(self) -> None:
        expected_titles = {
            "export.sectionPortfolio": "1 · Portfolio",
            "export.sectionAnalytics": "2 · Portfolio Analytics",
            "export.sectionExposure": "3 · Exposure Analysis",
        }
        expected_keys = {
            "export.open",
            "export.title",
            "export.close",
            "export.description",
            "export.scope",
            "export.scopePortfolio",
            "export.scopeCatalog",
            "export.allocationOnly",
            "export.generate",
            "export.generating",
            "export.pdfReady",
            "export.generationFailed",
            "export.portfolioStatus",
            "export.inPortfolio",
            "export.catalogOnly",
            "export.allocation",
            "export.shares",
            "export.unitPrice",
            "export.marketValue",
            "export.portfolioWeight",
            "export.summaryMetrics",
            "export.exposureRollups",
            "export.diversification",
            "export.redundancy",
            "export.coverage",
            "export.topCompanies",
            "export.rank",
            "export.company",
            "export.totalContribution",
            "export.etfContribution",
            "export.contributionPanel",
            "export.overlapPanel",
            "export.noData",
            "export.sector",
            "export.region",
            "export.currency",
            "export.pairwiseOverlap",
            "export.generatedAt",
            "export.buildIdentifier",
            "export.etfSnapshot",
            "export.livePrices",
            "export.website",
            "export.page",
        }

        for locale in ("en-CH", "de-CH", "pl-PL"):
            resources = json.loads(
                (WEB_ROOT / "locales" / f"{locale}.json").read_text(encoding="utf-8")
            )["translation"]
            self.assertTrue(expected_keys.issubset(resources.keys()), locale)
            for key, title in expected_titles.items():
                self.assertEqual(resources[key], title, locale)

    def test_export_dialog_has_accessible_scope_and_generation_controls(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn(
            '<dialog class="build-dialog export-dialog" id="export-report-dialog" '
            'aria-labelledby="export-report-title" aria-describedby="export-report-description">',
            index,
        )
        self.assertIn('<fieldset class="export-scope-options">', index)
        self.assertIn('<legend data-i18n="export.scope">', index)
        self.assertIn('name="export-report-scope" value="portfolio" checked', index)
        self.assertIn('name="export-report-scope" value="catalog"', index)
        self.assertIn('type="checkbox"', index[index.index('id="export-allocation-only"') - 80 :])
        self.assertIn('role="status" aria-live="polite"', index)

    def test_export_dialog_closes_only_after_successful_pdf_generation(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        start = app.index("async function generateExportReport()")
        end = app.index("\nfunction closeExportDialog()", start)
        handler = app[start:end]

        self.assertLess(handler.index("await generateReportPdf("), handler.index("closeExportDialog();"))
        self.assertLess(handler.index("closeExportDialog();"), handler.index("} catch (error)"))

    def test_report_renderer_builds_required_sections_without_pairwise_drilldown(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        renderer = (WEB_ROOT / "report-renderer.js").read_text(encoding="utf-8")

        self.assertIn("createReportSnapshot(scope)", app)
        self.assertIn("createReportAnalytics(snapshot)", app)
        for section in ("portfolio", "analytics", "exposure"):
            self.assertIn("appendSection(root, t('export.section", renderer)
            self.assertIn(f"'{section}'", renderer)
        for report_surface in (
            "pdf-report-portfolio-table",
            "pdf-report-company-table",
            "pdf-report-chart",
            "pdf-report-heatmap",
        ):
            self.assertIn(report_surface, renderer)
        self.assertNotIn("pairwise-holdings", renderer)

    def test_report_charts_are_created_inside_the_visible_report_layout(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        renderer = (WEB_ROOT / "report-renderer.js").read_text(encoding="utf-8")
        generate_report = app[app.index("async function generateExportReport()"):]

        self.assertLess(
            generate_report.index("elements.exportReportPreview.hidden = false;"),
            generate_report.index("renderReportDocument({"),
        )
        self.assertLess(
            renderer.index("const exposure = appendSection(root"),
            renderer.index("exposure.append(charts);"),
        )
        self.assertLess(
            renderer.index("exposure.append(charts);"),
            renderer.index("appendChart(charts, 'sector'"),
        )

    def test_report_analytics_boxes_and_compact_donut_layout(self) -> None:
        renderer = (WEB_ROOT / "report-renderer.js").read_text(encoding="utf-8")
        pdf_export = (WEB_ROOT / "pdf-export.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn("createElement('div', 'pdf-report-metric')", renderer)
        self.assertIn("createElement('div', 'pdf-report-chart-canvas-wrap')", renderer)
        self.assertIn("createElement('h3', 'pdf-report-top-companies-title', t('export.topCompanies'))", renderer)
        self.assertIn("createElement('h3', 'pdf-report-pairwise-title', t('export.pairwiseOverlap'))", renderer)
        self.assertIn("'.pdf-report-top-companies-title'", pdf_export)
        self.assertIn("'.pdf-report-pairwise-title'", pdf_export)
        self.assertIn("animation: false,", renderer)
        self.assertIn(".pdf-report-metric,\n.pdf-report-rollup {", styles)
        self.assertIn(".pdf-report-metrics {\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  width: 92%;\n  max-width: 100%;", styles)
        self.assertIn(".pdf-report-rollups {\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  width: 92%;\n  max-width: 100%;", styles)
        self.assertIn("width: 252px;\n  height: 252px;", styles)
        self.assertIn(".pdf-report {\n  --report-text: #17212b;", styles)
        self.assertIn("width: 1040px;\n  max-width: none;", styles)
        self.assertIn("windowWidth: 1040,", pdf_export)
        self.assertIn(".pdf-report-chart-legend {\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  margin-top: 48px;", styles)
        self.assertIn(".pdf-report-pairwise-title {\n  break-before: page;\n  page-break-before: always;", styles)
        self.assertIn(".pdf-report-top-companies-title {\n  break-before: page;\n  page-break-before: always;", styles)
        self.assertIn(".pdf-report-company-table th,\n.pdf-report-company-table td {\n  padding: 4px 6px;", styles)
        self.assertIn(".pdf-report-company-table th:nth-child(n + 3),\n.pdf-report-company-table td:nth-child(n + 3) {\n  text-align: right;", styles)
        self.assertIn("text: contribution.value == null ? '—' : formatPercent(contribution.value),", renderer)
        self.assertIn(".pdf-report-company-table {\n  width: max-content;\n  max-width: 100%;\n  table-layout: fixed;", styles)
        self.assertIn(".pdf-report-portfolio-table {\n  width: 96%;\n  max-width: 100%;\n  table-layout: fixed;", styles)
        self.assertIn(".pdf-report-portfolio-table th:first-child,\n.pdf-report-portfolio-table td:first-child {\n  width: 42%;\n  overflow-wrap: anywhere;", styles)
        self.assertIn("width: 216px;\n  min-width: 216px;\n  max-width: 216px;", styles)

    def test_numbered_pdf_sections_start_new_pages_and_analytics_stays_inside_margins(self) -> None:
        pdf_export = (WEB_ROOT / "pdf-export.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(".pdf-report-section[data-report-section=\"analytics\"]", pdf_export)
        self.assertIn(".pdf-report-section[data-report-section=\"exposure\"]", pdf_export)
        self.assertIn(".pdf-report-section[data-report-section=\"analytics\"],\n.pdf-report-section[data-report-section=\"exposure\"] {\n  break-before: page;\n  page-break-before: always;", styles)
        self.assertIn("width: 98%;\n  max-width: 100%;", styles)

    def test_app_translation_keys_exist_in_all_locales(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        charts = (WEB_ROOT / "charts.js").read_text(encoding="utf-8")
        taxonomy = (WEB_ROOT / "taxonomy.js").read_text(encoding="utf-8")
        keys = set(re.findall(r"\bt\(['\"]([^'\"]+)['\"]", app))
        keys.update(re.findall(r"labelKey: ['\"]([^'\"]+)['\"]", app))
        keys.update(re.findall(r"translate\(options, ['\"]([^'\"]+)['\"]", charts))
        keys.update(re.findall(r"\['[^']+',\s*'([^']+)'\]", taxonomy))
        keys.update(
            f"import.source.{status}" for status in ("live", "imported", "unavailable")
        )

        for locale in ("en-CH", "de-CH", "pl-PL"):
            resources = json.loads(
                (WEB_ROOT / "locales" / f"{locale}.json").read_text(encoding="utf-8")
            )["translation"]
            self.assertEqual(keys - resources.keys(), set(), locale)

    def test_score_information_buttons_open_matching_dialog_panels(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertEqual(index.count('class="score-info-button"'), 4)
        self.assertIn('aria-labelledby="score-info-dialog-title"', index)
        for topic in ("redundancy", "diversification"):
            self.assertIn(f'data-score-info="{topic}"', index)
            self.assertIn(f'data-score-info-panel="{topic}"', index)
        for topic in ("heatmap", "drilldown"):
            self.assertIn(f'data-pairwise-info="{topic}"', index)
            self.assertIn(f'data-pairwise-info-dialog="{topic}"', index)
        self.assertNotIn('data-score-info-panel="pairwise"', index)
        self.assertIn("candidate.hidden = candidate !== panel;", app)
        self.assertIn("elements.scoreInfoDialog.showModal()", app)
        self.assertIn("function openPairwiseInfoDialog(event)", app)
        self.assertIn("function restorePairwiseInfoFocus()", app)
        self.assertIn("dialog.addEventListener('cancel'", app)
        self.assertIn("elements.pairwiseInfoDialogs.forEach((dialog)", app)
        self.assertIn("state.scoreInfoReturnFocus?.focus();", app)

        english = json.loads(
            (WEB_ROOT / "locales" / "en-CH.json").read_text(encoding="utf-8")
        )["translation"]
        self.assertIn("70% and 30%", english["explore.scoreInfo.redundancyExample"])
        self.assertIn(
            "Herfindahl-Hirschman Index",
            english["explore.scoreInfo.diversificationCalculation"],
        )

    def test_developer_threshold_fields_share_two_column_grid_at_all_widths(
        self,
    ) -> None:
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            ".developer-threshold-settings {\n"
            "  display: grid;\n"
            "  grid-template-columns: repeat(2, minmax(0, 1fr));",
            styles,
        )
        self.assertNotIn(".near-identical-threshold-settings {", styles)
        self.assertNotIn(
            "  .developer-threshold-settings {\n"
            "    grid-template-columns: 1fr;\n"
            "  }",
            styles,
        )
        self.assertIn(
            ".developer-threshold-settings input {\n  width: 100%;",
            styles,
        )

    def test_pairwise_holdings_maximum_is_a_persisted_positive_integer_setting(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn('id="pairwise-holdings-max-companies"', index)
        self.assertIn('type="number" min="1" step="1" inputmode="numeric"', index)
        self.assertIn("loadPairwiseHoldingsMaxCompaniesPreference()", app)
        self.assertIn("savePairwiseHoldingsMaxCompaniesPreference(maximum)", app)
        self.assertIn("validatePairwiseHoldingsMaxCompanies", app)
        self.assertIn("developer.invalidPairwiseHoldingsMaximum", app)

    def test_top_holdings_maximum_is_a_persisted_unlimited_by_default_setting(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        locales = [
            json.loads((WEB_ROOT / "locales" / filename).read_text(encoding="utf-8"))[
                "translation"
            ]
            for filename in ("en-CH.json", "de-CH.json", "pl-PL.json")
        ]

        self.assertIn('id="top-holdings-maximum"', index)
        self.assertIn('type="number" min="0" step="1" inputmode="numeric"', index)
        self.assertIn("topHoldingsMaximum: DEFAULT_TOP_HOLDINGS_MAXIMUM,", app)
        self.assertIn("loadTopHoldingsMaximumPreference()", app)
        self.assertIn("saveTopHoldingsMaximumPreference(maximum)", app)
        self.assertIn("validateTopHoldingsMaximum", app)
        self.assertIn(
            "getTopHoldingsDisplayLimit(ranked.length, state.topHoldingsMaximum)", app
        )
        self.assertIn("if (searchTerm)", app)
        self.assertTrue(
            all("developer.topHoldingsMaximum" in locale for locale in locales)
        )
        self.assertTrue(
            all("developer.invalidTopHoldingsMaximum" in locale for locale in locales)
        )

    def test_pairwise_holdings_selectors_are_portfolio_scoped_and_accessible(
        self,
    ) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn(
            "reconcilePairwiseSelection(positions, state.pairwiseSelection)", app
        )
        self.assertIn('role="menuitemradio"', app)
        self.assertIn('aria-haspopup="menu" aria-expanded="false"', app)
        self.assertIn("pairwiseNeedTwo", app)

    def test_pairwise_holdings_detail_uses_pair_total_and_renders_contributors(
        self,
    ) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        heatmap_start = index.index('class="subcard stack pairwise-overlap-box"')
        heatmap_end = index.index("</article>", heatmap_start)
        detail_start = index.index('class="subcard stack pairwise-holdings-box"')
        self.assertGreater(detail_start, heatmap_end)
        detail_end = index.index("</article>", detail_start)
        detail_markup = index[detail_start:detail_end]
        heatmap_markup = index[heatmap_start:heatmap_end]
        self.assertIn('id="pairwise-holdings-content"', index)
        self.assertIn('data-i18n="explore.pairwiseHoldingsTitle"', index)
        self.assertIn('data-pairwise-info="drilldown"', detail_markup)
        self.assertIn('data-pairwise-info="heatmap"', heatmap_markup)
        self.assertIn('id="pairwise-holdings-info-dialog"', index)
        self.assertIn('id="pairwise-heatmap-info-dialog"', index)
        self.assertIn("renderPairwiseHoldingsDetail(positions)", app)
        self.assertIn("pair.overlapPct", app)
        self.assertIn("buildPairwiseHoldingsBreakdown(", app)
        self.assertIn("pairwiseRemainingContribution", app)
        self.assertNotIn("pairwise-remaining-holdings", app)
        self.assertNotIn("pairwise-remaining-totals", styles)
        self.assertIn("pairwiseWeightsUnit", app)
        self.assertIn('class="pairwise-holdings-footer"', app)
        self.assertIn(".pairwise-holdings-footer", styles)
        self.assertIn("flex-wrap: wrap;", styles)
        self.assertNotIn("pairwiseETFRemainingHoldings", app)
        self.assertIn('class="pairwise-weight-unit" role="note"', app)
        self.assertNotIn("remainingCompanies.map((company)", app)
        self.assertIn("pairwise-butterfly-side-track", app)
        self.assertIn('<i class="is-a"></i>', app)
        self.assertIn('<i class="is-b"></i>', app)
        self.assertIn("--pairwise-fill: ${fillRatio}fr", app)
        self.assertIn("pairwise-butterfly-legend", app)
        self.assertNotIn("pairwise-butterfly-axis", app)
        self.assertNotIn(".pairwise-butterfly-axis", styles)
        self.assertIn(".pairwise-butterfly-side-track", styles)
        self.assertIn("width: 100%;\n  font-size: 0.8rem;", styles)
        self.assertIn(
            "grid-template-columns: minmax(0, var(--pairwise-empty)) max-content 4px minmax(0, var(--pairwise-fill));",
            styles,
        )
        self.assertIn(
            "grid-template-columns: minmax(0, var(--pairwise-fill)) 4px max-content minmax(0, var(--pairwise-empty));",
            styles,
        )
        self.assertIn(
            ".pairwise-butterfly-side.is-a .pairwise-butterfly-side-track", styles
        )
        self.assertIn(
            ".pairwise-butterfly-side.is-b .pairwise-butterfly-side-track", styles
        )
        self.assertIn(
            "grid-template-columns: minmax(0, 1fr) 2px minmax(0, 1fr);", styles
        )
        self.assertIn("grid-column: 3;", styles)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", styles)
        self.assertIn("max-content 4px minmax(0, var(--pairwise-fill))", styles)
        self.assertIn("var(--pairwise-butterfly-a)", styles)
        self.assertIn("var(--pairwise-butterfly-b)", styles)
        self.assertNotIn("butterfly bars", index)
        self.assertIn('data-i18n="explore.scoreInfo.pairwiseHoldings"', index)
        english = json.loads(
            (WEB_ROOT / "locales" / "en-CH.json").read_text(encoding="utf-8")
        )["translation"]
        self.assertEqual(english["explore.pairwiseWeightsUnit"], "Weights in %.")

    def test_score_bands_have_touch_tooltips_for_both_scores(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertEqual(index.count('class="score-band-touch-tooltip"'), 2)
        self.assertIn(
            "bindScoreBandTouchTooltip(elements.redundancyMeter, elements.redundancySegments);",
            app,
        )
        self.assertIn(
            "bindScoreBandTouchTooltip(elements.diversificationMeter, elements.diversificationSegments);",
            app,
        )
        self.assertIn("event.clientX >= rect.left && event.clientX <= rect.right", app)
        self.assertIn("tooltip.textContent = t(translationKey);", app)
        self.assertIn(
            "const targetCenter = Math.min(Math.max(event.clientX, minCenter), maxCenter);",
            app,
        )
        self.assertIn("meterRect.bottom - scoreBoxRect.top + 6", app)
        self.assertIn(".score-band-touch-tooltip {\n  position: absolute;", styles)
        self.assertIn(".score-band-touch-tooltip[hidden] {", styles)

    def test_diversification_score_follows_pairwise_overlap(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        overlap_position = index.index('id="pairwise-overlap-title"')
        score_position = index.index('id="diversification-score-box"')
        companies_position = index.index(
            '<h3 data-i18n="ui.topCompanies">Top companies</h3>'
        )
        self.assertLess(overlap_position, score_position)
        self.assertLess(score_position, companies_position)
        self.assertIn('data-i18n="explore.diversificationTitle"', index)
        self.assertIn('id="diversification-meter" role="img"', index)
        self.assertIn('id="diversification-coverage-warning" role="status"', index)
        self.assertIn("renderDiversificationScore();", app)
        self.assertIn("calculateDiversificationScore(", app)
        self.assertNotIn("diversification-band-labels", index)
        self.assertIn(
            "elements.diversificationMarker.title = t(`explore.diversification.${result.rating}`);",
            app,
        )
        for key in (
            "explore.diversification.highlyConcentrated",
            "explore.diversification.concentrated",
            "explore.diversification.moderatelyDiversified",
            "explore.diversification.wellDiversified",
            "explore.diversification.highlyDiversified",
        ):
            self.assertIn(f'data-i18n-attr-title="{key}"', index)
        for rating in (
            "highly-concentrated",
            "concentrated",
            "moderately-diversified",
            "well-diversified",
            "highly-diversified",
        ):
            self.assertIn(f".redundancy-score-level.is-{rating}", styles)
        mobile_styles = styles[styles.index("@media (max-width: 760px)") :]
        self.assertIn(".diversification-coverage-warning {", mobile_styles)
        self.assertIn("clip-path: inset(50%);", mobile_styles)

    def test_redundancy_score_is_standalone_and_available_offline(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")
        service_worker = (WEB_ROOT / "sw.js").read_text(encoding="utf-8")
        cache_generation_helper = (
            REPOSITORY_ROOT / "scripts" / "pwa-cache-generation.ps1"
        ).read_text(encoding="utf-8")

        rollups_position = index.index('<h3 data-i18n="ui.rollups">Rollups</h3>')
        score_position = index.index('id="redundancy-score-box"')
        warning_position = index.index('id="near-identical-pair-warning"')
        heatmap_position = index.index('id="pairwise-overlap-title"')
        companies_position = index.index(
            '<h3 data-i18n="ui.topCompanies">Top companies</h3>'
        )
        self.assertLess(rollups_position, score_position)
        self.assertLess(score_position, warning_position)
        self.assertLess(warning_position, index.index("</article>", score_position))
        self.assertLess(score_position, heatmap_position)
        self.assertLess(heatmap_position, companies_position)
        self.assertNotIn('data-i18n="explore.redundancyEyebrow"', index)
        self.assertNotIn('id="redundancy-band-labels"', index)
        self.assertNotIn("redundancyBandLabels", app)
        self.assertNotIn(".redundancy-band-labels", styles)
        self.assertIn('data-redundancy-threshold="lowModerate"', index)
        self.assertIn('data-redundancy-threshold="moderateHigh"', index)
        self.assertIn("renderRedundancyScore();", app)
        self.assertIn("renderNearIdenticalPairWarning();", app)
        self.assertIn(
            "elements.redundancyMarker.title = t(`explore.redundancy.${level}`);", app
        )
        self.assertNotIn(".redundancy-scale-endpoints span:last-child", styles)
        self.assertNotIn("margin-right: 20px;", styles)
        self.assertIn(".redundancy-scale,\n.diversification-scale", styles)
        self.assertIn("gap: 14px;", styles)
        self.assertIn(
            ".redundancy-scale-endpoints {\n"
            "  display: flex;\n"
            "  justify-content: space-between;",
            styles,
        )
        for key in (
            "explore.redundancy.low",
            "explore.redundancy.moderate",
            "explore.redundancy.high",
        ):
            self.assertIn(f'data-i18n-attr-title="{key}"', index)
        self.assertIn("'diversification.js'", service_worker)
        self.assertIn("'diversification.js'", cache_generation_helper)
        self.assertIn('font-family: "Space Grotesk"', styles)
        self.assertIn(".redundancy-score-box", styles)
        self.assertIn(".redundancy-score-heading", styles)
        self.assertIn(
            ".aggregation-layout > .subcard {\n"
            "    padding: 20px;\n"
            "  }\n\n"
            "  .aggregation-layout > .subcard > .subcard-heading h3 {\n"
            "    margin: 0;\n"
            "    font-size: 1.08rem;\n"
            "  }",
            styles,
        )
        self.assertIn(".pairwise-overlap-viewport", styles)
        self.assertIn("max-height: min(62vh, 520px)", styles)
        self.assertIn("position: sticky;", styles)
        self.assertIn(".pairwise-overlap-table .pairwise-corner", styles)
        self.assertIn(
            ".pairwise-overlap-table tbody th,\n.pairwise-overlap-table tbody td",
            styles,
        )
        self.assertIn("height: 56px", styles)
        self.assertIn("height: 42px", styles)
        self.assertIn(
            "--pairwise-label-background: color-mix(in srgb, "
            "var(--table-header-background) 44%, var(--card-strong))",
            styles,
        )
        self.assertIn(
            "--pairwise-empty-background: color-mix(in srgb, "
            "var(--pairwise-label-background) 72%, var(--card-strong))",
            styles,
        )
        self.assertIn("background: var(--pairwise-label-background)", styles)
        self.assertIn(".pairwise-diagonal,\n.pairwise-empty", styles)
        self.assertIn("background: var(--pairwise-empty-background)", styles)
        self.assertIn(".pairwise-overlap-legend", styles)
        self.assertIn("scrollbar-width: none", styles)
        self.assertIn(
            ".pairwise-row-label small,\n  .pairwise-overlap-coverage", styles
        )
        self.assertIn("pairwiseLegendDescription", app)
        self.assertIn("'redundancy.js'", service_worker)
        self.assertIn("'redundancy.js'", cache_generation_helper)

    def test_pwa_assets_and_local_runtime_contract(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")
        importer = (WEB_ROOT / "portfolio-import.js").read_text(encoding="utf-8")
        publish_script = (
            REPOSITORY_ROOT / "scripts" / "publish-gh-pages.ps1"
        ).read_text(encoding="utf-8")
        deployment_validator = (
            REPOSITORY_ROOT / "scripts" / "validate-pwa-deployment.ps1"
        ).read_text(encoding="utf-8")
        cache_generation_helper = (
            REPOSITORY_ROOT / "scripts" / "pwa-cache-generation.ps1"
        ).read_text(encoding="utf-8")
        service_worker = (WEB_ROOT / "sw.js").read_text(encoding="utf-8")
        manifest = json.loads((WEB_ROOT / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["name"], "ETF Portfolio Lens")
        self.assertEqual(manifest["short_name"], "ETF Portfolio Lens")
        self.assertEqual(manifest["id"], "./")
        self.assertEqual(manifest["display"], "standalone")
        self.assertEqual(
            [icon["sizes"] for icon in manifest["icons"]], ["192x192", "512x512"]
        )
        self.assertIn('rel="manifest" href="./manifest.json"', index)
        self.assertIn(
            '<title data-i18n="ui.documentTitle">ETF Portfolio Lens</title>', index
        )
        self.assertIn('id="install-app-button"', index)
        self.assertIn('title="Install app"', index)
        self.assertIn('<meta name="theme-color" content="#152033" />', index)
        self.assertIn('src="./vendor/chart.umd.min.js"', index)
        self.assertIn('src="./vendor/i18next.min.js"', index)
        self.assertIn('src="./vendor/pdf.min.js"', index)
        self.assertIn('src="./vendor/html2pdf.bundle.min.js"', index)
        self.assertTrue((WEB_ROOT / "vendor/html2pdf.bundle.min.js").is_file())
        self.assertIn('src="./vendor/lucide.js"', index)
        self.assertIn('href="./fonts.css"', index)
        self.assertNotIn("fonts.googleapis.com", index)
        self.assertTrue((WEB_ROOT / "fonts" / "OFL.txt").is_file())
        for weight in ("400", "500", "700"):
            for subset in ("latin", "latin-ext"):
                font_path = (
                    WEB_ROOT
                    / "fonts"
                    / f"space-grotesk-{subset}-{weight}-normal.woff2"
                )
                self.assertTrue(font_path.is_file())
        self.assertIn("navigator.serviceWorker.register('./sw.js')", app)
        self.assertIn("beforeinstallprompt", app)
        self.assertIn("appinstalled", app)
        self.assertIn("function promptToInstall()", app)
        self.assertIn("function isStandaloneDisplayMode()", app)
        self.assertIn("function isMobileViewport()", app)
        self.assertIn("state.activeTab !== 'home'", app)
        self.assertIn("(max-width: 760px)", app)
        self.assertIn(".install-app-button:not([hidden])", styles)
        self.assertIn("./vendor/pdf.worker.min.js", importer)
        for path in (
            "icons/launchericon-192x192.png",
            "icons/launchericon-512x512.png",
            "vendor/chart.umd.min.js",
            "vendor/i18next.min.js",
            "vendor/lucide.js",
            "vendor/pdf.min.js",
            "vendor/pdf.worker.min.js",
            "vendor/html2pdf.bundle.min.js",
        ):
            self.assertTrue((WEB_ROOT / path).is_file())
            self.assertIn(path, publish_script)

        for path in (
            "localization.js",
            "report-data.js",
            "export-view.js",
            "report-renderer.js",
            "pdf-export.js",
            "taxonomy.js",
            "formatting.js",
            "locales/en-CH.json",
            "locales/de-CH.json",
            "locales/pl-PL.json",
            "vendor/i18next.min.js",
            "fonts.css",
            "fonts/space-grotesk-latin-400-normal.woff2",
            "fonts/space-grotesk-latin-500-normal.woff2",
            "fonts/space-grotesk-latin-700-normal.woff2",
            "fonts/space-grotesk-latin-ext-400-normal.woff2",
            "fonts/space-grotesk-latin-ext-500-normal.woff2",
            "fonts/space-grotesk-latin-ext-700-normal.woff2",
        ):
            self.assertTrue((WEB_ROOT / path).is_file())
            self.assertIn(path, publish_script)
            self.assertIn(path, cache_generation_helper)
            self.assertIn(path, service_worker)

        for path in (
            "vendor/html2pdf.LICENSE",
            "vendor/html2pdf.bundle.min.js.LICENSE.txt",
            "fonts/OFL.txt",
        ):
            self.assertTrue((WEB_ROOT / path).is_file())
            self.assertIn(path, publish_script)

        self.assertIn("manifest.json", publish_script)
        self.assertIn("sw.js", publish_script)
        self.assertIn("Required web asset is missing", publish_script)
        self.assertIn("PWA deployment validation passed", deployment_validator)
        self.assertIn("ETF Portfolio Lens", deployment_validator)
        self.assertIn("Content-Type", deployment_validator)
        self.assertIn("Get-PwaCacheGeneration", publish_script)
        self.assertIn("Set-PwaServiceWorkerGeneration", publish_script)
        self.assertIn("Get-PwaCacheGeneration", deployment_validator)
        self.assertIn("Get-PwaServiceWorkerGeneration", deployment_validator)
        self.assertIn("__PWA_CACHE_GENERATION__", service_worker)
        self.assertIn("Get-PwaCacheSensitivePaths", cache_generation_helper)
        self.assertIn("live_prices.json", publish_script)
        self.assertIn("live_prices.json", deployment_validator)
        self.assertTrue((REPOSITORY_ROOT / "data" / "live_prices.json").is_file())
        self.assertIn(
            "LIVE_PRICES_URL", (WEB_ROOT / "data.js").read_text(encoding="utf-8")
        )
        workflow = (
            REPOSITORY_ROOT / ".github" / "workflows" / "live-market-data.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("cron: '0 21 * * *'", workflow)
        self.assertIn("push:", workflow)
        self.assertIn("branches:\n      - main", workflow)
        self.assertIn("data/live_price_config.json", workflow)
        self.assertIn("YAHOO_QUOTE_URL_TEMPLATE", workflow)
        self.assertNotIn("data/live_prices.json", workflow.split("concurrency:", 1)[0])
        self.assertIn("workflow_dispatch", workflow)
        self.assertIn("SWISS_QUOTE_URL_TEMPLATE", workflow)
        self.assertIn(
            "run: python -m etf_ingestion_backend.live_cli --config data/live_price_config.json --output data/live_prices.json --debug",
            workflow,
        )
        self.assertNotIn("QUOTE_URL_CH0008899764", workflow)
        self.assertNotIn("https://", workflow)
        self.assertNotIn("-NoPush", workflow)
        self.assertIn("run: ./scripts/publish-gh-pages.ps1", workflow)
        self.assertNotIn("git add data/live_prices.json", workflow)
        self.assertNotIn("git commit", workflow)
        self.assertNotIn("git push", workflow)
        self.assertIn("HEAD:$Branch", publish_script)
        self.assertIn("--force-with-lease", publish_script)
        identity_name = 'git config user.name "github-actions[bot]"'
        identity_email = 'git config user.email "41898282+github-actions[bot]@users.noreply.github.com"'
        self.assertIn("- name: Render live market data summary", workflow)
        self.assertIn("id: live-summary", workflow)
        self.assertIn(
            "python -m etf_ingestion_backend.live_summary --input data/live_prices.json --output live-market-data-summary.md",
            workflow,
        )
        self.assertIn(
            'cat live-market-data-summary.md >> "$GITHUB_STEP_SUMMARY"', workflow
        )
        self.assertIn("echo 'markdown<<LIVE_MARKET_DATA_SUMMARY'", workflow)
        self.assertIn("echo 'LIVE_MARKET_DATA_SUMMARY'", workflow)
        publish_step = workflow.index("- name: Publish GitHub Pages")
        summary_step = workflow.index("- name: Render live market data summary")
        self.assertIn(identity_name, workflow)
        self.assertIn(identity_email, workflow)
        self.assertNotIn("config', 'user.name'", publish_script)
        self.assertNotIn("config', 'user.email'", publish_script)
        self.assertLess(workflow.index(identity_name), publish_step)
        self.assertLess(workflow.index(identity_email), publish_step)
        self.assertLess(summary_step, publish_step)

    def test_publish_script_includes_app_local_javascript_modules(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        publish_script = (
            REPOSITORY_ROOT / "scripts" / "publish-gh-pages.ps1"
        ).read_text(encoding="utf-8")

        imported_modules = re.findall(
            r"from ['\"]\./([^'\"?]+\.js)(?:\?[^'\"]*)?['\"]", app
        )
        for module in imported_modules:
            self.assertTrue((WEB_ROOT / module).is_file())
            self.assertIn(f"'{module}'", publish_script)

    def test_publish_script_stages_all_cache_sensitive_assets(self) -> None:
        publish_script = (
            REPOSITORY_ROOT / "scripts" / "publish-gh-pages.ps1"
        ).read_text(encoding="utf-8")
        cache_helper = (
            REPOSITORY_ROOT / "scripts" / "pwa-cache-generation.ps1"
        ).read_text(encoding="utf-8")

        def array_entries(source: str, variable: str) -> set[str]:
            match = re.search(
                rf"^[ \t]*\${re.escape(variable)}[ \t]*=[ \t]*@\((.*?)^[ \t]*\)",
                source,
                re.MULTILINE | re.DOTALL,
            )
            self.assertIsNotNone(match, f"PowerShell array ${variable} is missing")
            return set(re.findall(r"'([^']+)'", match.group(1)))

        cache_sensitive_assets = array_entries(cache_helper, "PwaCacheSensitivePaths")
        staged_assets = array_entries(publish_script, "requiredWebFiles")
        self.assertTrue(cache_sensitive_assets)
        self.assertFalse(
            cache_sensitive_assets - staged_assets,
            f"Cache-sensitive assets are not staged: {sorted(cache_sensitive_assets - staged_assets)}",
        )

    def test_portfolio_ui_polish_contract_covers_provenance_and_presentation(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="data-dialog-data-title"', index)
        self.assertIn('id="data-dialog-metadata"', index)
        self.assertIn('id="build-dialog-button"', index)
        self.assertIn('id="data-dialog-button"', index)
        self.assertIn('id="build-dialog"', index)
        self.assertIn('id="data-dialog"', index)
        self.assertIn("function renderBuildData()", app)
        self.assertIn("entry.snapshotPath || t('common.unavailable')", app)
        self.assertNotIn(
            '<div class="position-meta">Snapshot: ${entry.snapshotPath}</div>', app
        )
        self.assertIn("<span>· ${position.entry.name}</span>", app)
        self.assertIn(".positions-table .position-name", styles)
        self.assertIn("gap: 20px;", styles)

    def test_portfolio_ui_polish_contract_covers_debug_preference_and_metrics(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn('id="portfolio-import-debug-enabled"', index)
        self.assertIn('id="portfolio-import-debug"', index)
        self.assertIn("const PORTFOLIO_IMPORT_DEBUG_STORAGE_KEY", app)
        self.assertIn("function loadPortfolioImportDebug()", app)
        self.assertIn("function savePortfolioImportDebug()", app)
        self.assertIn(
            "state.portfolioImportDebug && window.__etfLensPdfImportPages?.length", app
        )
        self.assertIn("savePortfolioImportDebug();", app)
        self.assertIn("const shareCountTotal = positions.reduce", app)
        self.assertIn(
            "{ label: t('summary.shareUnits'), value: formatCount(shareCountTotal) }",
            app,
        )
        self.assertIn("function formatChfValue(value)", app)
        self.assertIn("{ label: t('summary.totalValue'), value: totalValueChf }", app)
        self.assertIn(": formatChfValue(0);", app)
        self.assertIn("cards[1].value = t('common.notAvailable');", app)
        self.assertIn(
            "const shareInputStep = isPercentagePortfolio ? '0.1' : '1';",
            app,
        )
        self.assertIn("Number(position.shares).toFixed(1)", app)
        self.assertIn("value >= 0", app)
        self.assertIn("t('common.unavailable')", app)

    def test_portfolio_currency_display_uses_shared_apostrophe_formatter(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        formatting = (WEB_ROOT / "formatting.js").read_text(encoding="utf-8")

        self.assertIn("function formatCurrencyValue(value, currency = 'CHF')", app)
        self.assertIn(
            "formatLocaleCurrency(value, currency, window.i18next.language)", app
        )
        self.assertIn(
            "new Intl.NumberFormat(resolvedLocale, numberOptions)", formatting
        )
        self.assertIn("currencyDisplay: 'code'", formatting)
        self.assertIn("return formatCurrencyValue(value, 'CHF');", app)
        self.assertIn(
            "getEffectiveValuation(position, state.livePrices, state.valuationMode)",
            app,
        )
        self.assertIn(
            "const valuation = isPercentagePortfolio ? null : getPositionValuation(position);",
            app,
        )
        self.assertIn(
            'id="portfolio-valuation-control"',
            (WEB_ROOT / "index.html").read_text(encoding="utf-8"),
        )
        self.assertIn(
            'id="portfolio-valuation"',
            (WEB_ROOT / "index.html").read_text(encoding="utf-8"),
        )
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn('id="portfolio-import-valuation"', index)
        self.assertIn('id="portfolio-valuation-status"', index)
        self.assertIn('class="portfolio-valuation-row"', index)
        self.assertIn("data-valuation-status-label", index)
        self.assertIn(
            "state.valuationMode === 'imported' ? t('valuation.imported') : t('valuation.live')",
            app,
        )
        self.assertIn("state.valuationMode !== 'latest'", app)
        self.assertIn(
            "formatCurrencyValue(valuation.valueChf) : t('common.unavailable')", app
        )
        self.assertNotIn(
            "formatCurrencyValue(valuation.valueChf)} (${valuation.status})", app
        )
        self.assertIn("@keyframes live-status-pulse", styles)
        self.assertIn("animation: live-status-pulse 2.8s ease-in-out infinite;", styles)
        self.assertIn(".portfolio-valuation-row {", styles)
        self.assertIn("align-items: flex-start;", styles)
        self.assertIn("width: 100%;", styles)
        self.assertIn("width: min(100%, 224px);", styles)
        self.assertNotIn("width: min(100%, 320px);", styles)
        self.assertIn(".portfolio-valuation-details {", styles)
        self.assertIn(
            ".portfolio-valuation-status {\n    align-self: flex-end;\n    flex: 0 0 auto;\n    margin: 0 0 0 auto;\n  }",
            styles,
        )
        self.assertIn(
            ".portfolio-valuation-control {\n    flex: 1 1 224px;\n    min-width: 0;\n    width: auto;\n  }",
            styles,
        )
        self.assertIn(
            ".portfolio-valuation-control select {\n    min-width: 0;\n    width: 100%;\n  }",
            styles,
        )
        self.assertIn(
            ".portfolio-valuation-details {\n    flex: 0 1 auto;\n    flex-wrap: nowrap;\n    width: 100%;\n  }",
            styles,
        )
        self.assertIn("margin: 0 0 0 auto;", styles)
        self.assertIn("align-self: flex-end;", styles)
        self.assertIn("align-self: flex-end;", styles)
        self.assertIn("flex-direction: column;", styles)
        self.assertIn("return formatCurrencyValue(value, currency);", app)
        self.assertIn("formatImportedMoney(row.value, row.currency)", app)
        self.assertIn("formatImportedMoney(row.valueChf)", app)
        self.assertIn("function getImportReviewPrice(row)", app)
        self.assertIn("price.readOnly = !reviewPrice.editable;", app)

    def test_percentage_portfolio_keeps_weight_and_omits_valuation_columns(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="portfolio-valuation-control"', index)
        self.assertIn(
            'id="portfolio-valuation-control" for="portfolio-valuation" hidden', index
        )
        self.assertIn(
            'class="position-weight" data-i18n="ui.weight">Weight</th>', index
        )
        self.assertIn(
            'class="position-remove" data-i18n="ui.remove">Remove</th>', index
        )
        self.assertIn(
            "const isPercentagePortfolio = state.portfolioMode === 'percentage';",
            app,
        )
        self.assertIn('colspan="${isPercentagePortfolio ? 4 : 6}"', app)
        self.assertIn("const valuationCells = isPercentagePortfolio\n        ? ''", app)
        self.assertIn(
            'const allocationCells = isPercentagePortfolio\n        ? `\n          <td class="position-weight"',
            app,
        )
        self.assertIn("header.hidden = isPercentagePortfolio;", app)
        self.assertIn(
            "elements.portfolioValuationStatus.hidden = isPercentagePortfolio;",
            app,
        )
        self.assertIn(
            ".portfolio-valuation-control[hidden],\n.portfolio-valuation-status[hidden] {\n  display: none;\n}",
            styles,
        )
        self.assertIn(
            "const valuation = isPercentagePortfolio ? null : getPositionValuation(position);",
            app,
        )
        self.assertIn("grid-template-areas:", styles)
        self.assertIn('"shares weight remove";', styles)
        self.assertIn(
            ".positions-table-wrap {\n    overflow-x: visible;\n    margin-top: 16px;",
            styles,
        )

    def test_portfolio_sharing_contract_covers_encoding_loading_and_feedback(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        share = (WEB_ROOT / "share.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn("const SHARE_FRAGMENT_KEY = 'portfolio';", app)
        self.assertIn("const LEGACY_SHARE_PAYLOAD_VERSION = 1;", share)
        self.assertIn("const SHARE_PAYLOAD_VERSION = 2;", share)
        self.assertIn(
            "export function encodePortfolioShare(portfolio, valuationMode = 'latest')",
            share,
        )
        self.assertIn("export function decodePortfolioShare(value)", share)
        self.assertIn("Number.isFinite(position.shares)", share)
        self.assertIn("seenIsins.has(isin)", share)
        self.assertIn("readPortfolioShareFromUrl()", app)
        self.assertIn("sharedPortfolio.status === 'valid'", app)
        self.assertIn("const savedPortfolio = loadPortfolioState();", app)
        self.assertIn("state.portfolioMode = savedPortfolio.mode;", app)
        self.assertIn("const PRIVATE_SHARE_PAYLOAD_VERSION = 2;", share)
        self.assertIn("function normalizePrivatePortfolio(portfolio)", share)
        self.assertIn("export function encodePrivatePortfolioShare(positions", share)
        self.assertIn("mode: 'percentage'", share)
        self.assertIn("position.valueChf !== undefined", share)
        self.assertIn("function confirmImport()", app)
        self.assertIn('id="portfolio-import-valuation"', index)
        self.assertIn("state.importValuationMode", app)
        self.assertIn("valuationMode: state.importValuationMode", app)
        self.assertIn("parsed?.version !== LEGACY_SHARE_PAYLOAD_VERSION", share)
        self.assertIn("state.portfolioMode = 'full';", app)
        self.assertNotIn(
            "elements.importControl.hidden = state.portfolioMode === 'percentage';", app
        )
        self.assertIn("Share percentages only", index)
        self.assertIn('id="private-share-portfolio-button"', index)
        self.assertIn('data-share-mode="percentage"', index)
        self.assertIn('id="share-portfolio-button"', index)
        self.assertIn("data-share-portfolio", index)
        self.assertIn('class="portfolio-sharing"', index)
        self.assertIn("Import Saxo Bank PDF", index)
        self.assertIn(
            "Imported PDF data stays in this browser and is never uploaded.", index
        )
        self.assertLess(
            index.index('class="portfolio-import-control"'),
            index.index('class="portfolio-sharing"'),
        )
        self.assertLess(
            index.index('</div>\n\n          <label class="portfolio-import-control"'),
            index.index('class="portfolio-import-control"'),
        )
        self.assertIn('aria-live="polite"', index)
        self.assertIn('class="share-portfolio-url-label"', index)
        self.assertIn(
            'class="share-portfolio-url-label" for="share-portfolio-url" hidden', index
        )
        self.assertIn('id="share-portfolio-url"', index)
        self.assertIn("const hasFallbackUrl = Boolean(state.shareFallbackUrl);", app)
        self.assertIn("elements.shareFallbackLabel.hidden = !hasFallbackUrl;", app)
        self.assertIn("elements.shareFallbackUrl.hidden = !hasFallbackUrl;", app)
        self.assertIn("navigator.clipboard?.writeText", app)
        self.assertIn("state.shareFeedback = mode === 'percentage'", app)
        self.assertIn("'share.copied'", app)
        self.assertIn(
            "latest published ETF data",
            json.loads(
                (WEB_ROOT / "locales" / "en-CH.json").read_text(encoding="utf-8")
            )["translation"]["share.copied"],
        )
        self.assertIn(".share-portfolio-url-label[hidden]", styles)
        self.assertIn(".share-portfolio-button", styles)
        self.assertIn(".portfolio-sharing", styles)

    def test_portfolio_mutations_clear_share_feedback_without_rewriting_url(
        self,
    ) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn("function clearShareFeedback()", app)
        self.assertIn("state.shareFeedback = '';", app)
        self.assertIn("state.shareFallbackUrl = '';", app)
        for function_name in (
            "confirmImport",
            "addPosition",
            "updatePositionShares",
            "removePosition",
        ):
            function_body = re.search(
                rf"function {function_name}\(.*?(?=\nfunction |\nasync function |\Z)",
                app,
                re.DOTALL,
            )
            self.assertIsNotNone(function_body)
            self.assertIn("clearShareFeedback();", function_body.group(0))
        import_function = re.search(
            r"async function importPortfolioFile\(.*?(?=\nfunction |\nasync function |\Z)",
            app,
            re.DOTALL,
        )
        self.assertIsNotNone(import_function)
        self.assertNotIn("clearShareFeedback();", import_function.group(0))
        self.assertNotIn("history.replaceState", app)
        self.assertNotIn("history.pushState", app)

    def test_selected_positions_have_mobile_and_accessibility_hooks(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertNotIn('id="warning-list"', index)
        self.assertIn('id="data-dialog-warning-list"', index)
        self.assertIn('id="data-dialog-warnings-title"', index)
        self.assertIn("data-label=\"${t('ui.etf')}\"", app)
        self.assertIn(
            "const shareInputLabel = isPercentagePortfolio ? t('ui.allocationPercent') : t('ui.shares');",
            app,
        )
        self.assertIn('data-label="${shareInputLabel}"', app)
        self.assertIn("data-label=\"${t('ui.weight')}\"", app)
        self.assertIn(
            "return (getPositionWeightBase(position) / totalShareUnits) * 100;", app
        )
        self.assertIn("data-label=\"${t('ui.remove')}\"", app)
        self.assertIn("aria-label=\"${t('portfolio.weightLabel'", app)
        self.assertIn("aria-label=\"${t('portfolio.removeTicker'", app)
        self.assertIn("title=\"${t('portfolio.removeTicker'", app)
        self.assertIn('data-lucide="trash-2"', app)
        self.assertIn("grid-template-areas:", styles)
        self.assertIn('"shares weight remove"', styles)
        self.assertIn(
            ".position-row .position-weight {\n    grid-area: weight;\n    display: flex;\n    align-items: center;",
            styles,
        )

        mobile_styles = styles[styles.index("@media (max-width: 760px)") :]
        mobile_row_start = mobile_styles.index("  .position-row {")
        mobile_row_end = mobile_styles.index("  .position-row td {", mobile_row_start)
        mobile_row_styles = mobile_styles[mobile_row_start:mobile_row_end]
        self.assertNotIn("border-bottom: 0;", mobile_row_styles)
        self.assertIn("border-bottom: 0;", mobile_styles[mobile_row_end:])

    def test_selected_positions_have_wide_two_line_card_hooks(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            "class=\"position-row${isPercentagePortfolio ? ' position-row--percentage' : ''}\"",
            app,
        )
        self.assertIn(
            'grid-template-areas:\n      "identity identity identity identity remove"\n      "shares price value weight remove";',
            styles,
        )
        self.assertIn(
            'grid-template-areas:\n      "identity identity remove"\n      "shares weight remove";',
            styles,
        )
        self.assertIn("border-radius: 18px;", styles)
        self.assertIn("content: attr(data-label);", styles)
        self.assertIn("gap: 8px 16px;", styles)
        self.assertIn("padding: 12px 14px;", styles)
        self.assertIn('class="position-metric-value"', app)
        self.assertIn(
            ".positions-table .position-metric-value {\n    display: inline-block;\n    transform: translateY(2px);",
            styles,
        )
        self.assertIn(
            ".positions-table-wrap {\n    margin-top: 10px;\n  }",
            styles,
        )
        self.assertIn("flex-direction: column;", styles)
        self.assertIn(
            ".positions-table .position-shares .position-input {\n    box-sizing: border-box;\n    height: 32px;\n    padding: 4px 12px;\n    transform: translateY(-4px);",
            styles,
        )
        self.assertIn(
            ".position-input {\n  width: 97px;",
            styles,
        )
        self.assertIn(
            "  .position-input {\n    width: 97px;\n    min-width: 0;\n  }",
            styles[styles.index("@media (max-width: 760px)") :],
        )
        self.assertIn(
            ".positions-table .position-remove {\n    grid-area: remove;\n    align-items: center;\n    justify-content: flex-end;",
            styles,
        )

    def test_data_dialog_retains_current_selection_warnings(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn("function getCurrentSelectionWarnings", app)
        self.assertIn("getCurrentSelectionWarnings()", app)
        self.assertIn("renderWarningItems(", app)
        self.assertIn("elements.dataDialogWarningList", app)

    def test_warning_count_only_includes_incomplete_match_statuses(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn(
            "const INCOMPLETE_MATCH_STATUSES = new Set(['ambiguous', 'unmatched']);",
            app,
        )
        self.assertNotIn(
            "const INCOMPLETE_MATCH_STATUSES = new Set(['ambiguous', 'isin_only', 'unmatched']);",
            app,
        )
        self.assertIn(
            "INCOMPLETE_MATCH_STATUSES.has(holding?.provenance?.match?.status)",
            app,
        )
        self.assertNotIn(
            "holding?.provenance?.match?.status !== 'matched'",
            app,
        )

    def test_explore_uses_canonical_identity_and_stable_order(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn("holding?.security?.canonical_name", app)
        self.assertIn("holding?.security?.company_id", app)
        self.assertIn("b.weight - a.weight || a.key.localeCompare(b.key)", app)

    def test_build_dialog_warnings_are_last_and_hidden_details_do_not_display(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertLess(
            index.index('class="developer-settings"'),
            index.index('class="build-dialog-warnings"'),
        )
        self.assertIn(".build-details-extra[hidden]", styles)
        self.assertIn("display: none;", styles)

    def test_color_mode_contract_covers_preferences_persistence_and_bootstrap(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")
        charts = (WEB_ROOT / "charts.js").read_text(encoding="utf-8")

        self.assertIn("etf-lens.color-mode.v1", index)
        self.assertIn("etf-lens.color-mode.v1", app)
        self.assertIn("['bright', 'automatic', 'dark']", index)
        self.assertIn("const COLOR_MODES = ['bright', 'automatic', 'dark'];", app)
        self.assertIn("prefers-color-scheme: dark", index)
        self.assertIn("window.matchMedia?.(DARK_MODE_MEDIA_QUERY)", app)
        self.assertIn("data-color-mode-control", index)
        self.assertIn('aria-haspopup="menu"', index)
        self.assertIn("data-color-mode-option", app)
        self.assertIn('data-lucide="${selectedMode.icon}"', app)
        self.assertIn(":root[data-color-mode='dark']", styles)
        self.assertIn("--chart-border", styles)
        self.assertIn("getThemeColor('--text'", charts)

    def test_color_mode_is_labeled_and_explore_sticky_column_follows_hover(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            '<header class="app-utility-bar" aria-label="Application utilities" data-i18n-attr-aria-label="ui.applicationUtilities">',
            index,
        )
        self.assertIn(
            '<span class="app-utility-label" data-i18n="ui.colorMode">Color mode</span>',
            index,
        )
        self.assertEqual(index.count('id="color-mode-button"'), 1)
        self.assertEqual(index.count('id="color-mode-menu"'), 1)
        self.assertNotIn('class="color-mode-setting"', index)
        self.assertLess(
            index.index('class="app-utility-bar"'),
            index.index('class="primary-navigation card"'),
        )
        self.assertIn(".app-utility-bar {\n  position: absolute;", styles)
        self.assertIn("top: 150px;", styles)
        self.assertIn("top: 96px;", styles)
        self.assertNotIn(".app-utility-bar {\n  width:", styles)
        self.assertIn(".app-utility-content", styles)
        self.assertIn(".app-utility-bar", styles)
        self.assertIn("--table-row-hover-background", styles)
        self.assertIn(
            "--table-sticky-row-background: rgba(255, 255, 255, 0.72);",
            styles,
        )
        self.assertIn(
            ".compact-explore-table .compact-explore-holding {\n  min-width: 300px;",
            styles,
        )
        self.assertIn(
            ".compact-explore-table .compact-explore-holding-name {\n  display: block;\n  min-width: 0;\n  flex: 1 1 auto;\n  max-width: 300px;",
            styles,
        )
        self.assertIn(
            ".compact-explore-table tbody tr:hover .compact-explore-holding {\n  background: var(--table-sticky-row-background);",
            styles,
        )
        self.assertIn(
            ".compact-explore-table tbody tr:nth-child(odd):hover .compact-explore-holding {\n  background: var(--table-sticky-row-alt-background);",
            styles,
        )
        self.assertIn(
            "--table-sticky-row-background: rgba(27, 36, 48, 0.78);",
            styles,
        )

    def test_compact_explore_header_sticks_to_page_and_tracks_horizontal_scroll(
        self,
    ) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn('class="compact-explore-sticky-header" aria-hidden="true"', app)
        self.assertIn("compact-explore-table-body", app)
        self.assertIn("function syncCompactExploreHeader(scrollContainer)", app)
        self.assertIn("translateX(-${scrollContainer.scrollLeft}px)", app)
        self.assertIn("--desktop-navigation-height: 82px;", styles)
        self.assertIn("height: var(--desktop-navigation-height);", styles)
        self.assertIn(
            ".compact-explore-sticky-header {\n  position: sticky;\n  top: var(--desktop-navigation-height);",
            styles,
        )
        mobile_styles = styles[styles.rfind("@media (max-width: 760px)") :]
        self.assertIn("--desktop-navigation-height: 0px;", mobile_styles)
        self.assertIn(
            ".compact-explore-table-scroll {\n  max-width: 100%;\n  overflow-x: auto;",
            styles,
        )
        self.assertIn(".compact-explore-table-semantic-header {", styles)

    def test_compact_explore_holding_header_stays_pinned_during_horizontal_scroll(
        self,
    ) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn(
            "const holdingHeader = headerTable.querySelector('.compact-explore-holding');",
            app,
        )
        self.assertIn(
            "holdingHeader.style.transform = `translateX(${scrollContainer.scrollLeft}px)`;",
            app,
        )

    def test_compact_explore_portfolio_and_fund_headings_are_right_aligned(
        self,
    ) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            'class="compact-explore-number-column compact-explore-total-column"',
            app,
        )
        self.assertIn(
            ".compact-explore-table .compact-explore-number-column {\n  width: 76px;",
            styles,
        )
        self.assertIn(
            ".compact-explore-table .compact-explore-total-column {\n  width: 92px;",
            styles,
        )
        self.assertIn(
            ".compact-explore-table th,\n.compact-explore-table td {\n  padding: 10px 12px;\n  border-bottom: 1px solid var(--border);\n  text-align: right;",
            styles,
        )
        self.assertIn(
            ".compact-explore-table .compact-explore-holding {\n  min-width: 300px;\n  text-align: left;",
            styles,
        )

    def test_compact_explore_search_and_table_preserve_horizontal_scrolling(
        self,
    ) -> None:
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(".company-list {\n  min-width: 0;", styles)
        self.assertIn(
            ".compact-explore-search {\n  width: 100%;\n  min-width: 0;", styles
        )
        self.assertIn(
            ".compact-explore-table-wrap {\n  width: 100%;\n  max-width: 100%;\n  min-width: 0;",
            styles,
        )
        self.assertIn(
            ".compact-explore-table-scroll {\n  max-width: 100%;\n  overflow-x: auto;",
            styles,
        )

    def test_color_mode_documentation_mentions_automatic_and_persistence(self) -> None:
        readme = (WEB_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("Automatic", readme)
        self.assertIn("localStorage", readme)

    def test_compact_explore_supports_ranked_company_search(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="compact-explore-search"', index)
        self.assertIn('id="company-search" type="search"', index)
        self.assertIn('placeholder="Search by company name"', index)
        self.assertIn('id="company-search-clear"', index)
        self.assertIn('aria-label="Clear company search"', index)
        self.assertIn('data-lucide="x"', index)
        self.assertIn("companySearchTerm: '',", app)
        self.assertIn("function buildCompactExploreRow(positions, company, rank)", app)
        self.assertIn(
            'class="compact-explore-rank" aria-label="${t(\'explore.rank\', { rank })}"',
            app,
        )
        self.assertIn(
            "const searchTerm = state.companySearchTerm.trim().toLowerCase();", app
        )
        self.assertIn("company.name.toLowerCase().includes(searchTerm)", app)
        self.assertIn(".map((company, index) => ({ company, rank: index + 1 }))", app)
        self.assertIn("elements.companySearch.addEventListener('input'", app)
        self.assertIn("state.companySearchTerm = event.target.value;", app)
        self.assertIn("function updateCompanySearchClearButton()", app)
        self.assertIn("elements.companySearchClear.addEventListener('click'", app)
        self.assertIn("elements.companySearch.value = '';", app)
        self.assertIn("elements.companySearch.focus();", app)
        self.assertIn(".compact-explore-holding-content", styles)
        self.assertIn(".compact-explore-rank", styles)
        self.assertIn("flex-wrap: nowrap;", styles)
        self.assertIn("white-space: nowrap;", styles)
        self.assertIn(".company-search-clear", styles)
        self.assertIn("width: 44px;", styles)
        self.assertIn("height: 44px;", styles)
        self.assertIn(
            ".company-search-control input::-webkit-search-cancel-button {\n  -webkit-appearance: none;\n  appearance: none;",
            styles,
        )

    def test_standard_explore_uses_the_company_search_filter(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn(
            "const searchTerm = state.companySearchTerm.trim().toLowerCase();", app
        )
        self.assertIn(
            "if (state.activeTab === 'aggregated') {\n      renderCompanyList();\n    }",
            app,
        )
        self.assertIn(
            "elements.companyList.innerHTML = matches\n      .map(({ company, rank }) => buildCompanyRow(company, rank - 1))\n      .join('');",
            app,
        )
        self.assertIn("state.companyVisibleCount = matches.length;", app)
        self.assertIn(
            "elements.companyHint.textContent = t('explore.showingTopHoldings');", app
        )
        self.assertIn("if (state.companyVisibleCount < unfilteredDisplayLimit) {", app)
        self.assertIn("ensureCompanyObserver();", app)

    def test_catalog_search_supports_an_explore_matching_clear_button(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="catalog-search" type="search"', index)
        self.assertIn('id="catalog-search-clear"', index)
        self.assertIn('aria-label="Clear ETF catalog search"', index)
        self.assertIn('data-lucide="x"', index)
        self.assertIn(
            "elements.catalogSearchClear = document.getElementById('catalog-search-clear');",
            app,
        )
        self.assertIn("function updateSearchClearButton(input, button)", app)
        self.assertIn("button.hidden = !input.value;", app)
        self.assertIn("elements.catalogSearch.addEventListener('input'", app)
        self.assertIn(
            "updateSearchClearButton(elements.catalogSearch, elements.catalogSearchClear);",
            app,
        )
        self.assertIn("elements.catalogSearchClear.addEventListener('click'", app)
        self.assertIn("elements.catalogSearch.value = '';", app)
        self.assertIn("state.searchTerm = '';", app)
        self.assertIn("elements.catalogSearch.focus();", app)
        self.assertIn("const term = state.searchTerm.trim().toLowerCase();", app)
        self.assertIn(
            ".company-search-control input::-webkit-search-cancel-button", styles
        )
        self.assertIn(".company-search-clear[hidden]", styles)

    def test_added_catalog_button_uses_outlined_status_presentation(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            "const selected = state.portfolio.some((position) => position.isin === entry.isin);",
            app,
        )
        self.assertIn('data-state="added" disabled', app)
        self.assertIn("${selected ? t('catalog.added') : t('catalog.add')}", app)
        self.assertIn("function addPosition(isin)", app)
        self.assertIn(
            "if (state.portfolio.some((position) => position.isin === isin)) {",
            app,
        )
        self.assertIn(".catalog-item button[data-state='added']", styles)
        self.assertIn("border: 2px solid var(--accent) !important;", styles)
        self.assertIn("color: var(--accent) !important;", styles)
        self.assertIn("background: #ffffff !important;", styles)
        self.assertIn("opacity: 1;", styles)

    def test_saxo_pdf_import_contract_covers_review_and_value_weighting(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        share = (WEB_ROOT / "share.js").read_text(encoding="utf-8")
        importer = (WEB_ROOT / "portfolio-import.js").read_text(encoding="utf-8")

        self.assertIn('src="./vendor/pdf.min.js"', index)
        self.assertIn('id="portfolio-import-file"', index)
        self.assertIn('accept="application/pdf,.pdf"', index)
        self.assertIn('id="portfolio-import-dialog"', index)
        self.assertIn('id="portfolio-import-confirm"', index)
        self.assertIn("extractPdfPages", app)
        self.assertIn("matchImportedRows", app)
        self.assertIn("state.portfolio = positions;", app)
        self.assertIn("valueChf", app)
        self.assertIn("function normalizePortfolioPositions", app)
        self.assertIn(
            "position.value != null && Number.isFinite(Number(position.value))", app
        )
        self.assertIn(
            "position.valueChf != null && Number.isFinite(Number(position.valueChf))",
            app,
        )
        self.assertIn(
            "position.valueChf != null && Number.isFinite(Number(position.valueChf))",
            share,
        )
        self.assertIn("function parseSaxoPages", importer)
        self.assertIn("bestande", importer)
        self.assertNotIn("EUR_TO_CHF_RATE = 1", importer)
        self.assertIn("SUPPORTED_CURRENCIES = new Set(['CHF', 'EUR', 'USD'])", importer)
        self.assertIn("matchStatus: entry ? 'matched' : 'unmatched'", importer)
        self.assertIn(
            "new URL('./vendor/pdf.worker.min.js', import.meta.url).href", importer
        )

    def test_global_color_mode_preserves_existing_behavior_hooks(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn("const COLOR_MODES = ['bright', 'automatic', 'dark'];", app)
        self.assertIn("function saveColorMode()", app)
        self.assertIn("function positionColorModeControl()", app)
        self.assertIn(".eyebrow, .panel-heading .section-label", app)
        self.assertIn("titleContainer = title?.closest('.hero, .panel-heading')", app)
        self.assertIn("positionColorModeControl();", app)
        self.assertIn(
            "localStorage.setItem(COLOR_MODE_STORAGE_KEY, state.colorMode)", app
        )
        self.assertIn("function handleSystemColorModeChange()", app)
        self.assertIn("renderComparisonCharts();", app)
        self.assertIn("const modes = [", app)
        self.assertIn(
            "{ key: 'bright', labelKey: 'colorMode.bright', icon: 'sun' }", app
        )
        self.assertIn(
            "{ key: 'automatic', labelKey: 'colorMode.automatic', icon: 'monitor' }",
            app,
        )
        self.assertIn("{ key: 'dark', labelKey: 'colorMode.dark', icon: 'moon' }", app)
        self.assertIn('role="menu" aria-label="Color mode"', index)
        self.assertIn('role="menuitemradio"', app)
        self.assertIn(
            "  .color-mode-button > span {\n    display: none;\n  }",
            styles,
        )
        self.assertLess(
            styles.index("  .color-mode-button > span {"),
            styles.index("  body {", styles.index("@media (max-width: 760px) {")),
        )
        self.assertIn(
            "<span>${selectedLabel}</span>",
            app,
        )
        self.assertIn(
            "<span>${t(mode.labelKey)}</span>",
            app,
        )
        self.assertIn('title="Change color mode"', index)

    def test_desktop_color_mode_clearance_preserves_mobile_boundary(self) -> None:
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        desktop_start = styles.index("@media (min-width: 761px) {")
        desktop_end = styles.index(".primary-navigation {", desktop_start)
        desktop_styles = styles[desktop_start:desktop_end]
        self.assertIn(
            ".home-panel .hero-meta {\n    padding-top: 54px;", desktop_styles
        )
        self.assertIn(
            "#portfolio-panel .panel-heading {\n    margin-bottom: 37px;",
            desktop_styles,
        )
        self.assertIn(
            "#portfolio-panel .panel-heading > .inline-note {\n    transform: translateY(37px);",
            desktop_styles,
        )
        self.assertIn(
            "#comparison-panel .panel-heading,\n  #aggregated-panel .panel-heading {\n    margin-bottom: 37px;",
            desktop_styles,
        )
        self.assertIn(
            "#comparison-panel .panel-heading > .panel-copy,\n  #aggregated-panel .panel-heading > .panel-copy {\n    transform: translateY(37px);",
            desktop_styles,
        )

        mobile_styles = styles[styles.index("@media (max-width: 760px)") :]
        self.assertNotIn("padding-top: 54px;", mobile_styles)
        self.assertNotIn("translateY(37px);", mobile_styles)

    def test_dark_navigation_uses_a_theme_gradient(self) -> None:
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            "--navigation-background: var(--card);",
            styles,
        )
        self.assertIn(
            "--navigation-background: rgba(23, 30, 40, 0.92);",
            styles,
        )
        self.assertIn(
            ".primary-navigation {\n  position: sticky;",
            styles,
        )
        self.assertIn(
            "  border: 0;\n  border-radius: 0 0 var(--radius) var(--radius);",
            styles,
        )
        self.assertNotIn(
            "    border-top: 1px solid var(--border);\n    background: var(--navigation-background);",
            styles,
        )
        self.assertIn("  background: var(--navigation-background);", styles)
        self.assertIn(
            ":root[data-color-mode='dark'] .primary-navigation::after {",
            styles,
        )
        self.assertIn(
            "    background: linear-gradient(0deg, var(--table-header-background), transparent);",
            styles,
        )
        self.assertIn(
            "    height: 9px;\n    background: linear-gradient(0deg, var(--table-header-background), transparent);",
            styles,
        )
        self.assertNotIn(
            ":root[data-color-mode='bright'] .primary-navigation::after {",
            styles,
        )
        self.assertIn(
            ":root[data-color-mode='bright'] .primary-navigation {\n    background: #ffffff;",
            styles,
        )
        self.assertIn(
            ":root[data-color-mode='dark'] .primary-navigation {\n    background: var(--card-strong);",
            styles,
        )

    def test_mobile_navigation_feedback_preserves_tab_activation(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn(
            ".primary-navigation .tab-button {\n  -webkit-tap-highlight-color: transparent;",
            styles,
        )
        self.assertIn(
            ".primary-navigation .tab-button:focus-visible {\n  outline: 3px solid var(--focus-ring);\n  outline-offset: 2px;",
            styles,
        )
        self.assertIn(
            "  .primary-navigation .tab-button:active {\n    background: color-mix(in srgb, var(--accent) 14%, transparent);",
            styles,
        )

        set_tab_start = app.index("function setTab(tabName) {")
        set_tab_end = app.index("\nfunction addPosition", set_tab_start)
        set_tab = app[set_tab_start:set_tab_end]
        self.assertIn("button.classList.toggle('active', isActive);", set_tab)
        self.assertIn("button.setAttribute('aria-current', 'page');", set_tab)
        self.assertIn(
            "panel.classList.toggle('active', panel.dataset.panel === state.activeTab);",
            set_tab,
        )


if __name__ == "__main__":
    unittest.main()

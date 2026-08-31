from pathlib import Path
import re
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPOSITORY_ROOT / "web"


class WebContractTests(unittest.TestCase):
    def test_publish_script_includes_app_local_javascript_modules(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        publish_script = (
            REPOSITORY_ROOT / "scripts" / "publish-gh-pages.ps1"
        ).read_text(encoding="utf-8")

        imported_modules = re.findall(r"from ['\"]\./([^'\"]+\.js)['\"]", app)
        for module in imported_modules:
            self.assertTrue((WEB_ROOT / module).is_file())
            self.assertIn(f"'{module}'", publish_script)

    def test_portfolio_ui_polish_contract_covers_provenance_and_presentation(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="build-data-title"', index)
        self.assertIn('id="build-data"', index)
        self.assertIn("function renderBuildData()", app)
        self.assertIn("entry.snapshotPath || 'Unavailable'", app)
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
            "{ label: 'Share units', value: formatCount(shareCountTotal) }", app
        )
        self.assertIn("function formatChfValue(value)", app)
        self.assertIn('replace(/,/g, "\'")', app)
        self.assertIn("{ label: 'Total value', value: totalValueChf }", app)
        self.assertIn("value >= 0", app)
        self.assertIn("'Unavailable'", app)

    def test_portfolio_sharing_contract_covers_encoding_loading_and_feedback(
        self,
    ) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertIn("const SHARE_FRAGMENT_KEY = 'portfolio';", app)
        self.assertIn("const SHARE_PAYLOAD_VERSION = 1;", app)
        self.assertIn("function encodePortfolioShare(portfolio)", app)
        self.assertIn("function decodePortfolioShare(value)", app)
        self.assertIn("Number.isFinite(position.shares)", app)
        self.assertIn("seenIsins.has(isin)", app)
        self.assertIn("readPortfolioShareFromUrl()", app)
        self.assertIn("sharedPortfolio.status === 'valid'", app)
        self.assertIn("state.portfolio = loadPortfolioState();", app)
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
        self.assertIn('id="share-portfolio-url"', index)
        self.assertIn("navigator.clipboard?.writeText", app)
        self.assertIn("latest published ETF data", app)
        self.assertIn(".share-portfolio-button", styles)
        self.assertIn(".portfolio-sharing", styles)

    def test_selected_positions_have_mobile_and_accessibility_hooks(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertNotIn('id="warning-list"', index)
        self.assertIn('id="build-warning-list"', index)
        self.assertIn('id="build-warnings-title"', index)
        self.assertIn('data-label="ETF"', app)
        self.assertIn('data-label="Shares"', app)
        self.assertIn('data-label="Weight"', app)
        self.assertIn(
            "return (getPositionWeightBase(position) / totalShareUnits) * 100;", app
        )
        self.assertIn('data-label="Remove"', app)
        self.assertIn(
            'data-label="Weight" aria-label="Weight ${formatPercent(weight)}">${formatPercent(weight)}</td>',
            app,
        )
        self.assertIn('aria-label="Remove ${position.entry.ticker}"', app)
        self.assertIn('title="Remove ${position.entry.ticker}"', app)
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

    def test_build_dialog_retains_current_selection_warnings(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn("function getCurrentSelectionWarnings", app)
        self.assertIn("getCurrentSelectionWarnings()", app)
        self.assertIn("renderWarningItems(", app)
        self.assertIn("elements.buildWarningList", app)

    def test_warning_count_only_includes_incomplete_match_statuses(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn(
            "const INCOMPLETE_MATCH_STATUSES = new Set(['ambiguous', 'unmatched']);",
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
            '<header class="app-utility-bar" aria-label="Application utilities">', index
        )
        self.assertIn('<span class="app-utility-label">Color mode</span>', index)
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
        self.assertIn('class="compact-explore-rank" aria-label="Rank ${rank}"', app)
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

    def test_saxo_pdf_import_contract_covers_review_and_value_weighting(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        importer = (WEB_ROOT / "portfolio-import.js").read_text(encoding="utf-8")

        self.assertIn(
            "cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js", index
        )
        self.assertIn('id="portfolio-import-file"', index)
        self.assertIn('accept="application/pdf,.pdf"', index)
        self.assertIn('id="portfolio-import-dialog"', index)
        self.assertIn('id="portfolio-import-confirm"', index)
        self.assertIn("extractPdfPages", app)
        self.assertIn("matchImportedRows", app)
        self.assertIn("state.portfolio = positions;", app)
        self.assertIn("valueChf", app)
        self.assertIn("function normalizePortfolioPositions", app)
        self.assertIn("function parseSaxoPages", importer)
        self.assertIn("bestande", importer)
        self.assertIn("EUR_TO_CHF_RATE = 1", importer)
        self.assertIn("matchStatus: entry ? 'matched' : 'unmatched'", importer)
        self.assertIn("pdf.worker.min.js", importer)

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
        self.assertIn("{ key: 'bright', label: 'Bright', icon: 'sun' }", app)
        self.assertIn("{ key: 'automatic', label: 'Automatic', icon: 'monitor' }", app)
        self.assertIn("{ key: 'dark', label: 'Dark', icon: 'moon' }", app)
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
            "<span>${selectedMode.label}</span>",
            app,
        )
        self.assertIn(
            "<span>${mode.label}</span>",
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


if __name__ == "__main__":
    unittest.main()

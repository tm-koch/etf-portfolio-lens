from pathlib import Path
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPOSITORY_ROOT / "web"


class WebContractTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()

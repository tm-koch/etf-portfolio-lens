from pathlib import Path
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPOSITORY_ROOT / "web"


class WebContractTests(unittest.TestCase):
    def test_selected_positions_have_mobile_and_accessibility_hooks(self) -> None:
        index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

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

    def test_warning_surfaces_share_current_selection_collection(self) -> None:
        app = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn("function getCurrentSelectionWarnings", app)
        self.assertIn("getCurrentSelectionWarnings()", app)
        self.assertIn("renderWarningItems(", app)
        self.assertIn("elements.warningList", app)
        self.assertIn("elements.buildWarningList", app)


if __name__ == "__main__":
    unittest.main()

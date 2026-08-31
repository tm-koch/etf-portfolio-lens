import json
import subprocess
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
IMPORTER_MODULE = (REPOSITORY_ROOT / "web" / "portfolio-import.js").as_uri()


class PortfolioImportTests(unittest.TestCase):
    def run_node(self, expression: str) -> object:
        result = subprocess.run(
            ["node", "--input-type=module", "-e", expression],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_saxo_holdings_row_extracts_german_values(self) -> None:
        text = (
            "Saxo Bank CH Transaktions- und Saldenbericht "
            "Bestände - (80000/187640), CHF "
            "iShares Core SPI (CH) ETF (ISIN: CH0237935652) "
            "CHSPI:xswx 7612485271 CHF 29-Mai-2026 178 1,0000 "
            "157,9644 172,0200 8,90 % 2.501,90 30.619,56"
        )
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages([{json.dumps({'pageNumber': 3, 'text': text})}])));"
        )
        rows = self.run_node(expression)
        self.assertEqual(rows[0]["isin"], "CH0237935652")
        self.assertEqual(rows[0]["shares"], 178)
        self.assertEqual(rows[0]["price"], 172.02)
        self.assertEqual(rows[0]["value"], 30619.56)

    def test_saxo_parser_rejects_non_saxo_text(self) -> None:
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            "try { parseSaxoPages([{pageNumber: 1, text: 'not a broker report'}]); "
            "console.log(JSON.stringify(false)); } catch { console.log(JSON.stringify(true)); }"
        )
        self.assertTrue(self.run_node(expression))

    def test_saxo_parser_accepts_split_hyphen_and_composed_umlaut_markers(self) -> None:
        text = (
            "Saxo Bank CH Transaktions - und Salden\u00adbericht "
            "Best\u00e4nde - EUR iShares MSCI Europe ETF (ISIN: IE00BF20LF40) "
            "EUMD:xlon 7655678456 EUR 30-Jun-2026 1.429 1,0000 "
            "9,4228 10,5700 12,18 % 1.639,39 15.104,53"
        )
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages([{json.dumps({'pageNumber': 8, 'text': text})}])));"
        )
        rows = self.run_node(expression)
        self.assertEqual(rows[0]["isin"], "IE00BF20LF40")
        self.assertEqual(rows[0]["shares"], 1429)

    def test_saxo_parser_extracts_values_without_ticker_prefix(self) -> None:
        text = (
            "Saxo Bank CH Transaktions- und Saldenbericht Bestände CHF "
            "ETF (ISIN: CH0237935652) CHSPI:xswx CHF 29-Mai-2026 178 1,0000 "
            "157,9644 172,0200 8,90 % 2.501,90 30.619,56"
        )
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages([{json.dumps({'pageNumber': 3, 'text': text})}])));"
        )
        rows = self.run_node(expression)
        self.assertEqual(rows[0]["shares"], 178)
        self.assertEqual(rows[0]["price"], 172.02)
        self.assertEqual(rows[0]["value"], 30619.56)

    def test_saxo_parser_accepts_dot_decimal_prices(self) -> None:
        text = (
            "Saxo Bank CH Transaktions- und Saldenbericht Bestände CHF "
            "ETF (ISIN: CH0237935652) CHSPI:xswx CHF 29-Mai-2026 178 1.0000 "
            "157.9644 172.0200 8.90 % 2,501.90 30,619.56"
        )
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages([{json.dumps({'pageNumber': 3, 'text': text})}])));"
        )
        rows = self.run_node(expression)
        self.assertEqual(rows[0]["shares"], 178)
        self.assertEqual(rows[0]["price"], 172.02)

    def test_saxo_parser_accepts_split_numeric_text_items(self) -> None:
        text = (
            "Saxo Bank CH Transaktions- und Saldenbericht Bestände CHF "
            "ETF (ISIN: CH0237935652) CHF 29. Mai 2026 178 1 , 0000 "
            "157 , 9644 172 , 0200 8 , 90 % 2 . 501 , 90 30 . 619 , 56"
        )
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages([{json.dumps({'pageNumber': 3, 'text': text})}])));"
        )
        rows = self.run_node(expression)
        self.assertEqual(rows[0]["shares"], 178)
        self.assertEqual(rows[0]["price"], 172.02)

    def test_supplied_saxo_report_rows_wrap_after_isin(self) -> None:
        pages = [
            {
                "pageNumber": 3,
                "text": (
                    "Saxo Bank CH Transaktions- und Saldenbericht\n"
                    "Bestände - (80000/187640), CHF\n"
                    "Börsengehandelte Produkte (ETF, ETC, ETN)\n"
                    "ETF (ISIN: CH0237935652)\n"
                    "CHSPI:xswx 7612485271 CHF 29-Mai-2026 178 1,0000 157,9644 "
                    "172,0200 8,90 % 2.501,90 30.619,56\n"
                    "UBS SPI(R) Mid ETF (ISIN: CH0130595124)\n"
                    "SPMCHA:xswx 7655679247 CHF 30-Jun-2026 227 1,0000 126,9828 "
                    "135,3400 6,58 % 1.897,08 30.722,18\n"
                    "State St SPDR MSCI AllCountryWorld (Acc) UCITS ETF (ISIN: IE00B44Z5B48)\n"
                    "ACWI:xswx 7655679248 CHF 30-Jun-2026 62 1,0000 241,4395 "
                    "266,3500 10,32 % 1.544,45 16.513,70"
                ),
            },
            {
                "pageNumber": 8,
                "text": (
                    "Saxo Bank CH Transaktions- und Saldenbericht\n"
                    "Bestände - EUR (80000/202685), EUR\n"
                    "Amundi Core Stoxx Europe 600 (Acc) UCITS ETF (ISIN: LU0908500753)\n"
                    "LYP6:xetr 7650468996 EUR 25-Jun-2026 46 1,0000 292,0413 "
                    "321,2500 10,00 % 1.343,60 14.777,50\n"
                    "iShares MSCI Europe Mid Cap UCITS ETF (ISIN: IE00BF20LF40)\n"
                    "EUMD:xlon 7655678456 EUR 30-Jun-2026 1.429 1,0000 9,4228 "
                    "10,5700 12,18 % 1.639,39 15.104,53"
                ),
            },
        ]
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages({json.dumps(pages)})));"
        )
        rows = self.run_node(expression)
        self.assertEqual(
            [(row["isin"], row["shares"], row["price"], row["value"]) for row in rows],
            [
                ("CH0237935652", 178, 172.02, 30619.56),
                ("CH0130595124", 227, 135.34, 30722.18),
                ("IE00B44Z5B48", 62, 266.35, 16513.7),
                ("LU0908500753", 46, 321.25, 14777.5),
                ("IE00BF20LF40", 1429, 10.57, 15104.53),
            ],
        )

    def test_attached_pdfjs_text_extracts_all_supplied_holdings(self) -> None:
        source = (REPOSITORY_ROOT / "data" / "etf-lens-pdfjs-text.txt").read_text(
            encoding="utf-8"
        )
        pages = []
        for page_number in (1, 3, 8):
            start = source.index(f"--- Page {page_number} ---") + len(
                f"--- Page {page_number} ---\n"
            )
            end_marker = f"\n\n--- Page {page_number + 1} ---"
            end = (
                source.index(end_marker, start)
                if end_marker in source[start:]
                else len(source)
            )
            pages.append({"pageNumber": page_number, "text": source[start:end]})
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages({json.dumps(pages)})));"
        )
        rows = self.run_node(expression)
        self.assertEqual(
            [(row["isin"], row["shares"], row["price"], row["value"]) for row in rows],
            [
                ("XX0000000001", 12, 12.0, 144.0),
                ("XX0000000002", 23, 23.0, 529.0),
                ("XX0000000003", 34, 34.0, 1156.0),
                ("XX0000000004", 45, 45.0, 2025.0),
                ("XX0000000005", 56, 56.0, 3136.0),
            ],
        )

    def test_pdf_text_items_are_reconstructed_in_visual_order(self) -> None:
        items = [
            {
                "str": "1,0000 157,9644 172,0200 8,90 % 2.501,90 30.619,56",
                "transform": [1, 0, 0, 1, 500, 700],
            },
            {
                "str": "Saxo Bank CH Transaktions- und Saldenbericht Bestände CHF",
                "transform": [1, 0, 0, 1, 40, 760],
            },
            {"str": "CHSPI:xswx", "transform": [1, 0, 0, 1, 220, 700]},
            {"str": "178", "transform": [1, 0, 0, 1, 400, 700]},
            {"str": "ETF (ISIN: CH0237935652)", "transform": [1, 0, 0, 1, 40, 700]},
            {"str": "CHF 29-Mai-2026", "transform": [1, 0, 0, 1, 300, 700]},
        ]
        expression = (
            f"import {{extractPdfPages, parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"const items = {json.dumps(items)}; "
            "const pdfjs = {GlobalWorkerOptions: {}, getDocument: () => ({promise: Promise.resolve({numPages: 1, getPage: async () => ({getTextContent: async () => ({items})})})})}; "
            "extractPdfPages({arrayBuffer: async () => new ArrayBuffer(0)}, pdfjs).then((pages) => console.log(JSON.stringify(parseSaxoPages(pages))));"
        )
        rows = self.run_node(expression)
        self.assertEqual(rows[0]["shares"], 178)
        self.assertEqual(rows[0]["price"], 172.02)
        self.assertEqual(rows[0]["value"], 30619.56)

    def test_adjacent_rows_keep_their_own_values(self) -> None:
        text = (
            "Saxo Bank CH Transaktions- und Saldenbericht Bestände CHF "
            "ETF (ISIN: CH0237935652) CHSPI:xswx CHF 29-Mai-2026 178 1,0000 "
            "157,9644 172,0200 8,90 % 2.501,90 30.619,56 "
            "ETF (ISIN: CH0130595124) CHSPI:xswx CHF 29-Mai-2026 227 1,0000 "
            "120,0000 135,3400 8,90 % 2.501,90 30.722,18"
        )
        expression = (
            f"import {{parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"console.log(JSON.stringify(parseSaxoPages([{json.dumps({'pageNumber': 3, 'text': text})}])));"
        )
        rows = self.run_node(expression)
        self.assertEqual(
            [(row["shares"], row["price"]) for row in rows],
            [(178, 172.02), (227, 135.34)],
        )

    def test_footer_numbers_are_not_used_for_holding_values(self) -> None:
        items = [
            {
                "str": "Saxo Bank CH Transaktions- und Saldenbericht Bestände CHF",
                "transform": [1, 0, 0, 1, 40, 760],
            },
            {
                "str": "ETF (ISIN: CH0237935652) CHF 29-Mai-2026 178 1,0000 157,9644 172,0200 8,90 % 2.501,90 30.619,56",
                "transform": [1, 0, 0, 1, 40, 700],
            },
            {
                "str": "Konto 8000012345 31-Dez-2025 999 1,0000 1,00 2,00 3,00 % 4,00 5,00",
                "transform": [1, 0, 0, 1, 40, 650],
            },
        ]
        expression = (
            f"import {{extractPdfPages, parseSaxoPages}} from '{IMPORTER_MODULE}'; "
            f"const items = {json.dumps(items)}; "
            "const pdfjs = {GlobalWorkerOptions: {}, getDocument: () => ({promise: Promise.resolve({numPages: 1, getPage: async () => ({getTextContent: async () => ({items})})})})}; "
            "extractPdfPages({arrayBuffer: async () => new ArrayBuffer(0)}, pdfjs).then((pages) => console.log(JSON.stringify(parseSaxoPages(pages))));"
        )
        rows = self.run_node(expression)
        self.assertEqual(rows[0]["shares"], 178)
        self.assertEqual(rows[0]["price"], 172.02)
        self.assertEqual(rows[0]["value"], 30619.56)

    def test_unmatched_isin_is_not_included(self) -> None:
        expression = (
            f"import {{matchImportedRows}} from '{IMPORTER_MODULE}'; "
            "const rows = matchImportedRows([{isin: 'XX0000000000', warnings: []}], "
            "{byIsin: new Map()}); console.log(JSON.stringify(rows[0]));"
        )
        row = self.run_node(expression)
        self.assertEqual(row["matchStatus"], "unmatched")
        self.assertFalse(row["included"])


if __name__ == "__main__":
    unittest.main()

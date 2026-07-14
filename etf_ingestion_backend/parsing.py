from __future__ import annotations

import csv
import io
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


@dataclass(slots=True)
class ParsedTable:
    headers: list[str]
    rows: list[dict[str, Any]]
    as_of: str | None = None
    title: str | None = None


def _normalize_header(text: str) -> str:
    return " ".join(text.strip().split())


def _find_header_index(rows: list[list[str]]) -> int:
    for index, row in enumerate(rows):
        normalized = {
            _normalize_header(cell).casefold() for cell in row if cell.strip()
        }
        if {"ticker", "name"}.issubset(normalized):
            return index
        if {"isin code", "name"}.issubset(normalized):
            return index
        if {"isin", "security name"}.issubset(normalized):
            return index
        if {"isin", "name"}.issubset(normalized):
            return index
        if {"securities", "isin"}.issubset(normalized):
            return index
    raise ValueError("Could not find holdings header row")


def _rows_to_dicts(
    rows: list[list[str]], stop_at_empty_row: bool = False
) -> ParsedTable:
    header_index = _find_header_index(rows)
    headers = [_normalize_header(cell) for cell in rows[header_index]]
    table_rows: list[dict[str, Any]] = []
    for row in rows[header_index + 1 :]:
        if not any(cell.strip() for cell in row):
            if stop_at_empty_row:
                break
            continue
        padded = row + [""] * (len(headers) - len(row))
        table_rows.append({headers[idx]: padded[idx] for idx in range(len(headers))})
    return ParsedTable(headers=headers, rows=table_rows)


def parse_csv_bytes(data: bytes) -> ParsedTable:
    text = data.decode("utf-8-sig", errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    header_index = _find_header_index([line.split(",") for line in lines])
    stream = io.StringIO("\n".join(lines[header_index:]))
    reader = csv.DictReader(stream)
    rows = [
        dict(row)
        for row in reader
        if any((value or "").strip() for value in row.values())
    ]
    return ParsedTable(
        headers=[_normalize_header(name) for name in reader.fieldnames or []], rows=rows
    )


def parse_csv_file(path: Path) -> ParsedTable:
    return parse_csv_bytes(path.read_bytes())


def parse_xml_spreadsheet_bytes(data: bytes) -> ParsedTable:
    root = ET.fromstring(data)
    namespace = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}
    rows: list[list[str]] = []
    for row in root.findall(".//ss:Worksheet/ss:Table/ss:Row", namespace):
        cells: list[str] = []
        for cell in row.findall("ss:Cell", namespace):
            data_node = cell.find("ss:Data", namespace)
            cells.append(
                (
                    data_node.text
                    if data_node is not None and data_node.text is not None
                    else ""
                ).strip()
            )
        rows.append(cells)
    return _rows_to_dicts(rows, stop_at_empty_row=True)


def parse_xml_spreadsheet_file(path: Path) -> ParsedTable:
    return parse_xml_spreadsheet_bytes(path.read_bytes())


def _col_to_index(col_ref: str) -> int:
    value = 0
    for char in col_ref:
        if not char.isalpha():
            break
        value = value * 26 + (ord(char.upper()) - 64)
    return value - 1


def _parse_xlsx_sheet(
    xml_bytes: bytes,
    shared_strings: list[str],
    stop_at_empty_row: bool = False,
) -> list[list[str]]:
    root = ET.fromstring(xml_bytes)
    namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows: list[list[str]] = []
    for row in root.findall(".//a:sheetData/a:row", namespace):
        values: dict[int, str] = {}
        max_index = -1
        for cell in row.findall("a:c", namespace):
            ref = cell.attrib.get("r", "A1")
            index = _col_to_index("".join(ch for ch in ref if ch.isalpha()))
            max_index = max(max_index, index)
            cell_type = cell.attrib.get("t")
            value_node = cell.find("a:v", namespace)
            inline_node = cell.find("a:is/a:t", namespace)
            if inline_node is not None and inline_node.text is not None:
                values[index] = inline_node.text
            elif value_node is not None and value_node.text is not None:
                if cell_type == "s":
                    shared_index = int(value_node.text)
                    values[index] = (
                        shared_strings[shared_index]
                        if shared_index < len(shared_strings)
                        else ""
                    )
                else:
                    values[index] = value_node.text
            else:
                values[index] = ""
        parsed_row = [values.get(i, "") for i in range(max_index + 1)]
        if stop_at_empty_row and not any(cell.strip() for cell in parsed_row):
            break
        rows.append(parsed_row)
    return rows


def _load_xlsx_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        shared_xml = archive.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    if not shared_xml:
        return []
    shared_root = ET.fromstring(shared_xml)
    namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    shared_strings: list[str] = []
    for item in shared_root.findall(".//a:si", namespace):
        text = "".join(node.text or "" for node in item.findall(".//a:t", namespace))
        shared_strings.append(text)
    return shared_strings


def _resolve_xlsx_sheet_paths(archive: zipfile.ZipFile) -> list[str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    namespace = {
        "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    rels_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rel_targets = {
        rel.attrib.get("Id"): rel.attrib.get("Target")
        for rel in rels_root
        if rel.attrib.get("Id") and rel.attrib.get("Target")
    }

    sheet_paths: list[str] = []
    for sheet in workbook.findall(".//a:sheets/a:sheet", namespace):
        rel_id = sheet.attrib.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )
        target = rel_targets.get(rel_id)
        if not target:
            continue
        sheet_paths.append(
            target.lstrip("/") if target.startswith("/") else f"xl/{target}"
        )
    return sheet_paths


def parse_xlsx_bytes(data: bytes, stop_at_empty_row: bool = False) -> ParsedTable:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        shared_strings = _load_xlsx_shared_strings(archive)
        last_error: ValueError | None = None
        for sheet_path in _resolve_xlsx_sheet_paths(archive):
            rows = _parse_xlsx_sheet(
                archive.read(sheet_path),
                shared_strings,
                stop_at_empty_row=stop_at_empty_row,
            )
            try:
                return _rows_to_dicts(rows)
            except ValueError as exc:
                last_error = exc
                continue
    if last_error:
        raise last_error
    raise ValueError("Could not find holdings header row")


def parse_xlsx_file(path: Path) -> ParsedTable:
    return parse_xlsx_bytes(path.read_bytes())


def parse_table(path: Path, stop_at_empty_row: bool = False) -> ParsedTable:
    raw = path.read_bytes()
    if raw.startswith(b"PK"):
        return parse_xlsx_bytes(raw, stop_at_empty_row=stop_at_empty_row)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return parse_csv_bytes(raw)
    if suffix == ".xls":
        return parse_xml_spreadsheet_bytes(raw)
    if suffix == ".xlsx":
        return parse_xlsx_bytes(raw, stop_at_empty_row=stop_at_empty_row)
    raise ValueError(f"Unsupported source format: {path.suffix}")

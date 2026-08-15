from __future__ import annotations

import html.parser
import json
import mimetypes
import re
import shutil
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class DownloadedSource:
    source_path: Path
    download_path: Path
    content_type: str | None
    source_format: str | None = None


AMUNDI_PRODUCT_API_URL = "https://www.amundietf.ch/mapi/ProductAPI/getProductsData"
AMUNDI_COMPOSITION_FIELDS = [
    "date",
    "type",
    "bbg",
    "isin",
    "name",
    "weight",
    "quantity",
    "currency",
    "sector",
    "country",
    "countryOfRisk",
]
DEFAULT_AMUNDI_CONTEXT = {
    "countryCode": "CHE",
    "countryName": "Switzerland",
    "googleCountryCode": "CH",
    "domainName": "www.amundietf.ch",
    "bcp47Code": "en-GB",
    "languageName": "English",
    "gtmCode": "GTM-57M8WTF",
    "languageCode": "en",
    "userProfileName": "INSTIT",
    "userProfileSlug": "instit",
    "portalProfileName": None,
    "portalProfileSlug": None,
}


class AmundiHoldingsError(ValueError):
    """Raised when Amundi does not return a complete holdings composition."""


class _HrefExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value:
                self.links.append(value)


def _ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _safe_name(value: str, fallback: str) -> str:
    value = value.strip()
    if not value:
        return fallback
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value.strip("._") or fallback


def _guess_extension(url: str, content_type: str | None = None) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix
    if suffix:
        return suffix
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
        if guessed:
            return guessed
    return ".bin"


def _is_html(content_type: str | None, url: str) -> bool:
    if content_type and "html" in content_type.lower():
        return True
    return Path(urllib.parse.urlparse(url).path).suffix.lower() in {".html", ".htm"}


def _extract_download_link(base_url: str, html_text: str) -> str | None:
    parser = _HrefExtractor()
    parser.feed(html_text)
    for link in parser.links:
        lowered = link.lower()
        if (
            any(ext in lowered for ext in (".csv", ".xls", ".xlsx"))
            or "download" in lowered
        ):
            return urllib.parse.urljoin(base_url, link)
    return None


def fetch_url(
    url: str, destination_dir: Path, preferred_name: str | None = None
) -> DownloadedSource:
    _ensure_directory(destination_dir)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request) as response:
        content_type = response.headers.get_content_type()
        data = response.read()

    extension = _guess_extension(url, content_type)
    filename = _safe_name(
        preferred_name or Path(urllib.parse.urlparse(url).path).stem or "download",
        "download",
    )
    source_path = destination_dir / f"{filename}{extension}"
    source_path.write_bytes(data)

    if _is_html(content_type, url):
        html_text = data.decode("utf-8", errors="replace")
        linked = _extract_download_link(url, html_text)
        if linked:
            return fetch_url(
                linked,
                destination_dir,
                preferred_name=Path(urllib.parse.urlparse(linked).path).stem
                or filename,
            )

    return DownloadedSource(
        source_path=source_path, download_path=source_path, content_type=content_type
    )


def fetch_amundi_full_holdings(
    isin: str,
    destination_dir: Path,
    context: dict[str, str] | None = None,
) -> tuple[DownloadedSource, list[dict[str, object]]]:
    _ensure_directory(destination_dir)
    request_body = {
        "context": {**DEFAULT_AMUNDI_CONTEXT, **(context or {})},
        "productIds": [isin],
        "characteristics": ["ISIN", "TICKER", "FUND_FUND_NAME"],
        "historics": [],
        "metrics": [],
        "breakDown": {"aggregationFields": ["FUND_TOP10"]},
        "productType": "PRODUCT",
        "composition": {"compositionFields": AMUNDI_COMPOSITION_FIELDS},
    }
    request = urllib.request.Request(
        AMUNDI_PRODUCT_API_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        content_type = response.headers.get_content_type()
        data = response.read()

    if content_type and "json" not in content_type.lower():
        raise AmundiHoldingsError(
            f"Amundi holdings response is not JSON: {content_type}"
        )
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AmundiHoldingsError("Amundi holdings response is not valid JSON") from exc

    products = payload.get("products") if isinstance(payload, dict) else None
    product = next(
        (item for item in products or [] if item.get("productId") == isin), None
    )
    composition = product.get("composition") if product else None
    rows = composition.get("compositionData") if composition else None
    total = composition.get("totalNumberOfInstruments") if composition else None
    if not isinstance(rows, list) or not isinstance(total, int):
        raise AmundiHoldingsError("Amundi response has no complete composition data")
    if total <= 10 or len(rows) != total:
        raise AmundiHoldingsError(
            f"Amundi composition is incomplete: expected {total}, received {len(rows)}"
        )

    normalized_rows: list[dict[str, object]] = []
    required = {"isin", "name", "weight"}
    for index, item in enumerate(rows):
        characteristics = item.get("compositionCharacteristics", {})
        if not required.issubset(characteristics):
            raise AmundiHoldingsError(
                f"Amundi composition row {index} is missing required fields"
            )
        normalized_rows.append(
            {
                "ISIN code": characteristics.get("isin"),
                "Name": characteristics.get("name"),
                "Asset class": characteristics.get("type"),
                "Currency": characteristics.get("currency"),
                "Weight": characteristics.get("weight"),
                "Sector": characteristics.get("sector"),
                "Country": characteristics.get("countryOfRisk")
                or characteristics.get("country"),
            }
        )

    download_path = destination_dir / f"{isin}_amundi_composition.json"
    download_path.write_bytes(data)
    return (
        DownloadedSource(
            source_path=download_path,
            download_path=download_path,
            content_type=content_type,
            source_format="json-api",
        ),
        normalized_rows,
    )


def copy_fixture(
    source_path: Path, destination_dir: Path, preferred_name: str | None = None
) -> DownloadedSource:
    _ensure_directory(destination_dir)
    extension = source_path.suffix or ".bin"
    filename = _safe_name(
        preferred_name or source_path.stem, source_path.stem or "download"
    )
    download_path = destination_dir / f"{filename}{extension}"
    shutil.copy2(source_path, download_path)
    return DownloadedSource(
        source_path=source_path, download_path=download_path, content_type=None
    )

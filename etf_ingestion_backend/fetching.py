from __future__ import annotations

import html.parser
import mimetypes
import re
import shutil
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class DownloadedSource:
    source_path: Path
    download_path: Path
    content_type: str | None


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

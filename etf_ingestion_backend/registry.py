from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .models import ETFSourceEntry


@dataclass(slots=True)
class ETFRegistry:
    entries: list[ETFSourceEntry]

    def select_by_isins(self, isins: list[str]) -> list[ETFSourceEntry]:
        wanted = {value.strip().upper() for value in isins}
        return [entry for entry in self.entries if entry.isin.upper() in wanted]


def load_registry(path: Path) -> ETFRegistry:
    payload = json.loads(path.read_text(encoding="utf-8"))
    entries = [ETFSourceEntry(**item) for item in payload.get("etfs", [])]
    return ETFRegistry(entries=entries)

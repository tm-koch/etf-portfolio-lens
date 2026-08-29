from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .exchange import normalize_exchange


def _key(value: str | None) -> str:
    return (value or "").strip().casefold()


@dataclass(slots=True)
class IdentityOverride:
    match: dict[str, str]
    set_values: dict[str, Any]
    source: str


class OverrideRegistry:
    def __init__(self, overrides: list[IdentityOverride], source: str) -> None:
        self.overrides = overrides
        self.source = source
        self._validate()

    @classmethod
    def empty(cls) -> "OverrideRegistry":
        return cls([], "none")

    @classmethod
    def from_json(cls, path: Path) -> "OverrideRegistry":
        payload = json.loads(path.read_text(encoding="utf-8"))
        overrides = []
        for item in payload.get("overrides", []):
            match = {
                str(k): str(v)
                for k, v in item.get("match", {}).items()
                if v not in (None, "")
            }
            set_values = dict(item.get("set", {}))
            overrides.append(IdentityOverride(match, set_values, str(path)))
        return cls(overrides, str(path))

    def _validate(self) -> None:
        seen: set[tuple[tuple[str, str], ...]] = set()
        for override in self.overrides:
            if not override.match:
                raise ValueError("Identity override must contain a match selector")
            normalized = dict(override.match)
            if "exchange" in normalized:
                normalized["exchange"] = (
                    normalize_exchange(normalized["exchange"]) or ""
                )
            signature = tuple(
                sorted((key, _key(value)) for key, value in normalized.items())
            )
            if signature in seen:
                raise ValueError(
                    f"Duplicate identity override selector: {dict(signature)}"
                )
            seen.add(signature)

    def find(self, holding: Any) -> IdentityOverride | None:
        candidates = []
        for override in self.overrides:
            match = override.match
            if "isin" in match and _key(match["isin"]) != _key(holding.isin):
                continue
            if "ticker" in match and _key(match["ticker"]) != _key(holding.ticker):
                continue
            if "exchange" in match and _key(
                normalize_exchange(match["exchange"])
            ) != _key(holding.exchange_code):
                continue
            if "country" in match and _key(match["country"]) != _key(holding.country):
                continue
            if "holding_name" in match and _key(match["holding_name"]) != _key(
                holding.name
            ):
                continue
            candidates.append(override)
        if not candidates:
            return None
        return max(candidates, key=lambda item: len(item.match))

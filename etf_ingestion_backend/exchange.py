from __future__ import annotations

import re

ALIASES = {
    "six": "SIX",
    "six swiss exchange": "SIX",
    "swiss exchange": "SIX",
    "nasdaq": "NASDAQ",
    "nasdaq global select market": "NASDAQ",
    "nyse": "NYSE",
    "new york stock exchange": "NYSE",
}


def normalize_exchange(value: str | None) -> str | None:
    if not value:
        return None
    key = re.sub(r"\s+", " ", value.strip().casefold())
    return ALIASES.get(key, value.strip().upper())

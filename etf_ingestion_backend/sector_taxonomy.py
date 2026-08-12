from __future__ import annotations

from typing import Final

CANONICAL_SECTOR_LABELS: Final[tuple[str, ...]] = (
    "Communication Services",
    "Consumer Discretionary",
    "Consumer Staples",
    "Energy",
    "Financials",
    "Health Care",
    "Industrials",
    "Information Technology",
    "Materials",
    "Real Estate",
    "Utilities",
)

UNKNOWN_SECTOR_LABEL: Final[str] = "Unknown"

SECTOR_ALIASES: Final[dict[str, str]] = {
    label.casefold(): label for label in CANONICAL_SECTOR_LABELS
}
SECTOR_ALIASES.update(
    {
        "communication": "Communication Services",
        "cash and/or derivatives": UNKNOWN_SECTOR_LABEL,
        "other": UNKNOWN_SECTOR_LABEL,
        "unassigned": UNKNOWN_SECTOR_LABEL,
    }
)


def normalize_sector_label(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    return SECTOR_ALIASES.get(text.casefold(), text)
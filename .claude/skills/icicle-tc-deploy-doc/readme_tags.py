"""readme_tags.py — resolve a component's catalog tags. **Standard library only**,
so the stdlib helpers (release_worker.py, api_parser.py) can import it as well as
readme_parser.py.

Source of truth, in order:
  1. the README's `**Tags:**` line (the icicle-readme-skill template), canonical
     tags only — anything else is reported as dropped, never invented into a doc;
  2. the release CSV's `Tags…` column — a fallback only, and may go away;
  3. neither → `source == "missing"`; callers flag the component and skip it.
"""

import re
from typing import List, Optional, Tuple

CANONICAL_TAGS = [
    "Software", "CI4AI", "AI4CI", "Foundation-AI", "PADI", "Visual-Analytics",
    "Digital-Agriculture", "Animal-Ecology", "Smart-Foodsheds", "Food-Access",
]
_CANON = {t.lower(): t for t in CANONICAL_TAGS}

# `**Tags:** a, b` / `**Tag**: a` / `Tags: a` / `` **Tags:** `a` `b` `` (first match wins)
_TAG_LINE = re.compile(r"^\s*(?:\*{1,2}\s*)?tags?\s*(?::\s*\*{1,2}|\*{1,2}\s*:|:)\s*(.+)$",
                       re.IGNORECASE | re.MULTILINE)
_FENCE = re.compile(r"^\s*(```|~~~).*?^\s*\1", re.MULTILINE | re.DOTALL)


def readme_tags(readme_text: str) -> Tuple[List[str], List[str]]:
    """Return (canonical_tags, dropped) from the first Tags line (outside code
    fences) that names a canonical tag. Both are empty when there is no Tags line."""
    first_dropped: List[str] = []
    for m in _TAG_LINE.finditer(_FENCE.sub("", readme_text or "")):
        line = re.sub(r"<!--.*?-->", "", m.group(1))
        tags, dropped = [], []
        for raw in re.split(r"[,|`\s]+", line):
            raw = raw.strip(" *_")
            if not raw:
                continue
            canon = _CANON.get(raw.lower())
            if canon is None:
                dropped.append(raw)
            elif canon not in tags:
                tags.append(canon)
        if tags:
            return tags, dropped
        first_dropped = first_dropped or dropped
    return [], first_dropped


def csv_tags(cell) -> List[str]:
    """Comma-separated tags from a CSV cell; empty / NaN cells give []."""
    raw = "" if cell is None else str(cell).strip()
    if raw.lower() == "nan":
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def resolve_tags(readme_text: str, csv_cell=None) -> Tuple[List[str], str, Optional[str]]:
    """Return (tags, source, note); source is "readme", "csv" or "missing".
    note is a human-readable warning (dropped/ignored tags, or the flag), else None."""
    tags, dropped = readme_tags(readme_text)
    fallback = csv_tags(csv_cell)
    notes = []
    if dropped:
        notes.append(f"non-canonical README tags dropped: {', '.join(dropped)}")
    if tags:
        if fallback and set(fallback) != set(tags):
            notes.append(f"CSV tags ignored (README wins): {', '.join(fallback)}")
        return tags, "readme", "; ".join(notes) or None
    if fallback:
        notes.append("no canonical tags in README — using CSV Tags fallback")
        return fallback, "csv", "; ".join(notes)
    notes.append("FLAG: no tags in README (**Tags:** line) or CSV — add canonical tags to the README")
    return [], "missing", "; ".join(notes)

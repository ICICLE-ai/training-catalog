#!/usr/bin/env python3
"""
seo_meta.py — search/LLM-friendly metadata for deployed component docs.

Standard library only. For each component folder under my-website/docs/ it:
  - gives section pages (how-to / explanation / tutorials / reference) a unique
    <title> ("<Component>: How-To Guides") while keeping the short sidebar and
    next/prev labels ("How-To Guides"), plus a meta description;
  - adds a meta description to the component's category page (_category_.json).

The description is the first prose paragraph of the component's main page (the
README description), so nothing is invented. Idempotent: re-running replaces the
keys it owns (title, sidebar_label, pagination_label, description) and leaves
every other frontmatter key (e.g. tags) untouched.

readme_parser.py calls apply_folder() after writing a component; run it by hand
to backfill:

    python3 seo_meta.py my-website/docs                      # every component
    python3 seo_meta.py my-website/docs --only "ICICLE Chatbook, HPC-MCP"
"""

import argparse
import json
import os
import re
from typing import List, Optional, Tuple

# Section pages as the parser names them, plus older variants still on the site.
SECTION_FILES = {"how-to.md", "explanation.md", "tutorials.md", "reference.md",
                 "explanations.md", "tutorial.md", "hot-to.md"}
OWNED_KEYS = ("title", "sidebar_label", "pagination_label", "description")
MAX_DESC = 160
BOILERPLATE_HEADING = re.compile(
    r"(acknowledg|references?\b|licen[cs]e|issue|citation|cite|funding|contact)", re.I)


def split_frontmatter(text: str) -> Tuple[List[str], str]:
    """Return (frontmatter lines without the --- fences, body)."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end].split("\n"), text[end + 5:]
    return [], text


def join_frontmatter(lines: List[str], body: str) -> str:
    lines = [l for l in lines if l.strip()]
    if not lines:
        return body
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def set_keys(lines: List[str], values: dict) -> List[str]:
    """Drop the keys we own, then append the new values (YAML double-quoted)."""
    kept = [l for l in lines if not re.match(r"^(%s):" % "|".join(OWNED_KEYS), l)]
    for k in OWNED_KEYS:
        if values.get(k):
            kept.append(f"{k}: {json.dumps(values[k], ensure_ascii=False)}")
    return kept


def first_h1(body: str) -> Optional[str]:
    in_fence = False
    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("# "):
            return line[2:].strip()
    return None


def plain(text: str) -> str:
    """Markdown/HTML paragraph -> one line of plain text."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)            # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)        # links -> text
    text = re.sub(r"<[^>]+>", "", text)                         # html tags
    text = re.sub(r"[*_`]+", "", text)                          # emphasis/code
    return re.sub(r"\s+", " ", text).strip()


def first_paragraph(body: str) -> Optional[str]:
    """First prose paragraph after the H1: skips headings, badges, HTML, fences."""
    in_fence = False
    for para in re.split(r"\n\s*\n", body):
        stripped = para.strip()
        fences = stripped.count("```")
        if in_fence or fences:
            # A code block may span blank lines; an odd fence count toggles it.
            if fences % 2 == 1:
                in_fence = not in_fence
            continue
        # A heading glued to its paragraph (no blank line) shouldn't hide it;
        # a list or badge line ends the prose part.
        lines = stripped.split("\n")
        while lines and lines[0].lstrip().startswith("#"):
            if BOILERPLATE_HEADING.match(lines[0].lstrip("# ").strip("*_ ")):
                return None  # past the description; don't borrow funding/licence text
            lines.pop(0)
        prose = []
        for line in lines:
            if line.lstrip().startswith(("- ", "* ", "|", "[![", "<", "```")):
                break
            prose.append(line)
        stripped = "\n".join(prose).strip()
        if not stripped:
            continue
        if stripped.startswith(("#", "<", "[![", "![", "---", ":::", "|", ">", "-", "*", "import ")):
            continue
        text = plain(stripped)
        if len(text) >= 40 and not text.lower().startswith("tags:"):
            return text
    return None


def clip(text: str, limit: int = MAX_DESC) -> str:
    """Trim to whole sentences within limit, else to a word boundary + ellipsis."""
    if len(text) <= limit:
        return text
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = ""
    for s in sentences:
        if len(out) + len(s) + 1 > limit:
            break
        out = (out + " " + s).strip()
    if len(out) >= limit * 0.6:
        return out
    # Whole sentences would leave the description too thin: cut mid-sentence.
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def main_file(folder: str) -> Optional[str]:
    name = os.path.basename(folder.rstrip("/")).lower()
    files = os.listdir(folder)
    for f in files:  # case-insensitive, so it behaves the same on Linux CI
        if f.lower() in (name + ".md", name + ".mdx"):
            return f
    others = [f for f in files
              if f.endswith((".md", ".mdx")) and f not in SECTION_FILES]
    return others[0] if len(others) == 1 else None


def component_label(folder: str) -> str:
    try:
        with open(os.path.join(folder, "_category_.json"), encoding="utf-8") as f:
            return json.load(f).get("label") or os.path.basename(folder)
    except (OSError, ValueError):
        return os.path.basename(folder.rstrip("/"))


def apply_folder(folder: str) -> List[str]:
    """Apply metadata to one component folder. Returns the files changed."""
    changed: List[str] = []
    label = component_label(folder)
    main = main_file(folder)
    summary = None
    if main:
        with open(os.path.join(folder, main), encoding="utf-8") as f:
            _, body = split_frontmatter(f.read())
        summary = first_paragraph(body)

    for fname in sorted(os.listdir(folder)):
        if fname not in SECTION_FILES:
            continue
        path = os.path.join(folder, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm, body = split_frontmatter(text)
        heading = first_h1(body)
        if not heading:
            continue
        title = heading if label.lower() in heading.lower() else f"{label}: {heading}"
        desc = f"{heading} for {label}."
        if summary:
            desc = clip(f"{desc} {summary}")
        new = join_frontmatter(set_keys(fm, {
            "title": title, "sidebar_label": heading,
            "pagination_label": heading, "description": desc,
        }), body)
        if new != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            changed.append(path)

    cat_path = os.path.join(folder, "_category_.json")
    if summary and os.path.exists(cat_path):
        with open(cat_path, encoding="utf-8") as f:
            cat = json.load(f)
        link = cat.get("link")
        if isinstance(link, dict) and link.get("type") == "generated-index":
            desc = clip(summary)
            if link.get("description") != desc:
                link["description"] = desc
                with open(cat_path, "w", encoding="utf-8") as f:
                    f.write(json.dumps(cat, indent=2, ensure_ascii=False) + "\n")
                changed.append(cat_path)
    return changed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("docs_dir", help="e.g. my-website/docs")
    ap.add_argument("--only", help="comma-separated component folders (case-insensitive)")
    args = ap.parse_args()
    only = {s.strip().lower() for s in args.only.split(",")} if args.only else None
    total = 0
    for name in sorted(os.listdir(args.docs_dir)):
        folder = os.path.join(args.docs_dir, name)
        if not os.path.isdir(folder) or (only and name.lower() not in only):
            continue
        n = len(apply_folder(folder))
        total += n
        if n:
            print(f"{name}: {n} file(s)")
    print(f"updated {total} file(s)")


if __name__ == "__main__":
    main()

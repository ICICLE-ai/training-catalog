#!/usr/bin/env python3
"""
resource_parser.py — reusable helpers for the ICICLE training-catalog
resource-listing deploy skill (.claude/skills/icicle-tc-deploy-resource).
**Standard library only** — no third-party deps, so it runs with any `python3`
(no venv needed).

Run it from `my-website/` so the default target path
(`other_resources/0_intro.md`) resolves. Subcommands mirror the skill's steps:

  csv-rows    Read the release-testing CSV and print, as JSON, only the rows that
              have a Resource Link — each with the component name, link, tags, and
              release. (Not every component has a resource link; the rest are
              skipped.) Descriptions are NOT in the CSV — the caller supplies one
              to `insert` (fetched from the page or the component README).
  check-link  HTTP-check that a URL resolves (follows redirects). Exit 0 + prints
              the status when reachable; non-zero when it does not resolve.
  insert      Insert (or idempotently replace) one resource entry in
              other_resources/0_intro.md at the correct alphabetical position —
              either as a new top-level `## <name>` product block, or, with
              --section, as a bold-bullet sub-entry inside an existing container
              section such as "TACC and Tapis Resources".

Typical flow for one resource:
  python3 resource_parser.py check-link --url <link>
  python3 resource_parser.py insert --name "<Name>" --link <link> \
      --description "<one-sentence description>"          # new top-level ## block
  # or, into an existing container section:
  python3 resource_parser.py insert --name "<Name>" --link <link> \
      --description "<...>" --section "TACC and Tapis Resources"
"""

import argparse
import csv
import json
import re
import sys
import urllib.request
import urllib.error

DEFAULT_FILE = "other_resources/0_intro.md"
LINK_ATTRS = 'target="_blank" rel="noopener noreferrer"'


# -----------------------------
# CSV helpers (shared conventions with the doc/api parsers)
# -----------------------------

def parse_tags(cell) -> list:
    return [t.strip() for t in str(cell or "").split(",") if t.strip()]


def find_column(fieldnames, *candidates, prefix=False):
    """Resolve a column name case-insensitively; with prefix=True also matches a
    column whose name *starts with* a candidate (so 'Tags: Training Catalog' and
    'Resource Link (optional)' resolve)."""
    lower = {c.strip().lower(): c for c in fieldnames}
    for cand in candidates:
        if cand.strip().lower() in lower:
            return lower[cand.strip().lower()]
    if prefix:
        for c in fieldnames:
            cl = c.strip().lower()
            if any(cl.startswith(cand.strip().lower()) for cand in candidates):
                return c
    return None


# -----------------------------
# Markdown section model for 0_intro.md
# -----------------------------
#
# The file is: a preamble (H1 + intro sentence) followed by level-2 `## ` sections.
# A "product" section is a `## <name>` block. A "container" section (e.g.
# "TACC and Tapis Resources") holds several `- **<name>**` bold bullets.

SECTION_RE = re.compile(r"(?m)^## +(.*)$")
BULLET_RE = re.compile(r"(?m)^- +\*\*(.+?)\*\*")


def split_sections(text):
    """Return (preamble, [(heading_text, block_text), ...]).

    block_text includes the `## heading` line and its body up to (not including)
    the next `## ` line or EOF.
    """
    matches = list(SECTION_RE.finditer(text))
    if not matches:
        return text, []
    preamble = text[: matches[0].start()]
    sections = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append([m.group(1).strip(), text[start:end]])
    return preamble, sections


def join_sections(preamble, sections):
    return preamble + "".join(block for _, block in sections)


def sort_key(name: str) -> str:
    return name.strip().lower()


def insert_sorted(sections, new_heading, new_block):
    """Insert or replace a top-level section, keeping alphabetical order and not
    disturbing existing entries. Idempotent on heading (case-insensitive)."""
    key = sort_key(new_heading)
    for i, (heading, _) in enumerate(sections):
        if sort_key(heading) == key:
            sections[i] = [new_heading, new_block]  # replace in place
            return "replaced"
    for i, (heading, _) in enumerate(sections):
        if sort_key(heading) > key:
            sections.insert(i, [new_heading, new_block])
            return "inserted"
    sections.append([new_heading, new_block])
    return "inserted"


# -----------------------------
# Entry builders
# -----------------------------

def product_block(name, link, description, link_text) -> str:
    return (
        f"## {name}\n\n"
        f"- {description}\n\n"
        f'  <a href="{link}" {LINK_ATTRS}>\n'
        f"    {link_text}\n"
        f"  </a>\n\n"
    )


def bold_bullet(name, link, description, link_text) -> str:
    return (
        f"- **{name}**\n\n"
        f"  {description}\n\n"
        f'  <a href="{link}" {LINK_ATTRS}>\n'
        f"  {link_text}\n"
        f"  </a>\n\n"
    )


def split_bullets(block_text):
    """Split a container section block into (head, [(bullet_name, bullet_text)]).

    head is the `## heading` line plus any intro text before the first bold bullet.
    """
    matches = list(BULLET_RE.finditer(block_text))
    if not matches:
        return block_text, []
    head = block_text[: matches[0].start()]
    bullets = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block_text)
        bullets.append([m.group(1).strip(), block_text[start:end]])
    return head, bullets


def insert_bullet_sorted(bullets, new_name, new_bullet):
    key = sort_key(new_name)
    for i, (name, _) in enumerate(bullets):
        if sort_key(name) == key:
            bullets[i] = [new_name, new_bullet]
            return "replaced"
    for i, (name, _) in enumerate(bullets):
        if sort_key(name) > key:
            bullets.insert(i, [new_name, new_bullet])
            return "inserted"
    bullets.append([new_name, new_bullet])
    return "inserted"


# -----------------------------
# Subcommands
# -----------------------------

def cmd_csv_rows(args):
    with open(args.csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fn = reader.fieldnames or []
        comp_c = find_column(fn, "Component")
        link_c = find_column(fn, "Resource Link", "Resource", prefix=True)
        tags_c = find_column(fn, "Tags", prefix=True)
        rel_c = find_column(fn, "Release Dates", "Release", prefix=True)
        if not link_c:
            sys.exit("CSV has no Resource Link column (looked for a column starting "
                     "with 'Resource').")
        only = {n.strip().lower() for n in ",".join(args.only or []).split(",") if n.strip()}
        rows = []
        for r in reader:
            link = (r.get(link_c) or "").strip()
            if not link or link.lower() == "nan":
                continue  # not every component ships a resource link — skip it
            name = (r.get(comp_c) or "").strip() if comp_c else ""
            if only and name.strip().lower() not in only:
                continue
            rows.append({
                "component": name,
                "name": name,
                "link": link,
                "tags": parse_tags(r.get(tags_c)) if tags_c else [],
                "release": (r.get(rel_c) or "").strip() if rel_c else "",
            })
    json.dump(rows, sys.stdout, indent=2)
    print()


def cmd_check_link(args):
    req = urllib.request.Request(args.url, method="GET",
                                 headers={"User-Agent": "icicle-resource-check"})
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:  # noqa: S310
            status = getattr(resp, "status", resp.getcode())
            print(json.dumps({"url": args.url, "status": status, "ok": True,
                              "final_url": resp.geturl()}))
    except urllib.error.HTTPError as e:
        # A 4xx/5xx still means the host resolved; report it but treat >=400 as not ok.
        print(json.dumps({"url": args.url, "status": e.code, "ok": False}))
        sys.exit(1)
    except (urllib.error.URLError, ValueError, OSError) as e:
        print(json.dumps({"url": args.url, "status": None, "ok": False,
                          "error": str(e)}))
        sys.exit(1)


def cmd_insert(args):
    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    link_text = args.link_text or f"Link to {args.name}"
    preamble, sections = split_sections(text)

    if args.section:
        # Insert as a bold-bullet sub-entry inside an existing container section.
        target = None
        for sec in sections:
            if sort_key(sec[0]) == sort_key(args.section):
                target = sec
                break
        if target is None:
            sys.exit(f"Container section {args.section!r} not found in {args.file}. "
                     "Omit --section to add a new top-level ## listing instead.")
        head, bullets = split_bullets(target[1])
        new_bullet = bold_bullet(args.name, args.link, args.description, link_text)
        action = insert_bullet_sorted(bullets, args.name, new_bullet)
        # Rebuild the container block: heading/intro + bullets, one blank line between.
        head = head.rstrip("\n") + "\n\n"
        body = "".join(b.rstrip("\n") + "\n\n" for _, b in bullets)
        target[1] = head + body
        where = f"{action} under '{args.section}'"
    else:
        new_block = product_block(args.name, args.link, args.description, link_text)
        action = insert_sorted(sections, args.name, new_block)
        where = f"{action} as top-level section"

    out = join_sections(preamble, sections)
    # Normalize: no more than two consecutive blank lines, single trailing newline.
    out = re.sub(r"\n{4,}", "\n\n\n", out).rstrip("\n") + "\n"
    with open(args.file, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"{where}: {args.name} -> {args.link}")


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("csv-rows", help="emit resource-link rows from the release CSV as JSON")
    s.add_argument("--csv", required=True)
    s.add_argument("--only", nargs="+", metavar="COMPONENT",
                   help="only emit row(s) whose Component matches (case-insensitive); "
                        'comma-separated, e.g. --only "FlexServe Inference, Smart Labeler"')
    s.set_defaults(func=cmd_csv_rows)

    s = sub.add_parser("check-link", help="verify a URL resolves (follows redirects)")
    s.add_argument("--url", required=True)
    s.add_argument("--timeout", type=float, default=15.0)
    s.set_defaults(func=cmd_check_link)

    s = sub.add_parser("insert", help="insert/replace a resource entry in 0_intro.md")
    s.add_argument("--name", required=True, help="entry name; NO invented version — "
                   "include a version only if the source actually provides one")
    s.add_argument("--link", required=True)
    s.add_argument("--description", required=True, help="one-sentence description "
                   "(fetched from the page or the component README by the caller)")
    s.add_argument("--section", help="existing container section to nest under as a "
                   'bold bullet, e.g. "TACC and Tapis Resources"; omit for a new '
                   "top-level ## listing")
    s.add_argument("--link-text", help="anchor text; defaults to 'Link to <name>'")
    s.add_argument("--file", default=DEFAULT_FILE, help=f"target markdown (default {DEFAULT_FILE})")
    s.set_defaults(func=cmd_insert)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

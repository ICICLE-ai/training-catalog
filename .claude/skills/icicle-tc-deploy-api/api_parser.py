#!/usr/bin/env python3
"""
api_parser.py — reusable helpers for the ICICLE training-catalog API-docs deploy
skill (.claude/skills/icicle-tc-deploy-api). **Standard library only** — no
third-party deps, so it runs with any `python3` (no venv needed).

Run it from `my-website/` so the relative paths (`api_config_files/`, `api-docs/`)
resolve. Subcommands mirror the skill's steps:

  csv-rows        Read the release-testing CSV and print, as JSON, only the rows
                  that have an OpenAPI JSON link — each with component name, slug,
                  spec source URL, tags, and release. (Not every component has a
                  spec; the rest are skipped.)
  stage           Download (GitHub blob->raw) or copy a spec into
                  api_config_files/<slug>.json and validate it is OpenAPI v3.
  config-snippet  Print the docusaurus-plugin-openapi-docs plugin block to paste
                  into docusaurus.config.js for a given name/slug.
  inject-tags     Add a `tags: [...]` line to every *.api.mdx in a generated
                  api-docs folder (idempotent — skips files already tagged).

Typical flow for one CSV row (slug = lowercase-hyphenated Component):
  python3 api_parser.py stage --source <openapi-url> --slug <slug>
  # add the block from `config-snippet` to docusaurus.config.js, then:
  npx docusaurus gen-api-docs <slug> -p openapi-<slug>
  python3 api_parser.py inject-tags --dir "api-docs/<Name>" --tags API <canonical...> "Release <YYYY-MM>"
"""

import argparse
import csv
import glob
import json
import os
import re
import shutil
import sys
import urllib.request


# -----------------------------
# Name / slug / URL helpers
# -----------------------------

def slugify(name: str) -> str:
    """'ICICLE Vector DB Service' -> 'icicle-vector-db-service'."""
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")


def title_case_repo(repo: str) -> str:
    """'icicle-ai-vector-service' -> 'Icicle Ai Vector Service' (bare-repo fallback)."""
    parts = re.split(r"[-_\s]+", repo.strip())
    return " ".join(p.capitalize() for p in parts if p)


def repo_name_from_url(url: str):
    """Pull the <repo> out of a github.com / raw.githubusercontent.com URL."""
    m = re.search(r"github(?:usercontent)?\.com/([^/]+)/([^/]+)", url)
    return m.group(2) if m else None


def blob_to_raw(url: str) -> str:
    """github.com/<u>/<r>/blob/<b>/<path> -> raw.githubusercontent.com/<u>/<r>/<b>/<path>."""
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/blob/(.+)$", url.strip())
    if m:
        user, repo, rest = m.groups()
        return f"https://raw.githubusercontent.com/{user}/{repo}/{rest}"
    return url.strip()


def parse_tags(cell) -> list:
    return [t.strip() for t in str(cell or "").split(",") if t.strip()]


def find_column(fieldnames, *candidates, prefix=False):
    """Resolve a column name case-insensitively; with prefix=True also matches a
    column whose name *starts with* a candidate (so 'Tags: Training Catalog' and
    'OPENAPI JSON' resolve)."""
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
# Subcommands
# -----------------------------

def cmd_csv_rows(args):
    with open(args.csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fn = reader.fieldnames or []
        comp_c = find_column(fn, "Component")
        api_c = find_column(fn, "OPENAPI JSON", "OpenAPI JSON Link", "OpenAPI JSON",
                            "OpenAPI", prefix=True)
        tags_c = find_column(fn, "Tags", prefix=True)
        rel_c = find_column(fn, "Release Dates", "Release", prefix=True)
        if not api_c:
            sys.exit("CSV has no OpenAPI JSON column (looked for a column starting "
                     "with 'OpenAPI').")
        # comma-separated and/or multiple args; names contain spaces, so split on commas
        only = {n.strip().lower() for n in ",".join(args.only or []).split(",") if n.strip()}
        rows = []
        for r in reader:
            src = (r.get(api_c) or "").strip()
            if not src or src.lower() == "nan":
                continue  # not every component ships an OpenAPI spec — skip it
            name = (r.get(comp_c) or "").strip() if comp_c else ""
            if not name or name.lower() == "nan":
                repo = repo_name_from_url(src)
                name = title_case_repo(repo) if repo else "api"
            if only and name.strip().lower() not in only:
                continue  # --only filter: skip components not requested
            rows.append({
                "component": name,
                "name": name,
                "slug": slugify(name),
                "source": src,
                "tags": parse_tags(r.get(tags_c)) if tags_c else [],
                "release": (r.get(rel_c) or "").strip() if rel_c else "",
            })
    json.dump(rows, sys.stdout, indent=2)
    print()


def cmd_stage(args):
    os.makedirs(args.config_dir, exist_ok=True)
    out = os.path.join(args.config_dir, f"{args.slug}.json")
    src = args.source
    if re.match(r"https?://", src):
        url = blob_to_raw(src)
        with urllib.request.urlopen(url) as resp:  # noqa: S310 (trusted GitHub URLs)
            data = resp.read()
        with open(out, "wb") as f:
            f.write(data)
    else:
        shutil.copyfile(src, out)

    try:
        with open(out, encoding="utf-8") as f:
            spec = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"{out}: not valid JSON ({e}).")
    version = str(spec.get("openapi", ""))
    if not version.startswith("3"):
        sys.exit(f"{out}: not OpenAPI v3 (openapi={version!r}). This pipeline expects v3 "
                 "— a v2/Swagger spec must be converted first.")
    print(json.dumps({"staged": out, "openapi": version,
                      "title": spec.get("info", {}).get("title")}))


def cmd_config_snippet(args):
    name = args.name
    slug = args.slug or slugify(name)
    print(
        "    [\n"
        "      'docusaurus-plugin-openapi-docs',\n"
        "      {\n"
        f"        id: 'openapi-{slug}', // Plugin ID\n"
        "        docsPluginId: 'api', // Associate it with API docs\n"
        "        config: {\n"
        f"          '{slug}': {{\n"
        f"            specPath: 'api_config_files/{slug}.json',\n"
        f"            outputDir: 'api-docs/{name}',\n"
        "            sidebarOptions: {\n"
        "              groupPathsBy: \"tag\",\n"
        "            },\n"
        "          },\n"
        "        },\n"
        "      },\n"
        "    ],"
    )


def cmd_inject_tags(args):
    tag_line = "tags: [" + ", ".join(args.tags) + "]"
    files = sorted(glob.glob(os.path.join(args.dir, "*.api.mdx")))
    if not files:
        sys.exit(f"No *.api.mdx files found in {args.dir!r}.")
    changed = skipped = 0
    for path in files:
        lines = open(path, encoding="utf-8").read().splitlines()
        if not lines or lines[0].strip() != "---":
            print(f"skip (no frontmatter): {path}")
            continue
        close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if close is None:
            print(f"skip (unterminated frontmatter): {path}")
            continue
        if any(l.strip().startswith("tags:") for l in lines[1:close]):
            skipped += 1
            continue
        # insert right after custom_edit_url: if present, else just before the close
        insert_at = close
        for i in range(1, close):
            if lines[i].startswith("custom_edit_url:"):
                insert_at = i + 1
                break
        lines.insert(insert_at, tag_line)
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        changed += 1
        print(f"tagged: {path}")
    print(f"{changed} file(s) tagged, {skipped} already had tags")


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("csv-rows", help="emit OpenAPI rows from the release CSV as JSON")
    s.add_argument("--csv", required=True)
    s.add_argument("--only", nargs="+", metavar="COMPONENT",
                   help="only emit row(s) whose Component matches (case-insensitive); "
                        'comma-separated, e.g. --only "ICICLE Vector DB Service, ICICLE Embedding Service"')
    s.set_defaults(func=cmd_csv_rows)

    s = sub.add_parser("stage", help="download/copy a spec and validate OpenAPI v3")
    s.add_argument("--source", required=True, help="OpenAPI spec URL (GitHub blob/raw) or local path")
    s.add_argument("--slug", required=True, help="lowercase-hyphenated spec/config key")
    s.add_argument("--config-dir", default="api_config_files")
    s.set_defaults(func=cmd_stage)

    s = sub.add_parser("config-snippet", help="print the docusaurus.config.js plugin block")
    s.add_argument("--name", required=True, help="Title/folder name, e.g. 'ICICLE Vector DB Service'")
    s.add_argument("--slug", help="defaults to slugify(name)")
    s.set_defaults(func=cmd_config_snippet)

    s = sub.add_parser("inject-tags", help="add a tags line to every *.api.mdx in a folder")
    s.add_argument("--dir", required=True, help="generated folder, e.g. 'api-docs/ICICLE Vector DB Service'")
    s.add_argument("--tags", nargs="+", required=True, help="tag values, e.g. API CI4AI Software 'Release 2026-05'")
    s.set_defaults(func=cmd_inject_tags)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

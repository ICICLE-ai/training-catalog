import argparse
import os
import re
import glob
import json
import posixpath
import requests
import pandas as pd  # required only if --excel_file is used
from urllib.parse import urlparse, quote
from typing import List, Optional, Tuple, Dict

"""
README parser modes:
1) Single repo mode:
   - uses --repo_link (+ optional --project_name, --tags, --release)
2) Batch mode (Excel via --excel_file, or CSV via --csv_file):
   - reads metadata per row from a table
   - column resolution is case-insensitive and tolerant of the catalog's
     release-spreadsheet headers:
     * README        : GitHub repo URL or README blob URL          (required)
     * Tags          : comma-separated tags (e.g. "AI4CI, Software")(required)
                       matched by prefix, so "Tags: Training Catalog" also works
     * Component     : project/folder name (optional; if missing/empty, derived
                       from the repo URL). When present it is the folder name.
     * Release Dates : YYYY-MM (optional); used per row when --release is absent
   - extra columns (e.g. OPENAPI JSON, Version, Source Code) are ignored here —
     they belong to the API-docs pipeline.
   - --release (CLI), if given, overrides the per-row release for every row.
"""

# -----------------------------
# GitHub helpers
# -----------------------------

def build_requests_session(github_pat: Optional[str] = None) -> requests.Session:
    """
    Create a requests session. If a GitHub PAT is provided (explicit arg or env),
    attach it as an Authorization header so private repos can be accessed.
    """
    token = github_pat or os.getenv("GITHUB_PAT")
    sess = requests.Session()
    if token:
        sess.headers.update({"Authorization": f"token {token.strip()}"})
    # Basic accept header is sometimes helpful for GitHub endpoints
    sess.headers.update({"Accept": "application/vnd.github.v3.raw"})
    return sess

def to_raw_readme_url(repo_link: str) -> Optional[str]:
    """
    Convert a normal GitHub URL to the corresponding raw.githubusercontent URL for README.md.
    Handles:
      - direct raw (returns as-is)
      - blob links (converts)
      - repo root links (tries main/master README.md)
    Returns None if conversion cannot be determined (rare).
    """
    if "raw.githubusercontent.com" in repo_link and repo_link.endswith(".md"):
        return repo_link  # already raw

    if "github.com" in repo_link and "/blob/" in repo_link:
        # e.g., https://github.com/user/repo/blob/branch/path/README.md
        parts = repo_link.split("/")
        # parts: ['https:', '', 'github.com', user, repo, 'blob', branch, path...]
        if len(parts) >= 7:
            user, repo, branch = parts[3], parts[4], parts[6]
            path = "/".join(parts[7:])  # includes README.md file
            return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
        return None

    # Standard repo URL (root, with or without trailing slash)
    parsed = urlparse(repo_link.rstrip("/"))
    if parsed.netloc == "github.com":
        path = parsed.path.strip("/")  # user/repo or user/repo/...
        if path.count("/") >= 1:
            user_repo = "/".join(path.split("/")[:2])
            # We'll try 'main' then 'master'
            for branch in ["main", "master"]:
                raw_url = f"https://raw.githubusercontent.com/{user_repo}/{branch}/README.md"
                # Don't fetch here; just return the first candidate. The caller can try both.
                # But to be robust, we return a list or let the fetcher test both.
                # We'll let get_raw_readme() handle the branch attempts.
            return f"https://raw.githubusercontent.com/{user_repo}/main/README.md"  # default try main first
    return None

def fetch_raw_readme(repo_link: str, session: requests.Session) -> Tuple[str, str]:
    """
    Fetch README content as text using a raw URL. Supports:
      - raw links
      - /blob/ links converted to raw
      - repo root links: tries main then master
    Returns a tuple of (readme_text, resolved_raw_url). The resolved raw URL is
    the raw.githubusercontent.com URL that actually succeeded; it carries the
    user/repo/branch/path needed to rewrite relative links and images.
    Raises Exception on failure.
    """
    # Case 1: raw or blob → raw
    raw_candidate = to_raw_readme_url(repo_link)
    if raw_candidate and "raw.githubusercontent.com" in raw_candidate:
        resp = session.get(raw_candidate)
        if resp.status_code == 200:
            return resp.text, raw_candidate
        # If it was a root link defaulting to main, try master as a fallback
        if "/main/" in raw_candidate:
            fallback = raw_candidate.replace("/main/", "/master/")
            resp2 = session.get(fallback)
            if resp2.status_code == 200:
                return resp2.text, fallback
        raise Exception(f"Could not fetch README.md, status code {resp.status_code} for {raw_candidate}")

    # Case 2: Standard repo URL we couldn't transform—try main/master explicitly
    parsed = urlparse(repo_link.rstrip("/"))
    path = parsed.path.strip("/")
    for branch in ["main", "master"]:
        raw_url = f"https://raw.githubusercontent.com/{path}/{branch}/README.md"
        resp = session.get(raw_url)
        if resp.status_code == 200:
            return resp.text, raw_url

    raise Exception("Could not fetch README.md from the provided repo link.")

def repo_home_url(repo_link: str) -> str:
    """
    Return the 'home' URL of the repo (no /blob/...). Useful for the badge link.
    """
    if "/blob/" in repo_link:
        return repo_link.split("/blob/")[0]
    return repo_link.rstrip("/")

def derive_project_name(repo_link: str) -> str:
    """
    Derive a project name from a repo URL if none is given.
    Uses the repository name portion.
    """
    parsed = urlparse(repo_link.rstrip("/"))
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 2:
        return parts[1]
    # Fallback: last path segment
    return parts[-1] if parts else "project"

# -----------------------------
# Relative link / image rewriting
# -----------------------------
#
# The catalog site is deployed away from GitHub, so relative paths in a README
# (./docs/x.md, images/diagram.png, ../CONTRIBUTING.md) would break once the
# content is lifted into Docusaurus. We rewrite them to absolute GitHub URLs so
# every reference stays clickable and points back to where it was authored:
#   - images          -> https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}
#   - all other links -> https://github.com/{user}/{repo}/blob/{branch}/{path}
# Absolute URLs (http/https/mailto/#anchors/protocol-relative) are left untouched.

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "ftp://", "data:", "//")

FENCE_PATTERN = re.compile(r"(```.*?```|~~~.*?~~~)", re.DOTALL)
MD_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MD_LINK_PATTERN = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
HTML_SRC_PATTERN = re.compile(r"(\bsrc\s*=\s*[\"'])([^\"']+)([\"'])", re.IGNORECASE)
HTML_HREF_PATTERN = re.compile(r"(\bhref\s*=\s*[\"'])([^\"']+)([\"'])", re.IGNORECASE)


def parse_raw_url(raw_url: str) -> Optional[Tuple[str, str, str, str]]:
    """
    Decompose a raw.githubusercontent.com URL into (user, repo, branch, readme_dir).
    readme_dir is the directory that contains the README ('' when at repo root),
    used as the base for resolving relative paths.
    """
    parsed = urlparse(raw_url)
    parts = [p for p in parsed.path.split("/") if p]
    # parts: [user, repo, branch, ...path, filename]
    if len(parts) < 4:
        return None
    user, repo, branch = parts[0], parts[1], parts[2]
    readme_dir = "/".join(parts[3:-1])  # drop the filename
    return user, repo, branch, readme_dir


def _is_external(url: str) -> bool:
    """True for URLs we must not rewrite (absolute, anchor, or empty)."""
    u = url.strip()
    if not u or u.startswith("#"):
        return True
    return u.lower().startswith(EXTERNAL_PREFIXES)


def _resolve_repo_path(rel_path: str, readme_dir: str) -> str:
    """
    Resolve a relative path to a repo-root-relative path, collapsing ./ and ../.
    A leading '/' is treated as repo-root anchored.
    """
    rel_path = rel_path.strip().strip("<>")
    if rel_path.startswith("/"):
        base = rel_path.lstrip("/")
    elif readme_dir:
        base = posixpath.join(readme_dir, rel_path)
    else:
        base = rel_path
    return posixpath.normpath(base).lstrip("/")


def _split_url_and_title(inner: str) -> Tuple[str, str]:
    """
    Split the inside of a markdown ()-target into (url, trailing) so an optional
    "title" or <angle-bracket> form is preserved on re-emit.
    """
    inner = inner.strip()
    if inner.startswith("<"):
        end = inner.find(">")
        if end != -1:
            return inner[1:end], inner[end + 1:]
    parts = inner.split(None, 1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " " + parts[1]


def rewrite_relative_links(text: str, user: str, repo: str, branch: str, readme_dir: str) -> str:
    """Rewrite relative image/link targets in README text to absolute GitHub URLs."""
    raw_base = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}"
    blob_base = f"https://github.com/{user}/{repo}/blob/{branch}"

    def to_raw(rel: str) -> str:
        return f"{raw_base}/{_resolve_repo_path(rel, readme_dir)}"

    def to_blob(rel: str) -> str:
        return f"{blob_base}/{_resolve_repo_path(rel, readme_dir)}"

    def repl_md_image(m: "re.Match") -> str:
        url, trailing = _split_url_and_title(m.group(2))
        if _is_external(url):
            return m.group(0)
        return f"![{m.group(1)}]({to_raw(url)}{trailing})"

    def repl_md_link(m: "re.Match") -> str:
        url, trailing = _split_url_and_title(m.group(2))
        if _is_external(url):
            return m.group(0)
        return f"[{m.group(1)}]({to_blob(url)}{trailing})"

    def repl_html_src(m: "re.Match") -> str:
        if _is_external(m.group(2)):
            return m.group(0)
        return f"{m.group(1)}{to_raw(m.group(2))}{m.group(3)}"

    def repl_html_href(m: "re.Match") -> str:
        if _is_external(m.group(2)):
            return m.group(0)
        return f"{m.group(1)}{to_blob(m.group(2))}{m.group(3)}"

    out: List[str] = []
    # Skip fenced code blocks so code samples are never mangled.
    for seg in FENCE_PATTERN.split(text):
        if seg.startswith("```") or seg.startswith("~~~"):
            out.append(seg)
            continue
        seg = MD_IMAGE_PATTERN.sub(repl_md_image, seg)
        seg = MD_LINK_PATTERN.sub(repl_md_link, seg)
        seg = HTML_SRC_PATTERN.sub(repl_html_src, seg)
        seg = HTML_HREF_PATTERN.sub(repl_html_href, seg)
        out.append(seg)
    return "".join(out)


# -----------------------------
# Content splitting & mapping
# -----------------------------

SECTION_SPLIT_REGEX = r"^\s*---\s*$"  # line containing only '---'
SECTION_PATTERN = re.compile(SECTION_SPLIT_REGEX, flags=re.MULTILINE)
FRONTMATTER_PATTERN = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n)?", re.DOTALL)

# Map target filenames to heading patterns (case-insensitive)
HEADING_MAP: Dict[str, List[re.Pattern]] = {
    "tutorials.md": [
        re.compile(r"^\s*#\s*tutorials?\s*$", re.IGNORECASE | re.MULTILINE)
    ],
    "how-to.md": [
        re.compile(r"^\s*#\s*how[-\s]*to\s*guides?\s*$", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^\s*#\s*how[-\s]*to\s*guide\s*$", re.IGNORECASE | re.MULTILINE),
    ],
    "explanation.md": [
        re.compile(r"^\s*#\s*explanations?\s*$", re.IGNORECASE | re.MULTILINE)
    ],
}

# -----------------------------
# File helpers
# -----------------------------

def tag_block(tags: List[str]) -> str:
    """Create a YAML frontmatter tag block."""
    unique = []
    seen = set()
    for t in tags:
        if t not in seen:
            unique.append(t)
            seen.add(t)
    if not unique:
        # An empty "tags:" block is invalid YAML frontmatter (parses as null)
        # and fails the Docusaurus build — emit no frontmatter at all instead.
        return ""
    lines = ["---", "tags:"]
    for tag in unique:
        lines.append(f"  - {tag}")
    lines.append("---\n")
    return "\n".join(lines)

def extract_frontmatter_tags(existing_text: str) -> List[str]:
    """
    Extract tag values from a YAML-like frontmatter block at top of file, if present.
    Only reads simple form:
      ---
      tags:
        - A
        - B
      ---
    """
    match = FRONTMATTER_PATTERN.match(existing_text)
    if not match:
        return []
    block = match.group(1)
    lines = block.splitlines()
    tags: List[str] = []
    in_tags = False
    for line in lines:
        if re.match(r"^\s*tags\s*:\s*$", line, flags=re.IGNORECASE):
            in_tags = True
            continue
        if in_tags:
            bullet = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if bullet:
                tags.append(bullet.group(1).strip())
            elif line.strip():
                # stop if a non-empty non-bullet key/value appears
                in_tags = False
    return tags

def unique_tags_keep_order(tags: List[str]) -> List[str]:
    """Deduplicate tags while preserving first-seen order."""
    out: List[str] = []
    seen = set()
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out

def strip_leading_frontmatter(content: str) -> str:
    """Remove a leading YAML frontmatter block from content if present."""
    return FRONTMATTER_PATTERN.sub("", content, count=1).lstrip()

def remove_stray_tag_lines(content: str) -> str:
    """
    Remove stray tag metadata lines from body content so tags only exist in top frontmatter.
    Removes lines like:
      - tags:
      - Tag:
      - Tasg,tags:
      - *tags*:
      - **Tags**:
      - **Tag**:
    and immediately following bullet list lines.
    """
    cleaned: List[str] = []
    lines = content.splitlines()
    i = 0
    tag_header_pattern = re.compile(
        r"^\s*(?:\*{1,2}\s*)?(?:tasg,\s*)?tags?(?:\s*\*{1,2})?\s*:\s*(?:.+)?$",
        flags=re.IGNORECASE,
    )
    while i < len(lines):
        line = lines[i]
        if tag_header_pattern.match(line):
            i += 1
            while i < len(lines) and re.match(r"^\s*-\s+.+$", lines[i]):
                i += 1
            continue
        cleaned.append(line)
        i += 1
    return "\n".join(cleaned).strip()

def is_badge_line(line: str) -> bool:
    """Heuristic to detect badge lines commonly found near top of README files."""
    s = line.strip().lower()
    if not s:
        return False
    return (
        "[![" in s
        or "shields.io" in s
        or "<img" in s
        or "badge" in s
    )

# -----------------------------
# License extraction / badge
# -----------------------------
#
# ICICLE READMEs carry license info in a "## License" / "### License" section in a
# few shapes: a shields.io License badge, a `[License: <name>](<link>)` link, or a
# "licensed under the <X> License … see [LICENSE](…)" sentence. We pull the license
# name + link out, drop the whole section from the body, and re-emit a single
# standardized License badge in the centered badge block next to the GitHub badge.

LICENSE_HEADING_RE = re.compile(r"^\s*#{1,6}\s*licen[sc]e\b.*$", re.IGNORECASE)
SHIELDS_LICENSE_BADGE_RE = re.compile(
    r"\[!\[[^\]]*\]\(\s*https?://img\.shields\.io/badge/License-(.+?)-[A-Za-z0-9]+\.svg[^)]*\)\]\(\s*([^)\s]+)\s*\)",
    re.IGNORECASE,
)
LICENSE_TEXT_LINK_RE = re.compile(
    r"\[\s*licen[sc]e\s*:?\s*([^\]]+?)\s*\]\(\s*([^)\s]+)\s*\)", re.IGNORECASE
)
LICENSED_UNDER_RE = re.compile(r"licensed under (?:the\s+)?(.+?)\s+licen[sc]e", re.IGNORECASE)


def _decode_badge_label(s: str) -> str:
    """shields.io badge label -> human text: '%20' -> space, '--' -> '-'."""
    return s.replace("%20", " ").replace("--", "-").strip()


def make_license_badge(name: str, link: str) -> str:
    """Build a standardized shields.io License badge that links to the license."""
    name = name.strip()
    enc = name.replace("-", "--").replace(" ", "%20")
    return (
        f"[![License: {name}](https://img.shields.io/badge/License-{enc}-yellow.svg)]"
        f"({link.strip()})"
    )


def is_license_badge(line: str) -> bool:
    """True for a markdown badge line that represents a license."""
    s = line.strip().lower()
    return "shields.io/badge/license" in s or s.startswith(("[![license", "![license"))


def extract_license(body: str) -> Tuple[Optional[str], str]:
    """
    Find license info in a README body. Returns (license_badge_or_None, cleaned_body),
    with the whole "License" section removed from the body when one is found. The raw
    `License: …` text is dropped — we represent it only as the standardized badge.
    """
    lines = body.splitlines()
    start = next((i for i, l in enumerate(lines) if LICENSE_HEADING_RE.match(l)), None)
    if start is None:
        return None, body

    level = len(re.match(r"^\s*(#+)", lines[start]).group(1))
    end = len(lines)
    for j in range(start + 1, len(lines)):
        m = re.match(r"^\s*(#+)\s", lines[j])
        if m and len(m.group(1)) <= level:  # next heading of same/higher level
            end = j
            break
    section = "\n".join(lines[start:end])

    badge = None
    mb = SHIELDS_LICENSE_BADGE_RE.search(section)
    mt = LICENSE_TEXT_LINK_RE.search(section)
    if mb:  # an existing shields License badge — reuse its name + link
        badge = make_license_badge(_decode_badge_label(mb.group(1)), mb.group(2))
    elif mt:  # a `[License: <name>](<link>)` text link
        badge = make_license_badge(mt.group(1), mt.group(2))
    else:  # "licensed under the <X> License … [LICENSE](link)"
        mu = LICENSED_UNDER_RE.search(section)
        ml = MD_LINK_PATTERN.search(section)
        if mu and ml:
            badge = make_license_badge(mu.group(1), ml.group(2))

    cleaned = "\n".join(lines[:start] + lines[end:]).strip()
    return badge, cleaned


def _center_badges(badges: List[str]) -> List[str]:
    """Wrap badge lines in a center-aligned div. The blank lines are required so MDX
    renders the markdown badges inside the HTML block."""
    return ['<div align="center">', ""] + badges + ["", "</div>"]


def move_top_badges_after_description(
    content: str,
    github_badge: Optional[str] = None,
    license_badge: Optional[str] = None,
) -> str:
    """
    Collect badge/shield lines from the top of the content and re-emit them as a single
    center-aligned block placed right after the first description paragraph. Order:
    GitHub badge, License badge, then any other badges. If no license_badge is supplied
    but a license badge is found among the top badges, it is used as the license badge
    (so it still lands next to GitHub).
    """
    lines = content.splitlines()

    # Collect badge lines near the top (after an optional title), removing them.
    collected: List[str] = []
    if lines:
        i = 0
        if i < len(lines) and re.match(r"^\s*#\s+.+$", lines[i]):
            i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        badge_start = i
        while i < len(lines) and (is_badge_line(lines[i]) or not lines[i].strip()):
            if is_badge_line(lines[i]):
                collected.append(lines[i].strip())
            i += 1
        if i > badge_start:
            lines = lines[:badge_start] + lines[i:]

    # Separate any license badge so it can sit right next to the GitHub badge.
    other_badges = [b for b in collected if not is_license_badge(b)]
    if license_badge is None:
        license_badge = next((b for b in collected if is_license_badge(b)), None)

    ordered: List[str] = []
    if github_badge:
        ordered.append(github_badge)
    if license_badge:
        ordered.append(license_badge)
    ordered.extend(other_badges)
    ordered = unique_tags_keep_order([b for b in ordered if b.strip()])

    if not ordered:
        return "\n".join(lines).strip()

    # Insertion point: after the first non-empty paragraph (the short description).
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx < len(lines) and re.match(r"^\s*#\s+.+$", lines[idx]):
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    insert_at = len(lines)
    para_started = False
    while idx < len(lines):
        if lines[idx].strip():
            para_started = True
            idx += 1
        else:
            if para_started:
                insert_at = idx
                break
            idx += 1

    prefix = lines[:insert_at]
    suffix = lines[insert_at:]
    stitched = prefix + [""] + _center_badges(ordered) + [""] + suffix
    return "\n".join(stitched).strip()

# -----------------------------
# Cross-link to API docs (same site)
# -----------------------------
#
# If this component also has OpenAPI docs in the site (api-docs/<Component>/, deployed
# by the icicle-tc-deploy-api skill), the main doc gets a link to that API reference
# page. The link is a root-relative route ('/api/<Component>/<info-id>') so Docusaurus
# prepends the site baseUrl (…/training-catalog/api/…) and the broken-link checker
# validates it. The check is *best-effort and order-independent*: if the API folder
# isn't there yet, no link is added (no broken link) — re-run the doc skill after the
# API docs exist to add it. So there's no ordering deadlock between the two skills.

def find_api_doc_route(component_name: str, api_docs_dir: str) -> Optional[str]:
    """
    Return the in-site API info-page route for a component if its API docs exist under
    `api_docs_dir/<component_name>/`, else None. The route is read from a generated
    *.api.mdx `info_path` (authoritative), falling back to the *.info.mdx `id`. Spaces
    are %20-encoded so it's a valid markdown link target.
    """
    folder = os.path.join(api_docs_dir, component_name)
    if not os.path.isdir(folder):
        return None

    info_path = None
    for f in sorted(glob.glob(os.path.join(folder, "*.api.mdx"))):
        m = re.search(r"^info_path:\s*(.+?)\s*$", open(f, encoding="utf-8").read(), re.MULTILINE)
        if m:
            info_path = m.group(1).strip()
            break
    if not info_path:
        infos = sorted(glob.glob(os.path.join(folder, "*.info.mdx")))
        if not infos:
            return None
        text = open(infos[0], encoding="utf-8").read()
        mid = re.search(r"^id:\s*(.+?)\s*$", text, re.MULTILINE)
        info_id = mid.group(1).strip() if mid else os.path.basename(infos[0])[: -len(".info.mdx")]
        info_path = f"api/{component_name}/{info_id}"

    return quote("/" + info_path.lstrip("/"), safe="/")


def _first_paragraph_end(lines: List[str]) -> int:
    """Index just past the first non-empty paragraph (skipping a leading title)."""
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx < len(lines) and re.match(r"^\s*#\s+.+$", lines[idx]):
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    started = False
    while idx < len(lines):
        if lines[idx].strip():
            started = True
            idx += 1
        elif started:
            return idx
        else:
            idx += 1
    return len(lines)


def insert_api_reference(body: str, route: str, label: str) -> str:
    """
    Insert a Docusaurus tip linking to the component's API docs, right after the
    centered badge block (its closing </div>) or, failing that, after the first
    paragraph. Idempotent: the body is rebuilt from the README every run, so this
    never stacks duplicate callouts.
    """
    admonition = (
        ":::tip API reference\n"
        f"This component exposes an HTTP API — see its "
        f"[API documentation]({route}) on this site.\n"
        ":::"
    )
    lines = body.splitlines()
    insert_at = next((i + 1 for i, l in enumerate(lines) if l.strip() == "</div>"), None)
    if insert_at is None:
        insert_at = _first_paragraph_end(lines)
    new_lines = lines[:insert_at] + ["", admonition, ""] + lines[insert_at:]
    return "\n".join(new_lines).strip()


def save_file(folder: str, fname: str, content: str, tags: List[str],
              github_link: Optional[str] = None, api_doc_route: Optional[str] = None):
    """
    Save a Markdown file with frontmatter.
    Behavior:
      - preserves existing frontmatter tags already present in file
      - appends new tags (deduplicated)
      - removes stray body tag metadata lines ('tags:' / 'Tasg,tags:')
      - ensures badges are placed after the initial description in main files
      - when api_doc_route is given, adds a tip linking to the component's API docs
    """
    os.makedirs(folder, exist_ok=True)
    out_path = os.path.join(folder, fname)

    existing_tags: List[str] = []
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            existing_text = f.read()
        existing_tags = extract_frontmatter_tags(existing_text)

    merged_tags = unique_tags_keep_order(existing_tags + tags)

    body = strip_leading_frontmatter(content)
    body = remove_stray_tag_lines(body)
    if github_link:
        github_badge = f'[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)]({github_link})'
        # Pull the license out of its README section and re-emit it as a badge next
        # to the GitHub badge; the raw "License: …" text is dropped from the body.
        license_badge, body = extract_license(body)
        body = move_top_badges_after_description(
            body, github_badge=github_badge, license_badge=license_badge
        )
        if api_doc_route:
            body = insert_api_reference(body, api_doc_route, os.path.splitext(fname)[0])
    else:
        body = move_top_badges_after_description(body)

    md = tag_block(merged_tags) + body.strip() + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    return merged_tags

def write_category_json(folder: str, project_name: str):
    """
    Write Docusaurus _category_.json to let the folder render a generated index.
    """
    cat_json = {
        "label": project_name,
        "link": {"type": "generated-index"}
    }
    with open(os.path.join(folder, "_category_.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(cat_json, indent=2) + "\n")

# -----------------------------
# Processing pipeline
# -----------------------------

def split_sections(readme_text: str) -> List[str]:
    """
    Split README text into sections using lines that contain only '---'.
    """
    parts = re.split(SECTION_PATTERN, readme_text)
    # Strip trailing whitespace from each part
    return [p.strip() for p in parts if p.strip()]

def classify_and_write_sections(
    folder: str,
    parts: List[str],
    base_tags: List[str],
    repo_link_for_badge: str,
    project_name: str,
    release: Optional[str] = None,
    api_doc_route: Optional[str] = None
):
    """
    - Save the first section as {project_name}.md (with optional Release tag injected only here)
    - For the remaining sections, detect headings and save into tutorials.md, how-to.md, explanation.md.
      If a section matches multiple categories (unlikely), first match wins.
    """
    # First part → main file; add Release tag if provided
    main_tags = list(base_tags)
    if release:
        main_tags.append(f"Release {release}")

    main_merged = save_file(
        folder=folder,
        fname=f"{project_name}.md",
        content=parts[0],
        tags=main_tags,
        github_link=repo_link_for_badge,
        api_doc_route=api_doc_route
    )

    # Section files inherit the main file's full tag set (including tags merged
    # from existing frontmatter) minus the per-release "Release <YYYY-MM>" markers,
    # which belong only on the main file.
    section_tags = [t for t in main_merged if not t.startswith("Release ")]

    written = set()
    for part in parts[1:]:
        assigned = False
        for out_name, patterns in HEADING_MAP.items():
            if out_name in written:
                continue
            if any(p.search(part) for p in patterns):
                save_file(folder, out_name, part, section_tags)
                written.add(out_name)
                assigned = True
                break
        # If not assigned, you could choose to skip or dump to 'extras.md'
        # Here we skip silently.

def process_single_repo(
    repo_link: str,
    project_name: Optional[str],
    output_folder: str,
    tags: List[str],
    release: Optional[str],
    session: requests.Session,
    api_docs_dir: Optional[str] = None
):
    """
    Process a single repo:
      - fetch README
      - split into sections
      - write markdown files and category json
      - cross-link to the component's API docs if they already exist on the site
    """
    repo_name = project_name or derive_project_name(repo_link)
    project_folder = os.path.join(output_folder, repo_name)
    os.makedirs(project_folder, exist_ok=True)

    # Default api-docs to the sibling of the docs output root (my-website/api-docs).
    if api_docs_dir is None:
        api_docs_dir = os.path.join(os.path.dirname(os.path.abspath(output_folder)), "api-docs")
    api_doc_route = find_api_doc_route(repo_name, api_docs_dir)

    readme_text, raw_url = fetch_raw_readme(repo_link, session)

    # Rewrite relative images/links to absolute GitHub URLs so they survive
    # being deployed outside GitHub.
    parsed_raw = parse_raw_url(raw_url)
    if parsed_raw:
        gh_user, gh_repo, gh_branch, readme_dir = parsed_raw
        readme_text = rewrite_relative_links(readme_text, gh_user, gh_repo, gh_branch, readme_dir)

    parts = split_sections(readme_text)

    repo_home = repo_home_url(repo_link)

    if not parts:
        # No content; write an empty main file at least
        save_file(project_folder, f"{repo_name}.md", "", (tags + ([f"Release {release}"] if release else [])), github_link=repo_home, api_doc_route=api_doc_route)
    else:
        classify_and_write_sections(
            folder=project_folder,
            parts=parts,
            base_tags=tags,
            repo_link_for_badge=repo_home,
            project_name=repo_name,
            release=release,
            api_doc_route=api_doc_route
        )

    write_category_json(project_folder, repo_name)

# -----------------------------
# Batch (Excel / CSV) helpers
# -----------------------------

def find_column(df: "pd.DataFrame", *candidates: str, prefix: bool = False) -> Optional[str]:
    """
    Resolve a column name case-insensitively. First tries an exact (lowercased,
    trimmed) match against each candidate. If none match and prefix=True, returns
    the first column whose lowercased/trimmed name *starts with* a candidate — this
    is how "Tags: Training Catalog" resolves for the candidate "tags".
    """
    lower = {str(c).strip().lower(): c for c in df.columns}
    for cand in candidates:
        if cand.strip().lower() in lower:
            return lower[cand.strip().lower()]
    if prefix:
        for c in df.columns:
            cl = str(c).strip().lower()
            if any(cl.startswith(cand.strip().lower()) for cand in candidates):
                return c
    return None

def parse_tags_cell(tags_cell, row_number: int) -> List[str]:
    """
    Parse comma-separated tags from a single table cell. Required in batch mode.
    """
    if pd.isna(tags_cell):
        raise ValueError(f"Row {row_number}: tags column is required and cannot be empty.")
    raw = str(tags_cell).strip()
    if not raw or raw.lower() == "nan":
        raise ValueError(f"Row {row_number}: tags column is required and cannot be empty.")
    parsed_tags = [t.strip() for t in raw.split(",") if t.strip()]
    if not parsed_tags:
        raise ValueError(f"Row {row_number}: tags must contain at least one comma-separated tag.")
    return parsed_tags

def read_repos_from_table(df: "pd.DataFrame", source_desc: str) -> List[Tuple[str, Optional[str], List[str], Optional[str]]]:
    """
    Resolve catalog columns from a DataFrame (Excel or CSV) and return a list of:
      (repo_link, project_name_opt, row_tags, row_release_opt)
    Required (resolved case-insensitively): README, a Tags* column.
    Optional: Component (folder name), Release Dates (per-row release).
    Rows with an empty README are skipped, so blank trailing rows don't break a batch.
    """
    readme_col = find_column(df, "README")
    if not readme_col:
        raise ValueError(f"{source_desc} is missing the required 'README' column.")
    tags_col = find_column(df, "Tags", prefix=True)
    if not tags_col:
        raise ValueError(
            f"{source_desc} is missing a tags column "
            "(a column named 'Tags' or beginning with 'Tags', e.g. 'Tags: Training Catalog')."
        )
    component_col = find_column(df, "Component")
    release_col = find_column(df, "Release Dates", "Release", prefix=True)

    repos: List[Tuple[str, Optional[str], List[str], Optional[str]]] = []
    for idx, row in df.iterrows():
        row_number = idx + 2  # +2: DataFrame is 0-based and row 1 is the header
        link = str(row[readme_col]).strip()
        if not link or link.lower() == "nan":
            continue  # skip rows without a README

        proj = None
        if component_col is not None and not pd.isna(row[component_col]):
            proj = str(row[component_col]).strip() or None
            if proj and proj.lower() == "nan":
                proj = None

        row_tags = parse_tags_cell(row[tags_col], row_number)

        row_release = None
        if release_col is not None and not pd.isna(row[release_col]):
            rv = str(row[release_col]).strip()
            if rv and rv.lower() != "nan":
                row_release = rv

        repos.append((link, proj, row_tags, row_release))
    return repos

def read_repos_from_excel(xlsx_path: str) -> List[Tuple[str, Optional[str], List[str], Optional[str]]]:
    """Read component rows from an Excel file. See read_repos_from_table for columns."""
    return read_repos_from_table(pd.read_excel(xlsx_path), f"Excel file '{xlsx_path}'")

def read_repos_from_csv(csv_path: str) -> List[Tuple[str, Optional[str], List[str], Optional[str]]]:
    """Read component rows from a CSV file. See read_repos_from_table for columns."""
    return read_repos_from_table(pd.read_csv(csv_path), f"CSV file '{csv_path}'")

# -----------------------------
# CLI
# -----------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch README from GitHub repos and split into docs sections.")
    # Single-run options
    parser.add_argument("--repo_link", type=str, help="GitHub repository URL or README blob URL (non-raw).")
    parser.add_argument("--project_name", type=str, help="Project name (folder and main file). If omitted, derived from repo URL.")
    # Batch mode via Excel or CSV
    parser.add_argument(
        "--excel_file",
        type=str,
        help=(
            "Path to an Excel file. Required columns: README, Tags (matched by "
            "prefix). Optional: Component (folder name), Release Dates."
        ),
    )
    parser.add_argument(
        "--csv_file",
        type=str,
        help=(
            "Path to a CSV file (same columns as --excel_file). Use this for the "
            "release-testing catalog CSV."
        ),
    )
    # Output and metadata
    parser.add_argument("--output_folder", type=str, default=".", help="Output root folder (defaults to current directory).")
    parser.add_argument(
        "--tags",
        nargs="+",
        default=[],
        help="Base tags (single mode only). Ignored in batch mode because tags come from the table's Tags column.",
    )
    parser.add_argument(
        "--release",
        type=str,
        help="Release in 'YYYY-MM' format, added as 'Release <value>' to main file(s). Overrides any per-row release in batch mode; otherwise the table's Release column is used per row.",
    )
    # Targeted update
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="COMPONENT",
        help="Batch mode: process only the row(s) whose Component matches, "
             "case-insensitive. Comma-separated (names contain spaces), e.g. "
             '--only "ICICLE Vector DB Service, Smart Labeler". Update a subset '
             "without rerunning the whole table.",
    )
    # Cross-linking
    parser.add_argument(
        "--api_docs_dir",
        type=str,
        help="Path to the site's api-docs root. Defaults to the 'api-docs' sibling of "
             "--output_folder. If api-docs/<Component>/ exists, the main doc links to it.",
    )
    # Auth
    parser.add_argument("--github_pat", type=str, help="Optional GitHub PAT (overrides GITHUB_PAT env var).")
    return parser.parse_args()

def main():
    args = parse_args()
    session = build_requests_session(args.github_pat)

    # Validation: exactly one input mode
    batch_file = args.excel_file or args.csv_file
    if args.excel_file and args.csv_file:
        raise SystemExit("Provide only one of --excel_file or --csv_file, not both.")
    if not batch_file and not args.repo_link:
        raise SystemExit("Provide --repo_link for single-run OR --excel_file/--csv_file for batch processing.")

    if batch_file:
        if args.tags:
            raise SystemExit(
                "In batch mode, do not pass --tags. Tags come from the table's Tags column per row."
            )
        repos = read_repos_from_csv(args.csv_file) if args.csv_file else read_repos_from_excel(args.excel_file)
        if not repos:
            raise SystemExit("No valid rows (with a README) found in the batch file.")
        if args.only:
            # Accept a comma-separated list and/or multiple args; names contain spaces
            # so commas (not spaces) are the delimiter.
            names = [n.strip() for n in ",".join(args.only).split(",") if n.strip()]
            wanted = {n.lower() for n in names}
            filtered = [r for r in repos if r[1] and r[1].strip().lower() in wanted]
            if not filtered:
                available = ", ".join(sorted({r[1] for r in repos if r[1]})) or "(none)"
                raise SystemExit(
                    f"--only matched no rows for: {', '.join(names)}. "
                    f"Available components: {available}"
                )
            missing = wanted - {r[1].strip().lower() for r in filtered}
            if missing:
                print(f"warning: --only names not found, skipped: {', '.join(sorted(missing))}")
            repos = filtered
        for repo_link, proj_name, row_tags, row_release in repos:
            process_single_repo(
                repo_link=repo_link,
                project_name=proj_name or args.project_name,  # CLI override, else table Component, else derived
                output_folder=args.output_folder,
                tags=row_tags,
                release=args.release or row_release,  # CLI release wins, else per-row release
                session=session,
                api_docs_dir=args.api_docs_dir
            )
    else:
        # Single repo path
        process_single_repo(
            repo_link=args.repo_link,
            project_name=args.project_name,
            output_folder=args.output_folder,
            tags=args.tags,
            release=args.release,
            session=session,
            api_docs_dir=args.api_docs_dir
        )

if __name__ == "__main__":
    main()

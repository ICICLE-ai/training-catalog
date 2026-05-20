import argparse
import os
import re
import json
import posixpath
import requests
import pandas as pd  # required only if --excel_file is used
from urllib.parse import urlparse
from typing import List, Optional, Tuple, Dict

"""
README parser modes:
1) Single repo mode:
   - uses --repo_link (+ optional --project_name, --tags, --release)
2) Excel batch mode:
   - uses --excel_file and reads metadata per row
   - strict required columns in Excel:
     * README        : GitHub repo URL or README blob URL
     * Tags          : comma-separated tags (example: "AI, NLP, Demo")
   - optional column:
     * Component     : project/folder name; if missing/empty, repo name is derived from URL
   - release is taken from CLI flag --release (same value applied to all rows for the run)
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

def move_top_badges_after_description(content: str, extra_badges: Optional[List[str]] = None) -> str:
    """
    Move top badge lines to after the first description paragraph.
    This keeps title + short description first in main project docs.
    """
    lines = content.splitlines()
    if not lines:
        badges = extra_badges or []
        return "\n".join(badges).strip()

    badges: List[str] = []
    if extra_badges:
        badges.extend(extra_badges)

    # Collect badge lines appearing near top (after optional title).
    i = 0
    if i < len(lines) and re.match(r"^\s*#\s+.+$", lines[i]):
        i += 1

    while i < len(lines) and not lines[i].strip():
        i += 1

    badge_start = i
    while i < len(lines) and (is_badge_line(lines[i]) or not lines[i].strip()):
        if is_badge_line(lines[i]):
            badges.append(lines[i].strip())
        i += 1

    # Remove collected badge area from original content.
    if i > badge_start:
        lines = lines[:badge_start] + lines[i:]

    badges = unique_tags_keep_order([b for b in badges if b.strip()])
    if not badges:
        return "\n".join(lines).strip()

    # Find insertion point after first non-empty paragraph (usually the short description).
    insert_at = len(lines)
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx < len(lines) and re.match(r"^\s*#\s+.+$", lines[idx]):
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

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
    stitched = prefix + [""] + badges + [""] + suffix
    return "\n".join(stitched).strip()

def save_file(folder: str, fname: str, content: str, tags: List[str], github_link: Optional[str] = None):
    """
    Save a Markdown file with frontmatter.
    Behavior:
      - preserves existing frontmatter tags already present in file
      - appends new tags (deduplicated)
      - removes stray body tag metadata lines ('tags:' / 'Tasg,tags:')
      - ensures badges are placed after the initial description in main files
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
        body = move_top_badges_after_description(body, extra_badges=[github_badge])
    else:
        body = move_top_badges_after_description(body)

    md = tag_block(merged_tags) + body.strip() + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

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
    release: Optional[str] = None
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

    save_file(
        folder=folder,
        fname=f"{project_name}.md",
        content=parts[0],
        tags=main_tags,
        github_link=repo_link_for_badge
    )

    written = set()
    for part in parts[1:]:
        assigned = False
        for out_name, patterns in HEADING_MAP.items():
            if out_name in written:
                continue
            if any(p.search(part) for p in patterns):
                save_file(folder, out_name, part, base_tags)
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
    session: requests.Session
):
    """
    Process a single repo:
      - fetch README
      - split into sections
      - write markdown files and category json
    """
    repo_name = project_name or derive_project_name(repo_link)
    project_folder = os.path.join(output_folder, repo_name)
    os.makedirs(project_folder, exist_ok=True)

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
        save_file(project_folder, f"{repo_name}.md", "", (tags + ([f"Release {release}"] if release else [])), github_link=repo_home)
    else:
        classify_and_write_sections(
            folder=project_folder,
            parts=parts,
            base_tags=tags,
            repo_link_for_badge=repo_home,
            project_name=repo_name,
            release=release
        )

    write_category_json(project_folder, repo_name)

# -----------------------------
# Excel helpers
# -----------------------------

def parse_excel_tags(tags_cell, row_number: int) -> List[str]:
    """
    Parse comma-separated tags from a single Excel cell.
    Strict: this value is required in Excel mode.
    """
    if pd.isna(tags_cell):
        raise ValueError(f"Row {row_number}: 'Tags' is required and cannot be empty.")
    raw = str(tags_cell).strip()
    if not raw or raw.lower() == "nan":
        raise ValueError(f"Row {row_number}: 'Tags' is required and cannot be empty.")
    parsed_tags = [t.strip() for t in raw.split(",") if t.strip()]
    if not parsed_tags:
        raise ValueError(f"Row {row_number}: 'Tags' must contain at least one comma-separated tag.")
    return parsed_tags

def read_repos_from_excel(xlsx_path: str) -> List[Tuple[str, Optional[str], List[str]]]:
    """
    Reads an Excel file and returns a list of:
      (repo_link, project_name_opt, row_tags)
    Strict required columns:
      - README
      - Tags
    Optional columns:
      - Component
    """
    df = pd.read_excel(xlsx_path)
    required_columns = ["README", "Tags"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            "Excel file is missing required column(s): "
            + ", ".join(missing)
            + ". Required: README, Tags."
        )
    
    repos: List[Tuple[str, Optional[str], List[str]]] = []
    has_component = "Component" in df.columns

    for idx, row in df.iterrows():
        row_number = idx + 2  # +2 because DataFrame is 0-based and row 1 is header in Excel
        link = str(row["README"]).strip()
        if not link or link.lower() == "nan":
            raise ValueError(f"Row {row_number}: 'README' is required and cannot be empty.")

        proj = str(row["Component"]).strip() if has_component and not pd.isna(row["Component"]) else None
        row_tags = parse_excel_tags(row["Tags"], row_number)
        repos.append((link, proj, row_tags))
    return repos

# -----------------------------
# CLI
# -----------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch README from GitHub repos and split into docs sections.")
    # Single-run options
    parser.add_argument("--repo_link", type=str, help="GitHub repository URL or README blob URL (non-raw).")
    parser.add_argument("--project_name", type=str, help="Project name (folder and main file). If omitted, derived from repo URL.")
    # Batch mode via Excel
    parser.add_argument(
        "--excel_file",
        type=str,
        help=(
            "Path to an Excel file. Required columns: README, Tags. "
            "Optional: Component."
        ),
    )
    # Output and metadata
    parser.add_argument("--output_folder", type=str, default=".", help="Output root folder (defaults to current directory).")
    parser.add_argument(
        "--tags",
        nargs="+",
        default=[],
        help="Base tags (single mode only). Ignored when --excel_file is used because tags come from Excel 'Tags' column.",
    )
    parser.add_argument(
        "--release",
        type=str,
        help="Release in 'YYYY-MM' format. Applied to generated main file(s). In --excel_file mode, one release value is used for all rows.",
    )
    # Auth
    parser.add_argument("--github_pat", type=str, help="Optional GitHub PAT (overrides GITHUB_PAT env var).")
    return parser.parse_args()

def main():
    args = parse_args()
    session = build_requests_session(args.github_pat)

    # Validation: either single mode or excel mode must be present
    if not args.excel_file and not args.repo_link:
        raise SystemExit("Provide either --repo_link for single-run OR --excel_file for batch processing.")

    if args.excel_file:
        if args.tags:
            raise SystemExit(
                "In --excel_file mode, do not pass --tags. "
                "Use Excel column 'Tags' per row."
            )
        repos = read_repos_from_excel(args.excel_file)
        if not repos:
            raise SystemExit("No valid rows found in the Excel file.")
        for repo_link, proj_name, row_tags in repos:
            process_single_repo(
                repo_link=repo_link,
                project_name=proj_name or args.project_name,  # allow CLI to override, else use Excel, else derive
                output_folder=args.output_folder,
                tags=row_tags,
                release=args.release,
                session=session
            )
    else:
        # Single repo path
        process_single_repo(
            repo_link=args.repo_link,
            project_name=args.project_name,
            output_folder=args.output_folder,
            tags=args.tags,
            release=args.release,
            session=session
        )

if __name__ == "__main__":
    main()
